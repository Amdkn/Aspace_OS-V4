"""Durable temporal evidence. Local callers supply authority; this is not an auth server."""
import copy
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from .temporal_truth.temporal_truth import TemporalCanonGraph
from .temporal_truth.compiler import ContextCompiler


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def timestamp(value):
    t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('Timezone required')
    return t.astimezone(timezone.utc).isoformat()


class EvidenceGraph(TemporalCanonGraph):
    """V4 query policy: historical imports cannot become current observations."""
    def state_at(self, subject, predicate, t, scope):
        t = timestamp(t)
        relevant = [copy.deepcopy(c) for c in self.claims.values()
                    if (c['subject'], c['predicate'], c['scope']) == (subject, predicate, scope)
                    and c['observed_at'] <= t]
        excluded = {'HISTORICAL', 'EXPERIMENTAL', 'PROPOSED', 'UNKNOWN', 'SUPERSEDED'}
        superseded = self._get_superseded_claim_ids(t)
        groups = {}
        historical = []
        for c in relevant:
            if c['claim_id'] in superseded:
                c['temporal_state'] = 'SUPERSEDED'
                historical.append(c)
            elif c['temporal_state'] in excluded:
                historical.append(c)
            elif (c.get('valid_from') and c['valid_from'] > t) or (c.get('valid_to') and c['valid_to'] <= t):
                c['temporal_state'] = 'HISTORICAL'
                historical.append(c)
            else:
                groups.setdefault(c['source_authority'], []).append(c)
        result = historical
        for claims in groups.values():
            latest = max(c['observed_at'] for c in claims)
            # Equal-time conflicting claims remain visible rather than choosing insertion order.
            for c in claims:
                c['temporal_state'] = 'CURRENT' if c['observed_at'] == latest else 'HISTORICAL'
                result.append(c)
        return sorted(result, key=lambda c: c['claim_id'])


class Journal:
    def __init__(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, timeout=10)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS event (seq INTEGER PRIMARY KEY, kind TEXT NOT NULL, identity TEXT NOT NULL, payload TEXT NOT NULL, digest TEXT NOT NULL, UNIQUE(kind, identity))')
        self.db.commit()

    def close(self):
        self.db.close()

    def graph(self, as_known_at=None):
        graph = EvidenceGraph()
        cutoff = timestamp(as_known_at) if as_known_at else None
        expected_prev = ""
        expected_seq = 1
        for seq, kind, payload, digest in self.db.execute('SELECT seq,kind,payload,digest FROM event ORDER BY seq'):
            if seq != expected_seq:
                raise ValueError('Journal integrity failure: Sequence gap detected')
            if hashlib.sha256((expected_prev + payload).encode()).hexdigest() != digest:
                raise ValueError('Journal integrity failure: Digest mismatch')
            expected_prev = digest
            expected_seq += 1
            item = json.loads(payload)
            if cutoff and item['recorded_at'] > cutoff:
                continue
            if kind == 'claim':
                graph.ingest_claim(item)
            else:
                graph.record_transition(item)
        return graph

    def append(self, kind, item, *, expected_authority):
        if kind not in ('claim', 'transition'):
            raise ValueError('Unknown event kind')
        item = copy.deepcopy(item)
        ident = item['claim_id' if kind == 'claim' else 'transition_id']
        owner = item['source_authority' if kind == 'claim' else 'resolution_authority']
        if not expected_authority or owner != expected_authority:
            raise ValueError('Authority mismatch')
        for key in ('observed_at', 'recorded_at', 'effective_at', 'valid_from', 'valid_to'):
            if item.get(key) is not None:
                item[key] = timestamp(item[key])
        if not item.get('recorded_at'):
            raise ValueError('Explicit recorded_at required')
        if kind == 'claim' and not item.get('temporal_state'):
            raise ValueError('Explicit temporal classification required')
        encoded = canonical(item)
        try:
            self.db.execute('BEGIN IMMEDIATE')
            prev = self.db.execute('SELECT digest FROM event ORDER BY seq DESC LIMIT 1').fetchone()
            prev_hash = prev[0] if prev else ""
            digest = hashlib.sha256((prev_hash + encoded).encode()).hexdigest()
            found = self.db.execute('SELECT payload FROM event WHERE kind=? AND identity=?', (kind, ident)).fetchone()
            if found:
                if found[0] != encoded:
                    raise ValueError('Immutable identity already has different content')
                self.db.commit()
                return ident
            graph = self.graph()
            dim = (item['subject'], item['predicate'], item['scope'])
            if kind == 'claim':
                refs = (item.get('supersedes') or []) + (item.get('contradicts') or [])
                if item.get('valid_from') and item.get('valid_to') and item['valid_from'] >= item['valid_to']:
                    raise ValueError('Invalid validity interval')
                for ref in refs:
                    prior = graph.claims.get(ref)
                    if not prior or (prior['subject'], prior['predicate'], prior['scope']) != dim:
                        raise ValueError('Claim relation crosses dimension or references missing claim')
                    if ref in (item.get('supersedes') or []) and prior['source_authority'] != owner:
                        raise ValueError('Cross-authority change requires explicit reconciliation')
                graph.validate_schema(item, 'TemporalClaim')
            else:
                if item['resolution_scope'] != item['scope']:
                    raise ValueError('Resolution scope mismatch')
                if not item['from_claims'] or not item['to_claims']:
                    raise ValueError('Transition must link existing alternatives')
                if set(item['from_claims']) & set(item['to_claims']):
                    raise ValueError('Transition cannot accept and retire the same claim')
                if set(item['resulting_canon_heads']) != set(item['to_claims']):
                    raise ValueError('Canonical heads must match selected claims')
                for ref in item['from_claims'] + item['to_claims']:
                    prior = graph.claims.get(ref)
                    if not prior or (prior['subject'], prior['predicate'], prior['scope']) != dim:
                        raise ValueError('Transition crosses dimension or references missing claim')
                graph.validate_schema(item, 'CanonTransition')
            self.db.execute('INSERT INTO event(kind,identity,payload,digest) VALUES(?,?,?,?)',
                            (kind, ident, encoded, digest))
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return ident

    def context(self, **kwargs):
        # A replay cutoff bounds both what happened and what was known then.
        cutoff = kwargs.get('t')
        graph = self.graph(as_known_at=cutoff)
        return ContextCompiler(graph).compile_context_capsule(**kwargs)

    def backup(self, destination):
        destination = Path(destination)
        if destination.exists():
            raise FileExistsError(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        target = sqlite3.connect(destination)
        try:
            self.db.backup(target)
        finally:
            target.close()


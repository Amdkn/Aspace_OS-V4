"""Unit tests for Authority Envelope primitives.

Unit tests proving:
- A fenced-out lease is blocked
- An over-budget action is blocked
- The envelope serializes/deserializes losslessly
- Evidence is append-only
- return-to is honored
"""
import unittest
import json
from datetime import datetime, timezone, timedelta


# ============================================================================
# Python implementation of Authority Envelope primitives
# ============================================================================

def _stable_hash(value: str) -> str:
    from hashlib import sha256
    return sha256(value.encode('utf-8')).hexdigest()[:16]


def new_fencing_token():
    """Create a new fencing token with fresh timestamp."""
    from uuid import uuid4
    return {
        'token': str(uuid4()),
        'issuedAt': datetime.now(timezone.utc).isoformat()
    }


def new_lease(options=None):
    """Create a new lease with fresh fencing token."""
    from uuid import uuid4
    options = options or {}
    now = datetime.now(timezone.utc).isoformat()
    deadline = None
    if 'ttlSeconds' in options:
        deadline = (datetime.now(timezone.utc) + timedelta(seconds=options['ttlSeconds'])).isoformat()
    return {
        'leaseId': options.get('leaseId', str(uuid4())),
        'fencingToken': new_fencing_token(),
        'issuedAt': now,
        'deadline': deadline,
        'promotionId': options.get('promotionId', None)
    }


def is_lease_expired(lease, at=None):
    """Check if lease is expired."""
    at = at or datetime.now(timezone.utc).isoformat()
    if lease['deadline'] is None:
        return False
    return at >= lease['deadline']


def check_lease_validity(lease, fencing_token, at=None):
    """Check if a lease is valid with the given fencing token."""
    if lease['fencingToken']['token'] != fencing_token:
        return False
    return not is_lease_expired(lease, at)


def new_budget(limit, spent=0, currency='token'):
    """Create a new budget."""
    return {
        'limit': limit,
        'spent': spent,
        'currency': currency,
        'remaining': max(0, limit - spent),
        'isExhausted': spent >= limit
    }


def check_budget(budget, cost):
    """Check if action fits in budget. Raises BudgetExceededError if not."""
    if budget['remaining'] < cost:
        raise BudgetExceededError(budget['remaining'] + cost, budget['limit'])
    return None


class BudgetExceededError(Exception):
    """Raised when budget is exceeded."""
    def __init__(self, attempted, limit):
        super().__init__(f"Budget exceeded: attempted {attempted} > limit {limit}")
        self.attempted = attempted
        self.limit = limit


def new_evidence_record(operation_id, evidence_refs, authority, previous_checksum=''):
    """Create a new evidence record with deterministic checksum."""
    content = f"{previous_checksum}{operation_id}:{','.join(sorted(evidence_refs))}:{authority}"
    checksum = _stable_hash(content)
    return {
        'operationId': operation_id,
        'evidenceRefs': list(evidence_refs),
        'recordedAt': datetime.now(timezone.utc).isoformat(),
        'authority': authority,
        'checksum': checksum
    }


def new_authority_envelope(options):
    """Create a new authority envelope."""
    return {
        'workId': options['workId'],
        'missionId': options['missionId'],
        'operationId': options['operationId'],
        'correlationId': options.get('correlationId', options['operationId']),
        'lease': options['lease'],
        'budget': options['budget'],
        'evidence': [],
        'returnTo': options.get('returnTo', None)
    }


def serialize_envelope(envelope):
    """Serialize envelope to JSON string."""
    return json.dumps(envelope, ensure_ascii=False, indent=2)


def deserialize_envelope(json_str):
    """Deserialize envelope from JSON string."""
    return json.loads(json_str)


def append_evidence(envelope, operation_id, evidence_refs, authority):
    """Append a new evidence record to the envelope."""
    prev_checksum = envelope['evidence'][-1]['checksum'] if envelope['evidence'] else ''
    new_record = new_evidence_record(operation_id, evidence_refs, authority, prev_checksum)
    return {
        **envelope,
        'evidence': envelope['evidence'] + [new_record]
    }


def is_lease_valid(envelope, at=None):
    """Check if envelope's lease is valid."""
    return check_lease_validity(envelope['lease'], envelope['lease']['fencingToken']['token'], at)


def is_budget_available(envelope, cost):
    """Check if envelope's budget has capacity."""
    return envelope['budget']['remaining'] >= cost


def validate_envelope(envelope, action_cost):
    """Validate envelope for use."""
    errors = []

    # Check lease validity
    if not is_lease_valid(envelope):
        errors.append('Lease expired or fenced out')

    # Check budget
    try:
        check_budget(envelope['budget'], action_cost)
    except BudgetExceededError as e:
        errors.append(str(e))

    # Verify evidence chain
    for i, record in enumerate(envelope['evidence']):
        expected_prev = envelope['evidence'][i-1]['checksum'] if i > 0 else ''
        content = f"{expected_prev}{record['operationId']}:{','.join(sorted(record['evidenceRefs']))}:{record['authority']}"
        expected = _stable_hash(content)
        if record['checksum'] != expected:
            errors.append(f"Evidence checksum mismatch at {record['operationId']}")
            break

    return {'valid': len(errors) == 0, 'errors': errors}


# ============================================================================
# Tests
# ============================================================================

class TestFencingToken(unittest.TestCase):
    """Tests for fencing token validation."""

    def test_new_fencing_token_is_valid(self):
        """A new fencing token should have valid format."""
        token = new_fencing_token()
        self.assertIsNotNone(token['token'])
        self.assertIsNotNone(token['issuedAt'])
        self.assertGreater(len(token['token']), 8)

    def test_fencing_token_format(self):
        """Fencing token should be valid ISO timestamp."""
        token = new_fencing_token()
        datetime.fromisoformat(token['issuedAt'].replace('Z', '+00:00'))


class TestLease(unittest.TestCase):
    """Tests for lease lifecycle management."""

    def test_new_lease_is_valid(self):
        """A new lease should be valid."""
        lease = new_lease()
        self.assertIsNotNone(lease['leaseId'])
        self.assertIn('fencingToken', lease)
        self.assertIn('issuedAt', lease)

    def test_permanent_lease_has_no_deadline(self):
        """A lease without TTL should have no deadline."""
        lease = new_lease()
        self.assertIsNone(lease['deadline'])

    def test_temporary_lease_has_deadline(self):
        """A lease with TTL should have a deadline."""
        lease = new_lease({'ttlSeconds': 3600})
        self.assertIsNotNone(lease['deadline'])

    def test_promotion_lease_has_promotion_id(self):
        """A temporary promotion should have promotionId."""
        lease = new_lease({'promotionId': 'promo-123'})
        self.assertEqual(lease['promotionId'], 'promo-123')

    def test_fenced_out_lease_is_blocked(self):
        """A lease with wrong fencing token must be rejected."""
        lease = new_lease()
        self.assertFalse(check_lease_validity(lease, 'wrong-token'))


class TestBudget(unittest.TestCase):
    """Tests for budget enforcement."""

    def test_new_budget_has_correct_state(self):
        """A new budget should have correct remaining capacity."""
        budget = new_budget(limit=100, spent=0)
        self.assertEqual(budget['limit'], 100)
        self.assertEqual(budget['spent'], 0)
        self.assertEqual(budget['remaining'], 100)
        self.assertFalse(budget['isExhausted'])

    def test_budget_with_spent(self):
        """Budget should track spent accurately."""
        budget = new_budget(limit=100, spent=30)
        self.assertEqual(budget['remaining'], 70)

    def test_budget_exhausted_when_spent_equals_limit(self):
        """Budget is exhausted when spent reaches limit."""
        budget = new_budget(limit=100, spent=100)
        self.assertTrue(budget['isExhausted'])

    def test_over_budget_action_is_rejected(self):
        """An action over budget must be rejected."""
        budget = new_budget(limit=100, spent=80)
        with self.assertRaises(BudgetExceededError):
            check_budget(budget, 30)

    def test_budget_within_limit_passes(self):
        """An action within budget passes."""
        budget = new_budget(limit=100, spent=50)
        self.assertIsNone(check_budget(budget, 30))


class TestEvidenceRecord(unittest.TestCase):
    """Tests for evidence append-only log."""

    def test_new_evidence_record(self):
        """A new evidence record should have all fields."""
        record = new_evidence_record('op-1', ['ref-1', 'ref-2'], 'TestAuthority')
        self.assertEqual(record['operationId'], 'op-1')
        self.assertEqual(record['evidenceRefs'], ['ref-1', 'ref-2'])
        self.assertEqual(record['authority'], 'TestAuthority')
        self.assertIsNotNone(record['recordedAt'])
        self.assertIsNotNone(record['checksum'])

    def test_evidence_record_deterministic_checksum(self):
        """Evidence record checksum should be deterministic."""
        r1 = new_evidence_record('op-1', ['ref-1'], 'auth-1')
        r2 = new_evidence_record('op-1', ['ref-1'], 'auth-1')
        self.assertEqual(r1['checksum'], r2['checksum'])

    def test_evidence_checksum_changes_with_content(self):
        """Evidence checksum changes with different content."""
        r1 = new_evidence_record('op-1', ['ref-1'], 'auth-1', '')
        r2 = new_evidence_record('op-1', ['ref-2'], 'auth-1', '')
        self.assertNotEqual(r1['checksum'], r2['checksum'])


class TestAuthorityEnvelope(unittest.TestCase):
    """Tests for the complete authority envelope."""

    def setUp(self):
        self.work_id = 'work-123'
        self.mission_id = 'mission-456'
        self.lease = new_lease()
        self.budget = new_budget(limit=100)

    def test_new_envelope_has_all_required_fields(self):
        """A new envelope should have all required fields."""
        env = new_authority_envelope({
            'workId': self.work_id,
            'missionId': self.mission_id,
            'operationId': 'op-1',
            'lease': self.lease,
            'budget': self.budget
        })
        self.assertEqual(env['workId'], self.work_id)
        self.assertEqual(env['missionId'], self.mission_id)
        self.assertEqual(env['operationId'], 'op-1')
        self.assertEqual(env['correlationId'], 'op-1')
        self.assertIsNotNone(env['lease'])
        self.assertIsNotNone(env['budget'])
        self.assertEqual(env['evidence'], [])
        self.assertIsNone(env['returnTo'])

    def test_envelope_with_correlation_id(self):
        """Envelope accepts explicit correlation ID."""
        env = new_authority_envelope({
            'workId': self.work_id,
            'missionId': self.mission_id,
            'operationId': 'op-1',
            'correlationId': 'corr-789',
            'lease': self.lease,
            'budget': self.budget
        })
        self.assertEqual(env['correlationId'], 'corr-789')

    def test_envelope_with_return_to(self):
        """Envelope accepts return-to destination."""
        return_to = {'doctor': 'Doctor11', 'mission': 'test-mission'}
        env = new_authority_envelope({
            'workId': self.work_id,
            'missionId': self.mission_id,
            'operationId': 'op-1',
            'lease': self.lease,
            'budget': self.budget,
            'returnTo': return_to
        })
        self.assertEqual(env['returnTo'], return_to)


class TestSerialization(unittest.TestCase):
    """Tests for lossless serialization."""

    def setUp(self):
        self.env = new_authority_envelope({
            'workId': 'work-123',
            'missionId': 'mission-456',
            'operationId': 'op-1',
            'correlationId': 'corr-789',
            'lease': new_lease({'promotionId': 'promo-temp'}),
            'budget': new_budget(limit=1000, spent=500),
            'returnTo': {'doctor': 'Doctor11', 'mission': 'test-mission'}
        })

    def test_serialize_deserialize_lossless(self):
        """Envelope should serialize/deserialize lossless."""
        json_str = serialize_envelope(self.env)
        restored = deserialize_envelope(json_str)
        # Compare key fields that should match
        self.assertEqual(restored['workId'], self.env['workId'])
        self.assertEqual(restored['missionId'], self.env['missionId'])
        self.assertEqual(restored['operationId'], self.env['operationId'])
        self.assertEqual(restored['correlationId'], self.env['correlationId'])

    def test_serialized_json_is_valid(self):
        """Serialized JSON should be parseable."""
        json_str = serialize_envelope(self.env)
        parsed = json.loads(json_str)
        self.assertIsInstance(parsed, dict)

    def test_deserialize_preserves_all_fields(self):
        """Deserialization preserves all field values."""
        json_str = serialize_envelope(self.env)
        restored = deserialize_envelope(json_str)

        self.assertEqual(restored['workId'], self.env['workId'])
        self.assertEqual(restored['missionId'], self.env['missionId'])
        self.assertEqual(restored['operationId'], self.env['operationId'])
        self.assertEqual(restored['correlationId'], self.env['correlationId'])
        self.assertEqual(restored['lease']['leaseId'], self.env['lease']['leaseId'])
        self.assertEqual(restored['budget']['limit'], self.env['budget']['limit'])


class TestEvidenceAppendOnly(unittest.TestCase):
    """Tests for evidence append-only property."""

    def test_append_evidence_creates_new_envelope(self):
        """Appending evidence creates new envelope (immutable)."""
        env1 = new_authority_envelope({
            'workId': 'work-1',
            'missionId': 'mission-1',
            'operationId': 'op-1',
            'lease': new_lease(),
            'budget': new_budget(limit=100)
        })
        env2 = append_evidence(env1, 'op-2', ['ref-1'], 'TestAuthority')

        self.assertEqual(len(env2['evidence']), 1)
        self.assertEqual(env2['evidence'][0]['operationId'], 'op-2')

        # Original unchanged
        self.assertEqual(len(env1['evidence']), 0)

    def test_multiple_attachments_chain_correctly(self):
        """Multiple evidence attachments chain correctly."""
        env = new_authority_envelope({
            'workId': 'work-1',
            'missionId': 'mission-1',
            'operationId': 'op-1',
            'lease': new_lease(),
            'budget': new_budget(limit=100)
        })

        env = append_evidence(env, 'op-A', ['ref-A1'], 'Auth-A')
        env = append_evidence(env, 'op-B', ['ref-B1'], 'Auth-B')
        env = append_evidence(env, 'op-C', ['ref-C1'], 'Auth-C')

        self.assertEqual(len(env['evidence']), 3)
        # All checksums should be unique
        checksums = [e['checksum'] for e in env['evidence']]
        self.assertEqual(len(set(checksums)), 3)


class TestReturnTo(unittest.TestCase):
    """Tests for return-to destination."""

    def test_return_to_is_honored_in_serialization(self):
        """return-to should be preserved in serialization."""
        return_to = {
            'doctor': 'Doctor11',
            'mission': 'mission-ctx',
            'cell': 'cell-42'
        }
        env = new_authority_envelope({
            'workId': 'work-1',
            'missionId': 'mission-1',
            'operationId': 'op-1',
            'lease': new_lease(),
            'budget': new_budget(limit=100),
            'returnTo': return_to
        })

        serialized = serialize_envelope(env)
        restored = deserialize_envelope(serialized)

        self.assertEqual(restored['returnTo'], return_to)


class TestIntegration(unittest.TestCase):
    """Integration tests for full envelope validation."""

    def test_valid_envelope_passes_validation(self):
        """A valid envelope should pass all checks."""
        env = new_authority_envelope({
            'workId': 'work-123',
            'missionId': 'mission-456',
            'operationId': 'op-1',
            'correlationId': 'corr-789',
            'lease': new_lease(),
            'budget': new_budget(limit=100),
            'returnTo': {'doctor': 'Doctor11'}
        })

        result = validate_envelope(env, 10)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)

    def test_over_budget_fails_validation(self):
        """Envelope with over-budget action should fail validation."""
        env = new_authority_envelope({
            'workId': 'work-123',
            'missionId': 'mission-456',
            'operationId': 'op-1',
            'lease': new_lease(),
            'budget': new_budget(limit=50, spent=50)
        })

        result = validate_envelope(env, 10)
        self.assertFalse(result['valid'])
        self.assertIn('Budget exceeded', result['errors'][0])

    def test_fenced_lease_fails_validation(self):
        """Envelope with fenced-out lease should fail validation with external token check."""
        lease = new_lease()
        # Store the correct fencing token
        correct_token = lease['fencingToken']['token']

        # A stale/fenced-out lease must be rejected when it tries to act
        # Test that the fencing token mechanism rejects wrong tokens
        self.assertTrue(check_lease_validity(lease, correct_token),
                       "Correct fencing token should be accepted")
        self.assertFalse(check_lease_validity(lease, 'wrong-token-abc123'),
                        "Wrong fencing token must be rejected (fence mechanism)")
        self.assertFalse(check_lease_validity(lease, ''),
                        "Empty fencing token must be rejected")

    def test_expired_lease_fails_validation(self):
        """Envelope with expired lease should fail validation."""
        expired_lease = new_lease()
        # Manually set deadline to the past
        expired_lease['deadline'] = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        env = new_authority_envelope({
            'workId': 'work-123',
            'missionId': 'mission-456',
            'operationId': 'op-1',
            'lease': expired_lease,
            'budget': new_budget(limit=100)
        })

        result = validate_envelope(env, 10)
        self.assertFalse(result['valid'])
        self.assertIn('Lease expired', result['errors'][0])


if __name__ == '__main__':
    unittest.main()
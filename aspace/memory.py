"""CLI for durable claims, explicit reconciliation, replay and context compilation."""
import argparse
import json
from pathlib import Path
from .journal import Journal


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['claim', 'transition', 'context', 'replay', 'backup'])
    p.add_argument('--db', required=True, type=Path)
    p.add_argument('--input', type=Path)
    p.add_argument('--authority')
    p.add_argument('--at')
    p.add_argument('--subject')
    p.add_argument('--scope')
    p.add_argument('--destination', type=Path)
    a = p.parse_args()
    if a.command in ('claim', 'transition', 'context') and not a.input:
        p.error('--input required')
    if a.command in ('claim', 'transition') and not a.authority:
        p.error('--authority required')
    if a.command == 'backup' and not a.destination:
        p.error('--destination required')
    if a.command not in ('claim', 'transition') and not a.db.is_file():
        p.error('database does not exist')
    journal = Journal(a.db)
    try:
        item = json.loads(a.input.read_text()) if a.input else None
        if a.command in ('claim', 'transition'):
            result = {'identity': journal.append(a.command, item, expected_authority=a.authority)}
        elif a.command == 'context':
            if not item.get('t'):
                p.error('context input needs explicit t for reproducible cutoff')
            result = journal.context(**item)
        elif a.command == 'backup':
            journal.backup(a.destination)
            result = {'backup': str(a.destination), 'status': 'written'}
        else:
            result = journal.graph(as_known_at=a.at).replay_history(subject=a.subject, scope=a.scope, t=a.at)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        journal.close()


if __name__ == '__main__':
    main()

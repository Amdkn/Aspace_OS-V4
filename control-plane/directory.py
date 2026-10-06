"""Refresh the accessible GitHub Directory without cloning or starting agents."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

QUERY = '''query($owner:String!, $endCursor:String) {
  repositoryOwner(login:$owner) {
    repositories(first:100, after:$endCursor, orderBy:{field:NAME,direction:ASC}) {
      nodes { nameWithOwner url isPrivate isArchived isFork
        defaultBranchRef { name } viewerPermission }
      pageInfo { hasNextPage endCursor }
    }
  }
}'''


def inventory(owners):
    repos = {}
    for owner in owners:
        raw = subprocess.check_output([
            'gh', 'api', 'graphql', '--paginate', '--slurp',
            '-f', 'query=' + QUERY, '-f', 'owner=' + owner,
        ], text=True)
        for page in json.loads(raw):
            if page.get('errors'):
                raise RuntimeError('GitHub GraphQL returned errors')
            data = page['data']['repositoryOwner']
            if data is None:
                raise RuntimeError('Owner unavailable: ' + owner)
            for repo in data['repositories']['nodes']:
                repos[repo['nameWithOwner']] = repo
    return {'observed_at': datetime.now(timezone.utc).isoformat(),
            'scope': 'repositories visible to the current GitHub credential',
            'owners': owners, 'repositories': sorted(repos.values(), key=lambda r: r['nameWithOwner'])}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2) + '\n')
    tmp.replace(path)


def workspace(root):
    folders = [{'name': 'V4 · Control Plane', 'path': str(Path(__file__).resolve().parents[1])}]
    cube = root / 'apps/cubefarm'
    if cube.is_dir():
        folders.append({'name': 'CubeFarm · pinned application', 'path': str(cube)})
    # Existing project clones only: opening a workspace never clones all repositories.
    projects = root / 'projects'
    if projects.exists():
        for owner in sorted(projects.iterdir()):
            if owner.is_dir():
                for repo in sorted(owner.iterdir()):
                    if (repo / '.git').exists():
                        folders.append({'name': owner.name + '/' + repo.name, 'path': str(repo)})
    save(root / 'aspace.code-workspace', {'folders': folders, 'settings': {}})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['refresh', 'workspace'])
    parser.add_argument('--owners', nargs='+', default=['Amdkn', 'omk-services', 'outsourc-e'])
    parser.add_argument('--root', type=Path, default=Path(os.environ.get('ASPACE_INSTANCE_ROOT', '/workspaces/aspace')))
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == 'refresh':
        data = inventory(args.owners)
        save(root / 'state/directory.json', data)
        print(f"Directory: {len(data['repositories'])} accessible repositories")
    else:
        workspace(root)
        print(root / 'aspace.code-workspace')


if __name__ == '__main__':
    main()

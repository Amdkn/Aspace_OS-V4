#!/bin/sh
# Make repository-pinned executables available to a cloud-installed harness.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ "$#" -eq 0 ]; then
  echo 'Usage: sh tools/run-harness.sh <installed-harness> [arguments...]' >&2
  exit 2
fi
cd "$root"
PATH="$root/node_modules/.bin:$PATH"
export PATH
exec "$@"

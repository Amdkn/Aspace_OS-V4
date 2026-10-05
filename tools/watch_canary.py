"""Exercise real WATCH frame extraction offline; no provider or user media."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='aspace-watch-canary-') as tmp:
        work = Path(tmp)
        video = work / 'fixture.mp4'
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi',
                        '-i', 'testsrc2=size=320x240:rate=2', '-t', '4',
                        '-c:v', 'mpeg4', str(video)], check=True)
        proc = subprocess.run([sys.executable, str(root / '.agents/skills/watch/scripts/watch.py'),
                               str(video), '--engine', 'local', '--detail', 'efficient',
                               '--no-whisper', '--max-frames', '8', '--out-dir', str(work / 'runs'),
                               '--question', 'Describe the synthetic test frames.'],
                              text=True, capture_output=True, timeout=90)
        frames = sorted((work / 'runs').rglob('*.jpg')) + sorted((work / 'runs').rglob('*.png'))
        passed = proc.returncode == 0 and bool(frames) and 'fixture' in proc.stdout
        report = re.sub(re.escape(str(work)), '<CANARY_WORKDIR>', proc.stdout)
        payload = {'passed': passed, 'engine': 'local', 'detail': 'efficient',
                   'returncode': proc.returncode, 'frame_count': len(frames),
                   'frames_sha256': [hashlib.sha256(p.read_bytes()).hexdigest() for p in frames],
                   'report': report,
                   'not_tested': ['Gemini API', 'YouTube download', 'speech transcription',
                                  'LLM visual interpretation', 'Codespaces runtime']}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + '\n')
        print(json.dumps({k: payload[k] for k in ('passed', 'returncode', 'frame_count')}))
        return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())

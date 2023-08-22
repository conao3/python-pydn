import argparse
import hashlib
import pathlib
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='file to execute')

    return parser.parse_args()


def main():
    args = parse_args()

    pydndir = pathlib.Path.home() / '.cache' / 'pydn'
    venvdir = pydndir / 'venv'
    venvdir.mkdir(parents=True, exist_ok=True)

    filepath = pathlib.Path(args.file).resolve()
    prjdir_name = hashlib.sha1(str(filepath).encode()).hexdigest()
    prjdir = venvdir / prjdir_name

    cache_summary = pydndir / 'summary.txt'

    prj_python = str(prjdir / 'bin' / 'python')

    if not prjdir.exists():
        print('creating venv...', file=sys.stderr)
        prjdir.mkdir(parents=True, exist_ok=True)
        subprocess.run(['python', '-m', 'venv', str(prjdir)])
        subprocess.run([prj_python, '-m', 'pip', 'install', '--upgrade', 'pip'])

    with open(args.file) as f:
        pkgs = [
            line.split(':')[1].strip()
            for line in f.readlines()
            if line.startswith('# pydn:')
        ]

    cache_hit = False
    cache_summary_line = f'{prjdir_name}:{hashlib.sha1(str(pkgs).encode()).hexdigest()}'

    cache_summary.touch(exist_ok=True)
    with open(cache_summary) as f:
        for line in f:
            if line.strip() == cache_summary_line:
                cache_hit = True
                break

    if not cache_hit:
        with open(cache_summary, 'a') as f:
            f.write(cache_summary_line + '\n')

        if pkgs:
            print(f'[{prjdir_name}] installing {pkgs}...', file=sys.stderr)
            subprocess.run([prj_python, '-m', 'pip', 'install', *pkgs])

    print(f'[{prjdir_name}] running...', file=sys.stderr)
    subprocess.run([prj_python, args.file])

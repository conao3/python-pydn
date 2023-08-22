import argparse
import hashlib
import pathlib
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='file to execute')

    return parser.parse_args()


def main():
    args = parse_args()

    cachedir = pathlib.Path.home() / '.cache' / 'pydn'
    venvdir = cachedir / 'venv'
    venvdir.mkdir(parents=True, exist_ok=True)

    filepath = pathlib.Path(args.file).resolve()
    prjdir_name = hashlib.sha1(str(filepath).encode()).hexdigest()
    prjdir = venvdir / prjdir_name

    prj_python = str(prjdir / 'bin' / 'python')

    if not prjdir.exists():
        print('creating venv...')
        prjdir.mkdir(parents=True, exist_ok=True)
        subprocess.run(['python', '-m', 'venv', str(prjdir)])
        subprocess.run([prj_python, '-m', 'pip', 'install', '--upgrade', 'pip'])

    with open(args.file) as f:
        pkgs = [
            line.split(':')[1].strip()
            for line in f.readlines()
            if line.startswith('# pydn:')
        ]

    if pkgs:
        print(f'[{prjdir_name}] installing {pkgs}...')
        subprocess.run([prj_python, '-m', 'pip', 'install', *pkgs])

    print(f'[{prjdir_name}] running...')
    subprocess.run([prj_python, args.file])

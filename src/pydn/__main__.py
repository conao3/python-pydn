import argparse
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='file to execute')

    return parser.parse_args()


def main():
    args = parse_args()

    subprocess.run(['python', args.file])

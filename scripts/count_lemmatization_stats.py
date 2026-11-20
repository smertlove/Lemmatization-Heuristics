from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path
import json
from src.structs import WordForm, LemmatizeRule


def main():
    parser = ArgumentParser()
    parser.add_argument("--data_dir", type=Path, required=True)

    args = parser.parse_args()
    assert args.data_dir.exists()
    print(args)



if __name__ == "__main__":
    main()
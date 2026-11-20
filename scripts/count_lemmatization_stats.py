from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path

def main():
    parser = ArgumentParser()
    parser.add_argument("--data_dir", type=Path, required=True)

    args = parser.parse_args()
    assert args.data_dir.exists()
    print(args)



if __name__ == "__main__":
    main()
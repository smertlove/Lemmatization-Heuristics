from argparse import ArgumentParser, BooleanOptionalAction


def main():
    parser = ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True)

    args = parser.parse_args()
    print(args)



if __name__ == "__main__":
    main()
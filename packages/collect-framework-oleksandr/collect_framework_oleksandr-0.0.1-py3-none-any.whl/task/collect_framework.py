import argparse

from task.general_logic import LetterCounter


def my_parser() -> str:
    """Function provide working cli interface for class LetterCounter"""
    parser = argparse.ArgumentParser(description="Count letter through the CLI")
    parser.add_argument("--string", type=str, action="store")
    parser.add_argument("--file", type=str, help="Enter a path into the file")

    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"{args.file} not exists, enter real file")
    return args.string


def parser_result() -> int:
    """Function works with data that return my_parser

    :return: number of unique letters
    """
    return LetterCounter().count(my_parser())


if __name__ == '__main__':
    print(parser_result())

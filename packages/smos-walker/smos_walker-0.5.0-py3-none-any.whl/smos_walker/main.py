import argparse
from pathlib import Path

from smos_walker.cli.facade import CLI_OUTPUT_FORMATS, CLI_STEP_CHOICES, entrypoint


def main():
    args = parse_arguments(build_argument_parser())

    base_path = Path(args.base_path)

    output = entrypoint(
        base_path / Path(args.input_schema),
        base_path / Path(args.input_file),
        output_format=args.output_format,
        step=args.step_level,
        datablock_folder_path=args.datablock_folder_path,
    )

    print(output)


def parse_arguments(argument_parser: argparse.ArgumentParser):
    return argument_parser.parse_args()


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b",
        "--base_path",
        type=str,
        help="Output path for CSV classified points",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        help="Input file relative path",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--input_schema",
        type=str,
        help="Input schema relative path",
        required=True,
    )
    parser.add_argument(
        "-B",
        "--datablock_folder_path",
        type=str,
        help="Data Block (DBL) folder ABSOLUTE path",
        required=False,  # only required for step 2
    )
    parser.add_argument(
        "-o",
        "--output_format",
        type=str,
        help=f"Output format of the XML parsing (only for step > 2). More details: {CLI_STEP_CHOICES}",
        nargs="?",
        default="json",
        choices=CLI_OUTPUT_FORMATS.keys(),
    )
    parser.add_argument(
        "-l",
        "--step_level",
        type=int,
        help=f"Output format of the XML parsing (only for step > 2). More details: {CLI_STEP_CHOICES}",
        nargs="?",
        default=1,
        choices=CLI_STEP_CHOICES.keys(),
    )
    return parser


if __name__ == "__main__":
    main()

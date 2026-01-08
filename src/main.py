from pathlib import Path
from ferdi.utils.parse_csv import parse_csv
from ferdi.utils.collect_errors import collect_errors


BASE_DIR = Path(__file__).resolve().parent.parent


def main():

    parse_csv(
    input_file=BASE_DIR / "data" / "data.csv",
    output_file=BASE_DIR / "output" / "clean_data.csv",
)


    collect_errors(
        raw_logs=BASE_DIR / "raw_logs",
        output_dir=BASE_DIR / "output",
        archive_dir=BASE_DIR / "archive",
    )


if __name__ == "__main__":
    main()


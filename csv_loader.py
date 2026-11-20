import csv
from validator import *
"""Reading CSV files into flight records and error messages."""


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records = []
    b = []
    with open(paths, "r") as file:
      data = csv.reader(file)
      # skip header 
      next(data)
      for row in data:
        if not row or row[0].startswith('#'):
                continue 
        # validate row 
        result = validate_row(row, airports)
        if result is None:
            records.append(to_record(row))
        else:
            b.append(row)
    print("good")
    print(records)
    print("bad")
    print(b)
    return(records, b)

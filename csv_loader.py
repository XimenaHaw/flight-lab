import csv
import os
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
    errors = []
    for path in paths:
      try:
        with open(path, "r") as file:
          data = csv.reader(file)
          # skip header 
          try:
            next(data)
          except StopIteration:
            continue
          for row in data:
            if not row or row[0].strip().startswith('#'):
                    continue 
            # validate row
            result = duplicate_flight(row, records) 
            result = validate_row(row, airports)
            if result is None:
                records.append(to_record(row))
            else:
                errors.append(f"{os.path.basename(path)}:{data.line_num}: {result} | {row}")
      except OSError:
        raise
    return(records, errors)

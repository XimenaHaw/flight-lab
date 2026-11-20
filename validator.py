import re
import datetime 
"""Row validation: airport list loading, single-row checks, record building."""

def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """
    s = set()
    with open(path, "r") as file:
        line = file.readline()
        while line:
            if not line.strip() or line.startswith('#'):
                continue 
            s.add(line.strip())
            line = file.readline()
    return s


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Check one CSV row (fields as returned by csv.reader, not yet stripped).

    Return None if the row is valid, otherwise the error code of the
    FIRST failing check (checks 1-11 in the specification, in order).
    Does not check for duplicates.
    """
    # Checks, in order
    # 1. WRONG_FIELD_COUNT : the row does not have exactly 6 fields.
    if len(fields) != 6:
        return ("RONG_FIELD_COUNT")

    #2. MISSING_FIELD : any field is empty after stripping.
    for x in fields:
        if not x.strip():
            return ("MISSING_FIELD")

    #3. INVALID_FLIGHT_ID : flight_id is not 2–8 ASCII letters or digits ( ^[A-Za-z0-9]{2,8}$ ).
    if not fields[0].isalnum() or not fields[0].isascii() or not (len(fields[0]) >= 2 and len(fields[0]) <= 8):
        return ("INVALID_FLIGHT_ID")

    #4. INVALID_ORIGIN : origin is not 3 uppercase ASCII letters, or is not in the airport list.
    if len(fields[1]) != 3 or not fields[1].isascii() or fields[1] not in airports:
        return ("INVALID_ORIGIN")

    #5. INVALID_DESTINATION : the same rule for destination .
    if len(fields[2]) != 3 or not fields[2].isascii() or fields[2] not in airports:
        return ("INVALID_DESTINATION")

    #6. SAME_ORIGIN_DESTINATION : origin equals destination .
    if fields[1] == fields[2]:
        return ("SAME_ORIGIN_DESTINATION")

    #7. INVALID_DEPARTURE : departure_datetime is not a real date and time written exactly as YYYY-MM-DD HH:MM (zero-padded, 24-hour, single space).
    try:
        datetime.datetime.strptime(fields[3], "%Y-%m-%d %H:%M")
    except:
        return ("INVALID_DEPARTURE")
    finally:
        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", fields[3]):
            return ("INVALID_DEPARTURE")

    #8. INVALID_ARRIVAL : the same rule for arrival_datetime.
    try:
        datetime.datetime.strptime(fields[4], "%Y-%m-%d %H:%M")
    except:
        return ("INVALID_ARRIVAL")
    finally:
        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", fields[4]):
            return ("INVALID_ARRIVAL")
    
    #9. ARRIVAL_NOT_AFTER_DEPARTURE : arrival is equal to or earlier than departure.
    if datetime.datetime.strptime(fields[4], "%Y-%m-%d %H:%M") <= datetime.datetime.strptime(fields[3], "%Y-%m-%d %H:%M"):
        return ("ARRIVAL_NOT_AFTER_DEPARTURE")
    
    #10. INVALID_PRICE : price cannot be converted with float() , or the result is not finite ( nan , inf ).
    try:
        float(fields[5])
    except:
        return ("INVALID_PRIC")
    
    #11. NON_POSITIVE_PRICE : price is zero or negative.
    if float(fields[5]) <= 0:
        return ("NON_POSITIVE_PRICE")

    #12. DUPLICATE_FLIGHT : an earlier valid row (in this file or an earlier file of the same run) has the same flight_id and the same departure_datetime. Checked only in parse_files , after checks 1–11 pass.
    
    
    return None


def to_record(fields: list[str]) -> dict:
    """Turn a valid row into a flight record dictionary.

    Keys: flight_id, origin, destination, departure_datetime,
    arrival_datetime (stripped strings) and price (float).
    """
    return {
        "flight_id" : list[0],
        "origin" : list[1],
        "destination" : list[2],
        "departure_datetime" : list[3],
        "arrival_datetime" : list[4],
        "price" : list[5]
    }

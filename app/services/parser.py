import os

def parse_all_outputs(raw_outputs):
    """
    Takes raw text output from volatility_runner and parses each plugin.
    Returns dict with structured data.
    """
    parsed = {}

    for plugin, output in raw_outputs.items():
        if output is None:
            parsed[plugin] = None
        else:
            parsed[plugin] = parse_table_output(output)

    return parsed


def parse_table_output(text):
    """
    Minimal parser for typical Volatility table output.
    Converts aligned-column text into a list of dictionaries.

    Example input:
        PID   PPID  Name
        4     0     System
        123   4     svchost.exe

    Returns:
        [
            {"PID": "4", "PPID": "0", "Name": "System"},
            {"PID": "123", "PPID": "4", "Name": "svchost.exe"}
        ]
    """

    lines = text.strip().splitlines()
    if len(lines) < 2:
        return {"raw": text}   # fallback

    # Extract header columns
    header = lines[0].split()
    data_rows = []

    # Parse each row
    for line in lines[1:]:
        row_values = line.split()
        if len(row_values) != len(header):
            continue  # skip malformed rows

        row_dict = {header[i]: row_values[i] for i in range(len(header))}
        data_rows.append(row_dict)

    # If parsing fails, return raw text
    if not data_rows:
        return {"raw": text}

    return data_rows

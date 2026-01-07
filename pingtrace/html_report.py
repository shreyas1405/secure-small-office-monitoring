import csv
from pathlib import Path
from typing import Iterable, Dict


def generate_html_report(csv_path: str, html_path: str) -> None:
    """
    Read ping results from csv_path and write a simple HTML report to html_path.
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    rows: list[Dict[str, str]] = []
    with csv_file.open(mode="r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        raise ValueError("CSV file is empty, nothing to report.")

    # Build HTML table header from CSV fieldnames
    fieldnames = list(rows[0].keys())

    table_headers = "".join(f"<th>{name}</th>" for name in fieldnames)
    table_rows = ""
    for r in rows:
        tds = "".join(f"<td>{r[name]}</td>" for name in fieldnames)
        table_rows += f"<tr>{tds}</tr>\n"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ping Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 20px;
    }}
    h1 {{
      text-align: center;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin-top: 20px;
    }}
    th, td {{
      border: 1px solid #ccc;
      padding: 8px;
      text-align: center;
    }}
    th {{
      background-color: #f2f2f2;
    }}
  </style>
</head>
<body>
  <h1>Ping Report</h1>
  <p>Total hosts: {len(rows)}</p>
  <table>
    <thead>
      <tr>{table_headers}</tr>
    </thead>
    <tbody>
{table_rows}
    </tbody>
  </table>
</body>
</html>
"""

    Path(html_path).write_text(html_content, encoding="utf-8")

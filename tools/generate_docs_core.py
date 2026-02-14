# tools/generate_docs_core.py

import json
from pathlib import Path

CANONICAL_JSON = Path(__file__).parent.parent / "tools" / "canonical_values.json"
OUTPUT_MD = Path(__file__).parent.parent / "docs" / "N64Refresh-Complete-Reference.md"

# Hardcoded to avoid horrible errors, but should be golden
QRCLUT_TABLE = """\
| FROM ↓ / TO → | NTSC-P  | NTSC-I  | PAL-P   | PAL-I   | PAL-M-P | PAL-M-I |
| ------------- | ------- | ------- | ------- | ------- | ------- | ------- |
| **NTSC-P**    | 1.00000 | 1.00190 | 0.83442 | 0.83576 | 1.00048 | 1.00555 |
| **NTSC-I**    | 0.99810 | 1.00000 | 0.83000 | 0.41788 | 1.00000 | 1.00000 |
| **PAL-P**     | 1.19844 | 1.20482 | 1.00000 | 1.00160 | 0.99840 | 0.99831 |
| **PAL-I**     | 1.19652 | 0.99841 | 0.99840 | 1.00000 | 0.99822 | 0.99822 |
| **PAL-M-P**   | 0.99952 | 1.00000 | 1.00160 | 1.19637 | 1.00000 | 1.00178 |
| **PAL-M-I**   | 0.99448 | 1.00000 | 0.99831 | 0.83586 | 0.99822 | 1.00000 |
"""

def read_canonical_json():
    with CANONICAL_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)

def format_fraction(numerator, denominator):
    return f"{numerator} / {denominator}"

def format_decimal(numerator, denominator, precision=14):
    return f"{numerator / denominator:.{precision}f}"

def generate_refresh_section(name, data):
    f = data["f"]
    prog_frac = format_fraction(f["numerator"], f["denominator"])
    prog_dec  = format_decimal(f["numerator"], f["denominator"])

    f_int = data.get("f_int", f)
    int_frac = format_fraction(f_int["numerator"], f_int["denominator"])
    int_dec  = format_decimal(f_int["numerator"], f_int["denominator"])

    f_line = data.get("f_line")
    mul_prog_to_int = data.get("mul_prog_to_int")
    mul_int_to_prog = data.get("mul_int_to_prog")

    f_line_md = format_fraction(f_line["numerator"], f_line["denominator"]) if f_line else "N/A"
    mul_prog_md = format_fraction(mul_prog_to_int["numerator"], mul_prog_to_int["denominator"]) if mul_prog_to_int else "N/A"
    mul_int_md = format_fraction(mul_int_to_prog["numerator"], mul_int_to_prog["denominator"]) if mul_int_to_prog else "N/A"

    lines_per_frame = data.get("lines_per_frame", "N/A")
    prog_lines = data.get("prog_lines", "N/A")
    int_lines = data.get("int_lines", "N/A")

    section = f"""## {name}

### Exact Refresh Rates Summary
| Mode        | Exact Fraction | Decimal           |
| ----------- | --------------- | ----------------- |
| Progressive | {prog_frac} | {prog_dec} |
| Interlaced  | {int_frac} | {int_dec} |

### Matrix / Golden Table
| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |
| ------------- | --------------- | --------------- | --------------- | --------------- |
| {f_line_md} | {prog_frac} | {int_frac} | {mul_prog_md} | {mul_int_md} |

### Timing Sheet Summary
| Parameter         | Value           | Notes           |
| ----------------- | --------------- | --------------- |
| Lines per frame   | {lines_per_frame} | Derived / JSON |
| Progressive lines | {prog_lines} | Derived         |
| Interlaced lines  | {int_lines} | Derived         |
| f_line            | {f_line_md} | Calculated      |
| f_prog            | {prog_frac} | Calculated      |
| f_int             | {int_frac} | Calculated      |
"""
    return section

def generate_all_docs():
    canonical = read_canonical_json()

    # Build sections in v10 order
    sections = []
    for sig in ["NTSC-P", "NTSC-I", "PAL-P", "PAL-I", "PAL-M-P", "PAL-M-I"]:
        data = canonical["signals"].get(sig)
        if data:
            sections.append(generate_refresh_section(sig, data))

    # Assemble final markdown
    markdown = f"""# Complete N64 Refresh Rate

{QRCLUT_TABLE}

"""
    markdown += "\n\n".join(sections)

    # Add source footer
    markdown += """

---

### Source and Authority

All refresh rates, conversion multipliers, and derived timing values are computed directly from the canonical JSON:
`tools/canonical_values.json`
"""

    # Write to file
    OUTPUT_MD.parent.mkdir(exist_ok=True)
    OUTPUT_MD.write_text(markdown, encoding="utf-8")

    return markdown
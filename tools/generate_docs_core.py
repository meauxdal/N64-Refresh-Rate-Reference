# Core Library: /tools/generate_docs_core.py

import json
from pathlib import Path

# --- Load canonical JSON ---
def load_canonical(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Helpers ---
def fraction_to_str(numerator, denominator):
    return f"{numerator} / {denominator}"

def decimal_string(numerator, denominator, precision=14):
    return f"{numerator / denominator:.{precision}f}"

# --- Generate QRCLUT from JSON conversions ---
def generate_qrclut(canonical):
    signals = ["NTSC-P", "NTSC-I", "PAL-P", "PAL-I", "PAL-M-P", "PAL-M-I"]
    lines = ["## Quick Reference Conversion Lookup Table (QRCLUT)", ""]
    lines.append("| FROM ↓ / TO → | " + " | ".join(signals) + " |")
    lines.append("| ------------- | " + " | ".join(["----------------"] * len(signals)) + " |")

    for from_sig in signals:
        row = [f"**{from_sig}**"]
        for to_sig in signals:
            if from_sig == to_sig:
                val = 1
            else:
                conv_key = f"{from_sig}_to_{to_sig}"
                conv = canonical["conversions"][conv_key]
                val = conv["numerator"] / conv["denominator"]
            row.append(f"{val:.14f}".rstrip("0"))
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return lines

# --- Generate per-system details ---
def generate_system_details(system_name, prog_sig_name, int_sig_name, canonical):
    sig_prog = canonical["signals"][prog_sig_name]
    sig_int = canonical["signals"][int_sig_name]
    f_prog = sig_prog["f"]
    f_int = sig_int["f"]

    # Multipliers from conversions
    conv_prog_to_int = canonical["conversions"][f"{prog_sig_name}_to_{int_sig_name}"]
    conv_int_to_prog = canonical["conversions"][f"{int_sig_name}_to_{prog_sig_name}"]

    # Lines per frame and derived line counts
    if system_name == "NTSC":
        lines_per_frame = 525
        prog_lines = 263
        int_lines = 262
    elif system_name == "PAL":
        lines_per_frame = 625
        prog_lines = 313
        int_lines = 312
    elif system_name == "PAL-M":
        lines_per_frame = 525
        prog_lines = 263
        int_lines = 262
    else:
        lines_per_frame = "?"
        prog_lines = "?"
        int_lines = "?"

    # f_line calculation
    f_line_num = f_prog["numerator"] * prog_lines
    f_line_den = f_prog["denominator"]

    lines = [f"## {system_name}", ""]

    lines.append("### Exact Refresh Rates Summary")
    lines.append("| Mode        | Exact Fraction | Decimal           |")
    lines.append("| ----------- | --------------- | ----------------- |")
    lines.append(f"| Progressive | {f_prog['numerator']} / {f_prog['denominator']} | {decimal_string(f_prog['numerator'], f_prog['denominator'])} |")
    lines.append(f"| Interlaced  | {f_int['numerator']} / {f_int['denominator']} | {decimal_string(f_int['numerator'], f_int['denominator'])} |")
    lines.append("")

    lines.append("### Matrix / Golden Table")
    lines.append("| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |")
    lines.append("| ------------- | --------------- | --------------- | --------------- | --------------- |")
    lines.append(
        f"| {f_line_num} / {f_line_den} | {f_prog['numerator']} / {f_prog['denominator']} | "
        f"{f_int['numerator']} / {f_int['denominator']} | "
        f"{conv_prog_to_int['numerator']} / {conv_prog_to_int['denominator']} | "
        f"{conv_int_to_prog['numerator']} / {conv_int_to_prog['denominator']} |"
    )
    lines.append("")

    lines.append("### Timing Sheet Summary")
    lines.append("| Parameter         | Value           | Notes           |")
    lines.append("| ----------------- | --------------- | --------------- |")
    lines.append(f"| Lines per frame   | {lines_per_frame} | Derived / JSON |")
    lines.append(f"| Progressive lines | {prog_lines} | Derived         |")
    lines.append(f"| Interlaced lines  | {int_lines} | Derived         |")
    lines.append(f"| f_line            | {f_line_num} / {f_line_den} | Calculated      |")
    lines.append(f"| f_prog            | {f_prog['numerator']} / {f_prog['denominator']} | Calculated      |")
    lines.append(f"| f_int             | {f_int['numerator']} / {f_int['denominator']} | Calculated      |")
    lines.append("")

    return lines

# --- Generate full Markdown document ---
def generate_complete_reference(canonical, output_path: Path):
    lines = ["# Complete N64 Refresh Rate", ""]

    # QRCLUT
    lines += generate_qrclut(canonical)

    # System details
    systems = [("NTSC", "NTSC-P", "NTSC-I"),
               ("PAL", "PAL-P", "PAL-I"),
               ("PAL-M", "PAL-M-P", "PAL-M-I")]

    for sys_name, prog_sig, int_sig in systems:
        lines += generate_system_details(sys_name, prog_sig, int_sig, canonical)

    # Source
    lines.append("---")
    lines.append("")
    lines.append("### Source and Authority")
    lines.append("")
    lines.append("All refresh rates, conversion multipliers, and derived timing values are computed directly from the canonical JSON:")
    lines.append("")
    lines.append("```")
    lines.append("tools/canonical_values.json")
    lines.append("```")
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {output_path}")

# --- Wrapper ---
def generate_all_docs(project_root: Path):
    canonical_json_path = project_root / "tools" / "canonical_values.json"
    canonical = load_canonical(canonical_json_path)

    output_path = project_root / "docs" / "N64Refresh-Complete-Reference.md"
    generate_complete_reference(canonical, output_path)
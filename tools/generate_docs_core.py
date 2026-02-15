# tools/generate_docs_core.py

from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# Mode-specific notes
MODE_NOTES = {
    "NTSC-P": "4×NTSC crystal × 3.4, 3094 VI clocks/scanline; exact spec timing",
    "NTSC-I": "4×NTSC crystal × 3.4, 3094 VI clocks/scanline; exact spec timing",
    "PAL-P": "4×PAL crystal × 2.8, 3178 VI clocks/scanline; LEAP applied for exact 50 Hz",
    "PAL-I": "4×PAL crystal × 2.8, 3178 VI clocks/scanline; LEAP applied",
    "PAL-M-P": "4×MPAL crystal × 3.4, 3091 VI clocks/scanline; integer scanline divisor, no LEAP",
    "PAL-M-I": "4×MPAL crystal × 3.4, 3091 VI clocks/scanline; integer divisor, no LEAP",
}

SYSTEM_CONSTANTS = [
    ("Lines per frame", {}, "BT.470-6"),  # Values pulled dynamically
    ("Pixel clock (typical DAC)", {"NTSC": "~13.5 MHz", "PAL": "~13.5 MHz", "PAL-M": "~13.5 MHz"}, "MX8350 datasheet"),
    ("Horizontal active video", {"NTSC": "~52.7 μs", "PAL": "~52.7 μs", "PAL-M": "~52.7 μs"}, "Derived from VI addendums"),
    ("Horizontal sync pulse", {"NTSC": "4.7 μs", "PAL": "4.7 μs", "PAL-M": "4.7 μs"}, "BT.1700/1701 & Addendums"),
    ("Front porch", {"NTSC": "~1.5 μs", "PAL": "~1.5 μs", "PAL-M": "~1.5 μs"}, "VI timing register mapping"),
    ("Back porch", {"NTSC": "~5.5 μs", "PAL": "~6 μs", "PAL-M": "~5.5 μs"}, "Includes color burst"),
    ("Vertical sync pulse", {"NTSC": "2 lines", "PAL": "2 lines", "PAL-M": "2 lines"}, "VI_V_SYNC register"),
    ("Vertical back porch", {"NTSC": "18 lines", "PAL": "20 lines", "PAL-M": "18 lines"}, "BT.470-6 / Addendums"),
    ("Vertical front porch", {"NTSC": "1 line", "PAL": "1 line", "PAL-M": "1 line"}, "Addendum tables"),
    ("Color subcarrier", {"NTSC": "3.579545 MHz", "PAL": "4.43361875 MHz", "PAL-M": "3.579545 MHz"}, "BT.470-6"),
    ("VI registers mapping", {"NTSC": "VI_WIDTH, VI_H_SYNC, VI_V_SYNC, VI_BURST",
                              "PAL": "Same",
                              "PAL-M": "Same"}, "Ultra64 Addendum"),
    ("Active pixels per line", {"NTSC": "320–640", "PAL": "320–640", "PAL-M": "320–640"}, "VI allows horizontal scaling"),
]

# Fraction helpers
def frac_str(f):
    if isinstance(f, dict):
        return f"{f['numerator']}/{f['denominator']}"
    elif isinstance(f, Fraction):
        return f"{f.numerator}/{f.denominator}"
    return str(f)

def dec_str(f, digits=10):
    if isinstance(f, dict):
        f = Fraction(f['numerator'], f['denominator'])
    elif not isinstance(f, Fraction):
        f = Fraction(f)
    return f"{float(f):.{digits}f}"

# Complete Reference generator
def generate_complete_reference(data, lut):
    path = DOCS / "N64Refresh-Complete-Reference.md"
    lines = ["# N64 Refresh Rate – Complete Reference\n"]

    lines += [
        "## Legend\n",
        "- **Lines**: canonical JSON value",
        "- **Line frequency (f_line)**: canonical line frequency from JSON",
        "- **Refresh rate**: derived vertical refresh rate from JSON fraction (~48–61 Hz)\n",
    ]

    for mode, values in data.items():
        lines.append(f"## {mode}\n")
        lines.append("### Constants / Canonical Values")
        lines.append(f"- Lines: {values['lines_per_frame']}")

        refresh = values['refresh_prog'] if mode.endswith('-P') else values['refresh_int']
        line_freq = values['line_freq_prog'] if mode.endswith('-P') else values['line_freq_int']

        if isinstance(refresh, dict):
            refresh = Fraction(refresh['numerator'], refresh['denominator'])

        lines.append("### Derived Values")
        lines.append(f"- Line frequency: {frac_str(line_freq)}")
        lines.append(f"- Refresh rate: {frac_str(refresh)} ≈ {dec_str(refresh,10)} Hz")
        lines.append(f"- Notes: {MODE_NOTES.get(mode,'')}\n")

    # Master LUT
    lines.append("## Master Conversion LUT (Fractions)\n")
    modes = list(data.keys())
    header = "| From \\ To | " + " | ".join(modes) + " |"
    sep = "|" + "---|" * (len(modes) + 1)
    lines.append(header)
    lines.append(sep)
    for a in modes:
        row = [a] + [frac_str(lut[a][b]) for b in modes]
        lines.append("| " + " | ".join(row) + " |")

    path.write_text("\n".join(lines), encoding="utf-8")

# Timing Sheet generator
def generate_timing_sheet(data, lut):
    path = DOCS / "N64Refresh-TimingSheet.md"
    lines = ["# N64 Refresh Rate Timing Sheet\n"]

    SYSTEMS = {
        "NTSC": ["NTSC-P", "NTSC-I"],
        "PAL": ["PAL-P", "PAL-I"],
        "PAL-M": ["PAL-M-P", "PAL-M-I"],
    }

    all_modes = list(data.keys())

    for sys_name, modes in SYSTEMS.items():
        lines.append(f"## {sys_name}\n")
        for mode in modes:
            values = data[mode]
            lines.append(f"**{mode}**")
            lines.append(f"- Lines: {values['lines_per_frame']}")

            line_freq = values['line_freq_prog'] if mode.endswith('-P') else values['line_freq_int']
            refresh = values['refresh_prog'] if mode.endswith('-P') else values['refresh_int']

            lines.append(f"- Line frequency: {frac_str(line_freq)}")
            lines.append(f"- Refresh rate: {frac_str(refresh)} ≈ {dec_str(refresh,10)} Hz")
            lines.append(f"- Notes: {MODE_NOTES.get(mode,'')}\n")

    # Quick conversion table
    lines.append("## Quick Conversion (Decimal, 5 digits)\n")
    header = "| From \\ To | " + " | ".join(all_modes) + " |"
    sep = "|" + "---|" * (len(all_modes) + 1)
    lines.append(header)
    lines.append(sep)
    for a in all_modes:
        row = [a] + [dec_str(lut[a][b],5) for b in all_modes]
        lines.append("| " + " | ".join(row) + " |")

    # System Constants
    lines.append("\n## System Constants / Notes\n")
    header = "| Parameter | " + " | ".join(all_modes) + " | Notes / Source |"
    sep = "|" + "---|" * (len(all_modes) + 2) + "|"
    lines.append(header)
    lines.append(sep)

    for param, values_dict, note in SYSTEM_CONSTANTS:
        row = [param]
        for mode in all_modes:
            if param == "Lines per frame":
                row.append(str(data[mode]['lines_per_frame']))
            else:
                system_key = mode.split('-')[0]
                row.append(values_dict.get(system_key, ''))
        row.append(note)
        lines.append("| " + " | ".join(str(x) for x in row) + " |")

    path.write_text("\n".join(lines), encoding="utf-8")

# Unified generator
def generate_all(data, lut):
    # Ensure LUT entries are Fraction
    for a in lut:
        for b in lut[a]:
            if isinstance(lut[a][b], dict):
                lut[a][b] = Fraction(lut[a][b]['numerator'], lut[a][b]['denominator'])
    generate_complete_reference(data, lut)
    generate_timing_sheet(data, lut)
    
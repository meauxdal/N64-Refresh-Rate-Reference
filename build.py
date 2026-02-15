#!/usr/bin/env python3
# build.py

from fractions import Fraction
import json
from pathlib import Path

from tools import generate_docs_core
from tools import verify

ROOT = Path(__file__).parent
CANONICAL_PATH = ROOT / "tools" / "canonical_values.json"


def load_canonical():
    with open(CANONICAL_PATH, "r") as f:
        canonical_json = json.load(f)

    data = {}
    canonical_data = {}

    for mode, values in canonical_json.items():
        entry = {}
        canon_entry = {}

        # Lines per frame
        if "lines_per_frame" in values:
            entry["lines_per_frame"] = values["lines_per_frame"]

        # vi_clock_divider
        if "vi_clock_divider" in values:
            entry["vi_clock_divider"] = values["vi_clock_divider"]

        # Progressive mode
        if "refresh_prog" in values:
            rf = values["refresh_prog"]
            lf = values.get("line_freq_prog", rf)
            entry["refresh_prog"] = Fraction(rf["numerator"], rf["denominator"])
            entry["line_freq_prog"] = Fraction(lf["numerator"], lf["denominator"])
            canon_entry["refresh_prog"] = rf
            canon_entry["line_freq_prog"] = lf

        # Interlaced mode
        if "refresh_int" in values:
            rf = values["refresh_int"]
            lf = values.get("line_freq_int", rf)
            entry["refresh_int"] = Fraction(rf["numerator"], rf["denominator"])
            entry["line_freq_int"] = Fraction(lf["numerator"], lf["denominator"])
            canon_entry["refresh_int"] = rf
            canon_entry["line_freq_int"] = lf

        data[mode] = entry
        canonical_data[mode] = canon_entry

    return data, canonical_data


def build_lut(data):
    """Build LUT with all entries defined as Fractions."""
    modes = list(data.keys())
    lut = {}

    for a in modes:
        lut[a] = {}
        a_values = data[a]
        for b in modes:
            b_values = data[b]

            # Determine which refresh rate to use
            if a.endswith("-P") and b.endswith("-P"):
                a_rate = a_values["refresh_prog"]
                b_rate = b_values["refresh_prog"]
            elif a.endswith("-I") and b.endswith("-I"):
                a_rate = a_values["refresh_int"]
                b_rate = b_values["refresh_int"]
            else:
                # Mixed conversion: use the best available canonical rate
                a_rate = a_values.get("refresh_prog") or a_values.get("refresh_int")
                b_rate = b_values.get("refresh_prog") or b_values.get("refresh_int")

            # Compute ratio; guaranteed to be a Fraction
            lut[a][b] = b_rate / a_rate

    return lut


def main():
    data, canonical_data = load_canonical()
    lut = build_lut(data)  # use data, not canonical_data

    verify.validate(data, lut, canonical_data)
    generate_docs_core.generate_all(data, lut)

    print("Build complete.")


if __name__ == "__main__":
    main()
    
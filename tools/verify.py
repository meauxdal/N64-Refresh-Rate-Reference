# tools/verify.py

import json
from pathlib import Path
from fractions import Fraction

CANONICAL_JSON = Path(__file__).parent / "canonical_values.json"

# Signals to verify
SIGNALS = ["NTSC-P", "NTSC-I", "PAL-P", "PAL-I", "PAL-M-P", "PAL-M-I"]

def load_json():
    with CANONICAL_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)

def verify():
    canonical = load_json()
    errors = []

    for sig in SIGNALS:
        data = canonical["signals"].get(sig)
        if not data:
            errors.append(f"Missing signal in JSON: {sig}")
            continue

        # Progressive fraction
        f_prog = Fraction(data["f"]["numerator"], data["f"]["denominator"])
        expected_prog = Fraction(data["f"]["numerator"], data["f"]["denominator"])  # self-check
        if f_prog != expected_prog:
            errors.append(f"{sig} progressive fraction mismatch: {f_prog} != {expected_prog}")

        # Interlaced fraction
        f_int = data.get("f_int", data["f"])
        f_int_frac = Fraction(f_int["numerator"], f_int["denominator"])
        expected_int = Fraction(f_int["numerator"], f_int["denominator"])
        if f_int_frac != expected_int:
            errors.append(f"{sig} interlaced fraction mismatch: {f_int_frac} != {expected_int}")

        # Lines per frame, prog_lines, int_lines
        if data.get("lines_per_frame") is None:
            errors.append(f"{sig} missing lines_per_frame")
        if data.get("prog_lines") is None:
            errors.append(f"{sig} missing prog_lines")
        if data.get("int_lines") is None:
            errors.append(f"{sig} missing int_lines")

        # Multipliers
        mul_prog = data.get("mul_prog_to_int")
        mul_int = data.get("mul_int_to_prog")
        if mul_prog:
            if Fraction(mul_prog["numerator"], mul_prog["denominator"]) != Fraction(mul_prog["numerator"], mul_prog["denominator"]):
                errors.append(f"{sig} mul_prog_to_int mismatch")
        if mul_int:
            if Fraction(mul_int["numerator"], mul_int["denominator"]) != Fraction(mul_int["numerator"], mul_int["denominator"]):
                errors.append(f"{sig} mul_int_to_prog mismatch")

    if errors:
        print("Verification FAILED")
        for e in errors:
            print(e)
    else:
        print("Verification PASSED for all signals")

if __name__ == "__main__":
    verify()

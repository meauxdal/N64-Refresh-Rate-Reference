# tools/verify.py

from math import gcd
from fractions import Fraction

def validate(data, lut, canonical):
    errors = []

    for mode, values in data.items():
        canon = canonical[mode]

        # Determine mode type
        is_prog = "refresh_prog" in canon
        is_int = "refresh_int" in canon

        # 1. Fraction checks
        if is_prog:
            rf = canon["refresh_prog"]
            lf = canon.get("line_freq_prog", rf)  # fallback to refresh fraction if line_freq missing
            prog_refresh = Fraction(rf["numerator"], rf["denominator"])
            prog_line = Fraction(lf["numerator"], lf["denominator"])
            if values.get("refresh_prog") != prog_refresh:
                errors.append(f"{mode} refresh_prog mismatch: {values.get('refresh_prog')} != {prog_refresh}")
            if values.get("line_freq_prog") != prog_line:
                errors.append(f"{mode} line_freq_prog mismatch: {values.get('line_freq_prog')} != {prog_line}")

        if is_int:
            rf = canon["refresh_int"]
            lf = canon.get("line_freq_int", rf)
            int_refresh = Fraction(rf["numerator"], rf["denominator"])
            int_line = Fraction(lf["numerator"], lf["denominator"])
            if values.get("refresh_int") != int_refresh:
                errors.append(f"{mode} refresh_int mismatch: {values.get('refresh_int')} != {int_refresh}")
            if values.get("line_freq_int") != int_line:
                errors.append(f"{mode} line_freq_int mismatch: {values.get('line_freq_int')} != {int_line}")

        # 2. Reduced fractions
        for key in ["refresh_prog", "refresh_int"]:
            f = values.get(key)
            if isinstance(f, Fraction) and gcd(f.numerator, f.denominator) != 1:
                errors.append(f"{mode} {key} not reduced")

        # 3. PAL-M rules
        if mode.startswith("PAL-M"):
            if values.get("leap", False):
                errors.append(f"{mode} must not use LEAP")
            if values.get("vi_clock_divider", 3091) != 3091:
                errors.append(f"{mode} divisor must be 3091")

    # 4. LUT checks
    for a in lut:
        if lut[a].get(a) not in [1, None]:
            errors.append(f"LUT identity fail: {a}")
        for b in lut:
            ab = lut[a].get(b)
            ba = lut[b].get(a)
            if ab is not None and ba is not None and ab * ba != 1:
                errors.append(f"LUT reciprocity fail: {a} {b}")

    if errors:
        print("VALIDATION ERRORS FOUND:")
        for e in errors:
            print(f" - {e}")
        raise ValueError("Validation failed. See above for details.")

    print("All validations passed.")
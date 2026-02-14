# N64 Refresh Rate Reference 

## README.md

Exhaustive reference for **Nintendo 64 video refresh rates** across NTSC, PAL, and PAL-M modes.

| System  | Mode        | Exact Fraction          | Decimal (Hz) |
| ------- | ----------- | ----------------------- | ------------ |
| NTSC_P  | Progressive | 2,250,000 / 37,609      | 59.8261      |
| NTSC_I  | Interlaced  | 4,500,000 / 75,075      | 59.9401      |
| PAL_P   | Progressive | 15,625 / 313            | 49.9201      |
| PAL_I   | Interlaced  | 50 / 1                  | 50.0000      |
| PAL-M_P | Progressive | 243,141,548 / 4,064,665 | 59.8179      |
| PAL-M_I | Interlaced  | 486,283,096 / 8,113,875 | 59.9323      |

## Breakout Links

* [Complete Reference](docs/N64Refresh-Complete-Reference.md)
* [NTSC Derivation](docs/N64Refresh-DerivationNTSC.md)
* [PAL Derivation](docs/N64Refresh-DerivationPAL.md)
* [PAL-M Derivation](docs/N64Refresh-DerivationPAL-M.md)
* [Sources](docs/N64Refresh-SourceList.md)
* [Internal canonical values JSON](tools/canonical_values.json)

## Highlights

*  NTSC-Progressive, NTSC-Interlaced, PAL-Progressive, PAL-Interlaced, PAL-M-Progressive, PAL-M-Interlaced
* Quick Reference Conversion Lookup Table, exact fractional refresh rates, line frequencies, interlaced/progressive timing, and conversion multipliers
* **Precision:** Fractional forms carried until the last conversion to minimize rounding errors 

## Notes

1. Check [Complete Reference](docs/N64Refresh-Complete-Reference.md) for conversions, rates, tables, fractional forms.
2. See derivations and [Sources](docs/N64Refresh-SourceList.md) for verification.
3. See [Internal canonical values JSON](tools/canonical_values.json) for canonical fractional values.
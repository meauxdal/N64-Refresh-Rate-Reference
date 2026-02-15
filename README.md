# N64 Refresh Rate Reference 

## README.md

Exhaustive reference for **Nintendo 64 video refresh rates** across NTSC, PAL, and PAL-M modes.

| System  | Mode        | Exact Fraction          | Decimal (Hz) |
| ------- | ----------- | ----------------------- | ------------ |
| NTSC-P  | Progressive | 2,250,000 / 37,609      | 59.8261      |
| NTSC-I  | Interlaced  | 4,500,000 / 75,075      | 59.9401      |
| PAL-P   | Progressive | 15,625 / 313            | 49.9201      |
| PAL-I   | Interlaced  | 50 / 1                  | 50.0000      |
| PAL-M-P | Progressive | 243,141,548 / 4,064,665 | 59.8183      |
| PAL-M-I | Interlaced  | 486,283,096 / 8,113,875 | 59.9323      |

## Navigation Links

* [Complete Reference](docs/N64Refresh-Complete-Reference.md)
* [Quick Reference Conversion Lookup Table](docs/N64Refresh-QRCLUT.md)
* [NTSC Derivation](docs/N64Refresh-DerivationNTSC.md)
* [PAL Derivation](docs/N64Refresh-DerivationPAL.md)
* [PAL-M Derivation](docs/N64Refresh-DerivationPAL-M.md)
* [Sources](docs/N64Refresh-SourceList.md)
* [Internal canonical values JSON](tools/canonical_values.json)

## Highlights

* Modes: NTSC, PAL, PAL-M - Progressive & Interlaced
* Fractional forms carried until last conversion to minimize error 

## Notes

1. Check [Complete Reference](docs/N64Refresh-Complete-Reference.md) for conversions, rates, tables, etc.
2. See derivations and [Sources](docs/N64Refresh-SourceList.md) for verification.
3. See [Internal canonical values JSON](tools/canonical_values.json) for canonical derived values.
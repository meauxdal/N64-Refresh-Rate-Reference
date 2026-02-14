# N64 Refresh Rate Reference 

## README.md

Exhaustive reference for **Nintendo 64 video refresh rates** across NTSC, PAL, and PAL-M modes.

| System  | Mode        | Exact Fraction          | Decimal (Hz) |
| ------- | ----------- | ----------------------- | ------------ |
| NTSC-P  | Progressive | 2,250,000 / 37,609      | 59.8261      |
| NTSC-I  | Interlaced  | 4,500,000 / 75,075      | 59.9401      |
| PAL-P   | Progressive | 15,625 / 313            | 49.9201      |
| PAL-I   | Interlaced  | 50 / 1                  | 50.0000      |
| PAL-M-P | Progressive | 243,141,548 / 4,064,665 | 59.8179      |
| PAL-M-I | Interlaced  | 486,283,096 / 8,113,875 | 59.9323      |

## Quick Links

* [Complete Reference](docs/N64Refresh-Complete-Reference.md) – All rates, conversions, and tables.
* [NTSC / PAL / PAL-M Derivations](docs/N64Refresh-DerivationNTSC.md) – Step-by-step calculations.
* [PAL Derivation](docs/N64Refresh-DerivationPAL.md)
* [PAL-M Derivation](docs/N64Refresh-DerivationPAL-M.md)
* [Sources](docs/N64Refresh-SourceList.md) – Standards, datasheets, SDKs, and community docs.

## Highlights

* **Modes Covered:** NTSC-P, NTSC-I, PAL-P, PAL-I, PAL-M-P, PAL-M-I
* **Content:** QRCLUT, exact refresh rates, line frequencies, interlaced/progressive timing, and conversion multipliers
* **Precision:** Exact fractions to prevent rounding errors; PAL-M uses NTSC vertical timing with PAL color encoding

## Usage

1. Check the **Complete Reference** for conversions.
2. Dive into derivations for calculations or verification.
3. Reference sources for official standards and hardware specs.

### Source and Authority

All refresh rates, conversion multipliers, and derived timing values are computed directly from the canonical JSON:

```
/tools/canonical_values.json
```

For detailed derivations and references, see:

* [NTSC Derivation](docs/N64Refresh-DerivationNTSC.md)
* [PAL Derivation](docs/N64Refresh-DerivationPAL.md)
* [PAL-M Derivation](docs/N64Refresh-DerivationPAL-M.md)
* [Sources](docs/N64Refresh-SourceList.md)
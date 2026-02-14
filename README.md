### N64 Refresh Rate Reference

This repository provides a comprehensive reference for Nintendo 64 video refresh rates across all supported video signals and modes, including NTSC, PAL, and PAL-M. It consolidates exact fractional refresh rates, decimal approximations, conversion multipliers between formats, and timing sheets derived from canonical values.

| System  | Mode        | Exact Fraction          | Decimal (Hz) |
| ------- | ----------- | ----------------------- | ------------ |
| NTSC-P  | Progressive | 2,250,000 / 37,609      | 59.8261      |
| NTSC-I  | Interlaced  | 4,500,000 / 75,075      | 59.9401      |
| PAL-P   | Progressive | 15,625 / 313            | 49.9201      |
| PAL-I   | Interlaced  | 50 / 1                  | 50.0000      |
| PAL-M-P | Progressive | 243,141,548 / 4,064,665 | 59.817987    |
| PAL-M-I | Interlaced  | 486,283,096 / 8,113,875 | 59.932374    |

---

### Source and Authority

All refresh rates, conversion multipliers, and derived timing values are computed directly from the canonical JSON:

```
/tools/canonical_values.json
```

For more detail and citations, see breakouts elsewhere in this repository.
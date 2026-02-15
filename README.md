# N64 Refresh Rate Reference 

## README.md

**Note: this repository is still a work in progress, but all math should be correct.**

Exhaustive reference for **Nintendo 64 video refresh rates** across NTSC, PAL, and PAL-M modes.

| System  | Mode        | Exact Fraction    | Decimal (Hz) |
| ------- | ----------- | ----------------- | ------------ |
| NTSC-P  | Progressive | 2250000/37609     | 59.826105    |
| NTSC-I  | Interlaced  | 60000/1001        | 59.940060    |
| PAL-P   | Progressive | 15625/313         | 49.920128    |
| PAL-I   | Interlaced  | 50/1              | 50.000000    |
| PAL-M-P | Progressive | 243141548/4064665 | 59.818349    |
| PAL-M-I | Interlaced  | 486283096/8113875 | 59.932288    |

## Navigation Links

* [Complete Reference](docs/N64Refresh-Complete-Reference.md)
* [Timing Sheet](docs/N64Refresh-TimingSheet.md)
* [Derivations](docs/N64Refresh-Derivations.md)
* [Sources](docs/N64Refresh-SourceList.md)
* [Internal canonical values JSON](tools/canonical_values.json)

## Highlights

* Modes: NTSC, PAL, PAL-M - Progressive & Interlaced
* Fractional forms carried to minimize error 

## Notes

1. See [Complete Reference](docs/N64Refresh-Complete-Reference.md) and [Timing Sheet](docs/N64Refresh-TimingSheet.md) for conversions, rates, tables, etc.
2. See [Derivations](docs/N64Refresh-Derivations.md) and [Sources](docs/N64Refresh-SourceList.md) for verification and data provenance.
3. See [Internal canonical values JSON](tools/canonical_values.json) for canonical derived values.
4. The [Timing Sheet](docs/N64Refresh-TimingSheet.md) file will be merged with the Reference file in a future version.

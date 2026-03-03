# N64 Video Timing Reference

This repository contains the precise refresh rates for the Nintendo 64's video interface. The values are derived from the hardware oscillators and internal register logic, ensuring cycle-accurate timing for emulators, FPGA cores, and other tools that require hardware-level precision.

## Reference

| Mode | Scan Type | Exact Refresh (f_V) | Decimal (Hz) |
| :--- | :--- | :--- | :--- |
| NTSC | Progressive | 2,250,000 / 37,609 | 59.8261054535 |
| NTSC | Interlaced | 60,000 / 1,001 | 59.9400599401 |
| PAL | Progressive | 15,625 / 313 | 49.9201277955 |
| PAL | Interlaced | 50 / 1 | 50 (exact) |
| PAL-M | Progressive | 6,953,850,000 / 116,249,419 | 59.8183634793 |
| PAL-M | Interlaced | 185,436,000 / 3,094,091 | 59.9323032193 |

# Primary document

[`N64_Timing_Reference.md`](N64_Timing_Reference.md)

# Canonical fractions for each signal

[`canonical_values.json`](tools/canonical_values.json)

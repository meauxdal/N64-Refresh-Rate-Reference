# N64 VI Timing Constants

This repository contains the precise refresh rates for the Nintendo 64's video interface. The values are derived from the hardware oscillators and internal register logic, ensuring cycle-accurate timing for emulators, FPGA cores, and other tools that require hardware-level precision.

## Quick Reference

| Mode | Scan Type | Exact Refresh (f_V) | Decimal (Hz) |
| :--- | :--- | :--- | :--- |
| NTSC | Progressive | 2,250,000 / 37,609 | 59.8261054535 |
| NTSC | Interlaced | 60,000 / 1,001 | 59.9400599401 |
| PAL | Progressive | 15,625 / 313 | 49.9201277955 |
| PAL | Interlaced | 50 / 1 | 50.0000000000 |
| PAL-M | Progressive | 243,141,548 / 4,064,665 | 59.8183486216 |
| PAL-M | Interlaced | 486,283,096 / 8,113,875 | 59.9322883333 |

## Usage

[`canonical_values.json`](tools/canonical_values.json)_ provides irreducible fractions to avoid floating-point precision loss in timing calculations. (important note - PAL-M constants need further revising)  
[`N64_Timing_Reference.md`](N64_Timing_Reference.md) shows how the hardware oscillators and register logic produce these timing constants, with full derivations.

## Hardware Specifics

Progressive modes include an extra half-line (526 for NTSC/PAL-M, 626 for PAL) to suppress interlace artifacts, resulting in a refresh rate slightly below the standard 60,000/1,001 Hz. PAL-M uses a distinct integer divisor of 3091 VI clocks per line. All NTSC derivations are based on the canonical 315/22 MHz crystal oscillator, not the commonly cited approximation of 14.318 MHz.

## Example
```cpp
// NTSC Progressive: 2,250,000 / 37,609 Hz
double frame_duration_ns = (37609.0 / 2250000.0) * 1e9; 
// Result: ~16,715,111.11 ns
```

Use double-precision or fixed-point arithmetic for cycle counters.

WIP until further noted. Corrections and reconciliation of errors ongoing.
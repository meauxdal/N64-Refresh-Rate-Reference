## 1. Mission

This repository serves as the definitive source for Nintendo 64 Video Interface (VI) timing constants. Values are mathematically derived from the N64’s hardware oscillators (f_xtal) and internal register logic, ensuring cycle-accurate precision for emulators, FPGA cores, and video processing tools.

## 2. QLUT (Quick Lookup Table)

| Mode | Scan Type | Exact Refresh (f_V) | Decimal (Hz) |
| --- | --- | --- | --- |
| **NTSC** | **Progressive** | 2,250,000 / 37,609 | **59.8261054535** |
|  | **Interlaced** | 60,000 / 1,001 | **59.9400599401** |
| **PAL** | **Progressive** | 15,625 / 313 | **49.9201277955** |
|  | **Interlaced** | 50 / 1 | **50.0000000000** |
| **PAL-M** | **Progressive** | 243,141,548 / 4,064,665 | **59.8183486216** |
|  | **Interlaced** | 486,283,096 / 8,113,875 | **59.9322883333** |

## 3. Usage Guide

* **For Implementation:** Use [`canonical_values.json`](canonical_values.json). This file contains irreducible fractions to avoid floating-point drift in your timing loops.
* **For Verification:** See [`N64_Timing_Reference.md`](N64_Timing_Reference.md). This document contains the full step-by-step mathematical derivations and memory-mapped I/O (MMIO) register details.

## 4. Key Hardware Insights

* **Progressive Offset:** The N64 adds one extra scanline in progressive modes (526 for NTSC/PAL-M, 626 for PAL) to prevent the field-toggle of analog interlacing. This results in a refresh rate slightly slower than the standard 60,000 / 1,001 Hz.
* **PAL-M Integer Constraint:** Unlike NTSC, which uses a specific fractional relationship, the N64 PAL-M implementation utilizes an integer divisor of **3091** VI clocks per line, creating a unique frequency fingerprint.
* **Crystal Accuracy:** All NTSC derivations are based on the canonical **315/22 MHz** crystal (**f_xtal**), not the rounded 14.318 MHz value.

## 5. Implementation Sample

```cpp
// Example: Calculating Frame Duration in Nanoseconds
// Using NTSC-P: 2,250,000 / 37,609 Hz
// Note: Use double or fixed-point for high-precision cycle counters
double frame_duration_ns = (37609.0 / 2250000.0) * 1e9; 
// Result: ~16,715,111.11 ns

```

## 6. Document Authority

**Document Authority Chain:**  
Primary Sources (ITU Standards, Datasheets, Patents)  
↓  
Mathematical Derivations (Section 6)  
↓  
**[N64_Timing_Reference.md](N64_Timing_Reference.md)**

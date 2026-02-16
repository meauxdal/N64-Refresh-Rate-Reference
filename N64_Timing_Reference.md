# N64 Refresh Rate Reference

Comprehensive reference for Nintendo 64 video refresh rates and timing specifications across all supported video modes. Vertical scan frequency (often colloquially termed 'refresh rate') defines the period of the vertical synchronization cycle. 

---

## 1. Introduction

The Nintendo 64 Video Interface (VI) supports three television standards (NTSC, PAL, and PAL-M), each with both progressive and interlaced scan modes, resulting in six distinct video timing configurations. This document provides exact timing values derived from hardware specifications, with all refresh rates expressed as both irreducible fractions and high-precision decimal values.

**Video Modes:**

* **NTSC**: Used in North America, Japan, and other regions (525/526 scanlines)
* **PAL**: Used in Europe, Australia, and other regions (625/626 scanlines)
* **PAL-M**: Used in Brazil (525/526 scanlines with PAL-like color encoding)

**Scan Types:**

* **Progressive (P)**: All scanlines drawn sequentially in a single pass
* **Interlaced (I)**: Scanlines drawn in two fields (odd lines, then even lines)

### 1.1 Nomenclature

This document adopts **Vertical Scan Frequency (fV)** as the primary metric for all timing intervals. While the common industry term "refresh rate" is used for general readability, **fV** precisely defines the frequency of the **Vertical Synchronization (VSYNC)** signal.

* Progressive Modes: This represents the Frame Frequency.
* Interlaced Modes: This represents the Field Frequency.

All values are derived from the system's Master Clock (**f_xtal**) and the Video Interface (VI) divisor logic. **fV** is measured from the leading edge of the first **VSYNC** pulse to the leading edge of the next. In this documentation, **fV** refers to the interval between **VSYNC** pulses. In interlaced modes, this is the Field Rate, meaning two cycles are required to complete one full frame of video data.

---

## 2. Refresh Rate Summary

The following table presents the exact refresh rates for all six N64 video modes. Fractional values are fully reduced and represent the mathematically exact refresh rate. Decimal values are computed to 10 decimal places.

| Mode | Type | Refresh Rate (Hz) | Refresh Rate (Hz) |
| --- | --- | --- | --- |
| NTSC-P | Progressive | 2250000/37609 | 59.8261054535 |
| NTSC-I | Interlaced | 60000/1001 | 59.9400599401 |
| PAL-P | Progressive | 15625/313 | 49.9201277955 |
| PAL-I | Interlaced | 50/1 | 50.0000000000 |
| PAL-M-P | Progressive | 243141548/4064665 | 59.8183486216 |
| PAL-M-I | Interlaced | 486283096/8113875 | 59.9322883333 |

---

## 3. Technical Specifications

Hardware constants and register mapping for implementing video timings.

### 3.1 Fundamental Constants

Hardware-defined values derived from the system's crystal oscillators and the Video Interface (VI) register logic.

| Mode | Crystal Frequency (f_xtal) | Multiplier (M) | VI Clocks / Line (L) | Scanlines (S) | VI_V_SYNC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NTSC** | 14.3181818182 MHz | 17 / 5 | 3094 | 525 / 526 | 0x20D / 0x20E |
| **PAL** | 17.7344750000 MHz | 14 / 5 | 3178 | 625 / 626 | 0x271 / 0x272 |
| **PAL-M** | 14.3024440000 MHz | 17 / 5 | 3091 | 525 / 526 | 0x20D / 0x20E |

![Figure 1: N64 Clock Generation Circuits - U7 (NTSC/PAL-M) and U15 (PAL)](fig1_clock_gen_schematic.png)
*Figure 1: N64 Clock Generation Circuits - U7 (NTSC/PAL-M) and U15 (PAL)*

**Implementation Notes:**
* **NTSC Clock Precision**: The NTSC crystal frequency is mathematically defined as exactly 315/22 MHz.
* **PAL Clock Precision**: The PAL crystal frequency is a fixed integer, defined as exactly 17,734,475 Hz.

### 3.2 Video Interface (VI) Register Mapping

The RCP (Reality Co-Processor) processes video timings through the following memory-mapped I/O (MMIO) registers:

![Figure 2: RCP-NUS Pinout showing VDC (Video Digital Complex) Timing Outputs](fig2_rcp_schematic.png)
*Figure 2: RCP-NUS Pinout showing VDC (Video Digital Complex) Timing Outputs*

* **VI_V_SYNC_REG (0x0440000C)**: Sets the total number of lines per frame (S).
* **VI_H_SYNC_REG (0x04400008)**: The lower 12 bits define the total line duration in VI clocks (L).
* **VI_V_CURRENT_LINE_REG (0x04400010)**: Indicates the current scanline being processed.

> **Developer Note on Field Alternation**: For interlacing, S is set to an odd integer (525 or 625). The VI hardware automatically offsets the VSYNC pulse (VDC_DSYNC) by 0.5 lines every other field.

### 3.3 Derived Timing Values

All values calculated from the fundamental constants above. Line frequencies and refresh rates are expressed as exact fractions (fully reduced) with corresponding decimal representations.

| Mode | Line Frequency (Hz) | Line Frequency (Hz) | Progressive Refresh (Hz) | Interlaced Refresh (Hz) |
| :--- | :--- | :--- | :--- | :--- |
| **NTSC** | 2250000/143 | 2250000/143 | 2250000/37609 | 60000/1001 |
| **PAL** | 15625/1 | 15625/1 | 15625/313 | 50/1 |
| **PAL-M** | 243141548/15455 | 243141548/15455 | 243141548/4064665 | 486283096/8113875 |

### 3.4 Hardware Signal Path

The generation of video timing follows a deterministic path from physical oscillation to digital counting and finally analog conversion:

1. **Source**: The MX8330MC Clock Generator utilizes a crystal oscillator (X1/X2) to produce the Master Clock (f_xtal).
2. **Logic**: The RCP (Reality Co-Processor) receives f_xtal and applies the Multiplier (M) to drive the internal Video Interface (VI) logic.
3. **Counting**: The VI hardware counts cycles based on values stored in `VI_H_SYNC_REG` (Line Length) and `VI_V_SYNC_REG` (Frame Height).
4. **Trigger**: Upon reaching the defined count, the RCP toggles the `VDC_DSYNC` and `VDC_HSYNC` pins.
5. **Output**: The Video Encoder (MAV-N64 or BU9906) receives these timing pulses to synchronize the final analog signal.

### 3.5 Quick Verification Table

Use these expected register values and physical pin mappings to verify timing implementation on hardware.

| Target Parameter | Register | NTSC (Value) | Physical Pin (RCP) | Physical Pin (Encoder) |
| :--- | :--- | :--- | :--- | :--- |
| **Frame Height (S)** | VI_V_SYNC_REG | 0x20D (525) | — | — |
| **Line Duration (L)** | VI_H_SYNC_REG | 0xC16 (3094) | — | — |
| **VSYNC Pulse** | VDC_DSYNC | — | Pin 14 | Pin 19 |
| **HSYNC Pulse** | VDC_HSYNC | — | Pin 15 | Pin 20 |
| **Burst Gate** | VDC_BURST | — | Pin 16 | Pin 21 |

> **Note on Signal Handover**: The RCP outputs digital timing pulses (VDC) which are received by the Video Encoder (typically the MAV-N64 or BU9906). These pins represent the last digital stage of the video pipeline before analog conversion.

---

## 4. Signal Analysis

Detailed per-mode timing specifications and hardware implementation notes.

### 4.1 Signal Parameters by Mode

![Figure 3: N64 VI Timing Diagram - Visualizing Register-Defined Bounds](fig3_n64_default_libdragon_240p_timing.png)
*Figure 3: N64 VI Timing Diagram - Visualizing Register-Defined Bounds*

| Mode | Scanlines | VI Clocks per Scanline | Line Frequency (Hz) | Refresh Rate (Hz) |
| --- | --- | --- | --- | --- |
| NTSC-P | 526 | 3094 | 15734.2657342657 | 59.8261054535 |
| NTSC-I | 525 | 3094 | 15734.2657342657 | 59.9400599401 |
| PAL-P | 626 | 3178 | 15625.0000000000 | 49.9201277955 |
| PAL-I  | 625 | 3178 | 15625.0000000000 | 50.0000000000 |
| PAL-M-P | 526 | 3091 | 15732.2256874798 | 59.8183486216 |
| PAL-M-I | 525 | 3091 | 15732.2256874798 | 59.9322883333 |

### 4.2 Mode-Specific Implementation Notes

**NTSC (Progressive and Interlaced)**

* Crystal frequency: 14.3181818182 MHz (315/22 MHz)
* VI clock frequency: 48.6818181818 MHz (5355/110 MHz)
* Color subcarrier: 3.5795454545 MHz (315/88 MHz)
* VI clock multiplier: 17/5 (3.4)
* LEAP register: Not used (0x00)

**PAL (Progressive and Interlaced)**

* Crystal frequency: 17734475 Hz (exact)
* VI clock frequency: 49656530 Hz (exact)
* Color subcarrier: 4433618.75 Hz (17734475/4 Hz)
* VI clock multiplier: 14/5 (2.8)
* LEAP register: Used to maintain exact 15625 Hz line frequency
* LEAP pattern: 5-field sequence (B-A-B-A-B) adds fractional VI clocks (6-5-6-5-6 pattern)
* Color Phase: Maintains the Bruch Phase (PAL switch); the V-component of the color subcarrier inverts on alternate lines via f_xtal synchronization.

**PAL-M (Progressive and Interlaced)**

* **Crystal frequency**: 14,302,444 Hz (exact)
* **VI clock frequency**: 48,628,309.6 Hz (243,141,548 / 5 Hz)
* **Color subcarrier**: 3,575,611 Hz (exact)
* **VI clock multiplier**: 17 / 5 (3.4)
* **Integer Divisor Constraint**: To match the NTSC standard line rate (approx. 15,734.27 Hz) exactly, the VI would require 3,090.589 clocks per line. Since the VI hardware utilizes integer counting for line duration, it employs the nearest integer (3091).
* **Frequency Deviation**: This results in a line frequency of approx. 15,732.23 Hz, a deviation of approx. 0.013%. This shift is negligible for CRT deflection circuits but is a key differentiator for high-precision digital capture synchronization.
* **LEAP register**: Not used (0x00).

---

## 5. Refresh Rate Conversion Tables

To convert from one mode to another, multiply the source refresh rate by the conversion factor.

### 5.1 Decimal Conversions

Factors rounded to 5 decimal places for practical use.

| From \ To | NTSC-P | NTSC-I | PAL-P | PAL-I | PAL-M-P | PAL-M-I |
| --- | --- | --- | --- | --- | --- | --- |
| NTSC-P | 1.00000 | 1.00190 | 0.83442 | 0.83576 | 0.99987 | 1.00177 |
| NTSC-I | 0.99810 | 1.00000 | 0.83283 | 0.83417 | 0.99797 | 0.99987 |
| PAL-P | 1.19844 | 1.20072 | 1.00000 | 1.00160 | 1.19828 | 1.20056 |
| PAL-I | 1.19652 | 1.19880 | 0.99840 | 1.00000 | 1.19637 | 1.19865 |
| PAL-M-P | 1.00013 | 1.00203 | 0.83453 | 0.83586 | 1.00000 | 1.00190 |
| PAL-M-I | 0.99823 | 1.00013 | 0.83294 | 0.83427 | 0.99810 | 1.00000 |

### 5.2 Exact Fractional Conversions

Irreducible fractions for mathematically precise conversions.

| From \ To | NTSC-P | NTSC-I | PAL-P | PAL-I | PAL-M-P | PAL-M-I |
| --- | --- | --- | --- | --- | --- | --- |
| NTSC-P | 1/1 | 526/525 | 37609/45072 | 37609/45000 | 790210031/790312500 | 207825238153/207457031250 |
| NTSC-I | 525/526 | 1/1 | 25025/30048 | 1001/1200 | 5531470217/5542725000 | 790210031/790312500 |
| PAL-P | 45072/37609 | 30048/25025 | 1/1 | 626/625 | 76103304524/63510390625 | 152206609048/126779296875 |
| PAL-I | 45000/37609 | 1200/1001 | 625/626 | 1/1 | 121570774/101616625 | 243141548/202846875 |
| PAL-M-P | 790312500/790210031 | 5542725000/5531470217 | 63510390625/76103304524 | 101616625/121570774 | 1/1 | 526/525 |
| PAL-M-I | 207457031250/207825238153 | 790312500/790210031 | 126779296875/152206609048 | 202846875/243141548 | 525/526 | 1/1 |

---

## 6. Mathematical Derivations

This section provides complete step-by-step derivations for all timing values. All calculations begin with documented hardware constants and proceed through to the final refresh rates.

### 6.1 NTSC Derivation

**Constants:**

```
Color burst frequency: f_colorburst = 315/88 MHz  (≈ 3.5795454545 MHz)
Crystal frequency: f_xtal = 4 × f_colorburst = 315/22 MHz  (≈ 14.3181818182 MHz)
VI clock multiplier: M = 17 / 5
VI clocks per scanline: L = 3,094
Progressive scanlines: S_prog = 526
Interlaced scanlines: S_int = 525
```

**Video clock frequency:**

```
f_vi = f_xtal × M
     = (315/22 MHz) × (17/5)
     = (315 × 17)/(22 × 5) MHz
     = 5,355/110 MHz
     ≈ 48.6818181818 MHz
```

**Horizontal scan frequency:**

```
f_line = f_vi / L
       = (5,355/110 MHz) / 3,094
       = 5,355,000,000 / (110 × 3,094) Hz
       = 5,355,000,000 / 340,340 Hz
       = 591,750,000 / 37,609 Hz  (reduced)
       = 2,250,000 / 143 Hz  (canonical value)
       ≈ 15,734.2657342657 Hz
```

**Refresh rate (Progressive):**

Progressive mode: 526 scanlines per vertical scan cycle, scanned sequentially.

```
fV_prog = f_line / (S_prog / 2)
        = (2,250,000 / 143) / (526 / 2)
        = (2,250,000 / 143) / 263
        = 2,250,000 / (143 × 263)
        = 2,250,000 / 37,609  (canonical value)
        ≈ 59.8261054535 Hz
```

**Refresh rate (Interlaced):**

Interlaced mode: 525 scanlines per vertical scan cycle, alternating between odd and even fields (262.5 scanlines each).

```
fV_int = f_line / (S_int / 2)
       = (2,250,000 / 143) / (525 / 2)
       = (2,250,000 / 143) / 262.5
       = (2,250,000 × 2) / (143 × 525)
       = 4,500,000 / 75,075
       = 60,000 / 1,001  (canonical value)
       ≈ 59.9400599401 Hz
```

### 6.2 PAL Derivation

**Constants:**

```
Color burst frequency: f_colorburst = 17,734,475 / 4 Hz  (≈ 4.4336187500 MHz)
Crystal frequency: f_xtal = 4 × f_colorburst = 17,734,475 Hz  (≈ 17.7344750000 MHz)
VI clock multiplier: M = 14 / 5
VI clocks per scanline: L = 3,178
Progressive scanlines: S_prog = 626
Interlaced scanlines: S_int = 625
```

**Video clock frequency:**

```
f_vi = f_xtal × M
     = 17,734,475 Hz × (14/5)
     = (17,734,475 × 14) / 5 Hz
     = 248,282,650 / 5 Hz
     = 49,656,530 Hz
     = 49656530 Hz  (exact)
```

**Horizontal scan frequency:**

Without LEAP compensation, the theoretical line frequency would be:

```
f_line (theoretical) = f_vi / L
                     = 49,656,530 / 3,178 Hz
                     ≈ 15,625.0881057269 Hz
```                 

The LEAP register compensates for this ~5.6 ppm error by adding fractional VI clocks during VSYNC, achieving:

```
f_line = 15,625 / 1 Hz  (canonical value)
       = 15,625 Hz  (exact)
```

**Refresh rate (Progressive):**

```
refresh_rate = f_line / (S_prog / 2)
             = 15,625 / (626 / 2)
             = 15,625 / 313
             = 15,625 / 313  (canonical value)
             ≈ 49.9201277955 Hz
```

**Refresh rate (Interlaced):**

```
refresh_rate = f_line / (S_int / 2)
             = 15,625 / (625 / 2)
             = (15,625 × 2) / 625
             = 31,250 / 625
             = 50 / 1  (canonical value)
             = 50 Hz  (exact)
```

**PAL Phase Synchronization and LEAP Logic:**

The N64 VI uses a hardware-level compensation mechanism to maintain the exact 15,625 Hz line rate required by PAL standards. Without this, the VI clock would produce a slight frequency drift (approx. 5.6 ppm).

* **Mechanism**: The hardware alternates the line duration by plus/minus 1 VI clock cycle during the vertical blanking interval.
* **Pattern**: A 5-field repeating sequence (B-A-B-A-B) ensures that the average frequency over time remains exactly 15,625 Hz.
* **Implementation**: The VI LEAP registers (VI_LEAP_A_REG and VI_LEAP_B_REG) define these alternating fractional clock patterns (typically a 6-5-6-5-6 cycle).
* **Developer Impact**: When manual timing is required, developers should account for this jitter if measuring signal stability at the microsecond level during the VSYNC period.

### 6.3 PAL-M Derivation

**Constants:**

```
Color burst frequency: f_colorburst = 3,575,611 Hz
Crystal frequency: f_xtal = 4 × f_colorburst = 14,302,444 Hz
VI clock multiplier: M = 17 / 5
VI clocks per scanline: L = 3,091
Progressive scanlines: S_prog = 526
Interlaced scanlines: S_int = 525
```

**Video clock frequency:**

```
f_vi = f_xtal × M
     = 14,302,444 Hz × 3.4
     = 48,628,309.6 Hz
     = 243,141,548 / 5 Hz
     = 48.6283096 MHz  (exact)
```

**Horizontal scan frequency:**

```
f_line = f_vi / L
       = (243,141,548 / 5) / 3,091
       = 243,141,548 / 15,455 Hz  (canonical value)
       ≈ 15,732.2256874798 Hz
```

**Refresh rate (Progressive):**

```
refresh_rate = f_line / (S_prog / 2)
             = (243,141,548 / 15,455) / (526 / 2)
             = (243,141,548 / 15,455) / 263
             = 243,141,548 / (15,455 × 263)
             = 243,141,548 / 4,064,665  (canonical value)
             ≈ 59.8183486216 Hz
```

**Refresh rate (Interlaced):**

```
refresh_rate = f_line / (S_int / 2)
             = (243,141,548 / 15,455) / (525 / 2)
             = (243,141,548 × 2) / (15,455 × 525)
             = 486,283,096 / 8,113,875  (canonical value)
             ≈ 59.9322883333 Hz
```

---

## 7. Sources and Documentation Map

### 7.1 Component Reference Map

This table maps the visual figures used in this document to their physical hardware components and primary reverse-engineering sources.

| Document Figure | Repo Filename | Component / Source |
| :--- | :--- | :--- |
| **Figure 1** | `fig1_clock_gen_schematic.png` | MX8330MC Clock Gen (U7/U15). Source: RWeick |
| **Figure 2** | `fig2_rcp_schematic.png` | RCP-NUS (U9) Pinout / VDC Bus. Source: RWeick |
| **Figure 3** | `fig3_n64_default_libdragon_240p_timing.png` | Libdragon VI Timing Bounds (240p). Source: lidnariq |

**Primary Schematic Source:**
* [RWeick/NUS-CPU-03-Nintendo-64-Motherboard](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard) — Comprehensive PCB schematics and pinout references.

### 7.2 General References

| Source                                                                                                                                                              | Notes                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [ITU-R Recommendation BT.470-6](https://www.itu.int/rec/R-REC-BT.470/en)                                                                                            | Broadcast standard: NTSC/PAL lines per frame, fields/sec, color subcarrier frequencies |
| [ITU-R Recommendation BT.1700](https://www.itu.int/rec/R-REC-BT.1700/en)                                                                                            | Broadcast standard: composite video signal levels, timing, and sync pulses             |
| [ITU-R Recommendation BT.1701](https://www.itu.int/rec/R-REC-BT.1701/en)                                                                                            | Broadcast standard: horizontal/vertical timing for composite video                     |
| [ATV Compendium (BATC)](https://batc.org.uk/wp-content/uploads/ATVCompendium.pdf)                                                                                   | PAL-M line rate (fH) to chroma frequency relationship, broadcast standard reference    |
| [SAA1101 Universal Sync Generator Datasheet](https://people.ece.cornell.edu/land/courses/ece4760/ideas/saa1101.pdf)                                                 | PAL-M chroma frequency specification (227.25 × fH), universal sync generator chip reference |
| [MX8350 Datasheet](https://www.datasheets360.com/part/detail/mx8350/-7133688394404043430/)                                                                          | Hardware datasheet: DAC/video encoder electrical limits and timing                     |
| [Nintendo 64 Functions Reference Manual (OS 2.0i/j/k/l)](https://ultra64.ca/files/documentation/online-manuals/functions_reference_manual_2.0i/os/osViSetMode.html) | Official SDK: VI register mappings and programmable timing                             |
| [Nintendo 64 Programming Manual](https://ultra64.ca/resources/documentation/)                                                                                       | Official SDK: memory-mapped I/O, VI mode definitions, system programming reference     |
| [Nintendo 64 Programming Manual Addendums PDF](https://n64squid.com/Nintendo%20Ultra64%20Programming%20Manual+Addendums.pdf)                                        | Official SDK addendum: corrections, detailed timing tables                             |
| [JRRA – N64 Documentation](https://jrra.zone/n64/doc/)                                                                                                              | Curated/official N64 hardware documentation and timing reference                       |
| [NUS-CPU-03 Nintendo 64 Motherboard](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard)                                                                  | Hardware reverse-engineered VI and CPU connections, register layout                    |
| [US6556197B1 – Programmable Video Timing Registers](https://patents.google.com/patent/US6556197B1/en)                                                               | Patent: horizontal/vertical sync, color burst                                          |
| [US4054919A – Video Image Positioning Control](https://patents.google.com/patent/US4054919A/en)                                                                     | Patent: sync counter generation                                                        |
| [JRRA – N64](https://jrra.zone/n64/)                                                                                                                                | Community reverse-engineering and documentation of N64 hardware and VI behavior        |
| [hkz-libn64](https://github.com/mark-temporary/hkz-libn64)                                                                                                          | Community SDK: direct register-level mappings including VI constants                   |
| [libdragon](https://libdragon.dev/)                                                                                                                                 | Community SDK: high-level API access to N64 hardware                                   |
| [n64brew.dev – Video Interface](https://n64brew.dev/wiki/Video_Interface)                                                                                           | Community reverse-engineering: detailed VI register behavior and timing examples       |
| [n64brew.dev – Libultra](https://n64brew.dev/wiki/Libultra)                                                                                                         | Community reverse-engineering: OS interface functions for VI and hardware access       |
| [n64.readthedocs.io – N64 Hardware Reference](https://n64.readthedocs.io/index.html#video-interface)                                                                | Community reverse-engineering: general hardware reference and verification             |
| [ares N64 Emulator](https://github.com/ares-emulator/ares/tree/master/ares/n64)                                                                                     | Emulator implementation for cross-checking VI timing and behavior                      |
| [CEN64 Emulator](https://github.com/n64dev/cen64)                                                                                                                   | Emulator implementation for cross-checking VI timing and behavior                      |
| [MAME Emulator](https://github.com/mamedev/mame/blob/master/src/mame/nintendo/n64.cpp)                                                                              | Emulator implementation for cross-checking VI timing and behavior                      |
| [MiSTer FPGA N64 Core HDL](https://github.com/MiSTer-devel/N64_MiSTer)                                                                                              | FPGA implementation for validation of VI timing                                        |
| [Wikipedia – NTSC](https://en.wikipedia.org/wiki/NTSC)                                                                                                              | General reference: broadcast standard overview                                         |
| [Wikipedia – PAL](https://www.wikipedia.org/wiki/PAL)                                                                                                               | General reference: broadcast standard overview                                         |
| [Wikipedia – PAL-M](https://www.wikipedia.org/wiki/PAL-M)                                                                                                           | General reference: broadcast standard overview                                         |
| [Everything Explained – NTSC](https://everything.explained.today/NTSC/)                                                                                             | Supplemental overview of NTSC signal and frame timing                                  |
| [Everything Explained – PAL](https://everything.explained.today/PAL/)                                                                                               | Supplemental overview of PAL signal and frame timing                                   |
| [Everything Explained – PAL-M](https://everything.explained.today/PAL-M/)                                                                                           | Supplemental overview of PAL-M signal and frame timing                                 |
| [Telecomponents NTSC](https://www.telecomponents.com/html/ntsc.htm)                                                                                                 | Supplemental broadcast signal reference                                                |
| [Telecomponents PAL](https://www.telecomponents.com/html/pal.htm)                                                                                                   | Supplemental broadcast signal reference                                                |
| [Martin Hinner – VGA/PAL](https://martin.hinner.info/vga/pal.html)                                                                                                  | Technical reference on PAL timing                                                      |
| [Danalee Analog Video](https://danalee.ca/ttt/analog_video.htm)                                                                                                     | Analog video timing reference                                                          |
| [Pembers Archive – World TV Standards](https://web.archive.org/web/20160512200958/http://www.pembers.freeserve.co.uk/World-TV-Standards/)                           | Archived global TV standard reference                                                  |
| [Optus N64RGB Archive](https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html)                                                                                  | Community N64 RGB signal documentation                                                 |
| [JunkerHQ – XRBG Optimal Timings](https://junkerhq.net/xrgb/index.php?title=Optimal_timings)                                                                        | Community guide for optimal dot clock and refresh timings                              |
| [Pineight – Dot Clock Rates](https://pineight.com/mw/page/Dot_clock_rates.xhtml)                                                                                    | Technical reference for dot clocks                                                     |

---

**Document Authority Chain:** 

Primary Sources (ITU Standards, Datasheets, Patents)  
↓  
Mathematical Derivations (Section 6)  
↓  
**[N64_Timing_Reference.md](N64_Timing_Reference.md)**
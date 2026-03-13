# N64 Refresh Rate Reference  

> Update 2026-03-12: This document is a work in progress. New primary source information has been made available; errors will be corrected. Both NTSC signals and PAL progressive values should be correct already. LEAP behavior may need slight corrections per primary sources. PAL interlaced and MPAL values pending correction. 

Reference for Nintendo 64 video refresh rates and timing specifications across all supported video modes. 

---

## Contents

* [§1 Introduction](#1-introduction)
    * [§1.1 Terminology](#11-terminology)
    * [§1.2 Annotations](#12-annotations)
    * [§1.3 Conventions](#13-conventions)
* [§2 N64 Video Output Summary](#2-n64-video-output-summary)
    * [§2.1 Refresh Rate](#21-refresh-rate)
    * [§2.2 Resolution](#22-resolution)
* [§3 Technical Specifications](#3-technical-specifications)
    * [§3.1 Fundamental Constants](#31-fundamental-constants)
    * [§3.2 Video Interface (VI) Register Mapping](#32-video-interface-vi-register-mapping)
    * [§3.3 Derived Timing Values](#33-derived-timing-values)
    * [§3.4 Hardware Signal Path](#34-hardware-signal-path)
    * [§3.5 Physical Variance and Stability](#35-physical-variance-and-stability)
    * [§3.6 Diagnostics](#36-diagnostics)
* [§4 Signal Analysis](#4-signal-analysis)
    * [§4.1 Signal Parameters by Mode](#41-signal-parameters-by-mode)
    * [§4.2 Mode-Specific Notes](#42-mode-specific-notes)
* [§5 Mathematical Derivations](#5-mathematical-derivations)
    * [§5.1 NTSC Derivation](#51-ntsc-derivation)
    * [§5.2 PAL Derivation](#52-pal-derivation)
    * [§5.3 PAL-M Derivation](#53-pal-m-derivation)
* [§6 Conversion Reference](#6-conversion-reference)
    * [§6.1 Approximate Decimal Conversions](#61-approximate-decimal-conversions)
    * [§6.2 Exact Fractional Conversions](#62-exact-fractional-conversions)
* [§7 Sources](#7-sources)
    * [§7.1 Figures](#71-figures)
    * [§7.2 References](#72-references)
    * [§7.3 Acknowledgements](#73-acknowledgements)
* [§8 Glossary](#8-glossary)

---

## 1. Introduction  

The Nintendo 64 **Video Interface (VI)** supports three television standards (**NTSC**, **PAL**, and **PAL-M**), each with both **progressive** and **interlaced** scan modes, resulting in six video timing configurations. This document provides exact timing values derived from hardware specifications, with presented results expressed in irreducible fractions and high-precision decimals.  

Video Modes:  

* **NTSC**: North America, Japan, South Korea, parts of Central America and the Caribbean  
* **PAL**: Europe, Australia, New Zealand, parts of Africa and Asia  
* **PAL-M**: Brazil (also referred to as **MPAL** or **PAL/M** in documentation and source code)  

Scan Types:  

* **Progressive (P)**: Lines drawn sequentially each vertical scan  
* **Interlaced (I)**: Lines drawn in alternating fields across two successive vertical scans  

### 1.1 Terminology

**Vertical scan frequency (fV)**, expressed in Hz, is the rate of vertical synchronization pulses. Precisely, fV measures the reciprocal of the VSYNC period, measured from the rising edge of one VSYNC pulse to the next rising edge. Where used in this document, "refresh rate" refers to this value. In progressive modes, fV represents frame frequency; in interlaced modes, fV represents field frequency.  

All video timing derives from a single physical source: a quartz crystal oscillator (X1), whose frequency is designated f_xtal. The VI clock (f_vi) is produced by multiplying f_xtal by a region-specific rational multiplier M (17/5 for NTSC and PAL-M; 14/5 for PAL). fH follows by dividing f_vi by L, the integer VI clock count per horizontal line. fV follows by dividing fH by S/2, the number of full scanlines.  

```
f_vi = f_xtal × M
fH   = f_vi / L
fV   = fH / (S / 2)

fV   = (f_xtal × M) / (L × S / 2)
```

All VI timing frequencies are rational derivatives of f_xtal.  

### 1.2 Annotations  

Parenthetical annotations clarify numerical representations:  

* `(exact)`: No rounding error; value derived from integer ratios  
* `(reduced)`: Common factors cancelled  
* `(canonical value)`: Fully reduced fraction; reference value at full precision  
* `(≈)`: Approximate decimal representation   

### 1.3 Conventions

#### 1.3.1 Counting Units

**Half-line (S)** is the atomic unit for VI vertical timing. One scanline equals 2 half-lines. This document favors half-line modelling where feasible. Adherence aligns with hardware register logic, yields consistent rational fractions, and avoids ambiguity introduced by "line" and "frame" terminology. See §5.1.  

#### 1.3.2 Registers

The document uses N64brew naming conventions throughout. SDK equivalents are noted here for cross-reference.

| N64brew Name | SDK Name | Address | Description |
|:---|:---|:---|:---|
| `VI_V_TOTAL` | `VI_V_SYNC_REG` | `0x04400018` | Terminal half-line count; effective half-lines = REG + 1 |
| `VI_H_TOTAL` | `VI_H_SYNC_REG` | `0x0440001C` | Terminal VI clock count per scanline; effective clocks = REG + 1 |
| `VI_H_TOTAL_LEAP` | `VI_H_SYNC_LEAP_REG` | `0x04400020` | LEAP_A [bits 27:16] and LEAP_B [bits 11:0] alternate scanline lengths for PAL compensation |
| `VI_V_CURRENT` | `VI_V_CURRENT_LINE_REG` | `0x04400010` | Current half-line; increments by 2 per line |
| `VI_BURST` | `VI_BURST_REG` | `0x04400014` | Color burst gate timing |
| `VI_H_VIDEO` | `VI_H_VIDEO_REG` | `0x04400024` | Active video horizontal start/end |
| `VI_V_VIDEO` | `VI_V_VIDEO_REG` | `0x04400028` | Active video vertical start/end |

All registers are terminal-counted; add 1 to derive the effective count. LEAP and hardware jitter affect the duration of individual half-lines but do not change the nominal half-line count. Interlaced VSYNC is automatically offset by 0.5 lines per field. See §5.2.1 for LEAP details.  
 
---

## 2. N64 Video Output Summary  

### 2.1 Refresh Rate  

The table lists refresh rates (fV) for all video modes. The fully reduced fractions shown below serve as reference values for the remainder of this text  

| Mode  | Scan Type   | Refresh Rate (fV, Hz)       | Refresh Rate (fV, Hz, .10f)   |  
| :---  | :---        | :---                        | :---                          |  
| NTSC  | Progressive | 2,250,000 / 37,609          | 59.8261054535                 |  
| NTSC  | Interlaced  | 60,000 / 1,001              | 59.9400599401                 |  
| PAL   | Progressive | 15,625 / 313                | 49.9201277955                 |  
| PAL   | Interlaced  | 50 / 1                      | 50 (exact)                    |  
| PAL-M | Progressive | 6,953,850,000 / 116,249,419 | 59.8183634793                 |  
| PAL-M | Interlaced  | 185,436,000 / 3,094,091     | 59.9323032193                 |  

> These values correspond to the derivations in §5.  

### 2.2 Resolution  

In the context of contemporary retail software, the N64 outputs four fixed video signals:  

| Signal | Scan Type   | Resolution |  
| :---   | :---        | :---       |  
| NTSC   | Progressive | 640x240p   |  
| NTSC   | Interlaced  | 640x480i   |  
| PAL    | Progressive | 640x288p   |   
| PAL    | Interlaced  | 640x576i   |  

> PAL-M signals share corresponding NTSC resolutions.  

---  

## 3. Technical Specifications  

Hardware constants and register mapping.  

### 3.1 Fundamental Constants  

Hardware constants derived from f_xtal and the Video Interface (VI) registers.  

| Mode              | Crystal Frequency (f_xtal) | Multiplier (M) | VI Clocks / Line (L) | Half-Lines (S) | `VI_V_TOTAL` |  
| :---              | :---                       | :---           | :---                 | :---           | :---         |  
| NTSC Progressive  | 14.3181818182 MHz          | 17 / 5         | 3094                 | 526            | `0x20D`      |  
| NTSC Interlaced   | 14.3181818182 MHz          | 17 / 5         | 3094                 | 525            | `0x20C`      |  
| PAL Progressive   | 17.734475 MHz (exact)      | 14 / 5         | 3178                 | 626            | `0x271`      |  
| PAL Interlaced    | 17.734475 MHz (exact)      | 14 / 5         | 3178                 | 625            | `0x270`      |  
| PAL-M Progressive | 14.3024475524 MHz          | 17 / 5         | 3091                 | 526            | `0x20D`      |  
| PAL-M Interlaced  | 14.3024475524 MHz          | 17 / 5         | 3091                 | 525            | `0x20C`      |  

![Figure 1](/figures/fig1_clock_gen_schematic.png)  
*N64 Clock Generation Circuits - U7 & U15 (Macronix MX8330MC). Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

> Some later N64 revisions replaced one or both MX8330MCs with the pin-compatible Macronix MX9911MC. Still later revisions consolidated both clocks into a single MX8350 dual-channel synthesizer (see §3.1.1).  

* NTSC Clock Precision: 315/22 MHz (exact) (≈ 14.3181818182 MHz)  
* PAL Clock Precision: 17,734,475 Hz (exact) = 17.734475 MHz  
* PAL-M Clock Precision: 2,045,250,000 ÷ 143 Hz (exact) (≈ 14.3024475524 MHz)  

#### 3.1.1 Clock Generator Hardware Revisions  

Early revisions use a single-channel clock synthesizer at U7, driven by crystal X1, to produce f_vi. FSEL multiplier logic is high (17/5) for NTSC and PAL-M; low (14/5) for PAL. X1 varies by region: 315/22 MHz for NTSC and PAL-M; 17,734,475 Hz for PAL. U7 is MX8330MC on NUS-CPU-01 through NUS-CPU-04, and MX9911MC on NUS-CPU-05 and NUS-CPU-05-1. U7 chip identity on NUS-CPU-06 and NUS-CPU-07 is not confirmed from available board photos. U15 on NUS-CPU-07 is MX8330MC per ChipWorks professional teardown (NUS-CPU-07 Annotated PCB, Rev 1.0, Nov 2000); U7 is not annotated in that document and is unconfirmed. On NUS-CPU-05, U15 retains MX8330MC; NUS-CPU-05-1 includes *at least* one MX9911MC (at U7), but may also include another at U15. See §3.5.1.1 for visual identification. MX9911MC is also confirmed at U7 on at least one NUS-CPU(P)-01 unit (`D177G8`/`D147M7I`), implying a similar changeover timeline.  

The MX9911MC is a Macronix single-channel clock synthesizer that is pin- and function-compatible with the MX8330MC: identical pinout, FSEL logic, FSC and FSO/5 outputs, and 5 ms power-up stabilization. Later revisions (NUS-CPU-08 onward, 1999+) consolidated video clock generation into a single MX8350 dual-channel chip.  
 
![Figure 1a](/figures/fig6_mx8350_table.png)  
*MX8350 (later revisions) output frequencies for NTSC/PAL/MPAL. Source: MX8350 datasheet*  

> While the MX8350 datasheet lists the MPAL crystal as 14.302446 MHz, the correct value (derived from the canonically defined PAL-M colorburst frequency) is 2,045,250,000 / 143 Hz (≈ 14.3024475524 MHz); the origin of this error is not indicated by sources. For precision and correctness, all derivations in this document use the fractional form. See §5.3.  

### 3.2 Video Interface (VI) Register Mapping  

The RCP (Reality Co-Processor) processes video timings through the following memory-mapped I/O (MMIO) registers:  

![Figure 2](/figures/fig2_rcp_schematic.png)  
*RCP-NUS VDC pinout & timing signals. Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

![Figure 2a](/figures/fig9_rcp_vdc_schematic.png)  
*VDC pin assignments - 7-bit digital output. Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

The VDC bus carries:  
* VDC_D0 through VDC_D6: 7-bit digital video data  
* VDC_DSYNC: Continuous timing signal; while low, sync information is encoded on the accompanying VDC data lines  

These signals are transmitted to the VDC-NUS (BU9801F, U4), which performs digital-to-analog conversion and generates CSYNC (Composite Sync) and BFP (Burst Flag Pulse) for the downstream ENC-NUS encoder (U5). This two-stage signal path (VDC-NUS + ENC-NUS) applies to NUS-CPU-01 through NUS-CPU-04. Other revisions consolidate both functions into a single chip; e.g. DENC-NUS, AVDC-NUS, & MAV-NUS. The substitution of these components is not known to affect timing values derived in this document.  

> VI registers operate on terminal counts; all derived timing values use the hardware-consistent half-line model described in §1.

* `VI_V_TOTAL` (`0x04400018`): The register stores a terminal half-line count; effective number of half-lines per frame is equal to `VI_V_TOTAL` + 1.  
* `VI_H_TOTAL` (`0x0440001C`): The register stores a terminal VI clock count (per full scanline); effective clocks per line is equal to `VI_H_TOTAL` + 1.  
* `VI_V_CURRENT` (`0x04400010`): Reports the current half-line count; increments by 2 per line. In interlaced mode, bit 0 toggles each field to indicate odd or even lines. Libdragon uses this register to determine which lines require redrawing in 480i mode.  
* `VI_H_VIDEO` (`0x04400024`): Defines the horizontal start and end of the active video window in VI pixels.  
* `VI_V_VIDEO` (`0x04400028`): Defines the vertical start and end of the active video window in half-lines.  

> For interlaced modes, S is set to an odd integer (525 or 625). The VI hardware automatically offsets the vertical sync position by 0.5 lines every other field.  

### 3.3 Derived Timing Values  

Timing values in this section are calculated from the fundamental constants in §3.1. fH is line frequency; fV is vertical scan frequency (refresh rate). Values are derived from fH and half-line count S. Progressive modes use the full half-line count, interlaced modes offset vertical sync by 0.5 lines per field.  

| Mode  | fH (Hz, .10f)                 | fH (Hz)                 | Progressive fV (Hz)  | Interlaced fV (Hz) |  
| :---- | :---                          | :---                    | :---                 | :---               |  
| NTSC  | 15,734.2657342657             | 2250000/143             | 2250000/37609        | 60000/1001         |  
| PAL   | 15,625 (exact)                | 15625/1                 | 15625/313            | 50/1               |  
| PAL-M | 15,732.2295950572             | 6953850000/442013       | 6953850000/116249419 | 185436000/3094091  |  

### 3.4 Hardware Signal Path

Video signal timing follows a deterministic path from crystal oscillation through digital counting to analog output. The following applies to NUS-CPU-01 through NUS-CPU-04, as documented in RWeick's NUS-CPU-03 schematics.

1. Source: Crystal X1 oscillates at f_xtal; the clock generator (U7) multiplies this by M to produce f_vi. f_xtal is the hardware primitive for all video timing derivations.¹  
2. Logic: The RCP (Reality Co-Processor, U9) receives f_vi to drive the internal VI logic.
3. Counting: The VI counts clock cycles according to `VI_H_TOTAL` (line length) and `VI_V_TOTAL` (vertical extent) to define the signal's timing boundaries.  
4. Encoding: The VI transmits pixel data to the VDC-NUS over the VDC bus: a 7-bit³ data bus (VDC_D0 through VDC_D6), VDC_DSYNC (a.k.a. !DSYNC), and a shared clock. Data is multiplexed across 4 VI clock cycles per pixel: cycle 0 carries sync data with VDC_DSYNC held low; cycles 1 through 3 carry Red, Green, and Blue. Each 4-cycle group constitutes one rendered pixel, referred to throughout as a "VI pixel."  
5. Output: The VDC-NUS (U4) performs digital-to-analog conversion, clocked by U7.FSO/5 (Frequency Synthesizer Output ÷ 5). It generates analog RGB, CSYNC (pin 14), and BFP (pin 13), passing these to the ENC-NUS (U5). The ENC-NUS receives the colorburst reference from U7.FSC (f_xtal ÷ 4) at its SCIN pin via the R13/R12 resistor divider and C21.²  

> Presence of CSYNC and BFP at U4 confirms a functioning signal path from RCP through DAC to encoder; see §3.6 for oscilloscope verification points.  

![Figure 2b](/figures/fig13_n64videosys.png)  
*N64 Video System - VDC bus multiplexing, VDC_DSYNC waveform. Source: Tim Worthington, N64RGB documentation*  

![Figure 2c](/figures/fig14_vdc-nus.png)  
*VDC-NUS (BU9801F) pinout. Source: Tim Worthington, N64RGB documentation*  

![Figure 2d](/figures/fig18_VDC-NUS.png)  
*VDC-NUS (BU9801F, U4) in circuit. Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

![Figure 2e](/figures/fig17_ENC-NUS.png)  
*ENC-NUS (U5) in circuit - YOUT (luma, S-Video Y channel) and VOUT (composite video) outputs; SCIN (Subcarrier Input, pin 8) receives U7.FSC (f_xtal ÷ 4) via R13/R12 divider network. Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

![Figure 2i](/figures/fig28_n64-nus-03_video_output_circuit_worthington.png)  
*NUS-CPU-03 video output circuit: VDC-NUS (U4, BU9801F) to ENC-NUS (U5); R13 = 4.3 kΩ, R12 = 820 Ω divider network feeding SCIN; R8/R9/R10 = 110 Ω RGB output resistors; LUMINANCE (pin 7), COMPOSITE VIDEO (pin 9), CHROMINANCE (pin 8) outputs. Source: Tim Worthington, GameSX Wiki, N64 RGB NTSC*  

¹ Later revisions consolidate the video clock into a single MX8350 in place of the single-channel chip at U7 (MX8330MC or MX9911MC, depending on revision). f_xtal derivations are equivalent across all variants. X1 drives U7 for all regional video modes; its frequency varies by region. The derivations in §5 are rooted in the respective regional X1 value in each case.  

² The schematic path shows the VDC-NUS output feeding ENC-NUS (U5) on NUS-CPU-01 through 04 revisions, whereas other revisions use DENC-NUS, AVDC-NUS, or MAV-NUS to natively generate S-Video and composite. Each implementation performs the same DAC/encoding function; see Figures 2f and 2g below.  

![Figure 2f](/figures/fig15_denc-nus.png)  
*DENC-NUS pinout. Source: Tim Worthington, N64RGB documentation*  

![Figure 2g](/figures/fig16_mav-nus.png)  
*MAV-NUS pinout. Source: Tim Worthington, N64RGB documentation*  

![Figure 2h](/figures/fig27_n64rgb_vdc_serial_to_parallel_worthington.png)  
*VDC bus serial-to-parallel protocol: four 7-bit bytes clocked on falling edge; byte 0 carries sync bits (CS, HS, CL, VS); bytes 1-3 carry R0-R6, G0-G6, B0-B6. Source: Tim Worthington, RGB Video DAC for Nintendo 64, Revision 0 (27/1/07)*  

> A notable variant uses the S-RGB A encoder, found on PAL systems marked NUS-CPU(R)-01 and sold in France. This chip is an RGB DAC, but the capability is non-functional without modification in retail units. It does not generate S-Video; consequently, NUS-001(FRA) consoles are limited to composite video output without modification. This chip was originally used in some SNES revisions before appearing in NUS-CPU(R)-01. 

![Figure 2j](/figures/fig30_snes_video_path_DarthCloud.png)  
*S-RGB A (U7) video circuit: RGB inputs from S-PPU2; discrete transistor drive stage (Q1–Q3); RGB, LUMA, C.VIDEO, and CHROMA outputs; CSYNC and Burst inputs. Source: DarthCloud, SNS-CPU-RGB-02 Video Circuit, 2009*  

³ Per [N64brew.dev Video DAC page](https://n64brew.dev/wiki/Video_DAC): "it is unclear why the DAC has only 7 bits of precision instead of 8, and no documentation already found explains this."  

### 3.5 Physical Variance and Stability  

The derivations in §5 assume an ideal crystal oscillator at exactly the specified frequency. In practice, fV's derivation from a non-ideal f_xtal proves less exact.  

#### 3.5.1 X1 Crystal Oscillator  

N64 video timings are derived from the X1 crystal oscillator. Variance in this component therefore propagates through the timing chain.  

##### 3.5.1.1 X1 Identification  

The clock crystal (X1) has no published datasheet. The manufacturer has not been confirmed from available sources; an unverified but unchallenged theory identifies the “D” prefix near-universally observed in stamp codes with Japanese manufacturer Daishinku Corp. (Daiwa Shinku Kogyosho, a.k.a. KDS, est. 1959). Certainty is not possible from currently available sources.  

The NUS-CPU-03 oscillator circuit presents a load capacitance of 21.5 pF + C_stray to X1, derived from C39 = C40 = 43 pF in a series configuration (see Figure 1, §3.1):  

```  
CL = (C39 × C40) / (C39 + C40) + C_stray  
   = (43 × 43) / (43 + 43) + C_stray  
   = 21.5 pF + C_stray  
```  

C_stray (the aggregate parasitic capacitance from PCB traces and IC pin capacitance) cannot be determined without direct measurement. Consumer PCB oscillator layouts may be estimated in the range of 2-5 pF, implying an effective CL of approximately 23.5-26.5 pF. Available documentation does not establish whether X1 was specified for this load or whether the circuit operates outside the nominal crystal load rating.  

##### 3.5.1.2 Stamp Code Format

X1 and X2 stamp codes follow the format `(P)(D)FFFMY(I)`, where:  

| Field | Description                                                                               |  
| :---  | :---                                                                                      |  
| `P`   | Always `Ⓜ`. Only yet observed on some PAL-M units⁴                                        |  
| `D`   | Always `D`⁵                                                                               |  
| `FFF` | Frequency in abbreviated MHz (e.g. `143` = 14.3 MHz, `147` = 14.7 MHz, `177` = 17.7 MHz)  |  
| `M`   | Month of manufacture (`A`-`M`, skipping `I`. `A`: January; through `M`: December)         |  
| `Y`   | Last digit of year of manufacture (e.g. `6` = 1996, `0` = 2000)                           |  
| `I`   | Always `I`. Uncommon; appears without obvious pattern; meaning not established            |  

The I-skip in the month field is a noted date code convention, where `I` is omitted to avoid ambiguity with numeral `1`. The `I` character is observed as suffix on some codes after an otherwise complete code (e.g. `D143L6I`, `D147J9I`, `D143K9I`, `D147F0I`); its meaning is not known. It appears across X1 and X2 independently, across multiple revisions and years, with no observable clustering by revision, region, or date.  

The decode convention is consistent across all three regional crystal frequencies (14.3 MHz, 14.7 MHz, 17.7 MHz) and across the full known production span of the hardware (1996-2000).   

⁴ The meaning of the circular-M (`Ⓜ`) marking observed on some PAL-M boards is unconfirmed. One plausible expansion is an `M`PAL-specific marking (using an available glyph) applied to distinguish these X1 units from NTSC X1 crystals, as they otherwise appear identical (e.g. `D143K7` could be either NTSC or PAL-M, whereas the presence of `Ⓜ` disambiguates).   

⁵ Near-universal presence. `D` prefix missing in a single observed CPU-NUS-(M)-05-1 example across entire board corpus. On said PAL-M X1, `Ⓜ` is seemingly marked *in place of* `D`.  

![Figure 5b](/figures/fig23_X1_(M)143G0_stamp_code.png)  
*`Ⓜ` marking visible on some PAL-M X1 crystal oscillators. Source: Mielke - MiSTer FPGA Discord*  

![Figure 5a](/figures/fig24_X1_(M)D143G7_stamp_code.png)  
*Both `Ⓜ` and `D` prefixes visible on a single PAL-M marking. Source: JASNet Soluções em Eletrônica*  

##### 3.5.1.3 X1 and X2 Stamp Codes by Revision  

The following table lists confirmed and provisional X1 and X2 stamp codes organised by board revision. X1 is the video clock crystal; X2 is not involved in video timing derivations. Both are included because their date clustering on individual boards provides independent corroboration of the decode convention. See §7.2.1 for the crystal stamp code spreadsheet.  

| Revision | X1 | X2 | X1 Date | X2 Date | Notes |  
| :--- | :--- | :--- | :--- | :--- | :--- |  
| NUS-CPU-01 | `D143A6` | `D147B6` | Jan 1996 | Feb 1996 | ID: Prominos_01 *(Initial configuration: CPU-NUS; RCP-NUS; 2x RDRAM18-NUS A; VDC-NUS; ENC-NUS; BU9480F; AMP-NUS; 2x MX8330MC; Sharp PQ7VZ5 (marking: `7VZ5`); TI SN74LVC125 (marking: `LC125`))* |  
| NUS-CPU-01 | `D143B6` | `D147B6` | Feb 1996 | Feb 1996 | [Photo by Yaca2671, CC BY-SA 3.0 (Wikimedia)](https://commons.wikimedia.org/w/index.php?curid=5777930) |
| NUS-CPU-01 | `D143B6` | `D147B6` | Feb 1996 | Feb 1996 | ID: modretro_01 |  
| NUS-CPU-02 | `D143B6` | `D147C6` | Feb 1996 | Mar 1996 | |  
| NUS-CPU-02 | `D143C6` | `D147B6` | Mar 1996 | Feb 1996 | |  
| NUS-CPU-02 | `D143F6` | `D147E6` | Jun 1996 | May 1996 | ID: cy_01 |  
| NUS-CPU-02 | `D143K6` | `D147K6` | Oct 1996 | Oct 1996 | |  
| NUS-CPU-03 | `D143A6` | `D147A6` | Jan 1996 | Jan 1996 | *CPU-NUS A and VDC-NUS A are introduced mid-03 run with no board rev. bump* |
| NUS-CPU-03 | `D143F6` | `D147E6` | Jun 1996 | May 1996 | |
| NUS-CPU-03 | `D143G6` | `D147F6` | Jul 1996 | Jun 1996 | |
| NUS-CPU-03 | `D143H6` | `D147F6` | Aug 1996 | Jun 1996 | |
| NUS-CPU-03 | `D143L6` | `D147L6` | Nov 1996 | Nov 1996 | ID: Prominos_03 |
| NUS-CPU-04 | `D143H6` | `D147J6` | Aug 1996 | Sep 1996 | |
| NUS-CPU-04 | `D143L6I` | `D147J7` | Nov 1996 | Sep 1997 | I-suffix on X1 |
| NUS-CPU-04 | `D143J7` | `D147J7` | Sep 1997 | Sep 1997 | ID: Prominos_04 |
| NUS-CPU-04 | `D143K7` | `D147K7` | Oct 1997 | Oct 1997 | |
| NUS-CPU-05 | `D143G8` | `D147G8I` | Jul 1998 | Jul 1998 | I-suffix on X2 *(U7 MX9911MC likely present on [05, 07] inclusive. U1 AVDC-NUS is a positive identifier of NUS-CPU-05; however U1 may be either AVDC-NUS (earlier serials) or MAV-NUS (later serials))* |
| NUS-CPU-05 | `D143G8` | `D147H8` | Jul 1998 | Aug 1998 | |
| NUS-CPU-05 | `D143J8` | `D147J8` | Sep 1998 | Sep 1998 | |
| NUS-CPU-05 | `D143K8` | `D147K8` | Oct 1998 | Oct 1998 | |
| NUS-CPU-05 | `D143L8` | `D147L8` | Nov 1998 | Nov 1998 | ID: Prominos_05 |
| NUS-CPU-05 | `D143G9` | `D147H9` | Jul 1999 | Aug 1999 | |
| NUS-CPU-05-1 | `D143C9` | `D147C9` | Mar 1999 | Mar 1999 | ID: Prominos_05-1 |
| NUS-CPU-05-1? | `D143L8` | `D147K8` | Nov 1998 | Oct 1998 | Revision not visible; U7+U15 both MX9911MC (never seen on pre-05-1 boards) |
| NUS-CPU-06 | - | - | - | - | Board image available; stamp codes illegible |
| NUS-CPU-07 | - | - | - | - | Board images available; stamp codes illegible |
| NUS-CPU-08 | `D143F9` | `D147F9` | Jun 1999 | Jun 1999 | *MX8350 present in 08 onward* |
| NUS-CPU-08 | `D143H9I` | `D147H9I` | Aug 1999 | Aug 1999 | ID: Prominos_08; I-suffix on both |
| NUS-CPU-08 | `D143H9` | `D147J9` | Aug 1999 | Sep 1999 | X2 year inferred |
| NUS-CPU-08 | `D143L9` | `D147L9` | Nov 1999 | Nov 1999 | |
| NUS-CPU-08-1 | `D143H9` | `D147H9` | Aug 1999 | Aug 1999 | |
| NUS-CPU-08-1 | `D143K9` | `D147J9` | Oct 1999 | Sep 1999 | ID: Prominos_08-1 |
| NUS-CPU-08-1 | `D143K9I` | `D147K9I` | Oct 1999 | Oct 1999 | I-suffix on both X1 and X2 |
| NUS-CPU-09 | `D143J0` | `D147H0` | Sep 2000 | Aug 2000 | ID: Prominos_09 |
| NUS-CPU-09 | `D143J0` | `D147J0` | Sep 2000 | Sep 2000 | |
| NUS-CPU-09 | `D143J0I` | `D147K0` | Sep 2000 | Oct 2000 | I-suffix on X1 |
| NUS-CPU-09-1 | `D143H0I` | `D147H0` | Aug 2000 | Aug 2000 | ID: Aringon_01; I-suffix on X1. All visible IC marks with likely decodes: `PIF-NUS A0027 EA` (`0027` NEC date code convention: wk 27, 2000); `CPU-NUS A 0002XK020` (wk 2, 2000); `RCP-NUS 9949KK008` (wk 49, 1999); `RDRAM36 9949KU621`; `AMP-NUS Ⓜ 90.6`⁶; `TI LV125A 9AK DE6J`; `MAV-NUS RS5C382 9MS 9Y`; `MX8350MC 43B TA245201` |
| NUS-CPU-09-1 | `D143K0I` | `D147L0` | Oct 2000 | Nov 2000 | I-suffix on X1 |
| NUS-CPU(R)-01 | `D177G7` | `D147E7` | Jul 1997 | May 1997 | PAL, NUS-001(FRA); ID: kwyjibo_01 |
| NUS-CPU(R)-01 | `D177G7` | `D147E7` | Jul 1997 | May 1997 | PAL, NUS-001(FRA); ID: Prominos_R01 |
| NUS-CPU(P)-01 | `D177J7` | `D147J7` | Sep 1997 | Sep 1997 | PAL; modretro_13 |
| NUS-CPU(P)-01 | `D177G8` | `D147M7I` | Jul 1998 | Dec 1997 | PAL; U7 MX9911MC; I-suffix on X2 |
| NUS-CPU(P)-02 | `D177J9` | `D147J9I` | Sep 1999 | Sep 1999 | PAL; I-suffix on X2 |
| NUS-CPU(P)-02? | `D177J9` | - | Sep 1999 | - | PAL; ID: gamingdoc_06.PAL; X2 not visible; PIF(P)-NUS (marking: `9940 E`; date code: wk 40, 1999); (P)-03 not excluded. U8: Toshiba TC74LCX125 (marking: `LCX 125 9 21`; wk 21, 1999?); only non-Texas Instruments part observed at U8 in corpus |
| NUS-CPU(P)-03-1 | - | - | - | - | PAL; ID: modretro_14. Board image available; stamp codes illegible *(MX8350 present.)* |
| NUS-CPU(M)-01 | `D143G6` | `D147G6` | Jul 1996 | Jul 1996 | PAL-M; ID: grav_01; two MX8330MCs confirmed |
| NUS-CPU(M)-02 | removed | `D147F7` | - | Jun 1997 | PAL-M; ID: gbonifa_01; X1+U6 absent (junk unit) |
| NUS-CPU(M)-02? | `ⓂD143G7` | `D147E7` | Jul 1997 | May 1997 | PAL-M; ID: jasnet_01; revision not visible. Markings: `1997 Nintendo`; `PIF(M)-NUS 9739 D`; `VDC-NUS A BU9801F 727 120`; `ENC-NUS 735 161`; `9480F 7935`; `MX8330MC TEC0968L` (2x); `AMP-NUS 726 180`; `TA78M05F 7I`; `287C` |
| NUS-CPU(M)-05-1 | `Ⓜ143G0` | `D147F0I` | Jul 2000 | Jun 2000 | PAL-M; ID: Mielke_01; `Ⓜ` marking on X1; I-suffix on X2 |

X1 and X2 date codes on individual boards cluster tightly, typically within one to two months of each other. This is consistent with batch component sourcing and provides independent corroboration of the decode. The crystal date progression across revisions also tracks known board revision chronology: NUS-CPU-01 through -04 uniformly yield 1996-1997 dates; NUS-CPU-05 yields 1998-1999; NUS-CPU-08 onward yields 1999-2000. The MHz field is self-evident from the regional clock frequency; the month and year fields are validated by this revision-anchored progression. The decode is therefore strongly self-corroborating across the current corpus.  

⁶ The `Ⓜ` on the AMP-NUS marking is a Matsushita (Panasonic) logo (confirmed by Prominos). It is unrelated the legal mask work protection symbol `Ⓜ` present elsewhere on this hardware (e.g. PIF-NUS); it is similarly distinct from the `Ⓜ` prefix observed on some PAL-M X1 crystals (see footnote ⁴).  

#### 3.5.2 X1 Oscillator Tolerance  

AT-cut crystals are effectively commodity parts; grade and cut determine the exact oscillation frequency. Current production equivalents specify ±30 ppm as the base grade tolerance (lidnariq), yielding a range of ±0.0018 Hz around the canonical values in §2 (e.g. NTSC progressive: [59.8243, 59.8279] Hz). GBS-C telemetry from two available NTSC N64 units corroborates:  

| Unit | Nickname | Progressive (Hz) | Interlaced (Hz) | Offset (P) | Offset (I) |  
| :--- | :--- | :--- | :--- | :--- | :--- |  
| Unit #1 (NUS-CPU-03, RGB-modded) | Daily driver | 59.82771 | 59.94166 | +26.8 ppm | +26.7 ppm |  
| Unit #2 (NUS-CPU-04, RGB-modded) | Junk unit | 59.82731 | 59.94126 | +20.1 ppm | +20.0 ppm |  

Both fall within the predicted tolerance window. The ppm offset within each unit is essentially identical across progressive and interlaced modes, as expected: both rates derive from the same crystal. The differing offsets between units reflect normal unit-to-unit crystal variance. Aggregate second-order variance factors (temperature, aging, supply voltage) require a larger sample to characterize effectively.  

Values derived in §5 are exact by construction, representing irreducible fractions traceable to hardware integers. The hardware itself operates within crystal tolerance. That the measurable values deviate is not a flaw in the derivation; it is the expected relationship between mathematical specification and physical implementation. GBS-C telemetry from PlayStation 1 and Sega Saturn hardware returns progressive values consistent with 2,250,000/37,609 Hz within crystal tolerance, further corroborating the over-determined nature of standards-compliant NTSC 526 half-line progressive timing: independent clock architectures converge on the same value.   

#### 3.5.3 Initialization Transient Behavior  

![Figure 1b](/figures/fig8_mx8330MC_table.png)  
*MX8330MC Rev. E application notice illustrating feedback divider stabilization and startup transient. Source: MX8330MC datasheet*  

MX8330MC and MX9911MC clock generators require an approximately 5 millisecond stabilization period after power-on before FSO reaches steady operation and the derived VI clock domain stabilizes. This occurs during the IPL startup sequence, prior to the first visible scanline. This behavior is not accounted for in the MX8350 datasheet. 

![Figure 1c](/figures/fig25_mx8330mc_macro_prominos.jpg)  
*MX8330MC (U7); 8-pin SOP package; lot code TEB61102. Source: Prominos (Video Game Preservation Collective Discord)*    

![Figure 1d](/figures/fig31_MX9911MC.png)  
*MX9911MC (U7); 8-pin SOP package; chamfered corner pin-1 indicator. Source: Prominos (Video Game Preservation Collective Discord)*  

![Figure 1e](/figures/fig32_MX8350MC.png)  
*MX8350MC (U17); 14-pin SOP package; lot code TA022201. Source: Prominos (Video Game Preservation Collective Discord)*  

### 3.6 Diagnostics  

Nintendo diagnostic procedures (D.C.N. NUS-06-0014-001A) specify the following oscilloscope verification points for clock signal integrity:  

| Signal                      | Component | Pin  | Expected Frequency | Expected Amplitude |  
| :---                        | :---      | :--- | :---               | :---               |  
| NTSC Color Subcarrier (FSC) | U7        | 8    | 3.58 MHz           | 3.0 Vpp            |  
| NTSC Video Clock (VCLK)     | U7        | 1    | 48.68 MHz          | 3.3 Vpp            |  
| PAL Video Clock (VCLK)      | U15       | 1    | 49.66 MHz          | 3.3 Vpp            |  
| System Master Clock         | U10       | 16   | 62.51 MHz          | -                  |  
| Rambus Clock (RCLK)         | U1        | 5    | 250.2 MHz          | -                  |  

> The System Master Clock (62.51 MHz) is a logic-domain frequency used by the CPU and RCP for execution timing. It is derived from the Rambus Clock (RCLK) synthesizer and is distinct from the crystal oscillator frequency (f_xtal) used in video timing derivations.  

---

## 4. Signal Analysis  

Detailed per-mode timing specifications and hardware implementation notes.  

### 4.1 Signal Parameters by Mode  

The following table defines the relationship between VI clock rate (f_vi) and the resulting display timing. See §3.1 for crystal frequencies and register values; fully reduced refresh rate fractions and line frequencies are in §3.3.  

| Mode    | f_vi (VI Clock)      | L (Clocks / Line) | S (Half-Lines) | fV (Refresh Rate) |  
| :---    | :---                 | :---              | :---           | :---              |  
| NTSC-P  | 48.6818181818 MHz    | 3094              | 526            | 59.8261054535 Hz  |  
| NTSC-I  | 48.6818181818 MHz    | 3094              | 525            | 59.9400599401 Hz  |  
| PAL-P   | 49.65653 MHz (exact) | 3178              | 626            | 49.9201277955 Hz  |  
| PAL-I   | 49.65653 MHz (exact) | 3178              | 625            | 50 Hz (exact)     |  
| PAL-M-P | 48.6283216783 MHz    | 3091              | 526            | 59.8183634793 Hz  |  
| PAL-M-I | 48.6283216783 MHz    | 3091              | 525            | 59.9323032193 Hz  |  

> f_vi for PAL-M is derived as exactly 6,953,850,000 ÷ 143 Hz. The slight deviation in NTSC-equivalent timing (≈ 0.0129407959%) is a hardware constraint caused by the requirement of an integer value for the Clocks ÷ Line (L) register.  

#### 4.1.1 Timing Map  

The figure below is a visualization created by lidnariq after oscilloscope analysis of N64 video output. The image dimensions map to signal timing for one NTSC progressive vertical scan period:  

![Figure 3](/figures/fig3_n64_default_libdragon_240p_timing.png)  
*N64 VI Timing Diagram (NTSC Progressive). Source: lidnariq / ares emulator Discord, hardware probe*  

* Vertical Axis (263 units): Represents a single progressive vertical refresh. 263 sequential lines are drawn before VSYNC instructs the display's scanning mechanism (the electron beam in a CRT) to return to the top-left of the raster. Lines are contiguous, with no interleaving.  

* Horizontal Axis (774 units): Represents the number of "VI pixels" per scanline. As established in §3.4, this quotient effectively represents VI clocks per line (L) divided by four (773.5).  

| Element | Region                 | Register                                           |  
| :---    | :---                   | :---                                               |  
| Canvas  | V_SYNC/H_SYNC boundary | `VI_V_TOTAL` and `VI_H_TOTAL` define signal limits |  
| Yellow  | Color Burst            | `VI_BURST` values; must not overlap H_START        |  
| Grey    | Active Area            | `VI_H_VIDEO` and `VI_V_VIDEO` start/end offsets    |  

> Technically, the hardware *will* allow overlap of `VI_BURST` and H_START. Doing so produces color corruption that modulates with scene content. See figure below.  

![Figure 4](/figures/fig22_VI_BURST-overlapping-H_START_devwizard.png)  
*`VI_BURST` overlapping H_START. Source: devwizard / N64brew.dev Discord*  

> Relatedly, if `VI_BURST` remains active at line end, the VI randomly fails to blank the left 7 VI pixels.  

### 4.2 Mode-Specific Notes  

NTSC (Progressive and Interlaced)  

* Crystal frequency: 14.3181818182 MHz (315/22 MHz)  
* VI clock frequency: 48.6818181818 MHz (5355/110 MHz)  
* Color subcarrier: 3.5795454545 MHz (315/88 MHz)  
* VI clock multiplier: 17/5 (3.4)  
* LEAP register: Not used (`0x00`)  

PAL (Progressive and Interlaced)  

* Crystal frequency: 17,734,475 Hz (exact)  
* VI clock frequency: 49,656,530 Hz (exact)  
* Color subcarrier: 4,433,618.75 Hz (exact) (17,734,475/4 Hz)  
* VI clock multiplier: 14/5 (2.8)  
* LEAP register: Used to maintain exact 15625 Hz line frequency  
* LEAP pattern: 5-stage sequence (6-5-6-5-6 pattern) extends scanline duration during blanking periods

PAL-M (Progressive and Interlaced)  

* Crystal frequency: 2,045,250,000 / 143 Hz (exact) (≈ 14.3024475524 MHz)  
* VI clock frequency: 6,953,850,000 / 143 Hz (exact) (≈ 48.6283216783 MHz)  
* Color subcarrier: 511,312,500 / 143 Hz (exact) (≈ 3,575,611.8881118881 Hz ≈ 3.5756118881 MHz)  
* VI clock multiplier: 17 / 5 (3.4)  
* LEAP register: Not used (`0x00`)  

> The VI requires an integer clock count per line; 3091 is the nearest integer to the exact value of 3,090.6, producing the line frequency given above.  

#### 4.2.1 Subcarrier Frequency Relationships  

All N64 video modes adhere to broadcast standard relationships between subcarrier frequency (fS) and horizontal scan frequency (fH):  

| Standard | fS to fH Relationship |  
| :---     | :---                  |  
| PAL      | fS = 283.7516 × fH    |  
| SECAM    | fS = 282 × fH         |  
| PAL-N    | fS = 229.2516 × fH    |  
| PAL-M    | fS = 227.25 × fH      |  
| NTSC     | fS = 227.5 × fH       |  

*Standard fS to fH ratios. Source: Wooding, M., The Amateur TV Compendium, p. 55*  

PAL-M nominally defines fS = 227.25 × fH, but this relationship does not resolve to an integer number of VI clocks per line. The exact colorburst frequency is 3,575,611 + 127/143 Hz. This remainder propagates through the derivation chain. The hardware resolves this by rounding to 3091 VI clocks per line, producing an fH of approximately 15,732.23 Hz rather than the NTSC-standard 15,734.27 Hz. The canonical fV values in this document are derived from the exact fractional colorburst frequency carried through each step; see §5.3 for full derivation.  

> The subcarrier reference signal is delivered to the ENC-NUS encoder (U5) via the SCIN pin (pin 8), which receives the U7.FSC output through a 4.3 kΩ ÷ 820 Ω resistor divider and coupling capacitor C21. This is the hardware path by which the crystal-derived fS enters the analog encode stage. See Figure 2e, §3.4, *ENC-NUS (U5) in circuit*.  

---

## 5. Mathematical Derivations  

This section provides step-by-step derivations for all timing values. Calculations begin with hardware constants and proceed through to the final refresh rates. All quantities originate from hardware-authoritative integers; no floating-point values are used in the derivation path. All frequencies are expressed in Hertz (Hz) unless otherwise noted.  

### 5.1 NTSC Derivation

Constants:

```
Color burst frequency: f_colorburst (fS) = 315/88 MHz  (≈ 3.5795454545 MHz)
Crystal frequency: f_xtal = 4 × f_colorburst = 315/22 MHz  (≈ 14.3181818182 MHz)
VI clock multiplier: M = 17 / 5
VI clocks per line (full scanlines): L = 3,094
Total half-lines (progressive): S_prog = 526
Total half-lines (interlaced): S_int = 525
```

Video clock frequency:

```
f_vi = f_xtal × M
     = (315/22) × (17/5) MHz
     = (315 × 17)/(22 × 5) 
     = 5,355/110  
     = 1,071/22  (reduced)
     ≈ 48.6818181818 MHz  
```

Horizontal scan frequency:

```
fH = f_vi / L
   = (5,355,000,000 / 110) / 3,094 Hz
   = 5,355,000,000 / (110 × 3,094)
   = 5,355,000,000 / 340,340
   = 591,750,000 / 37,609  (reduced)
   = 2,250,000 / 143  (canonical value)
   ≈ 15,734.2657342657 Hz
```

Vertical scan frequency (progressive):

*Progressive: 526 half-lines per vertical scan cycle, scanned sequentially.*  

```
fV_prog  = fH / (S_prog / 2)  
         = (2,250,000 / 143) / (526 / 2) Hz  
         = (2,250,000 / 143) / 263  
         = 2,250,000 / (143 × 263)  
         = 2,250,000 / 37,609  (canonical value)  
         ≈ 59.8261054535 Hz  
```

Vertical scan frequency (interlaced):

*Interlaced: 525 half-lines per vertical scan cycle, alternating between odd and even fields.*  

```
fV_int  = fH / (S_int / 2)
        = (2,250,000 / 143) / (525 / 2) Hz
        = (2,250,000 × 2) / (143 × 525)
        = 4,500,000 / 75,075
        = 60,000 / 1,001  (canonical value)  
        ≈ 59.9400599401 Hz  
```

*The relationship between the progressive and interlaced rates is a direct arithmetic consequence of the half-line count. Both values derive from the same colorburst root:*
```
fH      = 2,250,000 / 143 Hz  (derived above)
fV_int  = fH / (525/2) = 60,000 / 1,001      ≈ 59.9400599401 Hz
fV_prog = fH / (526/2) = 2,250,000 / 37,609  ≈ 59.8261054535 Hz
```

*The divisor (total half-lines ÷ 2) is the only variable. The ~0.12 Hz gap between the two rates is entirely and exactly the consequence of the single additional half-line in the progressive frame structure. See §1.3.*  

### 5.2 PAL Derivation  

Constants:  

```  
Color burst frequency: f_colorburst (fS) = 17,734,475 / 4 Hz  (= 4.43361875 MHz)  
Crystal frequency: f_xtal = 4 × f_colorburst = 17,734,475 Hz  (= 17.734475 MHz)  
VI clock multiplier: M = 14 / 5  
VI clocks per line (full scanlines): L = 3,178  
Total half-lines (progressive): S_prog = 626  
Total half-lines (interlaced): S_int = 625  
```  

Video clock frequency:  

```  
f_vi = f_xtal × M  
     = 17,734,475 × (14/5) Hz  
     = (17,734,475 × 14) / 5  
     = 248,282,650 / 5  
     = 49,656,530 Hz  
     = 49.65653 MHz  (exact)  
```  

Horizontal scan frequency:  

*Without LEAP compensation, the theoretical line frequency would be:*  

```  
fH (theoretical) = f_vi / L  
                 = 49,656,530 / 3,178 Hz  
                 = 24,828,265 / 1,589  (reduced)  
                 ≈ 15,625.0881057269 Hz  
```  

*The LEAP register compensates for this error by adding fractional VI clocks during VSYNC, resulting in an exact line frequency of 15,625 Hz. The ~5.64 ppm frequency error corresponds to a fractional excess of 0.01792 VI clocks per line (0.01792 ÷ 3178 ≈ 5.64 ppm), which accumulates to 5.6 clocks per vertical scan cycle. See §5.2.1.*  

```  
fH = 15,625 / 1 Hz  (canonical value)  
   = 15,625 Hz  (exact)  
```  

Vertical scan frequency (progressive):  

```  
fV_prog  =  fH / (S_prog / 2)  
         = 15,625 / (626 / 2) Hz  
         = 15,625 / 313  (canonical value)  
         ≈ 49.9201277955 Hz  
```  

Vertical scan frequency (interlaced):  

```  
fV_int  = fH / (S_int / 2)  
        = 15,625 / (625 / 2) Hz  
        = (15,625 × 2) / 625  
        = 31,250 / 625  
        = 50 / 1  (canonical value)  
        = 50 Hz  (exact)  
```  

### 5.2.1 PAL Phase Synchronization and LEAP

The N64 VI maintains the exact 15,625 Hz line frequency (fH) required for the PAL standard. The uncompensated line period (L = 3,178) produces a theoretical frequency of 49,656,530 / 3,178 ≈ 15,625.0881 Hz. To achieve the standard, the average number of VI clocks per line must be exactly:

```
L_avg = f_vi / fH = 49,656,530 / 15,625 = 9,931,306 / 3,125
```

The hardware corrects for the 56/3,125 fractional error using the LEAP mechanism, which adds an average of 28/5 VI clocks per S half-lines. For PAL interlaced (S = 625), the average adjustment per line is therefore:
```
LEAP adjustment per line = (28/5) / (S/2) = (28/5) / (625/2) = 56/3,125 VI clocks
```

The true average line length is the sum of the base line length and this LEAP adjustment. This confirms that the hardware mechanism exactly matches the required theoretical value:

```
True L_avg = 3,178 + 56/3,125 = (9,931,250 + 56) / 3,125 = 9,931,306 / 3,125
```

The LEAP mechanism is implemented via the `VI_H_TOTAL_LEAP` register (`0x04400020`). A repeating 5-stage sequence (B-A-B-A-B) alternates between adding 6 clocks (LEAP_B, stored as 3183 → effective L+6) and 5 clocks (LEAP_A, stored as 3182 → effective L+5) during the vertical blanking interval, yielding the required 28/5-clock average per S half-lines. The hardware encodes this as pattern `0x15` (0b10101); confirmed by Rasky and lidnariq (N64brew.dev Discord, 2026-03-05).

```
(6 + 5 + 6 + 5 + 6) / 5 = 28/5 (average clocks added per S half-lines)

fH = f_vi / (L + (28/5) / (S/2))
   = f_vi / (L + 56/3,125)
   = 49,656,530 / (9,931,306 / 3,125)
   = (49,656,530 / 9,931,306) × 3,125
   = 5 × 3,125
   = 15,625 Hz (exact)
```

> These additions occur only during the vertical blanking interval and do not affect active video timing. The sequence is encoded in the `VI_H_TOTAL_LEAP` register.

### 5.3 PAL-M Derivation

Constants:  

```  
Color burst frequency: f_colorburst (fS) = 511,312,500 / 143 Hz (≈ 3,575,611.8881118881 Hz) (≈ 3.5756118881 MHz)  
                                        (= 3,575,611 + 127/143 Hz) (per lidnariq; see §7.3)  
Crystal frequency: f_xtal = 4 × f_colorburst = 2,045,250,000 / 143 Hz (≈ 14,302,447.5524475524 Hz) (≈ 14.3024475524 MHz)  
VI clock multiplier: M = 17 / 5  
VI clocks per line (full scanlines): L = 3,091  
Total half-lines (progressive): S_prog = 526  
Total half-lines (interlaced): S_int = 525  
```  

Video clock frequency:  

```  
f_vi = f_xtal × M  
     = (2,045,250,000 / 143) × (17 / 5) Hz  
     = (2,045,250,000 × 17) / (143 × 5)  
     = 34,769,250,000 / 715  
     = 6,953,850,000 / 143  (canonical value)
     ≈ 48,628,321.6783 Hz  
     ≈ 48.6283216783 MHz  
```  

Horizontal scan frequency:  

```  
fH = f_vi / L  
       = (6,953,850,000 / 143) / 3,091 Hz  
       = 6,953,850,000 / (143 × 3,091)  
       = 6,953,850,000 / 442,013  (canonical value)  
       ≈ 15,732.2295950572 Hz  
```  

Vertical scan frequency (progressive):  

```  
fV_prog = fH / (S_prog / 2)  
        = (6,953,850,000 / 442,013) / 263 Hz 
        = 6,953,850,000 / (442,013 × 263)  
        = 6,953,850,000 / 116,249,419  (canonical value)  
        ≈ 59.8183634793 Hz  
```  

Vertical scan frequency (interlaced):  

```  
fV_int = fH / (S_int / 2)  
       = (6,953,850,000 / 442,013) / (525 / 2) Hz  
       = (6,953,850,000 × 2) / (442,013 × 525)  
       = 13,907,700,000 / 232,056,825  
       = 185,436,000 / 3,094,091  (canonical value)  
       ≈ 59.9323032193 Hz  
```  

#### 5.3.1 Derived Error Analysis  

PAL-M timing deviation from NTSC derives from the 127/143 fractional remainder in the colorburst definition and the integer constraint L = 3,091.  

```
fH_NTSC  = 2,250,000 / 143          ≈ 15,734.2657342657 Hz  
fH_PAL-M = 6,953,850,000 / 442,013  ≈ 15,732.2295950572 Hz  

deviation = ((fH_NTSC - fH_PAL-M) / fH_NTSC) × 100
          = (2.0361392085 / 15,734.2657342657) × 100  
          = 0.0129407959%  
```

---

## 6. Conversion Reference  

This section provides practical conversion matrices, most commonly for the purpose of speedrun timing comparison. The aim is to ease synchronization (thus, subsequent comparative analysis) of realtime speedruns recorded across regional hardware.  

These multipliers assume game logic is bound to video refresh rate (fV), and that the NTSC-to-PAL performance ratio corresponds exactly with the fV ratio. Under those conditions, a longer duration recorded on PAL hardware directly corresponds to a shorter equivalent time on NTSC hardware, and vice versa.  

> When comparing RTA (Real-Time Attack, speedruns measured in realtime) runs recorded at separate refresh rates, questions invariably arise regarding relative degree of difficulty. This document does not seek to provide judgment on the parity of conversion for any given software title.  

The conversion ratios described in this section assume signal homogeneity per source. However, some games switch between progressive and interlaced modes. No single conversion factor is perfectly accurate in such cases. The theoretically correct method (frame-counted weighted average) is largely impractical. One hypothetical compromise: game-specific approximate weighted multipliers based on reasonably representative sample ratios of signal prevalence.  

### 6.1 Approximate Decimal Conversions

For general conversions.

| From \ To | NTSC-P | NTSC-I | PAL-P | PAL-I | PAL-M-P | PAL-M-I |  
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |  
| NTSC-P  | 1.00000 | 0.99810 | 1.19844 | 1.19652 | 1.00013 | 0.99823 |  
| NTSC-I  | 1.00190 | 1.00000 | 1.20072 | 1.19880 | 1.00203 | 1.00013 |  
| PAL-P   | 0.83442 | 0.83283 | 1.00000 | 0.99840 | 0.83453 | 0.83294 |  
| PAL-I   | 0.83576 | 0.83417 | 1.00160 | 1.00000 | 0.83586 | 0.83427 |  
| PAL-M-P | 0.99987 | 0.99797 | 1.19828 | 1.19637 | 1.00000 | 0.99810 |  
| PAL-M-I | 1.00178 | 0.99987 | 1.20056 | 1.19865 | 1.00190 | 1.00000 |  


### 6.2 Exact Fractional Conversions  

For mathematically precise conversions. Fractions are fully reduced and traceable to the canonical values in §2.  

| From \ To | NTSC Progressive | NTSC Interlaced | PAL Progressive | PAL Interlaced | PAL-M Progressive | PAL-M Interlaced |  
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |  
| NTSC-P  | 1/1             | 525/526         | 45072/37609         | 45000/37609         | 15455/15453           | 2704625/2709426     |  
| NTSC-I  | 526/525         | 1/1             | 30048/25025         | 1200/1001           | 1625866/1622565       | 15455/15453         |  
| PAL-P   | 37609/45072     | 25025/30048     | 1/1                 | 625/626             | 581247095/696497616   | 386761375/464331744 |  
| PAL-I   | 37609/45000     | 1001/1200       | 626/625             | 1/1                 | 116249419/139077000   | 3094091/3708720     |  
| PAL-M-P | 15453/15455     | 1622565/1625866 | 696497616/581247095 | 139077000/116249419 | 1/1                   | 525/526             |  
| PAL-M-I | 2709426/2704625 | 15453/15455     | 464331744/386761375 | 3708720/3094091     | 526/525               | 1/1                 |  

---

## 7. Sources  

### 7.1 Figures  

| Figure | Filename | Description (Source) |  
| :--- | :--- | :--- |  
| Figure 1 | `fig1_clock_gen_schematic.png` | *N64 Clock Generation Circuits - U7 (NTSC/PAL-M) and U15 (PAL) (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 1a | `fig6_mx8350_table.png` | *MX8350 output frequencies for NTSC/PAL/MPAL configurations (Source: [MX8350 datasheet](/references/Macronix-MX8350-ocr.pdf))* |  
| Figure 1b | `fig8_mx8330MC_table.png` | *MX8330MC Rev. E application notice illustrating feedback divider stabilization and startup transient (Source: [MX8330MC datasheet](/references/Macronix-MX8330MC-ocr.pdf))* |  
| Figure 1c | `fig25_mx8330mc_macro_prominos.jpg` | *MX8330MC (U7); 8-pin SOP package; lot code TEB61102 (Source: Prominos, Video Game Preservation Collective Discord, [imgur.com](https://imgur.com/a/YpyuRET))* |  
| Figure 1d | `fig31_MX9911MC.png` | *MX9911MC (U7); 8-pin SOP package; chamfered corner pin-1 indicator (Source: Prominos, Video Game Preservation Collective Discord, [imgur.com](https://imgur.com/a/YpyuRET))* |  
| Figure 1e | `fig32_MX8350MC.png` | *MX8350MC (U17); 14-pin SOP package; lot code TA022201 (Source: Prominos, Video Game Preservation Collective Discord, [imgur.com](https://imgur.com/a/YpyuRET))* |  
| Figure 2 | `fig2_rcp_schematic.png` | *RCP-NUS Pinout showing VDC (Video Digital Complex) Timing Outputs (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2a | `fig9_rcp_vdc_schematic.png` | *Video Digital Complex (VDC) pin assignments showing 7-bit digital video output (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2b | `fig13_n64videosys.png` | *N64 Video System - 4-cycle VDC bus protocol, VDC_DSYNC waveform, and byte contents (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 2c | `fig14_vdc-nus.png` | *VDC-NUS (BU9801F) pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 2d | `fig18_VDC-NUS.png` | *VDC-NUS (BU9801F, U4) in circuit - digital input side and analog output stage (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2e | `fig17_ENC-NUS.png` | *ENC-NUS (U5) in circuit - YOUT (luma/S-Video Y) and VOUT (composite video) outputs; SCIN subcarrier input via R13/R12 divider (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2f | `fig15_denc-nus.png` | *DENC-NUS pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 2g | `fig16_mav-nus.png` | *MAV-NUS pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 2h | `fig27_n64rgb_vdc_serial_to_parallel_worthington.png` | *VDC bus serial-to-parallel protocol; 4-cycle byte structure with sync and RGB channel contents (Source: Tim Worthington, [RGB Video DAC for Nintendo 64, Revision 0, 27/1/07](https://gamesx.com/wiki/doku.php?id=av:n64rgb-ntsc))* |  
| Figure 2i | `fig28_n64-nus-03_video_output_circuit_worthington.png` | *NUS-CPU-03 video output circuit: VDC-NUS (U4, BU9801F) to ENC-NUS (U5); R13/R12 divider; RGB output resistors; LUMINANCE/COMPOSITE/CHROMINANCE outputs (Source: Tim Worthington, GameSX Wiki, N64 RGB NTSC, [gamesx.com](https://gamesx.com/wiki/doku.php?id=av:n64rgb-ntsc))* |
| Figure 2j | `fig30_snes_video_path_DarthCloud.png` | *S-RGB A (U7) video circuit: RGB inputs from S-PPU2; discrete transistor drive stage; RGB, LUMA, C.VIDEO, and CHROMA outputs (Source: DarthCloud, SNS-CPU-RGB-02 Video Circuit, 2009, [web.archive.com](https://web.archive.org/web/20260218142532/https://i36.photobucket.com/albums/e36/DarthCloud/snes_video_path.png))* |  
| Figure 3 | `fig3_n64_default_libdragon_240p_timing.png` | *N64 VI Timing Diagram (NTSC Progressive) (Source: lidnariq via ares emulator Discord server; [reverse-engineered via hardware probing](/figures/fig3_n64_default_libdragon_240p_timing.png))* |  
| Figure 4  | `fig22_VI_BURST-overlapping-H_START_devwizard.png` | *`VI_BURST` overlapping H_START (Source: devwizard / N64brew.dev Discord [youtube.com mirror](https://youtu.be/hSFQPQb00ns))*  |  
| Figure 5a | `fig24_X1_(M)D143G7_stamp_code.png` | *Both `Ⓜ` and `D` prefixes visible on a single PAL-M marking (Source: JASNet Soluções em Eletrônica, [Installing RGB Converter v2 on Nintendo 64](https://www.jasnetinfo.com/produtos/rgbconvv2/install/install_nintendo64.php))* |  
| Figure 5b | `fig23_X1_(M)143G0_stamp_code.png`  | *`Ⓜ` marking visible on some PAL-M X1 crystal oscillators (Source: Mielke - MiSTer FPGA Discord, [imgur.com](https://imgur.com/a/SjqcjYj))* |  
| Figure 6 | `fig29_raster_scan_progressive_ian_harvey.png` | *Progressive raster scan: electron beam traversal, horizontal retrace, and vertical retrace (Source: Ian Harvey, Wikimedia Commons, [CC0](https://commons.wikimedia.org/wiki/File:Raster-scan.svg))* |  
| Figure 7 | `fig33_S-RGB_A-SNS.png` | *ROHM BA6596F (S-RGB A) at U7 on SNS-CPU-RGB-01 (Source: SNES Model Differences, [consolemods.org](https://consolemods.org/wiki/SNES:SNES_Model_Differences))* |

### 7.2 References

* [Nintendo 64 Online Manuals (OS 2.0L, v5.2)](https://ultra64.ca/files/documentation/online-manuals/man-v5-2/allman52/) - Hardware behavior; VI implementation details.  
* [Nintendo 64 Online Manuals - Functions Reference Manual (OS 2.0I)](https://ultra64.ca/files/documentation/online-manuals/functions_reference_manual_2.0i/home.html) - VI register mappings; programmable timing.  
* [Nintendo 64 Online Manuals - Programming Manual (OS 2.0J)](https://ultra64.ca/files/documentation/online-manuals/man/pro-man/start/index.html) - Memory-mapped I/O; VI mode definitions; system programming reference.  
* [Nintendo 64 Programming Manual (D.C.N. NUS-06-0030-001 REV G)](https://ultra64.ca/files/documentation/nintendo/Nintendo_64_Programming_Manual_NU6-06-0030-001G_HQ.pdf) - Detailed timing tables.  
* [Nintendo 64 System Service Manual (D.C.N. NUS-06-0014-001 REV A)](https://drive.google.com/drive/folders/1kGlB2TyX7CsmPnSyzpxGcSKpJ1F-ywal) - Block diagrams; boot sequence; oscilloscope timing verification.  
* [Macronix MX8330MC Datasheet](/references/Macronix-MX8330MC-ocr.pdf) - Single-channel clock synthesizer; FSEL, FSC (crystal ÷ 4 color subcarrier output), and FSO (Rambus clock output) pin functions; Rev. E startup transient.  
* [Macronix MX8350 Datasheet](/references/Macronix-MX8350-ocr.pdf) - Dual-channel clock synthesizer; NTSC/PAL/MPAL output frequencies. 
* [Macronix MX9911MC Datasheet](/references/Macronix-MX9911MC-datasheet-ocr.pdf) - Single-channel clock synthesizer; functional equivalent to MX8330MC.    
* [Rohm BA7242F Datasheet](/references/Rohm-BA7242F-(ENC-NUS)-datasheet-ocr.pdf) - ENC-NUS (U5) video encoder IC; YOUT (pin 13) luminance, VOUT (pin 12) composite video, COUT (pin 10) chrominance outputs; SCIN input level 0.45-0.60 Vpp corroborating the R13/R12 attenuation network; NT/PAL pin logic (HIGH = NTSC, LOW = PAL).  
* [NUS-CPU-07 Annotated Circuit Board (ChipWorks, Rev 1.0, Nov 2000)](/references/NUS-CPU-07-Annotated-PCB-ChipWorks-ocr.pdf) - Professional teardown; board-level IC identification, manufacturer attribution, and component revision corroboration.    
* [ITU-R Recommendation BT.470-6](/references/R-REC-BT.470-6-199811-S!!PDF-E.pdf) - NTSC/PAL lines per frame, fields/sec, color subcarrier frequencies.  
* [ITU-R Recommendation BT.1700 Annex 1](/references/R-REC-BT.1700-0-200502-I!!ZPF-E_1700-e.pdf) - Composite video signal characteristics for NTSC, PAL, and SECAM; signal levels, sync timing, chrominance subcarrier frequencies and modulation.  
* [ITU-R Recommendation BT.1700 Annex 2](/references/R-REC-BT.1700-0-200502-I!!ZPF-E_S170m-2004.pdf) - SMPTE 170M-2004 (incorporated by reference); NTSC composite analog video for studio applications; subcarrier frequency, line/field frequency specifications, horizontal/vertical blanking and sync timing.  
* [ITU-R Recommendation BT.1701](/references/R-REC-BT.1701-1-200508-I!!PDF-E.pdf) - Horizontal/vertical timing for composite video.  
* [US4054919A - Video Image Positioning Control](https://patents.google.com/patent/US4054919A/en) (1977) - Sync counter generation and display positioning.  
* [US6239810B1 - High Performance Low Cost Video Game System](https://patents.google.com/patent/US6239810B1/en) (2001) - VI register set; HSYNC LEAP register; VSYNC/HSYNC timing registers; interlaced odd/even line handling; crystal-controlled clock generator.  
* [US6331856B1 - Video Game System with Coprocessor](https://patents.google.com/patent/US6331856B1/en) (2001) - VI register architecture; HSYNC LEAP register (Fig. 35I) with LEAP_A/LEAP_B fields; interlaced display field toggling; clock generator crystal timing chain.  
* [US6556197B1 - Programmable Video Timing Registers](https://patents.google.com/patent/US6556197B1/en) (2003) - Horizontal/vertical sync generation; color burst gate timing.  
* [Philips SAA1101 Universal Sync Generator Datasheet](/references/Philips-SAA1101-datasheet-ocr.pdf) - Corroborating hardware reference for PAL-M fS = 227.25 × fH relationship.  
* [RWeick - NUS-CPU-03-Nintendo-64-Motherboard (GitHub)](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard) - Complete NUS-CPU-03 KiCAD schematic; component values; signal paths.  
* [Tim Worthington - GamesX Wiki - N64 RGB NTSC](https://gamesx.com/wiki/doku.php?id=av:n64rgb-ntsc) - NUS-CPU-03 video output circuit schematic by Tim Worthington; corroborates YOUT/VOUT/COUT routing to Multi-AV connector.  
* [Tim Worthington - N64RGB Page](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html) - 4-cycle VDC bus protocol diagram and DAC pinouts (Figures 2b, 2c, 2f, 2g).  
* [Rodrigo Copetti - Nintendo 64 Architecture - A Practical Analysis](https://www.copetti.org/writings/consoles/nintendo-64/) - General hardware overview; encoder revision corroboration.  
* [Zoinkity - VI Settings Pastebin](https://web.archive.org/web/20260119215039/https://pastebin.com/pJG5SBnW) - 237/474 line libultra behavior; VI reverse-engineering details.  
* [Link83 et al - ModRetro Forums - N64 Motherboard Revisions](https://forums.modretro.com/threads/nintendo-64-motherboard-revisions-serials-info-request.1417/) - Motherboard revision history; component changes; video encoder chip progression across revisions; board scans.  
* [kwyjibo, Link83 et al - NFGGames Forum - NUS-CPU(R)-01 Discussion](https://nfggames.com/forum2/index.php?topic=3083.0) - Community documentation of the French PAL console, NUS-CPU(R)-01 board, and S-RGB A encoder.  
* [Link83 et al - NFGGames Forum - Datasheet Links Thread](https://nfggames.com/forum2/index.php?topic=3525.0) - Community identification of BA7242F as ENC-NUS match; source of datasheet link.  
* [QUAKEMASTER - N64 RGB Mod Guide (German)](https://web.archive.org/web/20130130062716/http://free-for-all.ath.cx:80/daten/n64rgbmod.html) - Identifies the NUS-CPU(R)-01 motherboard; documents the S-RGB A pinout for RGB restoration; confirms DENC-NUS' unsuitability for RGB output.  
* [N64brew.dev](https://n64brew.dev/) - VI register behavior; timing examples; LEAP implementation; video DAC chip variants (VDC-NUS, DENC-NUS, AVDC-NUS, MAV-NUS); 4-cycle bus protocol; VDC_DSYNC signal behaviour; OS interface functions for VI and hardware access.  
* [Libdragon](https://libdragon.dev/) - High-level API access to N64 hardware and VI timing abstraction.  
* [hkz-libn64](https://github.com/mark-temporary/hkz-libn64) - Direct register-level mappings including VI constants.  
* [n64.readthedocs.io - N64 Hardware Reference](https://n64.readthedocs.io/index.html#video-interface) - Emulator developer reference; SDK register naming corroboration; interrupt handling detail.  
* [ares N64](https://github.com/ares-emulator/ares/tree/master/ares/n64) / [CEN64](https://github.com/n64dev/cen64) / [MAME N64](https://github.com/mamedev/mame/blob/master/src/mame/nintendo/n64.cpp) - Software implementations of VI timing.  
* [Robert Peip et al - MiSTer FPGA N64 Core](https://github.com/MiSTer-devel/N64_MiSTer) - Corroboration of Zoinkity NTSC 237/474 libultra bounds via Clean HDMI function; FPGA implementation of N64 VI timing.  
* [Wikipedia - NTSC](https://en.wikipedia.org/wiki/NTSC) / [PAL](https://www.wikipedia.org/wiki/PAL) / [PAL-M](https://www.wikipedia.org/wiki/PAL-M) - Broadcast standard overviews.  
* [Mike Wooding - ATV Compendium (BATC)](https://batc.org.uk/wp-content/uploads/ATVCompendium.pdf) - PAL-M fS = 227.25 × fH relationship.  
* [Martin Hinner - VGA/PAL](https://martin.hinner.info/vga/pal.html) - PAL video timing specification (sourced from R. Salmon, sci.engr.television.broadcast, 1996).  
* [Alan Pemberton - World TV Standards](https://web.archive.org/web/20160512200958/http://www.pembers.freeserve.co.uk/World-TV-Standards/) - Detailed information on broadcast standards; HBI and VBI visualizations.  
* [David - EEVblog Forums - Nintendo 64 Game Console Teardown](https://www.eevblog.com/forum/blog/eevblog-491-nintendo-64-game-console-teardown/25/) - Chip progression by board revision; AVDC-NUS RGB tap rationale; AVDC-NUS/MAV-NUS shared pinout observation.  
* [Pacal - BitBuilt 2022 Summer Building Competition - Odyssey 64](https://bitbuilt.net/forums/threads/2022-contest-entry-odyssey-64.5061/) - NUS-CPU-05 board; `D143G8`/`D147G8I` crystal stamps.  
* [Miceeno - BitBuilt Forums - N64 Expansion Paks RAM Part Numbers](https://bitbuilt.net/forums/threads/n64-expansion-paks-ram-part-numbers.3943/post-44749) - NUS-CPU-05 board; `D143G9`/`D147H9`; MAV-NUS on NUS-CPU-05.  
* [Chunky-Soups - Reddit r/n64](https://www.reddit.com/r/n64/comments/1awwnao/does_this_n64_have_any_raritysignificance/) - NUS-CPU-09 board; `D143J0`/`D147J0`; MAV-NUS BU9906F confirmed.  
* [JASNet Soluções em Eletrônica - N64 RGB Install Guide (Portuguese)](https://www.jasnetinfo.com/produtos/rgbconvv2/install/install_nintendo64.php) - NUS-CPU(M)-02 candidate board; `ⓂD143G7`/`D147E7`; `Ⓜ` marking on X1.  
* [Prominos - N64 Motherboard Images](https://imgur.com/a/YpyuRET) - Collection of high quality N64 motherboard images including rare NUS-CPU(R)-01 model, shared by Prominos (Video Game Preservation Collective Discord).
* [Mielke - NUS-CPU(M)-05-1 Images](https://imgur.com/a/SjqcjYj) - Photos of rare MPAL model, shared by Mielke (MiSTer FPGA Discord).
* [grav - NUS-CPU(M)-01 Images](https://imgur.com/a/fD0AuBj) - Photos of rare MPAL model, shared by grav (Discord64 Discord).
* [Aringon - NUS-CPU-09-1 Images](https://imgur.com/a/yfoPbqS) - Photos of rare 09-1 model, shared by Aringon (Video Game Preservation Collective Discord).
* [Console Mods - SNES Model Differences](https://consolemods.org/wiki/SNES:SNES_Model_Differences) - Confirmation of S-RGB A usage in some SNES models via board photos.

![Figure 7](/figures/fig33_S-RGB_A-SNS.png)  
*ROHM BA6596F (S-RGB A) at U7 on SNS-CPU-RGB-01 (Source: SNES Model Differences, [consolemods.org](https://consolemods.org/wiki/SNES:SNES_Model_Differences))*

#### 7.2.1 Personal resources

* [N64 Motherboard Images Collection](https://imgur.com/a/B4uPSNF) - Collection of N64 motherboard images with source links. Some boards are damaged, trimmed, modified, or otherwise altered.

### 7.3 Acknowledgements

* [A post by awe444 on videogameperfection.com](https://videogameperfection.com/forums/topic/nintendo-64-de-blur/page/2/#post-12502) for the initial spark of curiosity.  
* lidnariq for PAL-M colorburst correction (§5.3), VDC_DSYNC behavior analysis (§3.2, §3.4), ±30 ppm crystal tolerance figure (§3.5.2), month decode suggestion (§3.5.1.2), VI timing map (Figure 3), several minor corrections, and extensive audits.  
* devwizard for sharing experimental observations of dynamic chroma modulation and left-pixel blanking failure under `VI_BURST` / H_START overlap (§4.1.1).  
* Robert Peip (FPGAzumSpass) for auditing and corroboration of `VI_V_CURRENT` behaviour.  
* Rasky for cross-referencing register naming against N64brew convention.  
* kev4cards for several research leads, refinement, and general auditing.  
* grav, Mielke, Prominos, and Aringon for sharing motherboard images including rare MPAL, NUS-001(FRA), and NUS-CPU-09-1 examples.

---

### 8. Glossary

A quick reference for terminology used in this document.

* **240p:** Shorthand for NTSC and PAL-M progressive mode. One vertical scan comprises 263 scanlines; a 23 scanline blanking period with the remaining 240 lines available for active video output. All N64 signal output is fixed at 640 pixels wide. Contemporary retail NTSC games built with libultra draw no more than 237 lines (474 half-lines) of visible content per vertical scan. PAL equivalent is 288p. *See also: Progressive, Raster, Vertical Scan Frequency.*

* **480i:** Shorthand for NTSC and PAL-M interlaced mode. One vertical refresh comprises two interlaced fields across 525 half-lines; a 45 half-line blanking period with the remaining 480 half-lines available for active video output. Contemporary retail NTSC games built with libultra draw no more than 474 half-lines of visible content per vertical refresh. PAL equivalent is 576i. *See also: Interlaced, Vertical Scan Frequency.*

* **BFP (Burst Flag Pulse):** A timing pulse generated by the VDC-NUS chip (U4) that gates the colorburst window on each active line. It signals to the downstream encoder (ENC-NUS, U5) the interval during which the chroma subcarrier reference should be inserted into the back porch of the composite output. The burst gate window duration is approximately 5.1 μs per oscilloscope observation. *See also: Chrominance Subcarrier Frequency, CSYNC.* 

* **C_stray:** The aggregate parasitic capacitance contributed by PCB traces and IC pin capacitance in an oscillator circuit. Not directly measurable without physical probing of the specific board. In the NUS-CPU-03 X1 load capacitance derivation, C_stray is estimated in the range of 2-5 pF, yielding an effective CL of approximately 23.5-26.5 pF. *See also: Crystal Oscillator Frequency, CL.*  

* **Chrominance Subcarrier Frequency (fS, f_colorburst):** A reference sine wave inserted into the back porch of the horizontal blanking interval on each active line, providing the phase and frequency reference against which a receiver decodes color information. Its frequency is defined by international broadcast standards: 315/88 MHz (NTSC), 17,734,475/4 Hz (PAL), and 511,312,500/143 Hz (PAL-M). In this document's derivations, fS serves as the starting constant from which f_xtal and all downstream timing values are established. *See also: BFP, fH.*  

* **CL (Load Capacitance):** The total capacitance presented to a crystal oscillator by its circuit, comprising the series combination of the two load capacitors plus C_stray. Determines the operating frequency of the crystal; a mismatch between specified and actual CL produces a frequency offset. *See also: C_stray, Crystal Oscillator Frequency.*

* **Colorburst:** *See Chrominance Subcarrier Frequency.*

* **Crystal Oscillator Frequency (f_xtal):** The principal high-frequency crystal oscillator signal that drives the N64's Reality Co-Processor (RCP). All video timing is derived from this signal through integer multiplication and division. On early revisions, f_xtal is produced at U7 (MX8330MC or MX9911MC, depending on revision; see §3.1.1) from crystal X1. X1's frequency varies by region: 315/22 MHz for NTSC and PAL-M; 17,734,475 Hz for PAL. VI clock (f_vi) equals f_xtal multiplied by the region-specific factor M (17/5 for NTSC and PAL-M; 14/5 for PAL). f_xtal is the hardware primitive from which N64 video timing is wholly derived.  

* **CSYNC (Composite Sync):** A signal generated by the VDC-NUS (U4) that combines horizontal sync (HSYNC) and vertical sync (VSYNC) into a single waveform. CSYNC is passed to the ENC-NUS encoder (U5) and embedded in the final composite video output, allowing a display to lock to the signal's horizontal and vertical timing simultaneously. *See also: VSYNC, BFP.*

* **f_xtal:** Symbol for crystal oscillator frequency. *See Crystal Oscillator Frequency.*  

* **fH:** Symbol for horizontal scan frequency. *See Horizontal Scan Frequency.*  

* **fS (f_colorburst):** Symbol for colorburst or chroma subcarrier signal. fS connotes broadcast standard constant. f_colorburst disambiguates. *See Chrominance Subcarrier Frequency.*  

* **fV:** Symbol for vertical scan frequency (refresh rate). *See Vertical Scan Frequency.*

* **Half-Line (S):** The atomic unit of vertical timing used by the N64's Video Interface (VI). Two half-lines constitute one full horizontal scanline. The total half-line count per vertical scan cycle is programmed via `VI_V_TOTAL`; the effective value is `VI_V_TOTAL` + 1. *See also: Terminal Count.*

* **Horizontal Scan Frequency (fH):** The number of horizontal lines transmitted per second, expressed in Hz. Derived as f_vi ÷ L. Also referred to as line frequency. *See also: L, fV.*

* **Interlaced (I):** A scan method in which lines are interleaved across two successive vertical scans in alternating stripes of even-odd (262.5 lines per vertical scan in NTSC and PAL-M interlaced modes). The VI offsets vertical sync by one half-line on every other scan, each constituting a field in broadcast terminology. fV represents the rate of each individual vertical scan. *See also: Progressive, Half-line, fV.*

* **L (VI Clocks per Line):** Symbol for the number of VI clock cycles that constitute one full horizontal scanline, as defined by the `VI_H_TOTAL` register. The effective value is `VI_H_TOTAL` + 1 (terminal-count convention). Values are 3,094 (NTSC), 3,178 (PAL), and 3,091 (PAL-M). *See also: Terminal Count, VI.*

* **LEAP Register:** A hardware compensation mechanism used exclusively by PAL N64 consoles. It periodically adjusts the length of a scanline by one VI clock cycle to correct for the fractional timing error that results from integer constraints in the horizontal timing registers. The adjustment follows a repeating 5-stage B-A-B-A-B sequence (6,5,6,5,6 VI clocks added; LEAP_B stores 3183 → L+6, LEAP_A stores 3182 → L+5; hardware pattern `0x15` = 0b10101) and allows fH to maintain the PAL standard 15,625 Hz line frequency. *See also: PAL, f_vi.*

* **M (VI Clock Multiplier):** The region-specific rational factor by which f_xtal is multiplied to produce f_vi. Values are 17/5 for NTSC and PAL-M, and 14/5 for PAL. M is a deterministic hardware ratio and does not vary; crystal tolerance affects f_xtal and propagates through the derivation chain, but M itself is fixed. *See also: Crystal Oscillator Frequency, Horizontal Scan Frequency.*

* **MX8330MC:** A single-channel Macronix clock synthesizer IC used at U7 on early N64 revisions to produce f_vi from crystal X1. FSEL high selects the 17/5 multiplier (NTSC and PAL-M); FSEL low selects 14/5 (PAL). X1 varies by region. U7 is MX8330MC on NUS-CPU-01 through NUS-CPU-04; U7 identity on NUS-CPU-06 and NUS-CPU-07 is unconfirmed. U15 on NUS-CPU-07 is MX8330MC per ChipWorks teardown; U7 is not annotated in that document. The chip outputs FSC (crystal ÷ 4, the chroma subcarrier reference) and FSO/5 from a dedicated pin to drive the video domain. Later revisions consolidated the video clock into the MX8350. *See also: MX9911MC, MX8350, Crystal Oscillator Frequency.*  

* **MX8350:** A dual-channel Macronix clock synthesizer that replaced the twin single-channel chip configuration in later N64 revisions (NUS-CPU-08 onward, 1999+). It consolidates both NTSC/PAL-M and PAL clock synthesis with equivalent output frequencies. Derived values are unaffected by this revision. *Physical chips are marked MX8350MC; datasheet Part No. is MX8350. See also: MX8330MC, MX9911MC.*

* **MX9911MC:** A single-channel Macronix clock synthesizer IC. Functionally equivalent to the MX8330MC: identical 8-pin SOP package, pin assignments, FSEL logic (High → 17/5 multiplier, Low → 14/5 multiplier), FSC (crystal ÷ 4) and FSO/5 outputs, and 5 ms power-up stabilization time. Math is unaffected. MX9911MC at U7 brackets the board revision to (05, 07) inclusive (NTSC); confirmed on NUS-CPU-05 and NUS-CPU-05-1; identity on NUS-CPU-06 and NUS-CPU-07 not confirmed from available board photos. MX9911MC at U15 is believed to bracket the revision to (05-1, 07) inclusive. NUS-CPU-05 retains MX8330MC at U15; NUS-CPU-05-1 includes at least one MX9911MC (at U7), and may include another at U15. *See also: MX8330MC, Crystal Oscillator Frequency.*  

* **NTSC (National Television System Committee):** The broadcast video standard used in North America, Japan, South Korea, and parts of Central America. Precisely, the standard name is NTSC-M (so-called due to combination of System M (a monochrome broadcast standard) and NTSC color specification). Defines a 525-line, approximately 59.94 Hz interlaced signal. On the N64, the NTSC crystal is 315/22 MHz (exact), the VI clock multiplier is 17/5, and there are 3,094 VI clocks per line. *See PAL, PAL-M.*  

* **PAL (Phase Alternating Line):** Broadcast video standard used across Europe, Australia, New Zealand, and much of Africa and Asia. 625-line, 50 Hz interlaced signal with a chroma subcarrier of exactly 4,433,618.75 Hz. On the N64, the PAL crystal is 17.734475 MHz (exact), the VI clock multiplier is 14/5, and LEAP register use is required to maintain standard 15,625 Hz line frequency. *See also NTSC, PAL-M.*  

* **PAL-M (MPAL):** A distinct Brazilian broadcast standard that combines PAL-derived color encoding with an NTSC-derived line rate. The "M" in PAL-M refers to CCIR System M. The chroma subcarrier is 511,312,500/143 Hz (containing a 127/143 fractional remainder), the crystal is 2,045,250,000/143 Hz, and there are 3,091 VI clocks per line. Commonly referred to as MPAL; less commonly, PAL/M.  *See also NTSC, PAL.*

* **Progressive (P):** A scan method in which all lines of a vertical scan are transmitted sequentially in a single pass. Half-lines per vertical scan (S) must be even in progressive modes (526, 626). fV represents the rate of each complete vertical scan. In full scanline units, 526 half-lines corresponds to 263 scanlines: 240 active and 23 vertical blanking. *See also: Interlaced, Half-line, fV.*

* **Raster:** The complete signal area of one vertical scan, encompassing both the active area and all blanking intervals. In the context of lidnariq's VI timing visualization (Figure 3), each horizontal unit represents one VI pixel group and each vertical unit represents one half-line. *See figure below.*

![Figure 6](/figures/fig29_raster_scan_progressive_ian_harvey.png)  
*Progressive raster scan: electron beam traversal, horizontal retrace, and vertical retrace. Source: Ian Harvey, Wikimedia Commons ([CC0](https://commons.wikimedia.org/wiki/File:Raster-scan.svg))*

* **RCP (Reality Co-Processor):** Principal Silicon Graphics co-processor in the N64 that handles both graphics (Reality Display Processor) and audio/system tasks (Reality Signal Processor). It contains the Video Interface (VI), which generates video timing signals.

* **S (Half-Lines per Vertical Scan):** Symbol for the total half-line count per vertical scan cycle, as programmed via the `VI_V_TOTAL` register. The effective value is `VI_V_TOTAL` + 1 (terminal-count convention). S / 2 gives the number of full scanlines. Values are 526 / 525 (NTSC and PAL-M progressive / interlaced) and 626 / 625 (PAL). *See also: Half-line, Terminal Count.*

* **S-Video:** Two-channel analog video interface that carries luminance (Y) and chrominance (C) as separate signals, mitigating chroma/luma quality loss via composite's single-channel muxing. *On N64 hardware, S-Video output is generated natively by the ENC-NUS, DENC-NUS, AVDC-NUS, and MAV-NUS encoder variants. S-RGB A encoder variants do not output S-Video.*  

* **Terminal Count:** A register convention used by the N64's Video Interface in which the stored value is one less than the effective hardware count. To derive the actual number of clocks or half-lines, add 1 to the register value: effective half-lines = `VI_V_TOTAL` + 1; effective clocks per line = `VI_H_TOTAL` + 1. Timing derivations in this document apply this correction before calculation.  

* **Vertical Scan Frequency (fV):** The rate of vertical scans per second, measured from one VSYNC pulse to the next, expressed in Hz. Also referred to as refresh rate. In progressive modes, fV refers to frame rate; in interlaced modes fV is the rate of each individual field. *See also: VSYNC, Horizontal Scan Frequency.*

* **VDC Bus:** The digital video bus between the RCP (U9) and VDC-NUS (U4). It carries seven bits of pixel data (VDC_D0-VDC_D6), VDC_DSYNC, and a shared clock. Data is transmitted in 4-cycle groups: cycle 0 carries synchronization/control data with VDC_DSYNC low; during active video output, cycles 1-3 carry the Red, Green, and Blue components of one rendered pixel. *See also: VDC_DSYNC, VDC-NUS.*  

* **VDC_DSYNC** *(a.k.a. !DSYNC):* Control qualifier on the VDC bus from the RCP (U9) to VDC-NUS (U4). When low, VDC_D0-VDC_D6 carry synchronization/control bits (cycle 0 of the four-cycle group); when high, the bus carries pixel color data (cycles 1-3). During active video it asserts low once every four VI clocks. During blanking, VDC_DSYNC is held low continuously, allowing the VI to transmit control signals (VSync, HSync, colorburst clamp, CSync) on every VI clock. *See also: VDC Bus.*  

* **VDC-NUS / ENC-NUS / DENC-NUS / S-RGB A / AVDC-NUS / MAV-NUS:** The N64 video output chip family, converting the RCP’s digital stream to analog. NUS-CPU-01 through NUS-CPU-04 use a two-chip path: VDC-NUS (VDC bus D0-D6, DSYNC, CLK in) performs DAC and generates CSYNC/BFP, outputting RGB, CSYNC, and BFP to ENC-NUS (U5), which handles composite/S-Video encoding and receives the chroma subcarrier at SCIN. Later revisions consolidate this into a single chip. Timing is unchanged. *Both AVDC-NUS and MAV-NUS have been observed on unrevised NUS-CPU-05 boards, confirming that they share the same package and compatible pinout (Link83, 2009; David/EEVblog, 2013). Whether they are the same silicon, a process revision, or two approved-equivalent parts is not confirmed. MAV-NUS pins 14–16 carry the audio interface (I2S) (lidnariq).*  

* **VI (Video Interface):** The hardware block within the RCP responsible for generating the N64's video signal. It reads from memory and uses a set of programmable registers (e.g., `VI_V_TOTAL`, `VI_H_TOTAL`) to define the timing, resolution, and format of the output signal.

* `VI_H_VIDEO` (`0x04400024`): Defines the horizontal start and end of the active video window in VI pixels.

* `VI_V_VIDEO` (`0x04400028`): Defines the vertical start and end of the active video window in half-lines.

* **VSYNC (Vertical Synchronization):** A timing pulse in the video signal marking the end of a vertical scan cycle. The rate of VSYNC pulses defines fV. *See also: fV, CSYNC.*

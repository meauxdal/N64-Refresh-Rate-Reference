# N64 Refresh Rate Reference  

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
* [Appendix A. X1 and X2 Crystal Stamp Code Table](#appendix-a-x1-and-x2-stamp-code-table)
    * [A.1 Stamp Code Format](#a1-stamp-code-format)
    * [A.2 X1 and X2 Stamp Codes by Revision (Full)](#a2-x1-and-x2-stamp-codes-by-revision-full)
* [Appendix B. VI Modes](#appendix-b-vi-modes)
    * [B.1 Libultra VI Mode Decoder](#b1-libultra-vi-mode-decoder)
    * [B.2 Libultra VI Mode Definitions](#b2-libultra-vi-mode-definitions)
    * [B.3 Libdragon VI Mode Definitions](#b3-libdragon-vi-mode-definitions)
* [Glossary](#glossary)

---

## 1. Introduction  

![NUS-CPU-01 motherboard](/figures/fig35_NUS-CPU-01_Prominos.jpg)  
*Nintendo 64 motherboard (NUS-CPU-01) showing the Nintendo Reality Coprocessor (RCP-NUS, U9) and NEC VR4300 (CPU-NUS, U10). The Video Interface (VI), part of the RCP, generates composite video timing for NTSC, PAL, and PAL-M output modes. Source: Prominos, photographed hardware board image, [imgur.com](https://imgur.com/a/YpyuRET).*  


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

All video timing derives from a quartz crystal piezoelectric resonator (designated **X1** on the N64 mainboard), whose oscillation frequency in circuit is designated **f_xtal**. The VI clock (**f_vi**) is produced by multiplying f_xtal by a region-specific rational multiplier M (17/5 for NTSC and PAL-M; 14/5 for PAL). **fH** (horizontal scan frequency) follows by dividing f_vi by **L**, the integer VI clock count per horizontal line. **fV** follows by dividing fH by the number of full scanlines (S/2, where **S** is the vertical half-line count).  

```
f_vi = f_xtal × M
fH   = f_vi / L
fV   = fH / (S / 2)

fV   = (f_xtal × M) / (L × (S / 2))
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

**Half-line (S)** is the atomic unit for VI vertical timing. One scanline equals 2 half-lines. This document favors half-line modeling to align with hardware counting. See [§5.1.1](#511-ntsc-leap-adjustment).  

#### 1.3.2 Registers

The document uses N64brew naming conventions throughout. SDK equivalents are noted here for cross-reference.

| N64brew Name | SDK Name | Address | Description |
|:---|:---|:---|:---|
| `VI_V_TOTAL` | `VI_V_SYNC_REG` | `0x04400018` | Terminal half-line count; effective half-lines = REG + 1 |
| `VI_H_TOTAL` | `VI_H_SYNC_REG` | `0x0440001C` | Terminal VI clock count per scanline; effective clocks = REG + 1 |
| `VI_H_TOTAL_LEAP` | `VI_H_SYNC_LEAP_REG` | `0x04400020` | LEAP_A [bits 27:16] and LEAP_B [bits 11:0] alternate scanline lengths for PAL compensation |
| `VI_V_CURRENT` | `VI_V_CURRENT_LINE_REG` | `0x04400010` | Current half-line; increments by 2 per scanline |
| `VI_BURST` | `VI_BURST_REG` | `0x04400014` | Color burst gate timing |
| `VI_H_VIDEO` | `VI_H_VIDEO_REG` | `0x04400024` | Active video horizontal start/end |
| `VI_V_VIDEO` | `VI_V_VIDEO_REG` | `0x04400028` | Active video vertical start/end |

All registers are terminal-counted; add 1 to the register value to derive the effective count. Interlaced VSYNC is automatically offset by 0.5 lines per field. See [§5.2.1](#521-pal-leap-adjustment) for details regarding the leap adjustment mechanism.  

![US6331856](/figures/fig34_US6331856-pp46-47.png)  
*Video Interface (VI) register layout from U.S. Patent 6,331,856 (sheets 46-47). Source: [U.S. Patent 6,331,856](https://patents.google.com/patent/US6331856B1/en)*
 
---

## 2. N64 Video Output Summary  

### 2.1 Refresh Rate  

The table lists refresh rates (fV) for all video modes. The fully reduced fractions shown below serve as reference values for the remainder of this text.  

| Mode  | Scan Type   | fV (Hz, fraction)            | fV (Hz, decimal)              |  
| :---  | :---        | :---                         | :---                          |  
| NTSC  | Progressive | 2,250,000 / 37,609           | 59.8261054535                 |  
| NTSC  | Interlaced  | 60,000 / 1,001               | 59.9400599401                 |  
| PAL   | Progressive | 15,625 / 313                 | 49.9201277955                 |  
| PAL   | Interlaced  | 50 / 1                       | 50 (exact)                    |  
| PAL-M | Progressive | 17,384,625,000 / 290,532,671 | 59.8370742270                 |  
| PAL-M | Interlaced  | 272,700,000 / 4,547,257      | 59.9702194092                 |  

> These values correspond to the derivations in [§5](#5-mathematical-derivations).  

### 2.2 Resolution  

In the context of contemporary retail software, the N64 outputs four distinct raster formats:  

| Signal | Scan Type   | Resolution |  
| :---   | :---        | :---       |  
| NTSC   | Progressive | 640x240p   |  
| NTSC   | Interlaced  | 640x480i   |  
| PAL    | Progressive | 640x288p   |   
| PAL    | Interlaced  | 640x576i   |  

Note that these are effective output resolutions, after all scaling operations. PAL-M signals share corresponding NTSC resolutions. See [Appendix B](#appendix-b-vi-modes) for full VI mode tables. 

---  

## 3. Technical Specifications  

Hardware constants and register mapping.  

### 3.1 Fundamental Constants  

Hardware constants derived from f_xtal and the Video Interface (VI) registers. L and S below are effective values. 

| Mode              | Crystal Frequency (f_xtal) | Multiplier (M) | VI Clocks / Line (L) | Half-Lines (S) | `VI_V_TOTAL` |  
| :---              | :---                       | :---           | :---                 | :---           | :---         |  
| NTSC Progressive  | 14.3181818182 MHz          | 17 / 5         | 3094                 | 526            | `0x20D`      |  
| NTSC Interlaced   | 14.3181818182 MHz          | 17 / 5         | 3094                 | 525            | `0x20C`      |  
| PAL Progressive   | 17.734475 MHz (exact)      | 14 / 5         | 3178                 | 626            | `0x271`      |  
| PAL Interlaced    | 17.734475 MHz (exact)      | 14 / 5         | 3178                 | 625            | `0x270`      |  
| PAL-M Progressive | 14.3024475524 MHz          | 17 / 5         | 3090                 | 526            | `0x20D`      |  
| PAL-M Interlaced  | 14.3024475524 MHz          | 17 / 5         | 3089                 | 525            | `0x20C`      |  

* NTSC f_xtal target: 315/22 MHz (exact) (≈ 14.3181818182 MHz)  
* PAL f_xtal target: 17,734,475 Hz (exact) = 17.734475 MHz  
* PAL-M f_xtal target: 2,045,250,000 ÷ 143 Hz (exact) (≈ 14.3024475524 MHz)  

#### 3.1.1 Clock Generator Hardware Revisions  

![Clock Generation Circuits](/figures/fig1_clock_gen_schematic.png)  
*N64 Clock Generation Circuits - U7 & U15 (Macronix MX8330MC). Source: RWeick, [NUS-CPU-03-Nintendo-64-Motherboard](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard)*  

Early revisions use a single-channel clock synthesizer at U7, driven by crystal X1, to produce f_vi. FSEL multiplier logic is high (17/5) for NTSC and PAL-M; low (14/5) for PAL. Later revisions substitute the pin-compatible MX9911MC at one or both synthesizer positions before consolidating both clocks into a single MX8350 dual-channel chip at U17 from NUS-CPU-08 onward. These substitutions do not affect derived timing values. See [§3.5.1.1](#3511-x1-identification) for visual identification.
 
![MX8350 table](/figures/fig6_mx8350_table.png)  
*MX8350 (later revisions) output frequencies for NTSC/PAL/MPAL. Source: [MX8350 datasheet](/references/Macronix-MX8350-ocr.pdf)*  

> While the MX8350 datasheet lists the PAL-M crystal as 14.302446 MHz, the correct rate (derived from the broadcast standard PAL-M colorburst frequency) is 2,045,250,000 / 143 Hz (≈ 14.3024475524 MHz); the origin of this discrepancy is not understood. Derivations in this document use the latter standard frequency. See [§5.3](#53-pal-m-derivation).  

### 3.2 Video Interface (VI) Register Mapping  

The RCP (Reality Co-Processor) processes video timings through the following memory-mapped I/O (MMIO) registers:  

![RCP-NUS in circuit](/figures/fig2_rcp_schematic.png)  
*RCP-NUS (U9) in circuit. Source: RWeick, [NUS-CPU-03-Nintendo-64-Motherboard](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard)*  

![VDC schematic detail](/figures/fig9_rcp_vdc_schematic.png)  
*VDC pin assignments - 7-bit digital output. Source: RWeick, [NUS-CPU-03-Nintendo-64-Motherboard](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard)*  

The VDC bus carries:  
* VDC_D0 through VDC_D6: 7-bit digital video data  
* VDC_DSYNC (a.k.a DSYNC or !DSYNC): Continuous timing signal; while low, sync information is encoded on the accompanying VDC data lines. Data is valid on the falling edge of this signal.

These signals are transmitted to the VDC-NUS (BU9801F, U4), which performs digital-to-analog conversion and generates CSYNC (Composite Sync) and BFP (Burst Flag Pulse) for the downstream ENC-NUS encoder (U5). This two-stage signal path (VDC-NUS + ENC-NUS) applies to NUS-CPU-01 through NUS-CPU-04, as well as early PAL-M revisions. Other revisions consolidate both functions into a single chip; e.g. DENC-NUS, AVDC-NUS, & MAV-NUS. The substitution of these components is not known to affect timing values derived in this document.  

> VI registers operate on terminal counts; all derived timing values use the hardware-consistent half-line model described in [§1](#1-introduction).

* `VI_V_TOTAL` (`0x04400018`): The register stores a terminal half-line count; effective number of half-lines per vertical scan is equal to `VI_V_TOTAL` + 1.  
* `VI_H_TOTAL` (`0x0440001C`): The register stores a terminal VI clock count (per full scanline); effective clocks per scanline is equal to `VI_H_TOTAL` + 1.  
* `VI_V_CURRENT` (`0x04400010`): Reports the current half-line count; increments by 2 per full scanline. In interlaced mode, bit 0 toggles each field to indicate odd or even lines.  
* `VI_H_VIDEO` (`0x04400024`): Defines the horizontal start and end of the active video window in VI pixels (L/4).  
* `VI_V_VIDEO` (`0x04400028`): Defines the vertical start and end of the active video window in half-lines.  

> For interlaced modes, S is set to an odd integer (525 or 625). The VI hardware automatically offsets the vertical sync position by 0.5 lines every other field.  

### 3.3 Derived Timing Values  

Timing values in this section are calculated from the fundamental constants in [§3.1](#31-fundamental-constants). fH is line frequency; fV is vertical scan frequency (refresh rate). Values are derived from fH and half-line count S. Progressive modes use the full half-line count, interlaced modes offset vertical sync by 0.5 lines per field.  

| Mode      | fH (Hz, decimal)              | fH (Hz, fraction)               | fV (Hz)                      | 
| :----     | :---                          | :---                            | :---                         |
| NTSC-P    | 15,734.2657342657             | 2250000/143                     | 2250000/37609                | 
| NTSC-I    | 15,734.2657342657             | 2250000/143                     | 60000/1001                   |
| PAL-P     | 15,625 (exact)                | 15625/1                         | 15625/313                    | 
| PAL-I     | 15,625 (exact)                | 15625/1                         | 50/1                         |
| PAL-M-P   | 15,737.1505217050             | 4,572,156,375,000 / 290,532,671 | 17,384,625,000 / 290,532,671 | 
| PAL-M-I   | 15,742.1825949138             | 71,583,750,000 / 4,547,257      | 272,700,000 / 4,547,257      | 

### 3.4 Hardware Signal Path

Video signal timing follows a deterministic path from crystal oscillation through digital counting to analog output. The following applies to NUS-CPU-01 through NUS-CPU-04, as documented in RWeick's NUS-CPU-03 schematics.

1. Source: Crystal X1 oscillates at f_xtal; the clock generator (U7)[^1] multiplies this by M to produce f_vi. f_xtal is the hardware primitive for N64 video timing. 
2. Logic: The RCP (Reality Co-Processor, U9) receives f_vi to drive the internal VI logic.
3. Counting: The VI counts clock cycles according to `VI_H_TOTAL` (line length) and `VI_V_TOTAL` (vertical extent) to define the signal's timing boundaries.  
4. Encoding: The VI transmits pixel data to the VDC-NUS over the VDC bus: a 7-bit[^2] data bus (VDC_D0 through VDC_D6), VDC_DSYNC (a.k.a. !DSYNC), and a shared clock. Data is multiplexed across 4 VI clock cycles per pixel: cycle 0 carries sync data with VDC_DSYNC held low; cycles 1 through 3 carry Red, Green, and Blue, respectively. Each 4-cycle group constitutes one rendered pixel, referred to throughout as a "VI pixel."  
5. Output: The VDC-NUS (U4) performs digital-to-analog conversion, clocked by U7.FSO/5 (Frequency Synthesizer Output ÷ 5). It generates analog RGB, CSYNC (pin 14), and BFP (pin 13), passing these to the ENC-NUS (U5). The ENC-NUS receives the colorburst reference from U7.FSC (f_xtal ÷ 4) at its SCIN pin via the R13/R12 resistor divider and C21. The schematic path shows the VDC-NUS output feeding ENC-NUS (U5) on NUS-CPU-01 through 04 revisions, whereas other revisions use DENC-NUS, AVDC-NUS, or MAV-NUS to natively generate S-Video and composite[^3]. Each implementation performs the same DAC/encoding function.  

[^1]: Later revisions consolidate clock generators at U7 and U15 into a single dual-channel MX8350 at U17. f_xtal derivations are equivalent across intraregional variants; X1's frequency varies by region. The derivations in [§5](#5-mathematical-derivations) are rooted in the respective regional X1 value in each case.  

[^2]: [N64brew.dev Video DAC page](https://n64brew.dev/wiki/Video_DAC): "Since there are three unused bits in the multiplex sequence, it is unclear why the DAC has only 7 bits of precision instead of 8, and no documentation already found explains thisit is unclear why the DAC has only 7 bits of precision instead of 8, and no documentation already found explains this."  

[^3]: A notable variant uses the S-RGB A encoder, found on PAL systems marked NUS-CPU(R)-01 and sold in France. This chip is an RGB DAC, but RGB output is not functional in retail units: the RGB output circuit is unpopulated. It does not generate S-Video; consequently, NUS-001(FRA) consoles are limited to composite video output without modification. See figure *S-RGB A video circuit* (DarthCloud, 2011). This chip was used in some SNES revisions before appearing in NUS-CPU(R)-01.  

![N64 Video System](/figures/fig13_n64videosys.png)  
*N64 Video System - VDC bus multiplexing, VDC_DSYNC waveform. Source: Tim Worthington, [N64RGB documentation](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html)*  

![NUS-CPU-03 video output circuit](/figures/fig28_n64-nus-03_video_output_circuit_worthington.png)  
*NUS-CPU-03 video output circuit: VDC-NUS (U4) to ENC-NUS (U5); LUMINANCE (pin 7), COMPOSITE VIDEO (pin 9), CHROMINANCE (pin 8) outputs. Source: Tim Worthington, [GameSX Wiki, N64 RGB NTSC](https://gamesx.com/wiki/doku.php?id=av:n64rgb-ntsc)*  

> Presence of CSYNC and BFP at U4 confirms a functioning signal path from RCP through DAC to encoder; see [§3.6](#36-diagnostics) for oscilloscope verification points.  

### 3.5 Physical Variance and Stability  

The derivations in [§5](#5-mathematical-derivations) assume ideal oscillation frequency. In practice, fV proves less exact.  

#### 3.5.1 X1 Crystal Oscillator  

N64 video timings are derived from the per-region quartz crystal resonator at X1. Variance in this component therefore propagates through the timing chain.  

##### 3.5.1.1 X1 Identification  

The clock crystal (X1) has no published datasheet. The manufacturer has not been confirmed from available sources; an unverified but unchallenged theory identifies the "D" prefix near-universally observed in stamp codes with Japanese manufacturer Daishinku Corp. (Daiwa Shinku Kogyosho, a.k.a. KDS, est. 1959).  

The NUS-CPU-03 oscillator circuit presents a load capacitance of 21.5 pF + C_stray to X1, derived from C39 = C40 = 43 pF in a series configuration (See [§3.1](#31-fundamental-constants)):  

```  
CL = (C39 × C40) / (C39 + C40) + C_stray  
   = (43 × 43) / (43 + 43) + C_stray  
   = 21.5 pF + C_stray  
```  

C_stray (the aggregate parasitic capacitance from PCB traces and IC pin capacitance) cannot be determined without direct measurement. Consumer PCB oscillator layouts may be estimated in the range of 2-5 pF, implying an effective CL of approximately 23.5-26.5 pF. Available documentation does not establish whether X1 was specified for this load or whether the circuit operates outside the nominal crystal load rating.  

##### 3.5.1.2 X1 and X2 Stamp Codes by Revision (Abridged) 

The following table lists confirmed and provisional X1 and X2 stamp codes organised by board revision. X1 is the video clock crystal; X2 is not involved in video timing derivations. Both are included because their date clustering on individual boards provides independent corroboration of the decode convention. See [Appendix A](#appendix-a-x1-and-x2-stamp-code-table) for the unabridged table. See [§7.2.1](#721-personal-resources) for a link to the annotated image collection.

| Revision | X1 | X2 | X1 Date | X2 Date | Notes |  
| :--- | :--- | :--- | :--- | :--- | :--- |  
| NUS-CPU-01 | `D143A6` | `D147B6` | Jan 1996 | Feb 1996 | ID: Prominos_01 |  
| NUS-CPU-02 | `D143B6` | `D147C6` | Feb 1996 | Mar 1996 | ID: Prominos_02 |  
| NUS-CPU-03 | `D143L6` | `D147L6` | Nov 1996 | Nov 1996 | ID: Prominos_03 |  
| NUS-CPU-04 | `D143J7` | `D147J7` | Sep 1997 | Sep 1997 | ID: Prominos_04 |  
| NUS-CPU-05 | `D143L8` | `D147L8` | Nov 1998 | Nov 1998 | ID: Prominos_05 |  
| NUS-CPU-05-1 | `D143C9` | `D147C9` | Mar 1999 | Mar 1999 | ID: Prominos_05-1 |  
| NUS-CPU-06 | `D143H8` | `D147M7I` | Aug 1998 | Dec 1997 | ID: DragonsHoard_01 |  
| NUS-CPU-07 | `D143B9` | `D147A9` | Feb 1999 | Jan 1999 | ID: RetroRepairZone_01 |  
| NUS-CPU-08 | `D143H9I` | `D147H9I` | Aug 1999 | Aug 1999 | ID: Prominos_08 |  
| NUS-CPU-08-1 | `D143K9` | `D147J9` | Oct 1999 | Sep 1999 | ID: Prominos_08-1 |  
| NUS-CPU-09 | `D143J0` | `D147H0` | Sep 2000 | Aug 2000 | ID: Prominos_09 |  
| NUS-CPU-09-1 | `D143H0I` | `D147H0` | Aug 2000 | Aug 2000 | ID: Aringon_01 |  
| NUS-CPU(R)-01 | `D177G7` | `D147E7` | Jul 1997 | May 1997 | PAL, NUS-001(FRA); ID: Prominos_R01 |  
| NUS-CPU(P)-01 | `D177J7` | `D147J7` | Sep 1997 | Sep 1997 | PAL; ID: modretro_13 |  
| NUS-CPU(P)-02 | `D177J9` | `D147J9I` | Sep 1999 | Sep 1999 | PAL; ID: modretro_14 |  
| NUS-CPU(P)-03 | - | - | - | - | PAL; no board image available |  
| NUS-CPU(P)-03-1 | - | - | - | - | PAL; ID: modretro_16; 1 board image available; stamp codes illegible |  
| NUS-CPU(M)-01 | `D143G6` | `D147G6` | Jul 1996 | Jul 1996 | PAL-M; ID: grav_01 |  
| NUS-CPU(M)-02 | `ⓂD143G7` | `D147E7` | Jul 1997 | May 1997 | PAL-M; ID: JASNetInfo_01; revision inferred |  
| NUS-CPU(M)-03 | `ⓂD143M8` | `D147K9I` | Dec 1998 | Nov 1999 | PAL-M; ID: Lima112_01 |  
| NUS-CPU(M)-04 | - | - | - | - | PAL-M; no board image available |  
| NUS-CPU(M)-05 | - | - | - | - | PAL-M; no board image available |  
| NUS-CPU(M)-05-1 | `Ⓜ143G0` | `D147F0I` | Jul 2000 | Jun 2000 | PAL-M; ID: Mielke_01; `Ⓜ` marking on X1  

#### 3.5.2 X1 Oscillator Tolerance  

AT-cut crystals are standard for consumer electronics applications in the X1 frequency range. Current production equivalents specify ±30 ppm as the base grade tolerance (lidnariq), yielding a range of ±0.0018 Hz around the target values in [§2](#2-n64-video-output-summary) (e.g. NTSC progressive: [59.8243, 59.8279] Hz). GBS-C telemetry from two available NTSC N64 units corroborates:  

| Unit                             | Nickname     | Progressive (Hz)    | Interlaced (Hz)   | Offset (P)    | Offset (I)    |  
| :---                             | :---         | :---                | :---              | :---          | :---          |  
| Unit #1 (NUS-CPU-03, RGB-modded) | Daily driver | 59.82771            | 59.94166          | +26.8 ppm     | +26.7 ppm     |  
| Unit #2 (NUS-CPU-04, RGB-modded) | Junk unit    | 59.82731            | 59.94126          | +20.1 ppm     | +20.0 ppm     |  

Both fall within the predicted tolerance window. The ppm offset within each unit is essentially identical across progressive and interlaced modes, as expected: both rates derive from the same crystal. The differing offsets between units reflect normal unit-to-unit crystal variance. Aggregate second-order variance factors (temperature, aging, supply voltage) require a larger sample to characterize effectively.  

Values derived in [§5](#5-mathematical-derivations) are exact by construction, representing irreducible fractions traceable to hardware integers. The hardware itself operates within crystal tolerance. That the measurable values deviate is not a flaw in the derivation; it is the expected relationship between mathematical specification and physical implementation. GBS-C telemetry from Sony PlayStation (1994) and Sega Saturn (1994) hardware returns progressive values consistent with 2,250,000/37,609 Hz within crystal tolerance, indicating the over-determined nature of standards-compliant NTSC progressive timing: independent clock architectures converge on the same value.  

#### 3.5.3 Initialization Transient Behavior  

![MX8330MC table](/figures/fig8_mx8330MC_table.png)  
*MX8330MC Rev. E application notice illustrating feedback divider stabilization and startup transient. Source: MX8330MC datasheet*  

MX8330MC and MX9911MC clock generators require an approximately 5 millisecond stabilization period after power-on before FSO reaches steady operation and the derived VI clock domain stabilizes. This occurs during the IPL startup sequence, prior to the first visible scanline. This behavior is not accounted for in the MX8350 datasheet. 

![MX8330MC image](/figures/fig25_mx8330mc_macro_prominos.jpg)  
*MX8330MC (U7); 8-pin SOP package; lot code TEB61102. Source: Prominos (Video Game Preservation Collective Discord)*    

![MX9911MC image](/figures/fig31_MX9911MC.png)  
*MX9911MC (U7); 8-pin SOP package. Source: Prominos (Video Game Preservation Collective Discord)*  

![MX8350MC image](/figures/fig32_MX8350MC.png)  
*MX8350MC (U17); 14-pin SOP package; lot code TA022201. Source: Prominos (Video Game Preservation Collective Discord)*  

### 3.6 Diagnostics  

Nintendo diagnostic procedures (D.C.N. NUS-06-0014-001A) specify the following oscilloscope verification points for clock signal integrity:  

| Signal                      | Component | Pin  | Expected Frequency | Expected Amplitude |  
| :---                        | :---      | :--- | :---               | :---               |  
| NTSC Color Subcarrier (FSC) | U7        | 8    | 3.58 MHz           | 3.0 Vpp            |  
| NTSC Video Clock (VCLK)     | U7        | 1    | 48.68 MHz          | 3.3 Vpp            |  
| PAL Video Clock (VCLK)      | U15       | 1    | 49.66 MHz          | 3.3 Vpp            |  
| Master Clock[^4]               | U10       | 16   | 62.51 MHz          | -                  |  
| Rambus Clock (RCLK)         | U1        | 5    | 250.2 MHz          | -                  |  

[^4]: The Master Clock (62.51 MHz) is the operating clock for RCP-to-CPU communication. It is derived from the Rambus Clock (RCLK) synthesizer and is distinct from the crystal oscillator frequency (f_xtal) used in video timing derivations.  

---

## 4. Signal Analysis  

Detailed per-mode timing specifications and hardware implementation notes.  

### 4.1 Signal Parameters by Mode  

The following table defines the relationship between VI clock rate (f_vi) and the resulting display timing. See §3.1 for crystal frequencies and register values; fully reduced refresh rate fractions and line frequencies are in §3.3. Values are effective.  

| Mode    | f_vi (VI Clock)      | L (Clocks / Line) | S (Half-Lines) | fV (Refresh Rate) |  
| :---    | :---                 | :---              | :---           | :---              |  
| NTSC-P  | 48.6818181818 MHz    | 3094              | 526            | 59.8261054535 Hz  |  
| NTSC-I  | 48.6818181818 MHz    | 3094              | 525            | 59.9400599401 Hz  |  
| PAL-P   | 49.65653 MHz (exact) | 3178              | 626            | 49.9201277955 Hz  |  
| PAL-I   | 49.65653 MHz (exact) | 3178              | 625            | 50 Hz (exact)     |  
| PAL-M-P | 48.6283216783 MHz    | 3090              | 526            | 59.8370742270 Hz  |  
| PAL-M-I | 48.6283216783 MHz    | 3089              | 525            | 59.9702194092 Hz  |  

> f_vi for PAL-M is derived as exactly 6,953,850,000 ÷ 143 Hz. The slight deviation in NTSC-equivalent timing (≈ 0.0129407959%) is a hardware constraint caused by the requirement of an integer value for the Clocks ÷ Line (L) register.  

#### 4.1.1 Timing Map  

The figure below is a visualization created by lidnariq after analysis of N64 video output. The image dimensions map to signal timing for one NTSC progressive vertical scan period:  

![N64 VI Timing Diagram (NTSC-P)](/figures/fig3_n64_default_libdragon_240p_timing.png)  
*N64 VI Timing Diagram (NTSC Progressive). Source: lidnariq / ares emulator Discord, hardware probe*  

* Vertical Axis (263 units): Represents a single progressive vertical refresh. 263 sequential lines are drawn before VSYNC instructs the display's scanning mechanism to return to the top-left of the raster. Lines are contiguous, with no interleaving.  

* Horizontal Axis (774 units): Represents the number of "VI pixels" per scanline. As established in [§3.4](#34-hardware-signal-path), this quotient effectively represents VI clocks per line (L) divided by four (773.5).  

| Element | Region                 | Register                                           |  
| :---    | :---                   | :---                                               |  
| Canvas  | V_SYNC/H_SYNC boundary | `VI_V_TOTAL` and `VI_H_TOTAL` define signal limits |  
| Yellow  | Color Burst            | `VI_BURST` values; must not overlap H_START        |  
| Gray    | Active Area            | `VI_H_VIDEO` and `VI_V_VIDEO` start/end offsets    |  

> Technically, the hardware *will* allow overlap of `VI_BURST` and H_START. Doing so on a revision with a two-stage encoder/decoder configuration produces color corruption that modulates with scene content (this has not been tested on single-stage output models, e.g. MAV-NUS). See figure below.  

![VI_BURST overlapping H_START](/figures/fig22_VI_BURST-overlapping-H_START_devwizard.png)  
*`VI_BURST` overlapping H_START in Super Mario 64 (1996). Source: devwizard / N64brew.dev Discord ([youtube.com mirror](https://www.youtube.com/watch?v=hSFQPQb00ns))*  

> Relatedly, if `VI_BURST` remains active at line end, the VI randomly fails to blank the left 7 VI pixels.  

### 4.2 Mode-Specific Notes  

*Following Libultra VI macro convention (as seen in the [Animal Forest decompilation source code](https://github.com/zeldaret/af/blob/main/lib/ultralib/src/vimodes/vimodepallan1.c)), L (base) and leap values are terminal-counted and leap patterns are described in (B, A) order. See [Appendix B](#appendix-b-vi-modes) for effective values.*

#### NTSC (Progressive and Interlaced)

* Crystal frequency: 14.3181818182 MHz (315/22 MHz)
* VI clock frequency: 48.6818181818 MHz (5355/110 MHz)
* Color subcarrier: 3.5795454545 MHz (315/88 MHz)
* VI clock multiplier: 17/5 (3.4)
* Leap compensation:
1. Baseline L (terminal-counted) is `3093` (effective 3094)
2. `LEAP_B`, `LEAP_A` is `3093`, `3093` (effective 3094)
3. Pattern: 0 = `0x00` = `0b00000` = `0-0-0-0-0` = 0 (no f_H compensation applied)

#### PAL (Progressive and Interlaced)

* Crystal frequency: 17,734,475 Hz (exact)
* VI clock frequency: 49,656,530 Hz (exact)
* Color subcarrier: 4,433,618.75 Hz (exact) (17,734,475/4 Hz)
* VI clock multiplier: 14/5 (2.8)
* Leap compensation pattern #1 (SGI, e.g. *Super Mario 64* (Europe), *Goldeneye 007* (Europe)):
1. Baseline L (terminal-counted) is `3177`
2. `LEAP_B`, `LEAP_A` is `3183`, `3182`
3. Pattern #1: 21 = `0x15` = `0b10101` = `6-5-6-5-6` = 28
4. 28/5 = 5.6 average additional VI clocks per scanline

* Leap compensation pattern #2 (Nintendo, e.g., *Mario Kart 64* (Europe)[^5] and later titles):
1. Baseline L (terminal-counted) is `3177`
2. `LEAP_B`, `LEAP_A` is `3183`, `3181`
3. Pattern #2: 23 = `0x17` = `0b10111` = `6-4-6-6-6` = 28
4. 28/5 = 5.6 average additional VI clocks per scanline

#### PAL-M Progressive

* Crystal frequency: 2,045,250,000 / 143 Hz (exact) (≈ 14.3024475524 MHz)
* VI clock frequency: 6,953,850,000 / 143 Hz (exact) (≈ 48.6283216783 MHz)
* Color subcarrier: ≈ 3.5756118881 MHz
* VI clock multiplier: 17 / 5 (3.4)
* Leap compensation:

1. Baseline L (terminal-counted) is `3089`
2. `LEAP_B`, `LEAP_A` is `3097`, `3098`
3. Pattern: 4 = `0x04` = `0b00100` = `9-9-8-9-9` = 44
4. 44/5 = 8.8 average additional VI clocks per scanline

> ITU-R BT.470-6 Table 2 item 2.11a lists the M/PAL subcarrier as 3,579,611.49 Hz, which is inconsistent with the relationship defined in item 2.11b (fsc = 909/4 × fH). Applying that relationship to the System M nominal fH yields 511,312,500/143 Hz (≈ 3,575,611.888 Hz). The ITU value appears to be a transcription error propagated unchanged across multiple revisions of the standard.  

#### PAL-M Interlaced

* Crystal frequency: 2,045,250,000 / 143 Hz (exact) (≈ 14.3024475524 MHz)
* VI clock frequency: 6,953,850,000 / 143 Hz (exact) (≈ 48.6283216783 MHz)
* Color subcarrier: ≈ 3.5756118881 MHz
* VI clock multiplier: 17 / 5 (3.4)
* Leap compensation:

1. Baseline L (terminal-counted) is `3088`
2. `LEAP_B`, `LEAP_A` is `3100`, `3100`
3. Pattern: 0 = `0x00` = `0b00000` = `12-12-12-12-12` = 60
4. 60/5 = 12 additional clocks per scanline

[^5]: The osViModeTable in *Mario Kart 64* (1996/1997) seemingly documents the transition point from PAL leap pattern #1 to #2. While PAL configurations utilizing the original SGI leap pattern (`0b10101`, LEAP(`3183`, `3182`)) are present in the table, European-specific (`VERSION_EU`) modes use the revised pattern (`0b10111`, LEAP(`3183`, `3181`)). This revised leap pattern appears in later titles, including *Star Fox 64* (1997) and *The Legend of Zelda: Ocarina of Time* (1998).

*Leap sums are divided by 5 (the 5-stage leap cycle) to produce the fractional increment added to L. See [§5.2.1](#521-pal-leap-adjustment) for details on PAL leap compensation.*

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

PAL-M nominally defines fS = 227.25 × fH, but this relationship does not resolve to an integer number of VI clocks per line. The exact colorburst frequency is 3,575,611 + 127/143 Hz. The fractional component propagates through the timing derivation chain. The hardware resolves this by rounding to 3090 (progressive) or 3089 (interlaced) VI clocks per line, producing an fH of approximately 15,737.15 Hz (progressive) or 15,742.18 Hz (interlaced). These differ slightly from the NTSC standard horizontal frequency of 15,734.27 Hz. The fV values in this document are derived from the fractional colorburst frequency carried through each step; see [§5.3](#53-pal-m-derivation) for full derivation.  

> The subcarrier reference signal is delivered to the ENC-NUS encoder (U5) via the SCIN pin (pin 8), which receives the U7.FSC output through a 4.3 kΩ ÷ 820 Ω resistor divider and coupling capacitor C21. This is the hardware path by which the crystal-derived fS enters the analog encode stage. See [§3.4](#34-hardware-signal-path), figure *ENC-NUS in circuit*.  

---

## 5. Mathematical Derivations  

This section provides step-by-step derivations for all timing values. Calculations begin with hardware constants and proceed through to the final refresh rates. All quantities originate from hardware-authoritative integers; no floating-point values are used in the derivation path. All frequencies are expressed in hertz (Hz) unless otherwise noted.  

### 5.1 NTSC Derivation

Constants:

```
Color burst frequency: f_colorburst (fS) = 315/88 MHz  (≈ 3.5795454545 MHz)
Crystal frequency: f_xtal = 4 × f_colorburst = 315/22 MHz  (≈ 14.3181818182 MHz)
VI clock multiplier: M = 17 / 5
VI clocks per scanline (base): L = 3,094
Total half-lines (progressive): S_prog = 526
Total half-lines (interlaced): S_int = 525
```

Video clock frequency:

```
f_vi = f_xtal × M
     = (315/22) × (17/5) MHz
     = (315 × 17) / (22 × 5)
     = 5,355 / 110
     = 1,071 / 22  (reduced)
     ≈ 48,681,818.1818181818 Hz
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
fV_prog = fH / (S_prog / 2)
        = (2,250,000 / 143) / (526 / 2) Hz
        = (2,250,000 / 143) / 263
        = 2,250,000 / (143 × 263)
        = 2,250,000 / 37,609  (canonical value)
        ≈ 59.8261054535 Hz
```

Vertical scan frequency (interlaced):

*Interlaced: 525 half-lines per vertical scan cycle, alternating between odd and even fields.*

```
fV_int = fH / (S_int / 2)
       = (2,250,000 / 143) / (525 / 2) Hz
       = (2,250,000 × 2) / (143 × 525)
       = 4,500,000 / 75,075
       = 60,000 / 1,001  (canonical value)
       ≈ 59.9400599401 Hz
```

*Both values derive from the same colorburst root:*

```
fH      = 2,250,000 / 143 Hz  (derived above)
fV_int  = fH / (525/2) = 60,000 / 1,001      ≈ 59.9400599401 Hz
fV_prog = fH / (526/2) = 2,250,000 / 37,609  ≈ 59.8261054535 Hz
```
*The relationship between progressive and interlaced rates in NTSC (and PAL) modes is defined by the differing half-line count.*

### 5.1.1 NTSC Leap Adjustment

The NTSC configuration programs HSYNC(`3093`, `0`) and LEAP(`3093`, `3093`) (terminal-counted). 

*[§5](#5-mathematical-derivations) follows the SDK macro convention of listing LEAP_B first in these parenthetical groupings. See [Appendix B](#appendix-b-vi-modes) for tables with effective values and A, B leap sorting.*

```
L_base = 3,094  VI clocks per scanline, base
LEAP_B = 3,094  effective  (register value 3,093 + 1)
LEAP_A = 3,094  effective  (register value 3,093 + 1)
```

Pattern `0x00` (`0b00000`) selects the LEAP_A on every VSYNC. As LEAP_A = L_base, every VSYNC is uniform. The `VI_H_TOTAL_LEAP` register produces no correction. fH is therefore exact from L alone, with no leap adjustment required.

*This contrasts with PAL-M interlaced, which also programs pattern `0x00` with LEAP_A = LEAP_B, but with both values set above L_base. See [§5.3.2.1](#5321-pal-m-interlaced-leap-adjustment).*

---

### 5.2 PAL Derivation

Constants:

```
Color burst frequency: f_colorburst (fS) = 17,734,475 / 4 Hz  (= 4.43361875 MHz)
Crystal frequency: f_xtal = 4 × f_colorburst = 17,734,475 Hz  (= 17.734475 MHz)
VI clock multiplier: M = 14 / 5
VI clocks per scanline: L = 3,178
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

*Without leap compensation, the theoretical line frequency would be:*

```
fH (theoretical) = f_vi / L
                 = 49,656,530 / 3,178 Hz
                 = 24,828,265 / 1,589  (reduced)
                 ≈ 15,625.0881057269 Hz
```

*Under the LEAP register mapping described in §5.2.1.1, the hardware compensates for this error by adding fractional VI clocks during VSYNC, yielding an exact line frequency of 15,625 Hz.*

```
fH = 15,625 / 1 Hz  (canonical value)
   = 15,625 Hz  (exact)
```

Vertical scan frequency (progressive):

```
fV_prog = fH / (S_prog / 2)
        = 15,625 / (626 / 2) Hz
        = 15,625 / 313  (canonical value)
        ≈ 49.9201277955 Hz
```

Vertical scan frequency (interlaced):

```
fV_int = fH / (S_int / 2)
       = 15,625 / (625 / 2) Hz
       = (15,625 × 2) / 625
       = 31,250 / 625
       = 50 / 1  (canonical value)
       = 50 Hz  (exact)
```

### 5.2.1 PAL Leap Adjustment

The N64 VI maintains the exact 15,625 Hz line frequency (fH) required for the PAL standard. The uncompensated line period (L = 3,178) produces a theoretical frequency of 49,656,530 / 3,178 ≈ 15,625.0881 Hz. To achieve the standard, the average number of VI clocks per line must be exactly:

```
L_avg = f_vi / fH = 49,656,530 / 15,625 = 9,931,306 / 3,125
```

The hardware corrects for the 56/3,125 fractional error using the leap mechanism, which adds an average of 28/5 VI clocks per VSYNC. For PAL interlaced (S = 625), the average adjustment per line is therefore:

```
Leap adjustment per line = (28/5) / (S/2) = (28/5) / (625/2) = 56/3,125 VI clocks
```

The true average line length is the sum of the base line length and this leap adjustment. This confirms that the hardware mechanism exactly matches the required theoretical value:

```
True L_avg = 3,178 + 56/3,125 = (9,931,250 + 56) / 3,125 = 9,931,306 / 3,125
```

The leap mechanism is implemented via the `VI_H_TOTAL_LEAP` register (`0x04400020`). A repeating 5-VSYNC sequence alternates between two extended line lengths during the vertical blanking interval, yielding the required 28/5-clock average per VSYNC. See [§5.2.1.1](#5211-pal-leap-pattern-and-bit-mapping).

```
fH = f_vi / (L + (28/5) / (S/2))
   = f_vi / (L + 56/3,125)
   = 49,656,530 / (9,931,306 / 3,125)
   = (49,656,530 / 9,931,306) × 3,125
   = 5 × 3,125
   = 15,625 Hz  (exact)
```

### 5.2.1.1 PAL Leap Pattern and Bit Mapping

At least two distinct PAL leap configurations appear across the N64 production run. This leap pattern change coincides with OS2.0 revision H (released February 24, 1997). 

*Super Mario 64* (1996):  

```
HSYNC(3177, 21)  ->  L_base = 3178,  pattern = 0b10101
LEAP(3183, 3182) ->  LEAP_B (effective) = 3184 (+6), LEAP_A (effective) = 3183 (+5)

Bit pattern applied:
slot 1 (1) -> LEAP_B: +6
slot 2 (0) -> LEAP_A: +5
slot 3 (1) -> LEAP_B: +6
slot 4 (0) -> LEAP_A: +5
slot 5 (1) -> LEAP_B: +6

Total extra over 5-VSYNC cycle: 6 + 5 + 6 + 5 + 6 = 28
Average per VSYNC: 28 / 5
```

*Animal Forest* (*どうぶつの森*, *Dōbutsu no Mori*) (2001):  

```
HSYNC(3177, 23)  ->  L_base = 3178,  pattern = 0b10111
LEAP(3183, 3181) ->  LEAP_B (effective) = 3184 (+6), LEAP_A (effective) = 3182 (+4)

Bit pattern applied:
slot 1 (1) -> LEAP_B: +6
slot 2 (1) -> LEAP_B: +6
slot 3 (1) -> LEAP_B: +6
slot 4 (0) -> LEAP_A: +4
slot 5 (1) -> LEAP_B: +6

Total extra over 5-VSYNC cycle: 6 + 6 + 6 + 4 + 6 = 28
Average per VSYNC: 28 / 5
```

The average is identical. The fH derivation in [§5.2](#52-pal-derivation) therefore holds for both configurations:

```
Leap adjustment per line = (28/5) / (S/2)
                              = (28/5) / (625/2)
                              = 56 / 3,125

L_avg = 3,178 + 56/3,125
      = (9,931,250 + 56) / 3,125
      = 9,931,306 / 3,125

fH = f_vi / L_avg
   = 49,656,530 / (9,931,306 / 3,125)
   = (49,656,530 × 3,125) / 9,931,306
   = 155,176,656,250 / 9,931,306
   = 15,625 Hz  (exact)
```

The timing result is unchanged regardless of pattern used; only the distribution of additions within the 5-VSYNC cycle differs. It is not currently understood why the pattern was updated in later revisions of the SDK. 

---

### 5.3 PAL-M Derivation

Constants:

```
Color burst frequency: f_colorburst (fS) = 511,312,500 / 143 Hz  (≈ 3,575,611.8881118881 Hz)
Crystal frequency: f_xtal = 4 × f_colorburst = 2,045,250,000 / 143 Hz  (≈ 14,302,447.5524475524 Hz)
VI clock multiplier: M = 17 / 5
Total lines (progressive): S_prog = 526
Total lines (interlaced): S_int = 525
```

Video clock frequency:

```
f_vi = f_xtal × M
     = (2,045,250,000 / 143) × (17 / 5) Hz
     = (2,045,250,000 × 17) / (143 × 5)
     = 34,769,250,000 / 715
     = 6,953,850,000 / 143  (canonical value)
     ≈ 48,628,321.6783216783 Hz 
     ≈ 48.6283216783 MHz
     
```

### 5.3.1 PAL-M Progressive Derivation

```
VI clocks per line (base): L_base = 3,090
```

*Without leap compensation, the theoretical line frequency would be:*

```
fH (theoretical) = f_vi / L_base
                 = (6,953,850,000 / 143) / 3,090 Hz
                 = 6,953,850,000 / (143 × 3,090)
                 = 6,953,850,000 / 441,870
                 = 1,158,975,000 / 73,645  (reduced)
                 ≈ 15,737.0621468927 Hz
```

*The LEAP register (partially) compensates for this error. See §5.3.1.1.*

```
fH = 4,572,156,375,000 / 290,532,671  (canonical value)
   ≈ 15,737.1505217050 Hz
```

Vertical scan frequency (progressive):

```
fV_prog = fH / (S_prog / 2)
        = (4,572,156,375,000 / 290,532,671) / (526 / 2) Hz
        = (4,572,156,375,000 / 290,532,671) / 263
        = 4,572,156,375,000 / (290,532,671 × 263)
        = 4,572,156,375,000 / 76,410,092,473
        = 17,384,625,000 / 290,532,671  (canonical value)
        ≈ 59.8370742270 Hz
```

### 5.3.1.1 PAL-M Progressive Leap Adjustment

The PAL-M progressive configuration programs HSYNC(`3089`, `4`) and LEAP(`3097`, `3098`). Terminal-counted:

```
L_base = 3,090  VI clocks per line, base
LEAP_B = 3,098  effective  (register value 3,097 + 1)
LEAP_A = 3,099  effective  (register value 3,098 + 1)
```

The bit mapping established in [§5.2.1.1](#5211-pal-leap-pattern-and-bit-mapping) applies. Pattern `0x04` (`0b00100`):

```
slot 1 (0) -> LEAP_A: +9
slot 2 (0) -> LEAP_A: +9
slot 3 (1) -> LEAP_B: +8
slot 4 (0) -> LEAP_A: +9
slot 5 (0) -> LEAP_A: +9

Total extra over 5-VSYNC cycle: 4 × 9 + 1 × 8 = 44
Average extra per VSYNC: 44 / 5
```

```
Leap adjustment per line = (44/5) / (S_prog / 2)
                              = (44/5) / (526 / 2)
                              = (44/5) / 263
                              = 44 / 1,315

L_avg = 3,090 + 44/1,315
      = (3,090 × 1,315 + 44) / 1,315
      = (4,063,350 + 44) / 1,315
      = 4,063,394 / 1,315

fH = f_vi / L_avg
   = (6,953,850,000 / 143) / (4,063,394 / 1,315)
   = (6,953,850,000 × 1,315) / (143 × 4,063,394)
   = 9,144,322,500,000 / 581,065,342
   = 4,572,156,375,000 / 290,532,671  (canonical value)
   ≈ 15,737.1505217050 Hz
```

---

### 5.3.2 PAL-M Interlaced Derivation

```
VI clocks per line (base): L_base = 3,089
```

*Without leap compensation, the theoretical line frequency would be:*

```
fH (theoretical) = f_vi / L_base
                 = (6,953,850,000 / 143) / 3,089 Hz
                 = 6,953,850,000 / (143 × 3,089)
                 = 6,953,850,000 / 441,727  (reduced)
                 ≈ 15,742.6271626032 Hz
```

*The LEAP register (partially) compensates for this error. See [§5.3.2.1](#5321-pal-m-interlaced-leap-adjustment).*

```
fH = 71,583,750,000 / 4,547,257  (canonical value)
   ≈ 15,742.1825949138 Hz
```

Vertical scan frequency (interlaced):

```
fV_int = fH / (S_int / 2)
       = (71,583,750,000 / 4,547,257) / (525 / 2) Hz
       = (71,583,750,000 × 2) / (4,547,257 × 525)
       = 143,167,500,000 / 2,387,309,925
       = 272,700,000 / 4,547,257  (canonical value)
       ≈ 59.9702194092 Hz
```

### 5.3.2.1 PAL-M Interlaced Leap Adjustment

The PAL-M interlaced configuration programs HSYNC(`3088`, `0`) and LEAP(`3100`, `3100`). Terminal-counted: 

```
L_base = 3,089  VI clocks per line, base
first  = 3,101  effective  (register value 3,100 + 1)
second = 3,101  effective  (register value 3,100 + 1)
```

Pattern `0x00` (`0b00000`) (Always use LEAP_A) sets LEAP_A to extend one line per VSYNC by 12 VI clocks unconditionally.

```
Extra clocks per VSYNC: 3,101 - 3,089 = 12
```

```
Leap adjustment per line = 12 / (S_int / 2)
                              = 12 / (525 / 2)
                              = 24 / 525
                              = 8 / 175

L_avg = 3,089 + 8/175
      = (3,089 × 175 + 8) / 175
      = (540,575 + 8) / 175
      = 540,583 / 175

fH = f_vi / L_avg
   = (6,953,850,000 / 143) / (540,583 / 175)
   = (6,953,850,000 × 175) / (143 × 540,583)
   = 1,216,923,750,000 / 77,303,369
   = 71,583,750,000 / 4,547,257  (canonical value)
   ≈ 15,742.1825949138 Hz
```
---

## 6. Conversion Reference  

This section provides practical conversion matrices, most commonly for the purpose of speedrun timing comparison. The aim is to ease synchronization (thus, subsequent comparative analysis) of realtime speedruns recorded across regional hardware.  

These multipliers assume game logic is bound to video refresh rate (fV), and that the NTSC-to-PAL performance ratio corresponds exactly with the fV ratio. Under those conditions, a longer duration recorded on PAL hardware directly corresponds to a shorter equivalent time on NTSC hardware, and vice versa.  

> When comparing RTA (Real-Time Attack, speedruns measured in realtime) runs recorded at separate refresh rates, questions invariably arise regarding relative degree of difficulty. This document does not seek to provide judgment on the parity of conversion for any given software title.  

The conversion ratios described in this section assume signal homogeneity per source. However, some games switch between progressive and interlaced modes. No single conversion factor is perfectly accurate in such cases. The theoretically correct method (frame-counted weighted average) is largely impractical. One hypothetical compromise: game-specific approximate weighted multipliers based on reasonably representative sample ratios of signal prevalence.  

### 6.1 Approximate Decimal Conversions

For general conversions.

| From \ To | NTSC-P  | NTSC-I  | PAL-P   | PAL-I   | PAL-M-P | PAL-M-I |  
| :---      | :---    | :---    | :---    | :---    | :---    | :---    |  
| NTSC-P    | 1.00000 | 0.99810 | 1.19844 | 1.19652 | 0.99982 | 0.99760 |
| NTSC-I    | 1.00190 | 1.00000 | 1.20072 | 1.19880 | 1.00172 | 0.99950 |
| PAL-P     | 0.83442 | 0.83283 | 1.00000 | 0.99840 | 0.83427 | 0.83242 |
| PAL-I     | 0.83576 | 0.83417 | 1.00160 | 1.00000 | 0.83560 | 0.83375 |
| PAL-M-P   | 1.00018 | 0.99828 | 1.19866 | 1.19674 | 1.00000 | 0.99778 |
| PAL-M-I   | 1.00241 | 1.00050 | 1.20132 | 1.19940 | 1.00223 | 1.00000 |

### 6.2 Exact Fractional Conversions  

For mathematically precise conversions. Fractions are fully reduced and traceable to the canonical values in [§2](#2-n64-video-output-summary).  

| From \ To | NTSC-P          | NTSC-I          | PAL-P               | PAL-I               | PAL-M-P               | PAL-M-I           |
| :---      | :---            | :---            | :---                | :---                | :---                  | :---              |
| NTSC-P    | 1/1             | 526/525         | 37609/45072         | 37609/45000         | 4064139/4063394       | 159378/158995     |
| NTSC-I    | 525/526         | 1/1             | 25025/30048         | 1001/1200           | 8112825/8126788       | 31815/31799       |
| PAL-P     | 45072/37609     | 30048/25025     | 1/1                 | 626/625             | 348248808/290532671   | 27313632/22736285 |
| PAL-I     | 45000/37609     | 1200/1001       | 625/626             | 1/1                 | 347692500/290532671   | 5454000/4547257   |
| PAL-M-P   | 4063394/4064139 | 8126788/8112825 | 290532671/348248808 | 290532671/347692500 | 1/1                   | 8126788/8108745   |
| PAL-M-I   | 158995/159378   | 31799/31815     | 22736285/27313632   | 4547257/5454000     | 8108745/8126788       | 1/1               |

---

## 7. Sources  

### 7.1 Figures (TODO: Needs updating) 

| Figure | Filename | Description (Source) |  
| :--- | :--- | :--- |  
| NUS-CPU-01 Motherboard | `fig35_NUS-CPU-01_Prominos.jpg` | *Nintendo 64 motherboard (NUS-CPU-01 revision) showing the Reality Coprocessor and system layout (Source: Prominos, photographed hardware board image, [imgur.com](https://imgur.com/a/YpyuRET)).* |
| US6331856 | `fig34_US6331856-pp46-47.png` | *Nintendo 64 Video Interface (VI) register layout showing control, sync timing, video window, burst, and scaling registers (Source: [U.S. Patent 6,331,856](https://patents.google.com/patent/US6331856B1/en), sheets 46-47).* |
| Clock Generation Circuits | `fig1_clock_gen_schematic.png` | *N64 Clock Generation Circuits - U7 (NTSC/PAL-M) and U15 (PAL) (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| MX8350 Table | `fig6_mx8350_table.png` | *MX8350 output frequencies for NTSC/PAL/MPAL configurations (Source: [MX8350 datasheet](/references/Macronix-MX8350-ocr.pdf))* |  
| RCP-NUS in Circuit | `fig2_rcp_schematic.png` | *RCP-NUS Pinout showing VDC (Video Digital Complex) Timing Outputs (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| VDC Schematic Detail | `fig9_rcp_vdc_schematic.png` | *Video Digital Complex (VDC) pin assignments showing 7-bit digital video output (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| N64 Video System | `fig13_n64videosys.png` | *N64 Video System - 4-cycle VDC bus protocol, VDC_DSYNC waveform, and byte contents (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| VDC-NUS in Circuit | `fig18_VDC-NUS.png` | *VDC-NUS (BU9801F, U4) in circuit - digital input side and analog output stage (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| ENC-NUS in Circuit | `fig17_ENC-NUS.png` | *ENC-NUS (U5) in circuit - YOUT (luma/S-Video Y) and VOUT (composite video) outputs; SCIN subcarrier input via R13/R12 divider (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| NUS-CPU-03 Video Output Circuit | `fig28_n64-nus-03_video_output_circuit_worthington.png` | *NUS-CPU-03 video output circuit: VDC-NUS (U4, BU9801F) to ENC-NUS (U5); R13/R12 divider; RGB output resistors; LUMINANCE/COMPOSITE/CHROMINANCE outputs (Source: Tim Worthington, GameSX Wiki, N64 RGB NTSC, [gamesx.com](https://gamesx.com/wiki/doku.php?id=av:n64rgb-ntsc))* |
| VDC-NUS Pinout | `fig14_vdc-nus.png` | *VDC-NUS (BU9801F) pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| DENC-NUS Pinout | `fig15_denc-nus.png` | *DENC-NUS pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| MAV-NUS Pinout | `fig16_mav-nus.png` | *MAV-NUS pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| MX8330MC Table | `fig8_mx8330MC_table.png` | *MX8330MC Rev. E application notice illustrating feedback divider stabilization and startup transient (Source: [MX8330MC datasheet](/references/Macronix-MX8330MC-ocr.pdf))* |  
| MX8330MC Image | `fig25_mx8330mc_macro_prominos.jpg` | *MX8330MC (U7); 8-pin SOP package; lot code TEB61102 (Source: Prominos, Video Game Preservation Collective Discord, [imgur.com](https://imgur.com/a/YpyuRET))* |  
| MX9911MC Image | `fig31_MX9911MC.png` | *MX9911MC (U7); 8-pin SOP package; chamfered corner pin-1 indicator (Source: Prominos, Video Game Preservation Collective Discord, [imgur.com](https://imgur.com/a/YpyuRET))* |  
| MX8350MC Image | `fig32_MX8350MC.png` | *MX8350MC (U17); 14-pin SOP package; lot code TA022201 (Source: Prominos, Video Game Preservation Collective Discord, [imgur.com](https://imgur.com/a/YpyuRET))* |  
| N64 VI Timing Diagram (NTSC-P) | `fig3_n64_default_libdragon_240p_timing.png` | *N64 VI Timing Diagram (NTSC Progressive) (Source: lidnariq via ares emulator Discord server; [reverse-engineered via hardware probing](/figures/fig3_n64_default_libdragon_240p_timing.png))* |  
| VI_BURST Overlapping H_START | `fig22_VI_BURST-overlapping-H_START_devwizard.png` | *`VI_BURST` overlapping H_START (Source: devwizard / N64brew.dev Discord [youtube.com mirror](https://youtu.be/hSFQPQb00ns))*  |  
| S-RGB A SNES | `fig33_S-RGB_A-SNS.png` | *ROHM BA6596F (S-RGB A) at U7 on SNS-CPU-RGB-01 (Source: SNES Model Differences, [consolemods.org](https://consolemods.org/wiki/SNES:SNES_Model_Differences))* |
| `Ⓜ` and `D` Markings | `fig24_X1_(M)D143G7_stamp_code.png` | *Both `Ⓜ` and `D` prefixes visible on a single PAL-M marking (Source: JASNet Soluções em Eletrônica, [Instalação do RGB Converter v2 no Nintendo 64](https://www.jasnetinfo.com/produtos/rgbconvv2/install/install_nintendo64.php))* |  
| `Ⓜ` Marking | `fig23_X1_(M)143G0_stamp_code.png`  | *`Ⓜ` marking visible on some PAL-M X1 crystal resonators (Source: Mielke - MiSTer FPGA Discord, [imgur.com](https://imgur.com/a/SjqcjYj))* |  
| Raster Scan | `fig29_raster_scan_progressive_ian_harvey.png` | *Progressive raster scan: electron beam traversal, horizontal retrace, and vertical retrace (Source: Ian Harvey, Wikimedia Commons, [CC0](https://commons.wikimedia.org/wiki/File:Raster-scan.svg))* |  
| S-RGB A Video Circuit | `fig36_snes_video_path_v3.png` | *S-RGB A (U7) video circuit: RGB inputs from S-PPU2; discrete transistor drive stage; RGB, LUMA, C.VIDEO, and CHROMA outputs (Source: DarthCloud, SNS-CPU-RGB-02 Video Circuit, 2011, [assemblergames.org](https://assemblergames.org/viewtopic.php?t=43494))* |  

### 7.2 References

* [Nintendo 64 Online Manuals (OS 2.0L, v5.2)](https://ultra64.ca/files/documentation/online-manuals/man-v5-2/allman52/) - Hardware behavior; VI implementation details.  
* [Nintendo 64 Online Manuals - Functions Reference Manual (OS 2.0I)](https://ultra64.ca/files/documentation/online-manuals/functions_reference_manual_2.0i/home.html) - VI register mappings; programmable timing.  
* [Nintendo 64 Online Manuals - Programming Manual (OS 2.0J)](https://ultra64.ca/files/documentation/online-manuals/man/pro-man/start/index.html) - Memory-mapped I/O; VI mode definitions; system programming reference.  
* [Nintendo 64 Programming Manual (D.C.N. NUS-06-0030-001 REV G)](https://ultra64.ca/files/documentation/nintendo/Nintendo_64_Programming_Manual_NU6-06-0030-001G_HQ.pdf) - Detailed timing tables.  
* [Nintendo 64 System Service Manual (D.C.N. NUS-06-0014-001 REV A)](https://drive.google.com/drive/folders/1kGlB2TyX7CsmPnSyzpxGcSKpJ1F-ywal) - Block diagrams; boot sequence; oscilloscope timing verification.  
* [Super Mario 64 Decompilation - osVITable.c (GitHub)](https://github.com/n64decomp/sm64/blob/9921382a68bb0c865e5e45eb594d9c64db59b1af/lib/src/osViTable.c) - Early libultra-defined Video Interface configurations.
* [Mario Kart 64 Decompilation - osVITable.c (GitHub)](https://github.com/n64decomp/mk64/blob/3b794dcce90543c2203ca2006eb77a41af49c05e/src/os/osViTable.c) - Transitional libultra-defined Video Interface configurations.  
* [Animal Forest Decompilation - vitbl.c (GitHub)](https://github.com/Kelebek1/af/blob/770d3c2dca047172c7b947c83f136468cb0dc7e0/lib/ultralib/src/io/vitbl.c) - Later libultra-defined Video Interface configurations.
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
* [US6331856B1 - Video Game System with Coprocessor](https://patents.google.com/patent/US6331856B1/en) (2001) - VI register architecture; HSYNC LEAP register with LEAP_A/LEAP_B fields; interlaced display field toggling; clock generator crystal timing chain.  
* [US6556197B1 - Programmable Video Timing Registers](https://patents.google.com/patent/US6556197B1/en) (2003) - Horizontal/vertical sync generation; color burst gate timing.  
* [F. R. Lack, G. W. Willard, I. E. Fair - Some Improvements in Quartz Crystal Circuit Elements](https://ieeexplore.ieee.org/document/6772950) (1934) - AT cut crystal oscillator properties.  
* [Ian Poole - Electronics Notes - Quartz Crystal Cuts: AT, BT, SC, CT](https://www.electronics-notes.com/articles/electronic_components/quartz-crystal-xtal/crystal-resonator-cuts-at-bt-sc-ct.php) - AT cut crystal properties; temperature coefficient; frequency range; thickness shear mode of vibration.  
* [RWeick - NUS-CPU-03-Nintendo-64-Motherboard (GitHub)](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard) - Complete NUS-CPU-03 KiCAD schematic; component values; signal paths.  
* [Tim Worthington - GamesX Wiki - N64 RGB NTSC](https://gamesx.com/wiki/doku.php?id=av:n64rgb-ntsc) - NUS-CPU-03 video output circuit schematic by Tim Worthington; corroborates YOUT/VOUT/COUT routing to Multi-AV connector.  
* [Tim Worthington - N64RGB Page](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html) - 4-cycle VDC bus protocol diagram and DAC pinouts.  
* [Rodrigo Copetti - Nintendo 64 Architecture - A Practical Analysis](https://www.copetti.org/writings/consoles/nintendo-64/) - High-level hardware overview; encoder revision corroboration.  
* [Zoinkity - VI Settings Pastebin](https://web.archive.org/web/20260119215039/https://pastebin.com/pJG5SBnW) - 237/474 line libultra behavior; VI reverse-engineering details.  
* [Link83 et al - ModRetro Forums - N64 Motherboard Revisions](https://forums.modretro.com/threads/nintendo-64-motherboard-revisions-serials-info-request.1417/) - Motherboard revision history; component changes; video encoder chip progression across revisions; board scans; corroboration of AVDC-NUS/MAV-NUS pin-compatibility per examples of both observed on NUS-CPU-05.  
* [kwyjibo, Link83 et al - NFGGames Forum - NUS-CPU(R)-01 Discussion](https://nfggames.com/forum2/index.php?topic=3083.0) - Community documentation of the French PAL console, NUS-CPU(R)-01 board, and S-RGB A encoder.  
* [Link83 et al - NFGGames Forum - Datasheet Links Thread](https://nfggames.com/forum2/index.php?topic=3525.0) - Community identification of BA7242F as ENC-NUS match; source of datasheet link.  
* [RDC, aflyingcougar et al](https://forums.modretro.com/threads/schematic-nus-cpu-04-ntsc-1996-1997.11227/) - NUS-CPU-03/04 schematics and board photos (RDC); identification of Mitsumi PST9128 at U3 (aflyingcougar).
* [QUAKEMASTER - N64 RGB Mod Guide (German)](https://web.archive.org/web/20130130062716/http://free-for-all.ath.cx:80/daten/n64rgbmod.html) - Identification of NUS-CPU(R)-01 motherboard; S-RGB A pinout documentation.  
* [N64brew.dev](https://n64brew.dev/) - VI register descriptions and behavior; timing examples; leap explanation; OS interface functions for VI and hardware access.  
* [Libdragon](https://libdragon.dev/) - Modernized open-source SDK; numerous implementation details.  
* [Libdragon - vi.h](https://github.com/DragonMinded/libdragon/blob/c4f1d72a8a93e4e4426c19c1967a6426afcdf279/src/vi.h) - Video Interface Subsystem information.
* [Libdragon - display.h](https://github.com/DragonMinded/libdragon/blob/c4f1d72a8a93e4e4426c19c1967a6426afcdf279/include/display.h) - VI -> RDP hardware rasterizer details.
* [pseultra](https://github.com/pseudophpt/pseultra) / [hkz-libn64](https://github.com/mark-temporary/hkz-libn64) / [n64dev](https://sourceforge.net/projects/n64dev/) - Open-source SDK implementations; VI handling abstraction.  
* [n64.readthedocs.io - N64 Hardware Reference](https://n64.readthedocs.io/index.html#video-interface) - Emulator developer reference; SDK register naming corroboration; interrupt handling detail.  
* [ares - N64](https://github.com/ares-emulator/ares/tree/master/ares/n64) / [CEN64](https://github.com/n64dev/cen64) / [MAME N64](https://github.com/mamedev/mame/blob/master/src/mame/nintendo/n64.cpp) - Software implementations of VI timing.  
* [Robert Peip et al - MiSTer FPGA N64 Core](https://github.com/MiSTer-devel/N64_MiSTer) - FPGA implementation of N64 VI timing; corroboration of NTSC 237/474 libultra bounds via Clean HDMI function.  
* [Wikipedia - NTSC](https://en.wikipedia.org/wiki/NTSC) / [PAL](https://www.wikipedia.org/wiki/PAL) / [PAL-M](https://www.wikipedia.org/wiki/PAL-M) - Broadcast standard overviews.  
* [Mike Wooding - ATV Compendium (BATC)](https://batc.org.uk/wp-content/uploads/ATVCompendium.pdf) - PAL-M fS = 227.25 × fH relationship.  
* [Martin Hinner - VGA/PAL](https://martin.hinner.info/vga/pal.html) - PAL video timing specification (sourced from R. Salmon, sci.engr.television.broadcast, 1996).  
* [Alan Pemberton - World TV Standards](https://web.archive.org/web/20160512200958/http://www.pembers.freeserve.co.uk/World-TV-Standards/) - Detailed information on broadcast standards; HBI and VBI visualizations.  
* [David - EEVblog Forums - Nintendo 64 Game Console Teardown](https://www.eevblog.com/forum/blog/eevblog-491-nintendo-64-game-console-teardown/25/) - Chip progression by board revision; AVDC-NUS RGB tap rationale; AVDC-NUS/MAV-NUS shared pinout observation.  

* [JASNet Soluções em Eletrônica - Instalação do RGB Converter v2 no Nintendo 64 (Portuguese)](https://www.jasnetinfo.com/produtos/rgbconvv2/install/install_nintendo64.php) - NUS-CPU(M)-02 candidate board; `ⓂD143G7`/`D147E7`; `Ⓜ` marking on X1.  
* [Prominos - N64 Motherboard Images](https://imgur.com/a/YpyuRET) - Collection of high quality N64 motherboard images including rare NUS-CPU(R)-01 model, shared by Prominos (Video Game Preservation Collective Discord).
* [Mielke - NUS-CPU(M)-05-1 Images](https://imgur.com/a/SjqcjYj) - Photos of rare PAL-M model, shared by Mielke (MiSTer FPGA Discord).
* [grav - NUS-CPU(M)-01 Images](https://imgur.com/a/fD0AuBj) - Photos of rare PAL-M model, shared by grav (Discord64 Discord).
* [Aringon - NUS-CPU-09-1 Images](https://imgur.com/a/yfoPbqS) - Photos of rare 09-1 model, shared by Aringon (Video Game Preservation Collective Discord).
* [Console Mods - SNES Model Differences](https://consolemods.org/wiki/SNES:SNES_Model_Differences) - Confirmation of S-RGB A usage in some SNES models via board photos.

![S-RGB A SNES](/figures/fig33_S-RGB_A-SNS.png)  
*ROHM BA6596F (S-RGB A) at U7 on SNS-CPU-RGB-01 (Source: SNES Model Differences, [consolemods.org](https://consolemods.org/wiki/SNES:SNES_Model_Differences))*

#### 7.2.1 Personal Resources

* [N64 Motherboard Images Collection](https://imgur.com/a/B4uPSNF) - Collection of N64 motherboard images with source links. Some boards are damaged, trimmed, modified, or otherwise altered.

### 7.3 Acknowledgements

* [A post by awe444 on videogameperfection.com](https://videogameperfection.com/forums/topic/nintendo-64-de-blur/page/2/#post-12502) for the initial spark of curiosity.  
* lidnariq for PAL-M colorburst correction (§5.3), VDC_DSYNC behavior analysis (§3.2, §3.4), ±30 ppm crystal tolerance figure (§3.5.2), month decode suggestion (§3.5.1.2), VI timing map (Figure 3), several minor corrections, and extensive audits.  
* devwizard for sharing experimental observations of dynamic chroma modulation and left-pixel blanking failure under `VI_BURST` / H_START overlap (§4.1.1).  
* Robert Peip (FPGAzumSpass) for auditing and corroboration of `VI_V_CURRENT` behaviour.  
* Rasky for cross-referencing register naming against N64brew convention.  
* kev4cards for several research leads, refinement, and general auditing.  
* grav, Mielke, Prominos, and Aringon for sharing motherboard images including rare PAL-M, NUS-001(FRA), and NUS-CPU-09-1 examples.

---

## Appendix A. X1 and X2 Stamp Code Table

### A.1 Stamp Code Format

X1 and X2 stamp codes follow the format `(P)(D)FFFMY(I)`, where:  

| Field | Description                                                                               |  
| :---  | :---                                                                                      |  
| `P`   | Always `Ⓜ`. Only yet observed on some PAL-M units[^6]                                        |  
| `D`   | Always `D`[^7]                                                                               |  
| `FFF` | Frequency in abbreviated MHz (e.g. `143` = 14.3 MHz, `147` = 14.7 MHz, `177` = 17.7 MHz)  |  
| `M`   | Month of manufacture (`A`-`M`, skipping `I`. `A`: January; through `M`: December)         |  
| `Y`   | Last digit of year of manufacture (e.g. `6` = 1996, `0` = 2000)                           |  
| `I`   | Always `I`. Uncommon; appears without obvious pattern; meaning not established            |  

The I-skip in the month field is a noted date code convention, where `I` is omitted to avoid ambiguity with numeral `1`. The `I` character is observed as suffix on some codes after an otherwise complete code (e.g. `D143L6I`, `D147J9I`, `D143K9I`, `D147F0I`); its meaning is not known. It appears across X1 and X2 independently, across multiple revisions and years, with no observable clustering by revision, region, or date.  

The decode convention is consistent across all three regional crystal frequencies (14.3 MHz, 14.7 MHz, 17.7 MHz) and across the full known production span of the hardware (1996-2000).   

[^6]: The meaning of the circular-M (`Ⓜ`) marking observed on some PAL-M boards is unconfirmed. One plausible expansion is an `M`PAL-specific marking (using an available glyph) applied to distinguish these X1 units from NTSC X1 crystals, as they otherwise appear identical (e.g. `D143K7` could be either NTSC or PAL-M, whereas the presence of `Ⓜ` disambiguates).   

[^7]: Near-universal presence. `D` prefix missing in a single observed CPU-NUS-(M)-05-1 example across entire board corpus. On said PAL-M X1, `Ⓜ` is seemingly marked *in place of* `D`.  

![`Ⓜ` marking](/figures/fig23_X1_(M)143G0_stamp_code.png)  
*`Ⓜ` marking visible on some PAL-M X1 crystal resonators. Source: Mielke - MiSTer FPGA Discord ([imgur.com](https://imgur.com/a/mielke-board-photos-SjqcjYj))*  

![`Ⓜ` and `D` markings](/figures/fig24_X1_(M)D143G7_stamp_code.png)  
*Both `Ⓜ` and `D` prefixes visible on a single PAL-M marking. Source: JASNet Soluções em Eletrônica, [Instalação do RGB Converter v2 no Nintendo 64](https://www.jasnetinfo.com/produtos/rgbconvv2/install/install_nintendo64.php)*  

#### A.2 X1 and X2 Stamp Codes by Revision (Full)  

| Revision | X1 | X2 | X1 Date | X2 Date | Notes |  
| :--- | :--- | :--- | :--- | :--- | :--- |  
| NUS-CPU-E7I | `D143A6` | `D147A6` | Jan 1996 | Jan 1996 | ID: KontrolledKhaos_01; non-retail engineering sample unit
| NUS-CPU-01 | `D143A6` | `D147B6` | Jan 1996 | Feb 1996 | ID: Prominos_01 *(Initial configuration: CPU-NUS; RCP-NUS; 2x RDRAM18-NUS A; VDC-NUS; ENC-NUS; BU9480F; AMP-NUS; 2x MX8330MC; Sharp PQ7VZ5 (marking: `7VZ5`); TI SN74LVC125 (marking: `LC125`))* |  
| NUS-CPU-01 | `D143B6` | `D147B6` | Feb 1996 | Feb 1996 | [Photo by Yaca2671, CC BY-SA 3.0 (Wikimedia)](https://commons.wikimedia.org/w/index.php?curid=5777930) |
| NUS-CPU-01 | `D143B6` | `D147B6` | Feb 1996 | Feb 1996 | ID: modretro_01 |  
| NUS-CPU-02 | `D143B6` | `D147C6` | Feb 1996 | Mar 1996 | ID: Prominos_02 |  
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
| NUS-CPU-05-1 | `D143L8` | `D147K8` | Nov 1998 | Oct 1998 | |
| NUS-CPU-05-1 | `D143C9` | `D147C9` | Mar 1999 | Mar 1999 | ID: Prominos_05-1 |
| NUS-CPU-06 | `D143H8` | `D147M7I` | Aug 1998 | Dec 1997 | ID: DragonsHoard_01; extremely rare revision; I-suffix on X2 |
| NUS-CPU-07 | `D143B9` | `D147A9` | Feb 1999 | Jan 1999 | ID: RetroRepairZone_01; extremely rare revision |  
| NUS-CPU-08 | `D143F9` | `D147F9` | Jun 1999 | Jun 1999 | *MX8350 present from NUS-CPU-08 onward* |
| NUS-CPU-08 | `D143H9I` | `D147H9I` | Aug 1999 | Aug 1999 | ID: Prominos_08; I-suffix on both |
| NUS-CPU-08 | `D143H9` | `D147J9` | Aug 1999 | Sep 1999 | X2 year inferred |
| NUS-CPU-08 | `D143L9` | `D147L9` | Nov 1999 | Nov 1999 | |
| NUS-CPU-08-1 | `D143H9` | `D147H9` | Aug 1999 | Aug 1999 | |
| NUS-CPU-08-1 | `D143K9` | `D147J9` | Oct 1999 | Sep 1999 | ID: Prominos_08-1 |
| NUS-CPU-08-1 | `D143K9I` | `D147K9I` | Oct 1999 | Oct 1999 | I-suffix on both X1 and X2 |
| NUS-CPU-09 | `D143J0` | `D147H0` | Sep 2000 | Aug 2000 | ID: Prominos_09 |
| NUS-CPU-09 | `D143J0` | `D147J0` | Sep 2000 | Sep 2000 | |
| NUS-CPU-09 | `D143J0I` | `D147K0` | Sep 2000 | Oct 2000 | I-suffix on X1 |
| NUS-CPU-09-1 | `D143H0I` | `D147H0` | Aug 2000 | Aug 2000 | ID: Aringon_01; I-suffix on X1. All visible IC marks with likely decodes: `PIF-NUS A0027 EA` (`0027` NEC date code convention: wk 27, 2000); `CPU-NUS A 0002XK020` (wk 2, 2000); `RCP-NUS 9949KK008` (wk 49, 1999); `RDRAM36 9949KU621`; `AMP-NUS Ⓜ`[^8] `90.6`; `TI LV125A 9AK DE6J`; `MAV-NUS RS5C382 9MS 9Y`; `MX8350MC 43B TA245201` |
| NUS-CPU-09-1 | `D143K0I` | `D147L0` | Oct 2000 | Nov 2000 | I-suffix on X1 |
| NUS-CPU(R)-01 | `D177G7` | `D147E7` | Jul 1997 | May 1997 | PAL, NUS-001(FRA); ID: kwyjibo_01 |
| NUS-CPU(R)-01 | `D177G7` | `D147E7` | Jul 1997 | May 1997 | PAL, NUS-001(FRA); ID: Prominos_R01 |
| NUS-CPU(P)-01 | `D177J7` | `D147J7` | Sep 1997 | Sep 1997 | PAL; modretro_13 |
| NUS-CPU(P)-01 | `D177G8` | `D147M7I` | Jul 1998 | Dec 1997 | PAL; U7 MX9911MC; I-suffix on X2 |
| NUS-CPU(P)-02 | `D177J9` | `D147J9I` | Sep 1999 | Sep 1999 | PAL; I-suffix on X2 |
| NUS-CPU(P)-02 | `D177J9` | - | Sep 1999 | - | PAL; ID: GamingDoc_06; revision inferred; X2 not visible; PIF(P)-NUS (marking: `9940 E`; wk 40, 1999); U8: Toshiba TC74LCX125 (marking: `LCX 125 9 21`) |
| NUS-CPU(P)-03 | - | - | - | - | PAL; no board image available
| NUS-CPU(P)-03-1 | - | - | - | - | PAL; ID: modretro_16. Board image available; stamp codes illegible *(MX8350 present)* |
| NUS-CPU(M)-01 | `D143G6` | `D147G6` | Jul 1996 | Jul 1996 | PAL-M; ID: grav_01; MX8330MC at U7 and U15 |
| NUS-CPU(M)-02 | `ⓂD143G7` | `D147E7` | Jul 1997 | May 1997 | PAL-M; ID: MeuGameAntigo_01
| NUS-CPU(M)-02 | removed | `D147F7` | - | Jun 1997 | PAL-M; ID: gbonifa_01; X1+U6 absent (junk unit) |
| NUS-CPU(M)-02 | `ⓂD143G7` | `D147E7` | Jul 1997 | May 1997 | PAL-M; ID: JASNetInfo_01; revision inferred. Markings: `1997 Nintendo`; `PIF(M)-NUS 9739 D`; `VDC-NUS A BU9801F 727 120`; `ENC-NUS 735 161`; `9480F 7935`; `MX8330MC TEC0968L` (2x); `AMP-NUS 726 180`; `TA78M05F 7I`; `287C` |
| NUS-CPU(M)-03 | `ⓂD143M8` | `D147K9I` | Dec 1998 | Nov 1999 | PAL-M; ID: Lima112_01; `Ⓜ` marking on X1; I-suffix on X2; `PIF(M)-NUS 9753 D`, `MAV-NUS RS5C382 9LS 9N`, `AMP-NUS 002 L66`, `MX9911MC` at U7, January 2000 PCB date code |
| NUS-CPU(M)-04 | - | - | - | - | PAL-M; no board image available
| NUS-CPU(M)-05 | - | - | - | - | PAL-M; no board image available
| NUS-CPU(M)-05-1 | `Ⓜ143G0` | `D147F0I` | Jul 2000 | Jun 2000 | PAL-M; ID: Mielke_01; `Ⓜ` marking on X1; I-suffix on X2 |

[^8]: The `Ⓜ` on the AMP-NUS marking is a Matsushita (Panasonic) logo (confirmed by Prominos). It is unrelated the legal mask work protection symbol `Ⓜ` present elsewhere on this hardware (e.g. PIF-NUS); it is similarly distinct from the `Ⓜ` prefix observed on some PAL-M X1 crystals (see footnote ⁴, §3.5.1.2).  

## Appendix B. VI Modes

Tables with SDK-defined VI mode definitions.

### B.1 libultra VI Mode Decoder

| Position | Options | Description |
| :--- | :--- | :--- |
| 1 | `L` (Low Res) / `H` (High Res) | Toggles the horizontal resolution between standard (320px) and high (640px+). |
| 2 | `A` (Anti-Aliased) / `P` (Point-Sampled) | Toggles VI anti-aliasing and resampling features. `P` disables them for a sharp, pixelated look. |
| 3 | `N` (Non-interlaced) / `F` (Filtered Interlaced) | Selects progressive (`N`) or interlaced (`F`) scan. Interlaced modes usually enable the VI deflicker filter. |
| 4 | `1` (16-bit) / `2` (32-bit) | Configures the VI for either a 16-bit or 32-bit color framebuffer. |

Examples using the decoder:
*   `LAN1`:
    *   `L` -> Low Resolution (320)
    *   `A` -> Anti-Aliased
    *   `N` -> Non-interlaced (Progressive)
    *   `1` -> 16-bit
*   `HPF2`:
    *   `H` -> High Resolution (640)
    *   `P` -> Point-Sampled
    *   `F` -> Interlaced (Filtered)
    *   `2` -> 32-bit

### B.2 libultra VI Mode Definitions

> SDK values derived from the [osViTable.c](https://github.com/n64decomp/sm64/blob/9921382a68bb0c865e5e45eb594d9c64db59b1af/lib/src/osViTable.c) present in the *Super Mario 64* (1996) decompilation source. These values were commpared against later SDK values ([osVITable.c](https://github.com/n64decomp/mk64/blob/3b794dcce90543c2203ca2006eb77a41af49c05e/src/os/osViTable.c) from the *Mario Kart 64* (1996/1997) decompilation, as well as [vitbl.c](https://github.com/Kelebek1/af/blob/770d3c2dca047172c7b947c83f136468cb0dc7e0/lib/ultralib/src/io/vitbl.c) from the *Animal Forest* (2001) decompilation).

Table values (VSYNC, HSYNC(TOTAL), LEAP(A, B)) are effective. HSYNC(LEAP) pattern values are unchanged.

### B.2.1 NTSC (SGI, 1996)

| Region | Decoder Name | Width | Height | Scan  | AA/Point | Depth  | VSYNC (S) | HSYNC(TOTAL, LEAP) | LEAP(A, B)   |
| :----- | :----------- | :---- | :----- | :---- | :------- | :----- | :----     | :----------------- | :----------- |
| NTSC   | NTSC_LAN1    | 320   | 240    | Prog  | AA       | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_LAN2    | 320   | 240    | Prog  | AA       | 32-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_LPN1    | 320   | 240    | Prog  | Point    | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_LPN2    | 320   | 240    | Prog  | Point    | 32-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_LAF1    | 320   | 240    | Inter | AA       | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_LAF2    | 320   | 240    | Inter | AA       | 32-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_LPF1    | 320   | 240    | Inter | Point    | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_LPF2    | 320   | 240    | Inter | Point    | 32-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_HAN1    | 640   | 480    | Inter | AA       | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_HAF1    | 640   | 480    | Inter | AA       | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_HPN1    | 640   | 480    | Inter | Point    | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_HPN2    | 640   | 480    | Inter | Point    | 32-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_HPF1    | 640   | 480    | Inter | Point    | 16-bit | 525       | 3094, 0            | 3094, 3094   |
| NTSC   | NTSC_HPF2    | 640   | 480    | Inter | Point    | 32-bit | 525       | 3094, 0            | 3094, 3094   |

### B.2.2 PAL (SGI, 1996)

| Region | Decoder Name | Width | Height | Scan  | AA/Point | Depth  | VSYNC (S) | HSYNC(TOTAL, LEAP) | LEAP(A, B)   |
| :----- | :----------- | :---- | :----- | :---- | :------- | :----- | :----     | :----------------- | :----------- |
| PAL    | PAL_LAN1     | 320   | 288    | Prog  | AA       | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_LAN2     | 320   | 288    | Prog  | AA       | 32-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_LPN1     | 320   | 288    | Prog  | Point    | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_LPN2     | 320   | 288    | Prog  | Point    | 32-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_LAF1     | 320   | 288    | Inter | AA       | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_LAF2     | 320   | 288    | Inter | AA       | 32-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_LPF1     | 320   | 288    | Inter | Point    | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_LPF2     | 320   | 288    | Inter | Point    | 32-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_HAN1     | 640   | 576    | Inter | AA       | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_HAF1     | 640   | 576    | Inter | AA       | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_HPN1     | 640   | 576    | Inter | Point    | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_HPN2     | 640   | 576    | Inter | Point    | 32-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_HPF1     | 640   | 576    | Inter | Point    | 16-bit | 625       | 3178, 21           | 3182, 3183   |
| PAL    | PAL_HPF2     | 640   | 576    | Inter | Point    | 32-bit | 625       | 3178, 21           | 3182, 3183   |

### B.2.4 MPAL (SGI, 1996)

| Region | Decoder Name | Width | Height | Scan  | AA/Point | Depth  | VSYNC (S) | HSYNC(TOTAL, LEAP) | LEAP(A, B)   |
| :----- | :----------- | :---- | :----- | :---- | :------- | :----- | :----     | :----------------- | :----------- |
| MPAL   | MPAL_LAN1    | 320   | 240    | Prog  | AA       | 16-bit | 525       | 3090, 4            | 3099, 3098   |
| MPAL   | MPAL_LAN2    | 320   | 240    | Prog  | AA       | 32-bit | 525       | 3090, 4            | 3099, 3098   |
| MPAL   | MPAL_LPN1    | 320   | 240    | Prog  | Point    | 16-bit | 525       | 3090, 4            | 3099, 3098   |
| MPAL   | MPAL_LPN2    | 320   | 240    | Prog  | Point    | 32-bit | 525       | 3090, 4            | 3099, 3098   |
| MPAL   | MPAL_LPF1    | 320   | 240    | Prog  | Point    | 16-bit | 525       | 3090, 4            | 3099, 3098   |
| MPAL   | MPAL_LAF1    | 320   | 240    | Inter | AA       | 16-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_LAF2    | 320   | 240    | Inter | AA       | 32-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_LPF2    | 320   | 240    | Inter | Point    | 32-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_HAN1    | 640   | 480    | Inter | AA       | 16-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_HAF1    | 640   | 480    | Inter | AA       | 16-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_HPN1    | 640   | 480    | Inter | Point    | 16-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_HPN2    | 640   | 480    | Inter | Point    | 32-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_HPF1    | 640   | 480    | Inter | Point    | 16-bit | 525       | 3089, 0            | 3101, 3101   |
| MPAL   | MPAL_HPF2    | 640   | 480    | Inter | Point    | 32-bit | 525       | 3089, 0            | 3101, 3101   |

### B.2.3 PAL (OS2.0H, Feb 24, 1997[^9])

| Region | Decoder Name | Width | Height | Scan  | AA/Point | Depth  | VSYNC (S) | HSYNC(TOTAL, LEAP) | LEAP(A, B)   |
| :----- | :----------- | :---- | :----- | :---- | :------- | :----- | :----     | :----------------- | :----------- |
| PAL    | PAL_LAN1     | 320   | 288    | Prog  | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_LAN2     | 320   | 288    | Prog  | AA       | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_LPN1     | 320   | 288    | Prog  | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_LPN2     | 320   | 288    | Prog  | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_LAF1     | 320   | 288    | Inter | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_LAF2     | 320   | 288    | Inter | AA       | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_LPF1     | 320   | 288    | Inter | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_LPF2     | 320   | 288    | Inter | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_HAN1     | 640   | 576    | Inter | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_HAF1     | 640   | 576    | Inter | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_HPN1     | 640   | 576    | Inter | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_HPN2     | 640   | 576    | Inter | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_HPF1     | 640   | 576    | Inter | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| PAL    | PAL_HPF2     | 640   | 576    | Inter | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |

[^9]: OS2.0H (February 24, 1997) introduced a new PAL leap pattern with the revision note: "The PAL table values have been corrected."

### B.2.5 FPAL[^10] (1997)

| Region | Decoder Name | Width | Height | Scan  | AA/Point | Depth  | VSYNC (S) | HSYNC(TOTAL, LEAP) | LEAP(A, B)   |
| :----- | :----------- | :---- | :----- | :---- | :------- | :----- | :----     | :----------------- | :----------- |
| FPAL   | FPAL_LAN1    | 320   | 288    | Prog  | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_LAN2    | 320   | 288    | Prog  | AA       | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_LPN1    | 320   | 288    | Prog  | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_LPN2    | 320   | 288    | Prog  | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_LAF1    | 320   | 288    | Inter | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_LAF2    | 320   | 288    | Inter | AA       | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_LPF1    | 320   | 288    | Inter | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_LPF2    | 320   | 288    | Inter | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_HAN1    | 640   | 576    | Inter | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_HAF1    | 640   | 576    | Inter | AA       | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_HPN1    | 640   | 576    | Inter | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_HPN2    | 640   | 576    | Inter | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_HPF1    | 640   | 576    | Inter | Point    | 16-bit | 625       | 3178, 23           | 3182, 3184   |
| FPAL   | FPAL_HPF2    | 640   | 576    | Inter | Point    | 32-bit | 625       | 3178, 23           | 3182, 3184   |

[^10]: FPAL expands to full-screen PAL (or full-height PAL). Standard PAL modes in libultra share NTSC/PAL-M internal line count limitations despite the PAL standard's additional lines. FPAL allows drawing to 48 more those lines (288 - 240 = 48). This mode was apparently developed by Rare Ltd. and subsequently integrated into libultra, per a Goldeneye 007 decompilation source code comment. It inherits the revised PAL leap pattern.

### B.3 libdragon VI Mode Definitions

> libdragon uses timing presets and computes other registers dynamically. Resolution, bit depth, and AA mode are applied separately. Values are effective.

| Region | Scan         | VSYNC (S)         | HSYNC(TOTAL, LEAP) | LEAP(A, B) |
| :---   | :---         | :---              | :---               | :---       |
| NTSC   | Progressive  | 526               | 3094, 0            | 3094, 3094 |
| NTSC   | Interlaced   | 525               | 3094, 0            | 3094, 3094 |
| PAL    | Progressive  | 626               | 3178, 21           | 3183, 3184 |
| PAL    | Interlaced   | 625               | 3178, 21           | 3183, 3184 |
| PAL-M  | Progressive  | 526               | 3090, 4            | 3099, 3098 |
| PAL-M  | Interlaced   | 525               | 3089, 0            | 3101, 3101 |

### B.3.1 libdragon Display Initialization Behavior

Unlike libultra, which defines a full OSViMode structure for each preset mode, libdragon separates timing configuration from framebuffer configuration. A timing preset establishes the base scan timing, including vertical sync, horizontal sync, and leap patterns. The display subsystem then programs several additional registers dynamically.

---

### Glossary

A quick reference for terminology used in this document.

* **240p:** Shorthand for NTSC and PAL-M progressive mode. One vertical scan comprises 263 scanlines; a 23 scanline blanking period with the remaining 240 lines available for active video output. All N64 signal output is fixed at 640 pixels wide. Contemporary retail NTSC games built with libultra draw no more than 237 lines (474 half-lines) of visible content per vertical scan. PAL equivalent is 288p. *See also: Progressive, Raster, Vertical Scan Frequency.*

* **480i:** Shorthand for NTSC and PAL-M interlaced mode. One vertical refresh comprises two interlaced fields across 525 half-lines; a 45 half-line blanking period with the remaining 480 half-lines available for active video output. Contemporary retail NTSC games built with libultra draw no more than 474 half-lines of visible content per vertical refresh. PAL equivalent is 576i. *See also: Interlaced, Vertical Scan Frequency.*

* **BFP (Burst Flag Pulse):** A timing pulse generated by the VDC-NUS chip (U4) that gates the colorburst window on each active line. It signals to the downstream encoder (ENC-NUS, U5) the interval during which the chroma subcarrier reference should be inserted into the back porch of the composite output. The burst gate window duration is approximately 5.1 μs per oscilloscope observation. *See also: Chrominance Subcarrier Frequency, CSYNC.* 

* **C_stray:** The aggregate parasitic capacitance contributed by PCB traces and IC pin capacitance in an oscillator circuit. Not directly measurable without physical probing of the specific board. In the NUS-CPU-03 X1 load capacitance derivation, C_stray is estimated in the range of 2-5 pF, yielding an effective CL of approximately 23.5-26.5 pF. *See also: Crystal Oscillator Frequency, CL.*  

* **Chrominance Subcarrier Frequency (fS, f_colorburst):** A reference sine wave inserted into the back porch of the horizontal blanking interval on each active line, providing the phase and frequency reference against which a receiver decodes color information. Its frequency is defined by international broadcast standards: 315/88 MHz (NTSC), 17,734,475/4 Hz (PAL), and 511,312,500/143 Hz (PAL-M). In this document's derivations, fS serves as the starting constant from which f_xtal and all downstream timing values are established. *See also: BFP, fH.*  

* **CL (Load Capacitance):** The total capacitance presented to a crystal oscillator by its circuit, comprising the series combination of the two load capacitors plus C_stray. Determines the operating frequency of the crystal; a mismatch between specified and actual CL produces a frequency offset. *See also: C_stray, Crystal Oscillator Frequency.*

* **Colorburst:** *See Chrominance Subcarrier Frequency.*

* **Crystal Oscillator Frequency (f_xtal):** The principal high-frequency oscillation signal driving the N64's Reality Co-Processor (RCP). All N64 video timing is derived from this rate through integer multiplication and division. On early revisions, f_xtal is produced at U7 (MX8330MC or MX9911MC; see §3.1.1) from crystal resonator X1. X1's frequency varies by region: approximately 14.318 MHz for NTSC; 17.734 MHz for PAL; and 14.302 MHz for PAL-M, respectively. VI clock (f_vi) equals f_xtal multiplied by the region-specific factor M (17/5 for NTSC and PAL-M; 14/5 for PAL).  

* **CSYNC (Composite Sync):** A signal generated by the VDC-NUS (U4) that combines horizontal sync (HSYNC) and vertical sync (VSYNC) into a single waveform. CSYNC is passed to the ENC-NUS encoder (U5) and embedded in the final composite video output, allowing a display to lock to the signal's horizontal and vertical timing simultaneously. *See also: VSYNC, BFP.*

* **f_xtal:** Symbol for crystal oscillator frequency. *See Crystal Oscillator Frequency.*  

* **fH:** Symbol for horizontal scan frequency. *See Horizontal Scan Frequency.*  

* **fS (f_colorburst):** Symbol for colorburst or chroma subcarrier signal. fS connotes broadcast standard constant. f_colorburst disambiguates. *See Chrominance Subcarrier Frequency.*  

* **fV:** Symbol for vertical scan frequency (refresh rate). *See Vertical Scan Frequency.*

* **Half-Line (S):** The atomic unit of vertical timing used by the N64's Video Interface (VI). Two half-lines constitute one full horizontal scanline. The total half-line count per vertical scan cycle is programmed via `VI_V_TOTAL`; the effective value is `VI_V_TOTAL` + 1. *See also: Terminal Count.*

* **Horizontal Scan Frequency (fH):** The number of horizontal lines transmitted per second, expressed in Hz. Derived as f_vi ÷ L. Also referred to as line frequency. *See also: L, fV.*

* **Interlaced (I):** A scan method in which lines are interleaved across two successive vertical scans in alternating stripes of even-odd (262.5 lines per vertical scan in NTSC and PAL-M interlaced modes). The VI offsets vertical sync by one half-line on every other scan, each constituting a field in broadcast terminology. fV represents the rate of each individual vertical scan. *See also: Progressive, Half-line, fV.*

* **L (VI Clocks per Line):** Symbol for the number of VI clock cycles that constitute one full horizontal scanline, as defined by the `VI_H_TOTAL` register. The effective value is `VI_H_TOTAL` + 1 (terminal-count convention). Values are 3,094 (NTSC), 3,178 (PAL), and 3,090 (PAL-M progressive) / 3,089 (PAL-M interlaced). *See also: Terminal Count, VI.*

* **LEAP Register:** A hardware compensation mechanism used for fractional L adjustments in non-NTSC regions. It periodically adjusts the length of a scanline to correct for the fractional timing error that results from integer constraints in the horizontal timing registers. In PAL-M's case, the correction to NTSC standards is imperfect. *See also: PAL, PAL-M, f_vi.*

* **M (VI Clock Multiplier):** The region-specific rational factor by which f_xtal is multiplied to produce f_vi. Values are 17/5 for NTSC and PAL-M, and 14/5 for PAL. M is a deterministic hardware ratio and does not vary; crystal tolerance affects f_xtal and propagates through the derivation chain, but M itself is fixed. *See also: Crystal Oscillator Frequency, Horizontal Scan Frequency.*

* **MX8330MC:** A single-channel Macronix clock synthesizer IC used at U7 on early N64 revisions to produce f_vi from crystal X1. FSEL high selects the 17/5 multiplier (NTSC and PAL-M); FSEL low selects 14/5 (PAL). X1 varies by region. U7 is MX8330MC on NUS-CPU-01 through NUS-CPU-04; U7 identity on NUS-CPU-06 and NUS-CPU-07 is unconfirmed. U15 on NUS-CPU-07 is MX8330MC per ChipWorks teardown; U7 is not annotated in that document. The chip outputs FSC (crystal ÷ 4, the chroma subcarrier reference) and FSO/5 from a dedicated pin to drive the video domain. Later revisions consolidated the video clock into the MX8350. *See also: MX9911MC, MX8350, Crystal Oscillator Frequency.*  

* **MX8350:** A dual-channel Macronix clock synthesizer that replaced the twin single-channel chip configuration in later N64 revisions (NUS-CPU-08 onward, 1999+). It consolidates both NTSC/PAL-M and PAL clock synthesis with equivalent output frequencies. Derived values are unaffected by this revision. *Physical chips are marked MX8350MC; datasheet Part No. is MX8350. See also: MX8330MC, MX9911MC.*

* **MX9911MC:** A single-channel Macronix clock synthesizer IC. Functionally equivalent to the MX8330MC: identical 8-pin SOP package, pin assignments, FSEL logic (High → 17/5 multiplier, Low → 14/5 multiplier), FSC (crystal ÷ 4) and FSO/5 outputs, and 5 ms power-up stabilization time. Math is unaffected. MX9911MC at U7 brackets the board revision to (05, 07) inclusive (NTSC); confirmed on NUS-CPU-05 and NUS-CPU-05-1; identity on NUS-CPU-06 and NUS-CPU-07 not confirmed from available board photos. MX9911MC at U15 is believed to bracket the revision to (05-1, 07) inclusive. NUS-CPU-05 retains MX8330MC at U15; NUS-CPU-05-1 includes at least one MX9911MC (at U7), and may include another at U15. *See also: MX8330MC, Crystal Oscillator Frequency.*  

* **NTSC (National Television System Committee):** The broadcast video standard used in North America, Japan, South Korea, and parts of Central America. Precisely, the standard name is NTSC-M (so-called due to combination of System M (a monochrome broadcast standard) and NTSC color specification). Defines a 525-line, approximately 59.94 Hz interlaced signal. On the N64, the NTSC crystal is 315/22 MHz (exact), the VI clock multiplier is 17/5, and there are 3,094 VI clocks per line. *See PAL, PAL-M.*  

* **PAL (Phase Alternating Line):** Broadcast video standard used across Europe, Australia, New Zealand, and much of Africa and Asia. 625-line, 50 Hz interlaced signal with a chroma subcarrier of exactly 4,433,618.75 Hz. On the N64, the PAL crystal is 17.734475 MHz (exact), the VI clock multiplier is 14/5, and LEAP register use is required to maintain standard 15,625 Hz line frequency. *See also NTSC, PAL-M.*  

* **PAL-M (MPAL):** A distinct Brazilian broadcast standard that combines PAL-derived color encoding with an NTSC-derived line rate. The "M" in PAL-M refers to CCIR System M. The chroma subcarrier is 511,312,500/143 Hz (containing a 127/143 fractional remainder), the crystal is 2,045,250,000/143 Hz, and there are 3,090 VI clocks per line in progressive modes (3089 when interlaced). Commonly referred to as MPAL; less commonly, PAL/M.  *See also NTSC, PAL.*

* **Progressive (P):** A scan method in which all lines of a vertical scan are transmitted sequentially in a single pass. Half-lines per vertical scan (S) must be even in progressive modes (526, 626). fV represents the rate of each complete vertical scan. In full scanline units, 526 half-lines corresponds to 263 scanlines: 240 active and 23 vertical blanking. *See also: Interlaced, Half-line, fV.*

* **Raster:** The complete signal area of one vertical scan, encompassing both the active area and all blanking intervals. In the context of lidnariq's VI timing visualization (Figure 3), each horizontal unit represents one VI pixel group and each vertical unit represents one half-line. *See figure below.*

![Raster Scan](/figures/fig29_raster_scan_progressive_ian_harvey.png)  
*Progressive raster scan: electron beam traversal, horizontal retrace, and vertical retrace. Source: Ian Harvey, Wikimedia Commons ([CC0](https://commons.wikimedia.org/wiki/File:Raster-scan.svg))*

* **RCP (Reality Co-Processor):** Principal Silicon Graphics co-processor in the N64 that handles both graphics (Reality Display Processor) and audio/system tasks (Reality Signal Processor). It contains the Video Interface (VI), which generates video timing signals.

* **S (Half-Lines per Vertical Scan):** Symbol for the total half-line count per vertical scan cycle, as programmed via the `VI_V_TOTAL` register. The effective value is `VI_V_TOTAL` + 1 (terminal-count convention). S / 2 gives the number of full scanlines. Values are 526 / 525 (NTSC and PAL-M progressive / interlaced) and 626 / 625 (PAL). *See also: Half-line, Terminal Count.*

* **S-Video:** Two-channel analog video interface that carries luminance (Y) and chrominance (C) as separate signals, mitigating chroma/luma quality loss via composite's single-channel muxing. *On N64 hardware, S-Video output is generated natively by the ENC-NUS, DENC-NUS, AVDC-NUS, and MAV-NUS encoder variants. S-RGB A encoder variants do not output S-Video.*  

* **Terminal Count:** A register convention used by the N64's Video Interface in which the stored value is one less than the effective hardware count. To derive the actual number of clocks or half-lines, add 1 to the register value: effective half-lines = `VI_V_TOTAL` + 1; effective clocks per line = `VI_H_TOTAL` + 1. Timing derivations in this document apply this correction before calculation.  

* **Vertical Scan Frequency (fV):** The rate of vertical scans per second, measured from one VSYNC pulse to the next, expressed in Hz. Also referred to as refresh rate. In progressive modes, fV refers to frame rate; in interlaced modes fV is the rate of each individual field. *See also: VSYNC, Horizontal Scan Frequency.*

* **VDC Bus:** The digital video bus between the RCP (U9) and VDC-NUS (U4). It carries seven bits of pixel data (VDC_D0-VDC_D6), VDC_DSYNC, and a shared clock. Data is transmitted in 4-cycle groups: cycle 0 carries synchronization/control data with VDC_DSYNC low; during active video output, cycles 1-3 carry the Red, Green, and Blue components of one rendered pixel. *See also: VDC_DSYNC, VDC-NUS.*  

* **VDC_DSYNC** *(a.k.a. !DSYNC):* Control qualifier on the VDC bus from the RCP (U9) to VDC-NUS (U4). When low, VDC_D0-VDC_D6 carry synchronization/control bits (cycle 0 of the four-cycle group); when high, the bus carries pixel color data (cycles 1-3). During active video it asserts low once every four VI clocks. During blanking, VDC_DSYNC is held low continuously, allowing the VI to transmit control signals (VSync, HSync, colorburst clamp, CSync) on every VI clock. *See also: VDC Bus.*  

* **VDC-NUS / ENC-NUS / DENC-NUS / S-RGB A / AVDC-NUS / MAV-NUS:** The N64 video output chip family, converting the RCP's digital stream to analog. NUS-CPU-01 through NUS-CPU-04 use a two-chip path: VDC-NUS (VDC bus D0-D6, DSYNC, CLK in) performs DAC and generates CSYNC/BFP, outputting RGB, CSYNC, and BFP to ENC-NUS (U5), which handles composite/S-Video encoding and receives the chroma subcarrier at SCIN. Later revisions consolidate this into a single chip. Timing is unchanged. *Both AVDC-NUS and MAV-NUS are observed on unrevised NUS-CPU-05 boards, confirming that they share the same package and compatible pinout (Link83, 2009; David/EEVblog, 2013). MAV-NUS pins 14-16 carry the audio interface (I2S) (lidnariq).*  

![S-RGB A video circuit](/figures/fig36_snes_video_path_v3.png)  
*S-RGB A (U7) video circuit: RGB inputs from S-PPU2; discrete transistor drive stage (Q1-Q3); RGB, LUMA, C.VIDEO, and CHROMA outputs; CSYNC and Burst inputs. Source: DarthCloud, 2011, [assemblergames.org](https://assemblergames.org/viewtopic.php?t=43494)*  

* **VI (Video Interface):** The hardware block within the RCP responsible for generating the N64's video signal. It reads from memory and uses a set of programmable registers (e.g., `VI_V_TOTAL`, `VI_H_TOTAL`) to define the timing, resolution, and format of the output signal.

* `VI_H_VIDEO` (`0x04400024`): Defines the horizontal start and end of the active video window in VI pixels.

* `VI_V_VIDEO` (`0x04400028`): Defines the vertical start and end of the active video window in half-lines.

* **VSYNC (Vertical Synchronization):** A timing pulse in the video signal marking the end of a vertical scan cycle. The rate of VSYNC pulses defines fV. *See also: fV, CSYNC.*

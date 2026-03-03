# N64 Refresh Rate Reference  

Reference for Nintendo 64 video refresh rates and timing specifications across all supported video modes. 

---

## Contents

* [§1 Introduction](#1-introduction)
  * [§1.1 Terminology](#11-terminology)
  * [§1.2 Annotations](#12-annotations)
  * [§1.3 Distinctions and Hazards](#13-distinctions-and-hazards)
* [§2 Refresh Rate Summary](#2-refresh-rate-summary)
* [§3 Technical Specifications](#3-technical-specifications)
  * [§3.1 Fundamental Constants](#31-fundamental-constants)
  * [§3.2 Video Interface (VI) Register Mapping](#32-video-interface-vi-register-mapping)
  * [§3.3 Derived Timing Values](#33-derived-timing-values)
  * [§3.4 Hardware Signal Path](#34-hardware-signal-path)
  * [§3.5 NTSC Progressive Verification Sample](#35-ntsc-progressive-verification-sample)
  * [§3.6 Diagnostics](#36-diagnostics)
  * [§3.7 Physical Variance and Environmental Stability](#37-physical-variance-and-environmental-stability)
* [§4 Signal Analysis](#4-signal-analysis)
  * [§4.1 Signal Parameters by Mode](#41-signal-parameters-by-mode)
  * [§4.2 Mode-Specific Notes](#42-mode-specific-notes)
* [§5 Mathematical Derivations](#5-mathematical-derivations)
  * [§5.1 NTSC Derivation](#51-ntsc-derivation)
  * [§5.2 PAL Derivation](#52-pal-derivation)
  * [§5.3 PAL-M Derivation](#53-pal-m-derivation)
* [§6 Conversion Reference](#6-conversion-reference)
  * [§6.1 Decimal Conversions](#61-decimal-conversions)
  * [§6.2 Exact Fractional Conversions](#62-exact-fractional-conversions)
* [§7 References and Metadata](#7-references-and-metadata)
  * [§7.1 Visual References](#71-visual-references)
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

* **Progressive (P)**: 526 half-lines per frame (counted sequentially) (PAL: 626)  
* **Interlaced (I)**: 525 half-lines per field (alternating odd/even) (PAL: 625)  

### 1.1 Terminology

**Vertical scan frequency (fV)**, expressed in Hz, is the reciprocal of the `VSYNC` period, measured from the rising edge of one `VSYNC` pulse to the next rising edge. Where used in this document, "refresh rate" refers to this value. In progressive modes, fV represents frame frequency; in interlaced modes, fV represents field frequency.  

All video timing derives from a single physical source: the quartz crystal oscillator. Its frequency is designated f_xtal. The VI clock (f_vi) is produced by multiplying f_xtal by a region-specific rational multiplier M (17/5 for NTSC and PAL-M; 14/5 for PAL). fH follows by dividing f_vi by L, the integer VI clock count per horizontal line. fV follows by dividing fH by half the nominal half-line count S.  

```
f_vi = f_xtal × M
fH   = f_vi / L
fV   = fH / (S / 2)

fV   = (f_xtal × M) / (L × S/2)
```

f_xtal is the sole true constant; all VI timing frequencies are rational derivatives of f_xtal.  

### 1.2 Annotations  

Parenthetical annotations clarify numerical representations:  

* `(exact)`: No rounding error; value derived from integer ratios  
* `(reduced)`: Common factors cancelled  
* `(canonical value)`: Fully reduced fraction; reference value at full precision  
* `(≈)`: Approximate decimal representation   

### 1.3 Distinctions and Hazards  

#### 1.3.1 Counting Units  

* **Half-line (S)** is the atomic unit for VI registers.  
* One line (or scanline) equals 2 half-lines. Progressive counts sequentially; interlaced alternates odd/even per field. Where feasible, this document endeavors to avoid "line" count modelling, favoring half-line models; adherence yields hardware-logic alignment, consistent rational fractions, and general disambiguation.  
* Similarly, this document aims to minimize "frame" and "frame rate" terminology to mitigate ambiguity. The term loses clear meaning when discussing both progressive and interlaced modes (e.g. "two interlaced fields compose a frame" modelling forces meaning to bifurcate per mode).
* The ~0.12 Hz difference between NTSC progressive and interlaced rates is not arbitrary; it is the arithmetic consequence of the additional half-line in the divisor (526 vs 525). See §5.1.  

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

#### 1.3.3 Modes  

- Progressive: lines per vertical refresh (frame)= total half-lines ÷ 2  
- Interlaced: lines per vertical refresh (field) = total half-lines ÷ 2  
- Interlaced VSYNC offsets 0.5 lines per field automatically

#### 1.3.4 Hazards  

- Registers are terminal-counted; add 1 when deriving effective counts.  
- Half-line vs full line must be accounted for.  
- LEAP and hardware jitter affect duration of individual half-lines but do not change nominal half-line count. See §5.2.1 for additional LEAP details.  
 
---

## 2. Refresh Rate Summary  

The table lists refresh rates (fV) for all video modes. Reduced fractions indicated below serve as reference for the remainder of this text.  

| Mode  | Scan Type   | Refresh Rate (fV, Hz)       | Refresh Rate (fV, Hz, .10f)   |  
| :---  | :---        | :---                        | :---                          |  
| NTSC  | Progressive | 2,250,000 / 37,609          | 59.8261054535                 |  
| NTSC  | Interlaced  | 60,000 / 1,001              | 59.9400599401                 |  
| PAL   | Progressive | 15,625 / 313                | 49.9201277955                 |  
| PAL   | Interlaced  | 50 / 1                      | 50 (exact)                    |  
| PAL-M | Progressive | 6,953,850,000 / 116,249,419 | 59.8183634793                 |  
| PAL-M | Interlaced  | 185,436,000 / 3,094,091     | 59.9323032193                 |  

> These values correspond to the derivations in §5.  

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
*N64 Clock Generation Circuits - U7 (NTSC/PAL-M) & U15 (PAL). Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

> Later N64 revisions used Macronix Part No. MX8350 instead of Part No. MX8330MC (see §3.1.1)  

* NTSC Clock Precision: 315/22 MHz (exact) (≈ 14.3181818182 MHz)  
* PAL Clock Precision: 17,734,475 Hz (exact) = 17.734475 MHz  
* PAL-M Clock Precision: 2,045,250,000 ÷ 143 Hz (exact) (≈ 14.3024475524 MHz)  

#### 3.1.1 Clock Generator Hardware Revisions  

Early revisions (NUS-CPU-01 through NUS-CPU-07, 1996-1998) used two separate MX8330MC chips: U7 (NTSC/PAL-M) with FSEL (Frequency Select) tied high → 17/5 multiplier, and U15 (PAL) with FSEL tied low → 14/5 multiplier. Later revisions (NUS-CPU-08 onward, 1999+) consolidated these into a single MX8350 dual-channel chip with equivalent output frequencies and timing characteristics.  

![Figure 1a](/figures/fig6_mx8350_table.png)  
*MX8350 (later revisions) output frequencies for NTSC/PAL/MPAL. Source: MX8350 datasheet*  

> While the MX8350 datasheet lists the MPAL crystal as 14.302446 MHz, the correct value (derived upward from the canonically defined PAL-M colorburst frequency) is 2,045,250,000 / 143 Hz (≈ 14.3024475524 MHz); the origin of this error is not indicated by sources. For precision and correctness, all derivations in this document use the fractional form. See §5.3.  

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

> For interlaced modes, S is set to an odd integer (525 or 625). The VI hardware automatically offsets the vertical sync position by 0.5 lines every other field.  

### 3.3 Derived Timing Values  

All values calculated from the fundamental constants above. Line frequencies and refresh rates are expressed as exact fractions (fully reduced) with corresponding decimal representations.  

| Mode  | Line Frequency (Hz) (.10f) | Line Frequency (Hz) | Progressive fV (Hz)  | Interlaced fV (Hz) |  
| :---  | :---                       | :---                | :---                 | :---               |  
| NTSC  | 15,734.2657342657 Hz       | 2250000/143         | 2250000/37609        | 60000/1001         |  
| PAL   | 15,625 Hz (exact)          | 15625/1             | 15625/313            | 50/1               |  
| PAL-M | 15,732.2295950572 Hz       | 6953850000/442013   | 6953850000/116249419 | 185436000/3094091  |  

### 3.4 Hardware Signal Path  

Video signal timing derives from a deterministic path from physical oscillation to digital counting and finally analog conversion. The following applies to NUS-CPU-01 through NUS-CPU-04, as documented in RWeick's NUS-CPU-03 schematics.  

1. Source: The MX8330MC Clock Generator (U7) interfaces with crystal X1 to synthesize clocks derived from f_xtal; this signal serves as the hardware primitive for all video timing derivations.¹  
2. Logic: The RCP (Reality Co-Processor, U9) receives the clock synthesizer output (derived from f_xtal) to drive the internal VI logic.
3. Counting: The VI hardware counts clock cycles according to `VI_H_TOTAL` (line length) and `VI_V_TOTAL` (frame height) to define the signal's timing boundaries.  
4. Encoding: The VI prepares pixel data for output using a 4-stage multiplexing process, where each stage corresponds to one VI clock cycle.²  
5. Output: The digital stream from the RCP is received by the VDC-NUS chip (U4), which performs the initial digital-to-analog conversion. U4's CLK pin is driven by U7.FSO/5; FSO being the Frequency Synthesizer Output, the Rambus-domain clock divided by five for video timing. The VDC-NUS generates analog RGB, CSYNC, and BFP, and passes these to the ENC-NUS (U5). The ENC-NUS receives the colorburst reference from U7.FSC (Subcarrier Frequency, fS = f_xtal ÷ 4) into its SCIN (Subcarrier Input) pin via the R13/R12 resistor divider and C21, attenuated from ~3 V to ~468 mV before injection into the encoder.  

The 4-stage multiplexing process described in step 4 above is key to understanding the N64's digital video bus. This process uses several signals to transmit data from the RCP to the VDC-NUS: the 7-bit³ data bus (VDC_D0-VDC_D6), the VDC_DSYNC (a.k.a. !DSYNC) signal, and a shared clock. The entire 4-stage group contains all the data for one final, rendered pixel and can be usefully conceptualized as a "VI pixel."  

VDC_DSYNC goes low during the first stage (Stage 0) to signal the start of a new 4-stage group on the data bus. During this process, three of the stages are used to transmit the 7-bit components of a single 21-bit color value (Red, Green, and Blue). The first stage is used for synchronization data. Because one "VI pixel" requires this 4-stage multiplex to be transmitted, the total number of VI pixels per scanline is the VI clocks per line (L) divided by four. Because L is not always evenly divisible by 4 (e.g., 3094 for NTSC), a scanline consists of a number of complete 4-stage groups plus a fractional remainder. See §4.1.1 for visualization.

![Figure 2b](/figures/fig13_n64videosys.png)  
*N64 Video System - 4-stage multiplexing behavior of VDC bus protocol, VDC_DSYNC waveform. Source: Tim Worthington, N64RGB documentation*  

![Figure 2c](/figures/fig14_vdc-nus.png)  
*VDC-NUS (BU9801F) pinout. Source: Tim Worthington, N64RGB documentation*  

![Figure 2d](/figures/fig18_VDC-NUS.png)  
*VDC-NUS (BU9801F, U4) in circuit - VDC bus (D0-D6), DSYNC, and CLK inputs; analog RGB, CSYNC, and BFP outputs to ENC-NUS. CLK driven by U7.FSO/5 (Frequency Synthesizer Output ÷ 5) via R28 (0 Ω). Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

![Figure 2e](/figures/fig17_ENC-NUS.png)  
*ENC-NUS (U5) in circuit - RGB inputs through 110 Ω termination and 1 µF coupling; YOUT and VOUT outputs; SCIN (Subcarrier Input, pin 8) receives U7.FSC (f_xtal ÷ 4) via R13/R12 divider network. Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard*  

¹ Later revisions use a single MX8350 in place of twin MX8330MCs. f_xtal derivations are equivalent. On PAL consoles, U15 (MX8330MC) is driven by crystal X2 to produce the PAL video clock; X1 drives U7 for NTSC and PAL-M. Both crystals feed into the same architectural model; the derivations in §5 are rooted in the respective regional crystal in each case.  

² The schematic path shows the VDC-NUS output feeding ENC-NUS (U5) on NUS-CPU-01 through 04 revisions, whereas other revisions use DENC-NUS, AVDC-NUS, or MAV-NUS to natively generate S-Video and composite. Each implementation performs the same DAC/encoding function; see Figures 2f and 2g below.  

![Figure 2f](/figures/fig15_denc-nus.png)  
*DENC-NUS pinout. Source: Tim Worthington, N64RGB documentation*  

![Figure 2g](/figures/fig16_mav-nus.png)  
*MAV-NUS pinout. Source: Tim Worthington, N64RGB documentation*  

> A notable variant uses the S-RGB A NUS encoder, found on motherboards marked NUS-CPU(R)-01 and primarily sold in France. This chip is a true RGB DAC, but its RGB output pins were not connected on the motherboard, and it does not generate an S-Video signal. Consequently, these consoles are limited to composite video output without modification.  

³ Per [N64brew.dev Video DAC page](https://n64brew.dev/wiki/Video_DAC): "it is unclear why the DAC has only 7 bits of precision instead of 8, and no documentation already found explains this."  

### 3.5 NTSC Progressive Verification Sample  

For NTSC progressive operation, the VI registers are programmed to `VI_V_TOTAL` = `0x20D` and `VI_H_TOTAL` = `0xC15`, yielding 526 half-lines per frame and 3,094 VI clocks per line respectively (effective values after applying the terminal-count convention described in §1.3).  

CSYNC (Composite Sync) and BFP (Burst Flag Pulse) are not register-programmed values. Both are generated downstream by the VDC-NUS (U4) from the decoded digital stream; they appear as hardware outputs on pins 14 and 13 respectively, and are passed directly to the ENC-NUS (U5). Their presence confirms a functioning signal path from RCP through DAC to encoder. See §3.4, step 5 and §3.6 for oscilloscope verification points.  

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

### 3.7 Physical Variance and Environmental Stability  

The derivations in §5 assume an ideal crystal oscillator at exactly the specified frequency. In practice, fV's derivation from a non-ideal f_xtal proves less exact.  

#### 3.7.1 X1 Crystal Oscillators  

The NTSC and PAL-M clock crystal (X1, likely KDS Daishinku) has no published datasheet. The NUS-CPU-03 oscillator circuit presents an effective load capacitance of approximately 23.5 to 26.5 pF (see C39, C40, Figure 1, §3.1, *N64 Clock Generation Circuits*). It is not currently established whether the crystals used were rated for this load or were effectively off-the-shelf parts operating out of spec.  

AT-cut crystals are effectively commodity parts; grade and cut determine the exact oscillation frequency (corroborated by lidnariq). Current production equivalents specify a tolerance of ±30 ppm as the base grade, yielding a range of ±0.0018 Hz around the canonical values in §2 (e.g. NTSC progressive: [59.8243, 59.8279] Hz). GBS-C telemetry from two NTSC N64 units corroborates:  

| Unit                             | Nickname      | Progressive (Hz) | Interlaced (Hz) | Offset (P) | Offset (I) |  
|:---                              |:---           |:---              |:---             |:---        |:---        |  
| Unit #1 (NUS-CPU-03, RGB-modded) | Daily driver  | 59.82771         | 59.94166        | +26.8 ppm  | +26.7 ppm  |  
| Unit #2 (NUS-CPU-03, RGB-modded) | Junk unit     | 59.82731         | 59.94126        | +20.1 ppm  | +20.0 ppm  |  

Both fall within the predicted tolerance window. The ppm offset within each unit is essentially identical across progressive and interlaced modes, as expected: both rates derive from the same crystal. The differing offsets between units reflect normal unit-to-unit crystal variance. Aggregate second-order variance factors (temperature, aging, supply voltage) would require a larger sample to characterize statistically.  

Values derived in §5 are exact by construction, representing irreducible fractions traceable to hardware integers. The hardware itself operates within crystal tolerance. That the measurable values deviate is not a flaw in the derivation; it is the expected relationship between mathematical specification and physical implementation. GBS-C telemetry from PlayStation 1 and Sega Saturn hardware returns progressive values consistent with 2,250,000 / 37,609 Hz within crystal tolerance. This further corroborates the over-determined nature of standards-compliant NTSC 526 half-line progressive timing: independent clock architectures converge on the same value.

#### 3.7.2 Initialization Transient Behavior  

![Figure 1b](/figures/fig12_mx8330mc_rev_e.png)  
*MX8330MC Rev. E application notice illustrating feedback divider stabilization and startup transient.*  

The MX8330MC requires an approximately 5 millisecond stabilization period after power-on before FSO reaches steady operation. This occurs during the IPL startup sequence, prior to the first visible scanline.  

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

* Horizontal Axis (774 units): Represents the number of "VI pixels" per scanline. As established in §3.4, this quotient reflects the total VI clocks per line (L) divided by four.  

> L = 3094 is not evenly divisible by 4; each NTSC line contains exactly 773 complete VI pixel groups and a 2-clock remainder. VDC_DSYNC is a free-running quotient (÷ 4) of f_vi and does not reset at HSYNC; line boundaries are not aligned to 4-stage group boundaries. HSYNC events are communicated to the VDC-NUS through the sync data bits in whichever Stage 0 is running at the time. This fact renders the non-integer quotient a non-issue. The visualization represents this as 774 horizontal units, capturing the full line duration including the partial terminal group.  

| Element | Region                 | Register                                           |  
| :---    | :---                   | :---                                               |  
| Canvas  | V_SYNC/H_SYNC boundary | `VI_V_TOTAL` and `VI_H_TOTAL` define signal limits |  
| Yellow  | Color Burst            | `VI_BURST` values; must not overlap `H_START`      |  
| Grey    | Active Area            | `VI_H_VIDEO` and `VI_V_VIDEO` start/end offsets    |  

> Technically, the hardware *will* allow overlap of `VI_BURST` and `H_START`. Doing so misplaces the burst signal; the TV's chroma decoder continuously struggles for phase lock, producing color corruption that modulates with scene content - chroma lock is lost and recovered dynamically, not terminally. See figure below.  

![Figure 21](/figures/fig22_VI_BURST-overlapping-H_START_lidnariq.png)  
*`VI_BURST` overlapping `H_START` Source: lidnariq / ares emulator Discord, hardware probe*  

> A separate but related failure mode: if `VI_BURST` remains active at line end, the VI randomly fails to blank the left 7 VI pixels.  

### 4.2 Mode-Specific Notes  

NTSC (Progressive and Interlaced)  

* Crystal frequency: 14.3181818182 MHz (315/22 MHz)  
* VI clock frequency: 48.6818181818 MHz (exact) (5355/110 MHz)  
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
| :------- | :-------------------- |  
| PAL      | fS = 283.7516 × fH    |  
| SECAM    | fS = 282 × fH         |  
| PAL-N    | fS = 229.2516 × fH    |  
| PAL-M    | fS = 227.25 × fH      |  
| NTSC     | fS = 227.5 × fH       |  

*Standard fS to fH ratios. Source: Wooding, M., The Amateur TV Compendium, p. 55*  

PAL-M nominally defines fS = 227.25 × fH, but this relationship does not resolve to an integer number of VI clocks per line. The exact colorburst frequency is 3,575,611 + 127/143 Hz. This remainder propagates through the derivation chain. The hardware resolves this by rounding to 3091 VI clocks per line, producing an fH of approximately 15,732.23 Hz rather than the NTSC-standard 15,734.27 Hz. The canonical fV values in this document are derived from the exact fractional colorburst frequency carried through each step; see §5.3 for the full derivation.  

> The subcarrier reference signal is physically delivered to the ENC-NUS encoder (U5) via the SCIN pin (pin 8), which receives the U7.FSC output through a 4.3 kΩ ÷ 850 Ω resistor divider and coupling capacitor C21. This is the hardware path by which the crystal-derived fS enters the analog encode stage. See Figure 2e, §3.4, *ENC-NUS (U5) in circuit*.  

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
   = (5,355 / 110 × 1,000,000) / 3,094 Hz  
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

*Interlaced: 525 half-lines per vertical scan cycle, alternating between odd and even fields (262.5 lines each).*  

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

The LEAP mechanism is implemented via the `VI_H_TOTAL_LEAP` register (`0x04400020`). A repeating 5-stage sequence (B-A-B-A-B) alternates between adding 6 clocks (LEAP_B) and 5 clocks (LEAP_A) during the vertical blanking interval, yielding the required 28/5-clock average per S half-lines.

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

deviation = ((f_H_ntsc - f_H_pal-m) / f_H_ntsc) × 100  
          = (2.0361392085 / 15,734.2657342657) × 100  
          = 0.0129407959%  
```

---

## 6. Conversion Reference  

With the canonical values established in §5, this section provides practical multipliers, most commonly for the purpose of speedrun timing comparison. The aim is to ease synchronization (thus, subsequent comparative analysis) of realtime speedruns recorded across regional hardware.  

Given the following assumptions:  
* game logic is bound to video refresh rate (fV), and  
* NTSC-to-PAL effective performance ratio exactly corresponds with signal fV ratio,  
a longer, slower duration recorded on PAL hardware will correspond to a shorter, faster equivalent time on NTSC hardware. However, important caveats exist.  

When comparing RTA (Real-Time Attack, speedruns measured in realtime) runs recorded at separate refresh rates, questions invariably arise regarding relative skill and status conferred. Communities will handle this on a case-by-case basis. This document only seeks to provide accurate math, not judgment on the parity of conversion for any given software title.  

The conversion ratios described in this section assume signal homogeneity per source. However, some games switch between progressive and interlaced modes. No single conversion factor is perfectly accurate in such cases. The theoretically correct method (frame-by-frame analysis to create a perfectly-weighted average) is largely impractical. One hypothetical solution: game-specific approximate weighted multipliers based on reasonably representative sample ratios of signal prevalence.  

### 6.1 Decimal Conversions

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

For mathematically precise conversions. Each fraction in §6.2 is fully reduced and traceable to the canonical values in §2.  

| From \ To | NTSC Progressive | NTSC Interlaced | PAL Progressive | PAL Interlaced | PAL-M Progressive | PAL-M Interlaced |  
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |  
| NTSC-P  | 1/1             | 525/526         | 45072/37609         | 45000/37609         | 15455/15453           | 2704625/2709426     |  
| NTSC-I  | 526/525         | 1/1             | 30048/25025         | 1200/1001           | 1625866/1622565       | 15455/15453         |  
| PAL-P   | 37609/45072     | 25025/30048     | 1/1                 | 625/626             | 581247095/696497616   | 386761375/464331744 |  
| PAL-I   | 37609/45000     | 1001/1200       | 626/625             | 1/1                 | 116249419/139077000   | 3094091/3708720     |  
| PAL-M-P | 15453/15455     | 1622565/1625866 | 696497616/581247095 | 139077000/116249419 | 1/1                   | 525/526             |  
| PAL-M-I | 2709426/2704625 | 15453/15455     | 464331744/386761375 | 3708720/3094091     | 526/525               | 1/1                 |  

---

## 7. Sources and References  

### 7.1 Visual References  

| Figure | Filename | Technical Source / Description |  
| :--- | :--- | :--- |  
| Figure 1 | `fig1_clock_gen_schematic.png` | *N64 Clock Generation Circuits - U7 (NTSC/PAL-M) and U15 (PAL) (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 1a | `fig6_mx8350_table.png` | *MX8350 output frequencies for NTSC/PAL/MPAL configurations (Source: MX8350 datasheet)* |  
| Figure 1b | `fig12_mx8330mc_rev_e.png` | *MX8330MC Rev. E application notice illustrating feedback divider stabilization and startup transient (Source: MX8330MC datasheet)* |  
| Figure 2 | `fig2_rcp_schematic.png` | *RCP-NUS Pinout showing VDC (Video Digital Complex) Timing Outputs (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2a | `fig9_rcp_vdc_schematic.png` | *Video Digital Complex (VDC) pin assignments showing 7-bit digital video output (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2b | `fig13_n64videosys.png` | *N64 Video System - 4-stage VDC bus protocol, DSYNC waveform, and byte contents (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 2c | `fig14_vdc-nus.png` | *VDC-NUS (BU9801F) pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 2d | `fig18_VDC-NUS.png` | *VDC-NUS (BU9801F, U4) in circuit - digital input side and analog output stage (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2e | `fig17_ENC-NUS.png` | *ENC-NUS (U5) in circuit - RGB termination, subcarrier injection via SCIN/U7.FSC, composite and S-Video outputs (Source: RWeick, NUS-CPU-03-Nintendo-64-Motherboard, [github.com](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard))* |  
| Figure 2f | `fig15_denc-nus.png` | *DENC-NUS pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 2g | `fig16_mav-nus.png` | *MAV-NUS pinout (Source: Tim Worthington, N64RGB documentation, [web.archive.org](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html))* |  
| Figure 3 | `fig3_n64_default_libdragon_240p_timing.png` | *N64 VI Timing Diagram (NTSC Progressive) (Source: lidnariq via ares emulator Discord server - reverse-engineered via hardware probing)* |  

### 7.2 References & Documentation Bridges  

#### 7.2.1 Primary Technical Documentation (Hardware & Standards)  

* Nintendo 64 Functions Reference Manual (OS 2.0i/j/k/l) - VI register mappings and programmable timing.  
* Nintendo 64 Programming Manual - Memory-mapped I/O, VI mode definitions, system programming reference.  
* Nintendo 64 Programming Manual Addendums - Corrections and detailed timing tables.  
* [Nintendo 64 Online Manual 5.2](https://jrra.zone/n64/doc/) - Hardware behavior, VI implementation details.  
* Nintendo 64 System Service Manual (D.C.N. NUS-06-0014-001A) - Block diagrams, boot sequence, oscilloscope timing verification.  
* Macronix MX8350 Datasheet - Dual-channel clock synthesizer, NTSC/PAL/MPAL output frequencies.  
* Macronix MX8330MC Datasheet - Single-channel clock synthesizer; FSEL (Frequency Select, explicit), FSC (Subcarrier Frequency; function confirmed as "1/4 of OSC1 frequency"; independently corroborated as "NTSC Color Subcarrier" in D.C.N. NUS-06-0014-001A §3.6 and by RWeick net label U7.FSC), FSO (Frequency Synthesizer Output; inferred from "Rambus clock output" functional description, corroborated by RWeick net label RAMBUS_ClkGen_FSO/5); startup transient (Rev. E application notice). SCIN expansion (Subcarrier Input) is a logical inference from schematic position and Nintendo Case 2 diagnostic chain; no datasheet definition exists.  
* [ITU-R Recommendation BT.470-6](https://www.itu.int/rec/R-REC-BT.470/en) - NTSC/PAL lines per frame, fields/sec, color subcarrier frequencies.  
* [ITU-R Recommendation BT.1700](https://www.itu.int/rec/R-REC-BT.1700/en) - Composite video signal levels, timing, sync pulses.  
* [ITU-R Recommendation BT.1701](https://www.itu.int/rec/R-REC-BT.1701/en) - Horizontal/vertical timing for composite video.  
* [US6556197B1 - Programmable Video Timing Registers](https://patents.google.com/patent/US6556197B1/en) - Horizontal/vertical sync generation, color burst gate timing.  
* [US4054919A - Video Image Positioning Control](https://patents.google.com/patent/US4054919A/en) - Sync counter generation and display positioning.  
* [SAA1101 Universal Sync Generator Datasheet](https://people.ece.cornell.edu/land/courses/ece4760/ideas/saa1101.pdf) - Corroborating hardware reference for PAL-M chroma frequency relationship (227.25 × fH).  

#### 7.2.2 Hardware Analysis & Reverse-Engineering  

* [RWeick/NUS-CPU-03-Nintendo-64-Motherboard](https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard) - Complete PCB layout, component values, signal paths.  
* [Rodrigo Copetti - Nintendo 64 Architecture](https://www.copetti.org/writings/consoles/nintendo-64/) - CPU, RCP, memory subsystem, graphics pipeline analysis.  
* [Zoinkity Pastebin regarding VI](https://web.archive.org/web/20260119215039/https://pastebin.com/pJG5SBnW) - 237/474 line libultra behavior, VI reverse-engineering details.
* [N64 Motherboard Revisions - ModRetro Forums](https://forums.modretro.com/threads/nintendo-64-motherboard-revisions-serials-info-request.1417/) - Motherboard revision history, component changes, and video encoder chip progression across revisions.  
* [Archived German N64 RGB Mod Guide](https://web.archive.org/web/20130130062716/http://free-for-all.ath.cx:80/daten/n64rgbmod.html) - Historical modding page identifying the NUS-CPU(R)-01 motherboard, documenting the S-RGB A pinout for RGB restoration, and confirming DENC-NUS' unsuitability for RGB output.  
* [NFGGames Forum - French N64 Discussion](https://nfggames.com/forum2/index.php?topic=3083.0) - Community analysis and discussion of the French PAL console and its unique S-RGB A encoder.  

#### 7.2.3 Community Development Resources (SDKs & Tools)  

* [libdragon](https://libdragon.dev/) - High-level API access to N64 hardware and VI timing abstraction.  
* [N64brew.dev - Video Interface](https://n64brew.dev/wiki/Video_Interface) - VI register behavior, timing examples, LEAP implementation.  
* [N64brew.dev - Video DAC](https://n64brew.dev/wiki/Video_DAC) - Video DAC chip variants (VDC-NUS, DENC-NUS, AVDC-NUS, MAV-NUS), 4-stage bus protocol, and DSYNC signal behaviour.  
* [N64brew.dev - Libultra](https://n64brew.dev/wiki/Libultra) - OS interface functions for VI and hardware access.  
* [hkz-libn64](https://github.com/mark-temporary/hkz-libn64) - Direct register-level mappings including VI constants.  
* [n64.readthedocs.io - N64 Hardware Reference](https://n64.readthedocs.io/index.html#video-interface) - General hardware reference and verification.  

#### 7.2.4 Emulator & FPGA Implementations (Cross-Validation)  

* [ares N64 Emulator](https://github.com/ares-emulator/ares/tree/master/ares/n64) - Software VI timing implementation.  
* [CEN64 Emulator](https://github.com/n64dev/cen64) - Software VI timing implementation.  
* [MAME Emulator](https://github.com/mamedev/mame/blob/master/src/mame/nintendo/n64.cpp) - Software VI timing implementation.  
* [MiSTer FPGA N64 Core HDL](https://github.com/MiSTer-devel/N64_MiSTer) - Hardware VI timing implementation.  

#### 7.2.5 General Overview & Contextual References  

* [Wikipedia - NTSC](https://en.wikipedia.org/wiki/NTSC) / [PAL](https://www.wikipedia.org/wiki/PAL) / [PAL-M](https://www.wikipedia.org/wiki/PAL-M) - Broadcast standard overviews.  
* [ATV Compendium (BATC)](https://batc.org.uk/wp-content/uploads/ATVCompendium.pdf) - PAL-M line rate to chroma frequency relationships.  
* [Martin Hinner - VGA/PAL](https://martin.hinner.info/vga/pal.html) - PAL timing specifications and sync relationships.  
* [Danalee Analog Video](https://danalee.ca/ttt/analog_video.htm) - Composite signal structure and timing.  
* [Pembers Archive - World TV Standards](https://web.archive.org/web/20160512200958/http://www.pembers.freeserve.co.uk/World-TV-Standards/) - International broadcast specifications.  
* [JunkerHQ - XRGB Optimal Timings](https://junkerhq.net/xrgb/index.php?title=Optimal_timings) - Optimal dot clock and refresh timings.  
* [Pineight - Dot Clock Rates](https://pineight.com/mw/page/Dot_clock_rates.xhtml) - Dot clock calculations for various video standards.  
* [Optus N64RGB Archive](https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html) - N64 RGB signal modification documentation; source of 4-stage VDC bus protocol diagram and DAC pinouts (Figures 2b, 2c, 2f, 2g).  

### 7.3 Acknowledgements  

* A thread on [videogameperfection.com](https://videogameperfection.com/forums/topic/nintendo-64-de-blur/) for the initial spark of curiosity.  
* lidnariq for PAL-M colorburst correction (§5.3), DSYNC behavior analysis (§3.2, §3.4), ±30 ppm crystal tolerance (§3.7.1), the VI timing map (Figure 3), extensive derivation review, and experimental observations of dynamic chroma modulation and left-pixel blanking failure under `VI_BURST` / `H_START` overlap (§4.1.1). This document could not exist in its current form without these contributions.  
* Robert Peip (FPGAzumSpass) for auditing and corroboration of `VI_V_CURRENT` behaviour.  
* Rasky for cross-referencing register naming against N64brew convention.  
* kev4cards for research leads and additional auditing and refinement.  

---

### 8. Glossary

A quick reference for terminology used in this document.

* **240p:** Shorthand for NTSC and PAL-M progressive (PAL equivalent: 288p). In NTSC and PAL-M progressive modes, the N64 outputs 240 active lines per vertical scan at 640 pixels wide, regardless of internal framebuffer resolution. Of the 263 total scanlines per vertical scan, 240 carry active video (though no retail NTSC game outputs more than 237 lines of visible content) and 23 constitute the vertical blanking interval. *See also: Progressive, Raster, Vertical Scan Frequency.*  

* **480i:** Shorthand for NTSC and PAL-M interlaced (PAL equivalent: 576i). The N64 outputs 480 active lines across two fields in interlaced mode at 640 pixels wide, regardless of internal framebuffer resolution. Contemporary retail games built with libultra draw no more than 474 lines of visible content. *See also: Interlaced, Vertical Scan Frequency.*  

* **BFP (Burst Flag Pulse):** A timing pulse generated by the VDC-NUS chip (U4) that gates the colorburst window on each active line. It signals to the downstream encoder (ENC-NUS, U5) the interval during which the chroma subcarrier reference should be inserted into the back porch of the composite output. The burst gate window duration is approximately 5.1 μs per oscilloscope observation. *See also: Chrominance Subcarrier Frequency, CSYNC.*  

* **Chrominance Subcarrier Frequency (fS, f_colorburst):** A reference sine wave inserted into the back porch of the horizontal blanking interval on each active line, providing the phase and frequency reference against which a receiver decodes color information. Its frequency is defined by international broadcast standards: 315/88 MHz (NTSC), 17,734,475/4 Hz (PAL), and 511,312,500/143 Hz (PAL-M). In this document's derivations, fS serves as the starting constant from which f_xtal and all downstream timing values are established. *See also: BFP, fH.*  

* **Colorburst:** *See Chrominance Subcarrier Frequency.*

* **Crystal Oscillator Frequency (f_xtal):** The principal high-frequency crystal oscillator signal that drives the N64's Reality Co-Processor (RCP). All video timing is derived from this signal through integer multiplication and division. On NUS-CPU-01 through NUS-CPU-07, f_xtal is produced by U7 (MX8330MC) from crystal X1 for NTSC and PAL-M, and by U15 (MX8330MC) from crystal X2 for PAL. VI clock (f_vi) equals f_xtal multiplied by the region-specific factor M (17/5 for NTSC and PAL-M; 14/5 for PAL). f_xtal is the sole true constant within the context of N64 video timing.  

* **CSYNC (Composite Sync):** A signal generated by the VDC-NUS (U4) that combines horizontal sync (HSYNC) and vertical sync (VSYNC) into a single waveform. CSYNC is passed to the ENC-NUS encoder (U5) and embedded in the final composite video output, allowing a display to lock to the signal's horizontal and vertical timing simultaneously. *See also: VSYNC, BFP.*

* **f_xtal:** Symbol for crystal oscillator frequency. *See Crystal Oscillator Frequency.*  

* **fH:** Symbol for horizontal scan frequency. *See Horizontal Scan Frequency.*  

* **fS (f_colorburst):** Symbol for colorburst or chroma subcarrier signal. fS connotes broadcast standard constant. f_colorburst disambiguates. *See Chrominance Subcarrier Frequency.*  

* **fV:** Symbol for vertical scan frequency (refresh rate). *See Vertical Scan Frequency.*

* **Half-Line (S):** The atomic unit of vertical timing used by the N64's Video Interface (VI). Two half-lines constitute one full horizontal scanline. The total half-line count per vertical scan cycle is programmed via `VI_V_TOTAL`; the effective value is `VI_V_TOTAL` + 1. *See also: Terminal Count.*

* **Horizontal Scan Frequency (fH):** The number of horizontal lines transmitted per second, expressed in Hz. Derived as f_vi ÷ L. Also referred to as line frequency. *See also: L, fV.*

* **Interlaced (I):** A scan method in which lines are transmitted across two successive vertical scans. Half-lines are output in alternating stripes of even, then odd (262.5 lines per vertical scan in NTSC and PAL-M interlaced modes). Each vertical scan is a field in broadcast terminology. S is set to an odd integer (525 for NTSC and PAL-M; 625 for PAL), and the VI hardware offsets the vertical sync position by half a line on every other vertical scan. fV represents the rate of each individual vertical scan. *See also: Progressive, Half-line, fV.*

* **L (VI Clocks per Line):** Symbol for the number of VI clock cycles that constitute one full horizontal scanline, as defined by the `VI_H_TOTAL` register. The effective value is `VI_H_TOTAL` + 1 (terminal-count convention). Values are 3,094 (NTSC), 3,178 (PAL), and 3,091 (PAL-M). *See also: Terminal Count, VI.*

* **LEAP Register:** A hardware compensation mechanism used exclusively by PAL N64 consoles. It periodically adjusts the length of a scanline by one VI clock cycle to correct for the small fractional timing error that results from integer constraints in the horizontal timing registers. The adjustment follows a repeating 5-stage B-A-B-A-B sequence, averaging 5.6 VI clocks per stage, and maintains the exact 15,625 Hz line frequency required by the PAL timing standard. Not used in NTSC or PAL-M modes. *See also: PAL, f_vi.*

* **M (VI Clock Multiplier):** The region-specific rational factor by which f_xtal is multiplied to produce f_vi. Values are 17/5 for NTSC and PAL-M, and 14/5 for PAL. M is a deterministic hardware ratio and does not vary; crystal tolerance affects f_xtal and propagates through the derivation chain, but M itself is fixed. *See also: Crystal Oscillator Frequency, Horizontal Scan Frequency.*

* **MX8330MC:** A single-channel Macronix clock synthesizer IC. In early N64 revisions (NUS-CPU-01 through NUS-CPU-07), two MX8330MC chips were used: U7 (NTSC/PAL-M, FSEL high → 17/5 multiplier) driven by crystal X1, and U15 (PAL, FSEL low → 14/5 multiplier) driven by crystal X2. Each chip outputs FSC (its input crystal ÷ 4, the chroma subcarrier reference) and FSO (the Rambus clock); the chip additionally outputs FSO/5 from a dedicated pin to drive the video domain. *See also: MX8350, Crystal Oscillator Frequency.*  

* **MX8350:** A dual-channel Macronix clock synthesizer that replaced the twin MX8330MC configuration in later N64 revisions (NUS-CPU-08 onward, 1999+). It consolidates both NTSC/PAL-M and PAL clock synthesis with equivalent output frequencies. Derived values are unaffected by this revision. *See also: MX8330MC.*  

* **NTSC (National Television System Committee):** The broadcast video standard used in North America, Japan, South Korea, and parts of Central America. Precisely, the standard name NTSC-M (so-called due to combination of System M (a monochrome broadcast standard) and NTSC color). Defines a 525-line, approximately 59.94 Hz interlaced signal. On the N64, the NTSC crystal is 315/22 MHz (exact), the VI clock multiplier is 17/5, and there are 3,094 VI clocks per line. *See PAL, PAL-M.*  

* **PAL (Phase Alternating Line):** Broadcast video standard used across Europe, Australia, New Zealand, and much of Africa and Asia. 625-line, 50 Hz interlaced signal with a chroma subcarrier of exactly 4,433,618.75 Hz. On the N64, the PAL crystal is 17.734475 MHz (exact), the VI clock multiplier is 14/5, and LEAP register use is required to maintain standard 15,625 Hz line frequency. *See also NTSC, PAL-M.*  

* **PAL-M (MPAL):** A distinct Brazilian broadcast standard that combines PAL-derived color encoding with an NTSC-derived line rate. The "M" in PAL-M refers to CCIR System M. The chroma subcarrier is 511,312,500/143 Hz (containing a 127/143 fractional remainder), the crystal is 2,045,250,000/143 Hz, and there are 3,091 VI clocks per line. Commonly referred to as MPAL; less commonly, PAL/M.  *See also NTSC, PAL.*

* **Progressive (P):** A scan method in which all lines of a vertical scan are transmitted sequentially in a single pass. Half-lines per vertical scan (S) must be even in progressive modes (526, 626). fV represents the rate of each complete vertical scan. In full scanline units, 526 half-lines corresponds to 263 scanlines: 240 active and 23 vertical blanking. Interestingly, NTSC and PAL-M games built with Nintendo's libultra library never draw more than 237 lines of actual content in progressive modes. *See also: Interlaced, Half-line, fV.*

* **Raster:** The complete signal area of one vertical scan, encompassing both the active area and all blanking intervals. In the context of lidnariq's VI timing visualization (Figure 3), each horizontal unit represents one VI pixel group and each vertical unit represents one half-line.

* **RCP (Reality Co-Processor):** Principal Silicon Graphics co-processor in the N64 that handles both graphics (Reality Display Processor) and audio/system tasks (Reality Signal Processor). It contains the Video Interface (VI), which generates video timing signals.

* **S (Half-Lines per Vertical Scan):** Symbol for the total half-line count per vertical scan cycle, as programmed via the `VI_V_TOTAL` register. The effective value is `VI_V_TOTAL` + 1 (terminal-count convention). S / 2 gives the number of full scanlines. Values are 526 / 525 (NTSC and PAL-M progressive / interlaced) and 626 / 625 (PAL). *See also: Half-line, Terminal Count.*

* **S-Video:** Two-channel analog video interface that carries luminance (Y) and chrominance (C) as separate signals, mitigating chroma/luma quality loss via composite's single-channel muxing. On N64 hardware, S-Video output is generated natively by the DENC-NUS, AVDC-NUS, and MAV-NUS encoder variants. The VDC-NUS + ENC-NUS two-chip path found on NUS-CPU-01 through NUS-CPU-04 produces composite and S-Video, but not RGB without modification.

* **Terminal Count:** A register convention used by the N64's Video Interface in which the stored value is one less than the effective hardware count. To derive the actual number of clocks or half-lines, add 1 to the register value: effective half-lines = `VI_V_TOTAL` + 1; effective clocks per line = `VI_H_TOTAL` + 1. Timing derivations in this document apply this correction before calculation.

* **Vertical Scan Frequency (fV):** The rate of vertical scans per second, measured from one VSYNC pulse to the next, expressed in Hz. Also referred to as refresh rate. In progressive modes fV is the vertical scan rate directly; in interlaced modes fV is the rate of each individual field. *See also: VSYNC, Horizontal Scan Frequency.*

* **VDC Bus:** The digital video bus between the RCP (U9) and the VDC-NUS chip (U4). It carries seven bits of pixel data (VDC_D0 through VDC_D6), the VDC_DSYNC timing signal, and a shared clock. Data is transmitted in a four-stage multiplexed cycle, one stage per VI clock: Stage 0 carries synchronization data with VDC_DSYNC held low; Stages 1-3 carry the Red, Green, and Blue color components of a single rendered pixel. Each 4-stage group can be modelled as a "VI pixel". 2-stage phase-walk occurs on NTSC and PAL; 3-stage on PAL-M. Phase-walk here is immaterial to video out. *See also: VDC_DSYNC, VDC-NUS.*

* **VDC_DSYNC** *(a.k.a. !DSYNC):* A signal on the VDC bus transmitted from the RCP (U9) to the VDC-NUS (U4). Free-running clock at f_vi ÷ 4 during active video. When low, accompanying data lines carry synchronization and control information (not pixel color data). During blanking, VDC_DSYNC may be held low for multiple consecutive VI clocks to transmit control signals including HSYNC, VSYNC, colorburst clamp, and CSYNC. VDC_DSYNC does not reset at HSYNC; line boundaries are not aligned to its four-stage cycle. *See also: VDC Bus.*

* **VDC-NUS / ENC-NUS / DENC-NUS / AVDC-NUS / MAV-NUS / S-RGB A NUS:** The family of video output chips used across N64 motherboard revisions; each configuration converts the RCP's digital video stream to an analog output signal. NUS-CPU-01 through NUS-CPU-04 use a two-chip path: VDC-NUS acts as a DAC (Digital to Analog Converter) as well as generating CSYNC and BFP; ENC-NUS (U5) handles composite and S-Video encoding, receiving the chroma subcarrier reference via its SCIN pin. Other revisions use a single chip for consolidated functionality. Timing is unaffected.

* **VI (Video Interface):** The hardware block within the RCP responsible for generating the N64's video signal. It reads from memory and uses a set of programmable registers (e.g., `VI_V_TOTAL`, `VI_H_TOTAL`) to define the timing, resolution, and format of the output signal.

* **VSYNC (Vertical Synchronization):** A timing pulse in the video signal marking the end of a vertical scan cycle. The interval between successive VSYNC pulses defines fV. *See also: fV, CSYNC.*

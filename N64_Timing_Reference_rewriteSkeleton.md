# N64 Refresh Rate Reference

Reference for Nintendo 64 video refresh rates and timing specifications across all supported video modes.

---

## Contents

* [§1 Introduction](#1-introduction)
    * [§1.1 Terminology](#11-terminology)
    * [§1.2 Conventions](#12-conventions)
        * [§1.2.1 Counting Units](#121-counting-units)
        * [§1.2.2 Registers](#122-registers)
* [§2 Signal Path](#2-signal-path)
* [§3 Clocks & Crystal Reference](#3-clocks--crystal-reference)
    * [§3.1 Crystal 1 (X1)](#31-crystal-1-x1)
        * [§3.1.1 Crystal Frequency Derivation](#311-crystal-frequency-derivation)
        * [§3.1.2 Clock Synthesis](#312-clock-synthesis)
        * [§3.1.3 Clock Generator Hardware Revisions](#313-clock-generator-hardware-revisions)
    * [§3.2 Crystal 2 (X2)](#32-crystal-2-x2)
* [§4 Mathematical Derivations](#4-mathematical-derivations)
    * [§4.1 NTSC Derivation](#41-ntsc-derivation)
        * [§4.1.1 NTSC Leap Adjustment](#411-ntsc-leap-adjustment)
    * [§4.2 PAL Derivation](#42-pal-derivation)
        * [§4.2.1 PAL Leap Adjustment](#421-pal-leap-adjustment)
        * [§4.2.1.1 PAL Leap Pattern and Bit Mapping](#4211-pal-leap-pattern-and-bit-mapping)
    * [§4.3 PAL-M Derivation](#43-pal-m-derivation)
        * [§4.3.1 PAL-M Progressive Derivation](#431-pal-m-progressive-derivation)
            * [§4.3.1.1 PAL-M Progressive Leap Adjustment](#4311-pal-m-progressive-leap-adjustment)
        * [§4.3.2 PAL-M Interlaced Derivation](#432-pal-m-interlaced-derivation)
            * [§4.3.2.1 PAL-M Interlaced Leap Adjustment](#4321-pal-m-interlaced-leap-adjustment)
* [§5 Derived Timing Reference](#5-derived-timing-reference)
* [§6 VI Register Reference & Mode Notes](#6-vi-register-reference--mode-notes)
    * [§6.1 Register Mapping](#61-register-mapping)
    * [§6.2 Signal Parameters by Mode](#62-signal-parameters-by-mode)
        * [§6.2.1 Timing Map](#621-timing-map)
        * [§6.2.2 Clock Diagram](#622-clock-diagram)
    * [§6.3 Mode-Specific Notes](#63-mode-specific-notes)
        * [§6.3.1 Subcarrier Frequency Relationships](#631-subcarrier-frequency-relationships)
* [§7 Physical Variance & Stability](#7-physical-variance--stability)
    * [§7.1 X1 Crystal Oscillator](#71-x1-crystal-oscillator)
        * [§7.1.1 Load Capacitance](#711-load-capacitance)
        * [§7.1.2 Stamp Codes by Revision (Abridged)](#712-stamp-codes-by-revision-abridged)
    * [§7.2 Oscillator Tolerance](#72-oscillator-tolerance)
    * [§7.3 Initialization Transient Behavior](#73-initialization-transient-behavior)
* [§8 Sources](#8-sources)
    * [§8.1 References](#81-references)
    * [§8.2 Personal Resources](#82-personal-resources)
    * [§8.3 Acknowledgements](#83-acknowledgements)
* [Appendix A. X1 and X2 Crystal Stamp Code Table](#appendix-a-x1-and-x2-crystal-stamp-code-table)
    * [A.1 Stamp Code Format](#a1-stamp-code-format)
    * [A.2 X1 and X2 Stamp Codes by Revision (Full)](#a2-x1-and-x2-stamp-codes-by-revision-full)
* [Appendix B. VI Modes](#appendix-b-vi-modes)
    * [B.1 Libultra VI Mode Decoder](#b1-libultra-vi-mode-decoder)
    * [B.2 Libultra VI Mode Definitions](#b2-libultra-vi-mode-definitions)
    * [B.3 Libdragon VI Mode Definitions](#b3-libdragon-vi-mode-definitions)
* [Glossary](#glossary)

---

## 1. Introduction

<!-- MOVE: current §1 intro text and figure (NUS-CPU-01 motherboard photo) -->

<!-- NOTE: The three video mode bullet lists (NTSC/PAL/PAL-M regions; Progressive/Interlaced) stay here -->

### 1.1 Terminology

<!-- MOVE: current §1.1 -->

<!-- NOTE: fV, fXTAL, fVI, fH, fV equation block stays here -->

<!-- NOTE: The ±30 ppm sentence stays here; rephrase to make clear it propagates to all
     derived values. The long-precision decimals sentence should be strengthened here
     to carry the full nominal ≠ actual point rather than restating it per section. -->

### 1.2 Conventions

<!-- MOVE: current §1.3 (renamed from §1.3 Conventions → §1.2 Conventions) -->

<!-- NOTE: §1.2 Annotations (current §1.2) is REMOVED entirely. The four parenthetical
     labels (exact, reduced, canonical value, ≈) are dropped. No replacement needed;
     clean derivation steps carry the work. -->

<!-- NOTE: Add a brief statement here establishing nominal ≠ actual: something like —
     "The exact rational values and long-precision decimals throughout this document
     are nominal: they reflect the derivation chain from standard-defined constants
     and hardware integers. Physical hardware frequencies are bounded by the ±30 ppm
     crystal tolerance established in [§7.2](#72-oscillator-tolerance); no value
     presented here is a claim about any specific unit." -->

#### 1.2.1 Counting Units

<!-- MOVE: current §1.3.1 -->

#### 1.2.2 Registers

<!-- MOVE: current §1.3.2 register naming table -->

<!-- NOTE: This table stays in §1.2.2 as a naming convention reference.
     Full register behavior detail moves to §6.1. -->

---

## 2. Signal Path

<!-- MOVE: current §3.4 Hardware Signal Path (main body prose, steps 1–5) -->

<!-- MOVE: current §3.2 Video Interface (VI) Register Mapping
     — the prose register descriptions (VI_V_TOTAL, VI_H_TOTAL, VI_V_CURRENT,
       VI_H_VIDEO, VI_V_VIDEO bullets) belong here as they describe signal behavior.
     — the register table itself moves to §6.1. -->

<!-- MOVE: figures from current §3.2 and §3.4:
     - fig2_rcp_schematic.png   SOURCE: update attribution to cy/OpeN64 if applicable
     - fig9_rcp_vdc_schematic.png   SOURCE: update attribution to cy/OpeN64 if applicable
     - fig13_n64videosys.png (Tim Worthington VDC bus diagram) — stays as-is
     - fig28_n64-nus-03_video_output_circuit_worthington.png — stays as-is -->

<!-- NOTE: fig1_clock_gen_schematic.png currently attributed to RWeick moves to §3.1.3.
     Attribution should be updated to cy/OpeN64. -->

<!-- NOTE: current §3.2 blockquote "VI registers operate on terminal counts..." can
     remain as a callout here or fold into §1.2.2 Conventions. -->

<!-- NOTE: The interlaced 0.5-line offset note ("For interlaced modes, S is set to an
     odd integer...") belongs here, after VI counting behavior is established. -->

---

## 3. Clocks & Crystal Reference

<!-- MOVE: current §3.1 Fundamental Constants (intro prose only; tables move to §5) -->

### 3.1 Crystal 1 (X1)

<!-- MOVE: current §3.1 X1 prose — region variation, synthesizer role -->

#### 3.1.1 Crystal Frequency Derivation

<!-- MOVE: current clock_timing.mediawiki §Crystal Frequency Derivation structure
     is better organized than the current paper's treatment here — worth comparing.
     Source of truth remains the paper derivations in §4. -->

<!-- MOVE: fSC derivation table (Standard / fH / fSC:fH / fSC / X1) — exact fraction
     and decimal rows. Currently lives implicitly in §3.1 and §4.2.1 of subcarrier notes. -->

#### 3.1.2 Clock Synthesis

<!-- MOVE: clock synthesis prose and FSEL logic table (NTSC/MPAL High 17×; PAL Low 14×) -->

<!-- MOVE: VCLK = X1 × Multiplier / 5 equation -->

<!-- MOVE: VCLK result table (Standard / FSC / X1 / FSEL / Multiplier / VCLK) -->

<!-- MOVE: MX8330MC, MX9911MC, MX8350 pinout tables -->

#### 3.1.3 Clock Generator Hardware Revisions

<!-- MOVE: current §3.1.1 Clock Generator Hardware Revisions -->

<!-- NOTE: fig1_clock_gen_schematic.png — update source attribution from RWeick to
     cy/OpeN64. Caption and footnote need updating. -->

<!-- MOVE: fig6_mx8350_table.png — stays; source is MX8350 datasheet, unaffected -->

<!-- NOTE: [^mx8350_mpal] footnote stays with the MX8350 table -->

### 3.2 Crystal 2 (X2)

<!-- MOVE: X2 chain table (X2 / RCLK / MClock / CPU / SI / Cartridge-PIF) with
     exact fractions and decimal columns -->

<!-- MOVE: VR4300 Clock Domains subsection and DivMode table -->

<!-- NOTE: [^divmode] footnote stays; 93.75 MHz nominal / DivMode 01 -->

---

## 4. Mathematical Derivations

<!-- MOVE: current §5 intro paragraph (step-by-step, no floating-point in derivation path) -->

<!-- NOTE: All "canonical value" labels are REMOVED throughout this section.
     Fully reduced fractions stand without annotation. Intermediate steps should
     be clear enough that no label is needed. Review each derivation block and
     add a clean intermediate step anywhere the reduction jump is non-obvious. -->

### 4.1 NTSC Derivation

<!-- MOVE: current §5.1 in full -->

#### 4.1.1 NTSC Leap Adjustment

<!-- MOVE: current §5.1.1 in full -->

### 4.2 PAL Derivation

<!-- MOVE: current §5.2 in full -->

#### 4.2.1 PAL Leap Adjustment

<!-- MOVE: current §5.2.1 in full -->

#### 4.2.1.1 PAL Leap Pattern and Bit Mapping

<!-- MOVE: current §5.2.1.1 in full -->

### 4.3 PAL-M Derivation

<!-- MOVE: current §5.3 intro and fVI derivation block -->

#### 4.3.1 PAL-M Progressive Derivation

<!-- MOVE: current §5.3.1 -->

##### 4.3.1.1 PAL-M Progressive Leap Adjustment

<!-- MOVE: current §5.3.1.1 -->

#### 4.3.2 PAL-M Interlaced Derivation

<!-- MOVE: current §5.3.2 -->

##### 4.3.2.1 PAL-M Interlaced Leap Adjustment

<!-- MOVE: current §5.3.2.1 -->

---

## 5. Derived Timing Reference

<!-- NOTE: This section presents results derived in §4. No new math here. -->

<!-- MOVE: current §3.1 Fundamental Constants hardware constants table
     (Standard / fXTAL / M / L / S / VI_V_TOTAL) -->

<!-- MOVE: current §3.3 Derived Timing Values table (Mode / fH decimal / fH fraction / fV) -->

<!-- MOVE: current §2.1 Refresh Rate table (Standard / Scan / fV fraction / fV decimal)
     — now presented as results of §4, not summary up front -->

<!-- NOTE: Resolution (640×240p / 288p / 480i / 576i) is REMOVED from this section.
     Add a footnote to the fV table noting standard retail resolutions per mode,
     pointing to README for the overview table. Something like:
     "Standard retail software outputs 640×240p (NTSC/PAL-M progressive),
     640×480i (NTSC/PAL-M interlaced), 640×288p (PAL progressive), or 640×576i
     (PAL interlaced). See README for summary." -->

---

## 6. VI Register Reference & Mode Notes

### 6.1 Register Mapping

<!-- MOVE: the register table from current §1.3.2
     (N64brew Name / Libultra Name / Address / Description) — full table lives here;
     §1.2.2 retains a trimmed naming-convention version -->

<!-- MOVE: VI_H_VIDEO and VI_V_VIDEO prose descriptions from current §3.2 -->

<!-- NOTE: Blockquote "VI registers operate on terminal counts..." moves here if not
     kept in §2. -->

### 6.2 Signal Parameters by Mode

<!-- MOVE: current §4.1 Signal Parameters by Mode table
     (Mode / fVI / L / S / fV) -->

#### 6.2.1 Timing Map

<!-- MOVE: current §4.1.1 Timing Map — lidnariq figure and surrounding prose -->

<!-- MOVE: VI_BURST / H_START overlap callout and devwizard figure -->

<!-- NOTE: Left-pixel blanking note (7 framebuffer pixels) stays here -->

#### 6.2.2 Clock Diagram

<!-- MOVE: current §4.1.2 Clock Diagram — eb1560 figure and prose -->

### 6.3 Mode-Specific Notes

<!-- MOVE: current §4.2 Mode-Specific Notes in full:
     - NTSC (Progressive and Interlaced)
     - PAL (Progressive and Interlaced) — both leap patterns
     - PAL-M Progressive
     - PAL-M Interlaced -->

<!-- NOTE: [^itu-r_error] footnote (ITU-R digit transposition) stays with PAL-M Progressive -->
<!-- NOTE: [^leap_mk64] footnote stays with PAL leap pattern discussion -->
<!-- NOTE: [^leap_os20h] footnote stays; TODO item to add attribution remains open -->

#### 6.3.1 Subcarrier Frequency Relationships

<!-- MOVE: current §4.2.1 Subcarrier Frequency Relationships —
     table (Standard / fSC:fH / Exact ratio) and surrounding prose -->

<!-- MOVE: fig41_ccir-1990-rep.624-4.png figure -->

---

## 7. Physical Variance & Stability

<!-- MOVE: current §3.5 intro sentence -->

### 7.1 X1 Crystal Oscillator

<!-- MOVE: current §3.5.1 X1 Crystal Oscillator prose
     (KDS identification, AT-49, gbhwdb attribution) -->

#### 7.1.1 Load Capacitance

<!-- MOVE: current §3.5.1.1 Load Capacitance in full -->

<!-- NOTE: Cap values (39 pF) — re-attribute to cy/OpeN64, not RWeick.
     This is a tracked TODO item. -->

#### 7.1.2 Stamp Codes by Revision (Abridged)

<!-- MOVE: current §3.5.1.2 abridged stamp code table -->

### 7.2 Oscillator Tolerance

<!-- MOVE: current §3.5.2 X1 Oscillator Tolerance in full —
     ±30 ppm discussion, GBS-C telemetry table, three-unit comparison -->

<!-- NOTE: [^gbs-c] footnote (PS1 and Saturn corroboration) stays here -->

### 7.3 Initialization Transient Behavior

<!-- MOVE: current §3.5.3 in full — MX8330MC 5ms stabilization -->

<!-- MOVE: fig8_mx8330MC_table.png, fig25_mx8330mc_macro_prominos.jpg,
     fig31_MX9911MC.png, fig32_MX8350MC.png -->

---

## 8. Sources

### 8.1 References

<!-- MOVE: current §7.1 References list in full -->

<!-- NOTE: RWeick entry — tracked TODO: remove from references per todo.md -->

<!-- NOTE: cy-888/OpeN64 entry — confirm present and correctly cited -->

### 8.2 Personal Resources

<!-- MOVE: current §7.2 Personal Resources -->

### 8.3 Acknowledgements

<!-- MOVE: current §7.3 Acknowledgements -->

---

## Appendix A. X1 and X2 Crystal Stamp Code Table

### A.1 Stamp Code Format

<!-- MOVE: current Appendix A.1 in full — format table and figures -->

<!-- MOVE: fig49_kds_month_code.png, fig50_kds_date_code.png -->
<!-- MOVE: fig23, fig24 (Ⓜ marking photos) -->

<!-- NOTE: [^mpal_mark] footnote — SOURCE for board photo still tracked as open TODO -->
<!-- NOTE: [^x1_prefix] footnote stays -->

### A.2 X1 and X2 Stamp Codes by Revision (Full)

<!-- MOVE: current A.2 full table in full -->

<!-- NOTE: [^matsushita] footnote stays -->

---

## Appendix B. VI Modes

### B.1 Libultra VI Mode Decoder

<!-- MOVE: current B.1 in full -->

### B.2 Libultra VI Mode Definitions

<!-- MOVE: current B.2 in full — all subsections:
     B.2.1 NTSC (SGI 1996)
     B.2.2 PAL (SGI 1996)
     B.2.3 PAL (OS2.0H 1997)
     B.2.4 MPAL (SGI 1996)
     B.2.5 FPAL (1997) -->

<!-- NOTE: [^fpal] and [^leap_os20h] footnotes stay -->

### B.3 Libdragon VI Mode Definitions

<!-- MOVE: current B.3 and B.3.1 in full -->

<!-- NOTE: Elle to lead secondary pass here — elaboration on the libdragon preview
     branch PR (MPAL progressive/interlaced unification and any subsequent changes).
     Placeholder: add a note mirroring the current footer note about the preview branch
     MPAL configuration until the prose pass. -->

---

## Glossary

<!-- MOVE: current Glossary in full, alphabetical order preserved -->

<!-- NOTE: Any glossary entries referencing removed sections (§3.6 Diagnostics,
     §4.3 Hardware Variants) should have cross-references updated or removed.
     Specifically check: BFP entry (references §3.6), CSYNC entry (references §3.6),
     Aleck64 entry, iQue Player entry, Ultra 64 Dev Board entry. These hardware
     variant entries can stay in the glossary as brief definitions without
     cross-referencing a now-removed section. -->

---

<!-- ============================================================
     REMOVED FROM MAIN PAPER — TEXT PRESERVED BELOW THIS LINE
     ============================================================ -->

<!-- HARDWARE VARIANTS (→ revision paper)
     Save: current §4.3 and all subsections:
     §4.3.1 Ultra 64 Development Board
     §4.3.2 Aleck64
     §4.3.3 iQue Player
     All figures: fig48, fig42, fig43, fig44, fig47
     All footnotes: [^x3], [^ique-pll]
-->

<!-- DIAGNOSTICS (→ later, own equipment)
     Save: current §3.6 Diagnostics table
     (Signal / Component / Pin / Expected Frequency / Expected Amplitude)
     [^masterclock] footnote
-->

<!-- CONVERSION REFERENCE (→ README only)
     Save: current §6 in full (already in README; no action needed)
-->

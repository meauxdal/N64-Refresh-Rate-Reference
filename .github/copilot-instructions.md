# N64 Video Timing Document — Style & Architecture Guide (/.github/copilot-instructions.md)

## Handoff — 2026.03.03

This is a rigorous technical document regarding vertical scan frequency math for the Nintendo 64 video game console (1996). It traces the signal path from crystal oscillation to final analog output, and provides accurate rational fractional forms of refresh rates for all regional and mode combinations: (NTSC, PAL, PAL-M) × (Progressive, Interlaced) = 6 signals.

This document is not a thesis. It is a technical reference and an experiment. Precision is non-negotiable; register-level formality throughout is not. Natural contractions and informal technical shorthand (e.g. "spec", "mux") are acceptable where they are not factually wrong and reflect how engineers actually talk about this hardware.

**Philosophical guideline: every word is a liability.** If we don't know, we research. If we can't verify, we don't imply we can. No speculation. Ground everything to source material. Ask if you don't know.

A-B-C-D-E consistency mnemonic:
A) Analyze conventions
B) Be on the lookout for outliers
C) Cognitively reason about them
D) Decide on action
E) Execute and iterate

f_xtal is derived from fS - f_xtal is a "hardware primitive" not a "true constant"

---

## 0. Recent Session Notes — 2026.03.05

### 0.1 Changes Applied This Session (v9.0)

- **MX9911MC confirmed at U7 on NUS-CPU-05.** Board photo analysis and datasheet (Macronix PM0463 REV. 1.2, August 1997) confirm the MX9911MC is a functionally equivalent single-channel clock synthesizer: identical 8-pin SOP package, pin assignments, FSEL logic (High → 17/5, Low → 14/5), FSC and FSO/5 outputs, and 5 ms power-up stabilization. It is a previously undocumented N64 clock chip variant, now confirmed in production hardware and independently selected in the N64Micro community schematic. lidnariq had not previously encountered it.

- **§3.1.1 rewritten.** Previous claim ("NUS-CPU-01 through NUS-CPU-07 used two separate MX8330MC chips") was demonstrably incorrect for at least NUS-CPU-05. Corrected to: U15 is MX8330MC throughout early revisions; U7 is MX8330MC on 01–04 and 07, MX9911MC on at least 05, NUS-CPU-06 unconfirmed from available photos. NUS-CPU-08+ consolidates to MX8350.

- **§3.4 footnote ¹ updated.** "Twin MX8330MCs" replaced with accurate phrasing covering both chip variants.

- **§3.5.2 updated.** Startup transient note extended to cover MX9911MC (same 5 ms spec).

- **Glossary: Crystal Oscillator Frequency updated.** U7 chip reference no longer hardcodes MX8330MC.

- **Glossary: MX8330MC updated.** Revision range claim corrected; cross-references MX9911MC.

- **Glossary: MX9911MC added.** New entry documenting the chip, its confirmation context, and functional equivalence.

- **§7.2 References updated.** Added: MX9911MC datasheet, Mitsumi PST91XX (U3), TI SN74LV125A (U8/LC125), N64Micro community schematic (corroborating MX9911MC selection), meauxdal crystal stamp spreadsheet.

- **§7.3 Acknowledgements updated.** meauxdal (Elle) added for board photo research, crystal stamp code documentation, and MX9911MC identification.

- **Source list fully deduplicated.** Organized into buckets: Broadcast Standards, Nintendo Official Docs, Schematics & Hardware, Datasheets, Patents, Board Revisions, Motherboard Images, RGB Mods, Community Docs, SDKs, Emulators/FPGA, Test ROMs, Misc.

### 0.2 New Datasheets Acquired This Session

All locally saved. Not all are yet cited in the document.

| Part | File | Notes |
| :--- | :--- | :--- |
| Macronix MX9911MC | MX9911MC-datasheet.pdf | U7 on NUS-CPU-05; clock gen; now documented in §3.1.1 |
| Mitsumi PST91XX | Mitsumi-PST91XX-datasheet.PDF | U3 voltage supervisor; PST9128 variant confirmed on 02/03 |
| TI SN74LV125A | sn74lv125a-datasheet.pdf | U8 quad bus buffer (LC125); CSYNC buffer on early revisions |
| Rohm BA7242F | Rohm-BA7242F ENC-NUS datasheet.pdf | ENC-NUS (U5); already in doc |
| Rohm BA6591AF | Rohm-BA6591AF datasheet.pdf | Possible AMP-NUS candidate; not yet investigated |
| Rohm BA6592F | Rohm-BA6592F datasheet.pdf | Possible AMP-NUS candidate; not yet investigated |
| Rohm BA78MXXCP | Rohm-BA78MXXCP-datasheet.PDF | Voltage regulator family; possibly U13 |
| Sharp PQ7VZ5 | Sharp PQ7VZ5 datasheet.pdf | Voltage regulator; confirmed at U13 in board photos |
| Rohm 173425/178M18CP | 173425_ROHM_178M18CP datasheet.pdf | 178M05 family sheet; partial match |
| NEC uPD488130/488170 | NEC uPD488130 488170 datasheet.pdf | RDRAM controller; not directly timing-relevant |
| Rambus DRAM (LG) | Rambus DRAM datasheet LG GM73V1892AH16L GM73V1892AH17L.pdf | RDRAM speed grade variants (16L/17L); not directly timing-relevant |
| Toshiba TC59R1809 | Toshiba TC59R1809VK TC59R1809HK.pdf | RDRAM variant |
| SGI R4300 Spec | SGI_R4300_RISC_Processor_Specification_REV2.2.pdf | CPU-NUS die; not timing-relevant |

### 0.3 New Primary Sources Acquired This Session

Patents not previously in the doc or source list:

| Patent | File | Notes |
| :--- | :--- | :--- |
| US6239810 | US6239810.*.pdf | "High performance low cost video game system" — likely core N64 system patent |
| US6331856 | US6331856.*.pdf | "Video game system with coprocessor providing high performance" — likely core N64 patent |
| US6022274 | US6022274.pdf | Not yet identified |
| US20010016517 | US20010016517*.pdf | Not yet identified |
| US4799635 | US4799635.pdf | Not yet identified |
| US5070479 | US5070479.pdf | Not yet identified |

Board scans acquired:
- NUS-CPU-03 front and back (JPEG + XCF, very high resolution GIMP source files)
- NUS-CPU-09-1 (PDN format)
- Full modretro board photo set: NUS-CPU-01 through NUS-CPU-09-1, NUS-CPU(P)-01 through 03-1, NUS-CPU(R)-01
- NUS-CPU(M)-02 board photo (Brazilian MPAL, © 1997 Nintendo, Gradiente sticker, "PRODUZIDO NA ZONA FRANCA DE MANAUS"). X1 depopulated on this unit (black screen / parts donor). U7 chip present but unreadable at available resolution. Only current MPAL board photo in the collection.

RDC schematic (N64 NUS-CPU-03-04.pdf):
- DipTrace format, authored by RDC, created 2015-04-24
- Single schematic file covers both NUS-CPU-03 and NUS-CPU-04 (revisions similar enough to share one document)
- Distinct from the RWeick KiCAD schematic; different source, different format, useful as cross-reference

CPU-NUS pin documentation (SwimmingKittens schematics):
- CPU-NUS-schematic1: Official Nintendo 120-pin QFP package pinout. Confirms pin names including MasterClock (input, pin 16), TClock (pin 18), SyncIn (pin 24), SyncOut (pin 21), SysAD[31:0], SysCmd[4:0], JTAG pins. Unfinished but informative.
- CPU-NUS-schematic2: KiCAD-style symbol for the CPU-NUS, two-part layout. Cross-references schematic1.

Other files noted:
- Nintendo_64_Game_Console-BPT.pdf: Component-level chip breakdown by an Ottawa firm (BPT = Board Probe Test or similar). This was the original source of the single-MX8330MC claim that preceded MX9911MC discovery; exact part numbers in this doc helped identify further datasheet leads. May contain a chip count error or simply pre-date NUS-CPU-05.
- NUS-101_Extra_Circuit.webp: Small auxiliary circuit board found in Pikachu N64 variants (Funtastic series). Controls Pikachu cheek illumination. Not relevant to timing; archived for completeness.

Crystal stamp spreadsheet (meauxdal):
- X1/X2 stamp code database covering NTSC, PAL, PAL-M hardware
- Board revision component tracking (U4, U5, U7, U15, etc.)
- Primary source for MX9911MC revision identification

### 0.4 Previous Session Notes — 2026.03.04

- **LEAP_A / LEAP_B labels corrected throughout:** libdragon `vi.h` register presets confirm LEAP_A (upper bits 27:16) stores 3183 → effective L+6; LEAP_B (lower bits 11:0) stores 3182 → effective L+5. Sequence is A-B-A-B-A, not B-A-B-A-B. Corrected in §5.2.1 and LEAP glossary entry. The arithmetic was correct throughout; only the labels were inverted.
- **libdragon `vi.h` added to §7.2:** Primary source for PAL LEAP register values (vi_pal_p and vi_pal_i presets). Added directly beneath N64brew Video Interface entry.
- **N64brew LEAP prose error identified (not corrected in their wiki):** N64brew's explanatory note states average 5,6,5,6,5 = 5.4, yielding 27 extra clocks — which does not produce exact 15,625 Hz. Their register values are correct; their bit-assignment labels (LEAP_A / LEAP_B) are swapped. Document's arithmetic confirmed correct independently.
- **LEAP glossary sentence repaired:** Broken embedded-quote artifact removed. fH result (15,625 Hz) restored per session flag.
- **§4.1.1 `(may?)` resolved:** "randomly fails" confirmed as lidnariq's phrasing. Artifact removed.
- **§4.1.1 capitalization fixed:** "Relatedly, If" → "Relatedly, if".
- **§1.3 renamed:** "Distinctions and Hazards" → "Conventions". TOC slug updated.
- **§6 Conversion Reference:** Second paragraph and bullet combo rewritten for clarity. Sneaky em dash removed; comma substituted.

### 0.5 Previous Session Notes — 2026.03.03 (Session 2)

- **Stage → Cycle throughout:** "Stage" replaced with "cycle" (lowercase) as the canonical term for one step of the 4-cycle VDC bus group.
- **H_START:** Backtick code-blocking removed from all four occurrences. Plain ALLCAPS, consistent with N64brew convention.
- **§5.3.1 notation fix:** `f_H_ntsc` / `f_H_pal-m` corrected to `fH_NTSC` / `fH_PAL-M`.
- **VDC_DSYNC blanking behavior: resolved.** Phase-correction hypothesis retired. Source: lidnariq, N64brew.dev Video DAC page. Research obligation closed.
- **Figure 2d caption simplified.** Figure 2e caption updated: YOUT and VOUT identified and sourced.
- **Glossary trimming pass completed.**

### 0.6 Previous Session Notes — 2026.03.03 (Session 1)

- **§1.1 Terminology:** X1/X2 wording corrected.
- **§1.3:** Restructured. §1.3.3 Modes and §1.3.4 Hazards collapsed.
- **§3.4:** Substantially rewritten. "Free-running" removed throughout.
- **§3.5 / §3.6 renumbering:** All cross-references updated.
- **§5.1 fH derivation:** `× 1,000,000` mid-chain violation corrected.
- **§7.2 References:** Full formatting pass.
- **Quick-Reference-LaTeX-Tables.md:** Headers expanded.

---

## 1. Document Status

### 1.1 Milestone

Document is at v9.0. §3.1.1 clock hardware revision history is now accurate and sourced. No detected language or math errors. Formatting consistent throughout.

### 1.2 Open Items

- **NUS-CPU-06 U7 chip identity:** Not confirmed from available board photos. Known possibilities: MX8330MC (as on 01–04, 07) or MX9911MC (as on 05). Flag in §3.1.1 as unconfirmed.
- **BA6591AF / BA6592F investigation:** Are either of these AMP-NUS? Not yet determined.
- **New patents (US6239810, US6331856, US6022274, US20010016517, US4799635, US5070479):** Not yet read or cited. US6239810 and US6331856 are likely core N64 system patents and may be citable.
- **BU9801F (VDC-NUS) datasheet:** Still not found. All leads exhausted.

### 1.3 Research Obligations

**PAL LEAP behavior expansion.** Resolved.

**S-RGB A NUS datasheet sourcing.** No datasheet or primary hardware documentation located. One further sourcing attempt warranted before formally closing.

### 1.4 PAL Active Line Counts

NTSC active vertical spans are well-sourced (§11.1). PAL is not. The following is observed but not independently verified.

**Unknown:**
- Whether a PAL libultra interlaced ceiling exists equivalent to NTSC's 474.

**Suggested verification paths:**
- Build and test the 240p test suite for N64 (updates pending release as of March 2026).
- paraLLEl-RDP printf readout of PAL framebuffer dimensions for titles of interest.
- Expanded MiSTer signal detection pass across PAL retail library.

**Leading theory:**
- PAL developers simply never used more than 475~478 half-lines and tended to use VI scaling to fill 576 half-lines for performance reasons.

[JunkerHQ - 240p Test Suite, Sega Dreamcast](https://junkerhq.net/xrgb/index.php?title=240p_test_suite#Sega_Dreamcast)

Slight corroboration here; Dreamcast hardware engineers knew no one actually drew to PAL exclusive lines in the vast majority of cases and implemented hardware that limits their usage.

---

## 2. Formatting Rules

**Hard prohibitions:**
- No LaTeX, anywhere.
- No em dashes (`—`) or en dashes (`–`). These are treated as forensic markers of unreviewed LLM output. Use semicolons, colons, or restructure. A space-hyphen-space ` - ` is acceptable only if structurally unavoidable.
- No floating-point math in derivation chains. Decimals used only for representation and legibility.
- No "Where:", "Let:", or similar construction preambles.

**Minimalism:**
- Minimal bolding. Minimal bullet points. Minimal numbered lists.
- Prefer prose. Integrate loose information into prose rather than listing it.
- Italics used only for soft annotative notes and one approved word of emphasis: *technically*.
- Blockquotes used only for asides.
- Footnotes acceptable; do not overuse.

**Line endings (LLM guidance):**
Two-space line endings are an authorship fingerprint of the human author. Retain them when editing in-place. Never add them to newly emitted text. Exception: figures must use double-spaced line endings to force newline behavior in Markdown renderers.

---

## 3. Core Notation Canon

Non-negotiable. All mathematical and technical symbols must conform to this standard.

- `f_xtal`: Crystal oscillator frequency (Hz). Retain underscore.
- `f_vi`: VI clock frequency (~48 MHz). Retain underscore.
- `fH`: Horizontal scan frequency (line frequency). No underscore.
- `fV`: Vertical scan frequency (refresh rate). No underscore.
- `fS`: Chrominance subcarrier frequency. Broadcast engineering variable; used in §4.2.1 context only.
- `f_colorburst`: Hardware derivation primitive for the same physical signal as `fS`. Used in §5 derivations. On first use in each §5 derivation, annotate `(fS)`.

---

## 4. Code Blocking Rules

Code blocking in the main document applies to exactly two categories:

1. **Register names** (e.g. `VI_V_TOTAL`, `VI_H_TOTAL`, `VI_V_CURRENT`, `VI_V_VIDEO`, `VI_H_VIDEO`, `VI_X_SCALE`, `VI_Y_SCALE`)
2. **Hex addresses** (e.g. `0x04400018`)

**Signal names, pin names, chip designators, and all other technical terms are never code-blocked.** No exceptions.

This means: CSYNC, BFP, HSYNC, VSYNC, FSC, FSO, FSO/5, FSEL, SCIN, VDC_DSYNC, VDC_D0–VDC_D6, H_START are all plain text in prose.

---

## 5. Division Operator Convention

Context determines the operator. Do not normalize to a single symbol.

- `/` is used in derivation chains, tables, code blocks, and inline mathematical expressions (fraction notation). Also used when reproducing schematic pin labels verbatim (e.g. FSO/5).
- `÷` is used in prose when describing hardware signal relationships in natural language (e.g. "FSO ÷ 5", "f_vi ÷ 4").

Code block division uses space-padded ` / `. Fraction notation uses unpadded `/`.

---

## 6. Derivation Convention

All frequencies inside derivation chains must be expressed in Hz.

1. Resolve MHz to Hz at the point of entry into a derivation chain.
2. Once inside the chain, all `=` lines carry Hz without further annotation.
3. Do not insert `× 1,000,000` mid-chain.

---

## 7. Caution Words and Canonical Terminology

### 7.1 Prohibited or Restricted Terms

- **"Master clock"**: Do not use. f_xtal is the master crystal frequency. "System Master Clock" appears once in a header row to align with primary sources; leave it unaltered.
- **"Beat"**: Never used. Do not insert. "Cycle" is the correct term for one step of the 4-cycle VDC bus group.
- **"Stage"**: Retired. Replaced by "cycle" (lowercase) throughout. Do not reintroduce.
- **"Frame"**: Avoid. Use risks corrupting mental half-line model alignment with hardware ground truth. Avoid in derivations and vertical timing contexts entirely.
- **"Field"**: Avoid in LEAP and vertical timing derivations. The half-line model (S) is canonical. Exception: acceptable in prose when specifically describing interlaced signals. Field is markedly less ambiguous than frame.
- **"Line" / "scanline"**: Use sparingly. Strongly prefer the atomic canonical hardware unit "half-line" (S). Scanline is acceptable where its use avoids worse repetition or ambiguity, provided the half-line model is already established in context.
- **"Free-running"**: Do not use to describe VDC_DSYNC. The blanking behavior is now resolved and documented; the term is both imprecise and no longer needed.
- **"K"**: Never use as a variable. Has appeared once in LLM-generated output with no definition and no legitimate referent. It is contaminant; delete on sight.

### 7.2 Canonical Vertical Frequency Terminology

Accepted (in order of preference):
- Vertical scan frequency (canonical)
- Vertical scan cycle
- Refresh rate (acceptable)
- Singular: "vertical scan" or "vertical refresh"

Never use:
- Frame rate / framerate
- VI/S or VPS (vertical interrupts per second)
- Field rate / fieldrate

### 7.3 Chrominance Subcarrier Naming

The canonical expanded name is **Chrominance Subcarrier Frequency**. In prose, "colorburst", "chroma subcarrier", and "chroma" are all acceptable shorthand. The full expanded name is required only on first use and in the glossary header.

---

## 8. Hardware Signal Path — Established Facts

### 8.1 Crystal and Clock Generator

Early revisions use two separate single-channel clock synthesizer chips:

- U7 is driven by crystal X1. Handles NTSC and PAL-M. FSEL high → 17/5 multiplier.
  - MX8330MC on NUS-CPU-01 through NUS-CPU-04, and NUS-CPU-07.
  - MX9911MC on at least NUS-CPU-05. NUS-CPU-06 unconfirmed.
  - MX9911MC is functionally equivalent: identical pin assignments, FSEL logic, FSC and FSO/5 outputs, 5 ms power-up stabilization. Confirmed by datasheet (PM0463 REV. 1.2, August 1997) and N64Micro community schematic.
- U15 (MX8330MC) is driven by crystal X2. Handles PAL. FSEL low → 14/5 multiplier.
- Each chip outputs FSC (input crystal ÷ 4, chroma subcarrier reference) and FSO (Rambus clock).
- FSO/5 is output from a dedicated pin on each chip and drives the video domain.

On NUS-CPU-08 onward: single MX8350 replaces the twin single-channel chips. Derived values unaffected.

**X2 is the PAL video crystal. It is not unrelated to video timing.** Any body text implying X1/U7 is universal must be corrected. The full document has been audited; the model is consistent throughout as of this handoff.

### 8.2 VDC_DSYNC Behavior — Resolved

VDC_DSYNC going low defines cycle 0 of the 4-cycle VDC bus group. During active video it asserts low once every four VI clocks. During blanking, VDC_DSYNC is held low continuously, allowing the VI to transmit control signals (VSync, HSync, colorburst clamp, CSync) on every VI clock.

Source: lidnariq, N64brew.dev Video DAC page — "The Video Interface relies on being able to send control signals (VSync, HSync, 'clamp'=colorburst, CSync) every VI clock during blanking by keeping the !DSYNC input low for multiple clocks in a row."

The phase-correction hypothesis is retired. The blanking behavior is fully accounted for by the control signal transmission requirement. Do not reintroduce phase-walk framing.

### 8.3 Phase-Walk Values (L mod 4)

- NTSC: 3094 mod 4 = 2
- PAL: 3178 mod 4 = 2
- PAL-M: 3091 mod 4 = 3

These are arithmetic facts about line boundary alignment and remain correct. The prior framing — that VDC_DSYNC blanking behavior exists to correct this offset — is retired. The offset exists; its effect on video output is not the mechanism driving blanking behavior.

### 8.4 ENC-NUS Output Identification

YOUT and VOUT on the ENC-NUS (U5) are identified as follows:

- YOUT = luma output, S-Video Y channel
- VOUT = composite video output

Confirmed via two independent lines of evidence:
1. RWeick NUS-CPU-03 schematic: YOUT and VOUT net routing to AV connector (Figure 2e).
2. DENC-NUS pinout (Figure 2f, Tim Worthington): equivalent chip labels the same pins VIDEO and LUMA explicitly.

SCIN (pin 8) receives U7.FSC via R13 (4.3 kΩ) / R12 (850 Ω) divider and C21. Confirmed by schematic; values verified.

### 8.5 Other Confirmed Component Identifications

| Designator | Part | Notes |
| :--- | :--- | :--- |
| U3 | Mitsumi PST9128 | Voltage supervisor/reset IC; confirmed on NUS-CPU-02/03 |
| U8 | TI SN74LV125A (LC125) | Quad bus buffer; CSYNC buffering on early revisions |
| U13 | Sharp PQ7VZ5 | Voltage regulator; confirmed in board photos |

**Unresolved:**
- AMP-NUS chip identity: BA6591AF and BA6592F (both Rohm) are candidates. Datasheets acquired; investigation pending.
- BU9801F (VDC-NUS) datasheet: not found.

---

## 9. Epistemic Policy for Initialisms

Body text uses expanded initialisms without qualification. The epistemic burden is carried exclusively in §7.2 References.

**Established expansions:**

- `RCP` (Reality Co-Processor): Explicit — Nintendo Introductory Manual (Nintendo of America, 1999).
- `RDP` (Reality Display Processor): Explicit — same source. Do not use "Reality Drawing Processor"; it is incorrect.
- `RSP` (Reality Signal Processor): Explicit — same source.
- `FSEL` (Frequency Select): Explicit — MX8330MC datasheet; confirmed MX9911MC datasheet.
- `FSC` (Subcarrier Frequency): Corroborated by Nintendo diagnostics and schematics.
- `FSO` (Frequency Synthesizer Output): Inferred from functional description; corroborated by schematics.
- `FSO/5`: Schematic pin label (RWeick NUS-CPU-03). Reproduced verbatim; the `/` is part of the label, not a division operator.
- `MasterClock`: CPU-NUS pin 16 per SwimmingKittens CPU-NUS pinout. The clock input to the CPU-NUS from the RCP clock domain. Distinct from f_xtal. Do not conflate.
- `SCIN` (Subcarrier Input): Inferred from schematic position and diagnostic logic. No datasheet definition exists.
- `YOUT` (luma output / S-Video Y): Confirmed by schematic net tracing and DENC-NUS corroboration. See §8.4.
- `VOUT` (composite video output): Confirmed by schematic net tracing and DENC-NUS corroboration. See §8.4.

---

## 10. Register vs. Hardware Signal Distinction

Programmer-visible register states and hardware-generated signals must not be conflated.

- `VI_V_TOTAL`, `VI_H_TOTAL`, `VI_V_VIDEO`, `VI_H_VIDEO`, etc. are registers.
- CSYNC, BFP, VDC_DSYNC are hardware-generated signals with no register state.

All register values are terminal-counted. Clarity is required to prevent off-by-one errors in derivations.

---

## 11. Active Line Count Reference

### 11.1 NTSC and PAL-M (Well-Sourced)

- Progressive output signal: 240 lines. Sources: Rasky (N64brew Discord), libdragon.
- Progressive drawable ceiling (libultra retail): 237 lines. Sources: Zoinkity, MiSTer observation, libdragon.
- Interlaced output signal: 480 lines (240 per field).
- Interlaced drawable span (libultra retail): 474 half-lines total. Sources: Zoinkity, MiSTer observation.
- VI_V_VIDEO standard difference: 474 half-lines (NTSC). Source: Zoinkity.
- VI_H_VIDEO standard difference: 640 pixels. Source: Zoinkity.
- "480 is a myth" is NTSC-specific (Zoinkity). 474 is the correct active span for libultra retail games.

### 11.2 PAL (Partially Sourced — See §1.4)

- Progressive output signal: 288 lines (640×288 conventional). Source: Rasky (single source, unverified).
- Progressive observed: 237 lines (SM64 Europe, MiSTer signal detection). Not confirmed as ceiling.
- Interlaced output signal: 576 lines (625 total - blanking).
- Interlaced observed values (MiSTer FPGA signal detection, meauxdal, March 2026):
  - 475 half-lines: StarCraft 64 Germany, Pokémon Stadium 2 Europe
  - 478 half-lines: Star Wars Episode I Racer Europe (highest observed retail value)
  - 236 lines progressive: Blast Corps PAL (possibly VI crop/scissor artifact)
- No canonical PAL ceiling established. PAL games do not appear to follow a single libultra-equivalent ceiling.

---

## 12. Conversion Table Semantics

The tables in §6 express duration multipliers, not frequency ratios.

> Multiply the source duration by the cell value at [From row, To column] to obtain the equivalent destination duration.

Example: PAL-I 1:23:45 (5,025 s) × 37,609/45,000 ≈ 4,200.8 s ≈ 1:10:01 NTSC-P equivalent.

---

## 13. Symbol Audit Checklist

Consistency required across: =, ≈, ≠, <, >, +, -, ×, ÷, ±, ∈, {,}, [,]

Status: complete throughout. Glossary overhaul complete.

---

## 14. Repository Structure
```
N64-Refresh-Rate-Reference/
├── .github/
│   └── copilot-instructions.md       <- this file
├── docs/
│   ├── Quick-Reference-LaTeX-Tables.md
│   ├── WIP_N64-Repair-Docs-Summary.docx
│   └── [ITU-R standards PDFs]
├── figures/
│   └── fig1-fig22.*                  <- all figures and figure-PDFs
├── tools/
│   └── canonical_values.json
├── N64_Timing_Reference.md           <- main document
└── README.md
```

---

## 15. Tiny Notes

### 15.1 Document Authority

The text between the following lines used to be at the end of the document (roughly. I edited it ~Elle):

---

**Document Authority Chain:** Primary Sources (Official documentation, ITU standards, datasheets, patents)  
↓  
Mathematical Derivations  
↓  
N64_Timing_Reference.md

---

I didn't like it there anymore. But I want to keep the wording here at the end of this instruction sheet.

### 15.2 README Refuse

## Hardware Specifics

Progressive modes include an extra half-line (526 for NTSC/PAL-M, 626 for PAL) to suppress interlace artifacts, resulting in a refresh rate slightly below the standard 60,000/1,001 Hz. PAL-M uses a distinct integer divisor of 3091 VI clocks per line. All NTSC derivations are based on the canonical 315/22 MHz crystal oscillator, not the commonly cited approximation of 14.318 MHz.

## Example
```cpp
// NTSC Progressive: 2,250,000 / 37,609 Hz
double frame_duration_ns = (37609.0 / 2250000.0) * 1e9; 
// Result: ~16,715,111.11 ns
```

Precision is only preserved if your implementation carries it.

# N64 Video Timing Document — Style & Architecture Guide (/.github/copilot-instructions.md)

## Handoff — 2026.03.02.ver03

This is a rigorous technical document regarding vertical scan frequency math for the Nintendo 64 video game console (1996). It traces the signal path from crystal oscillation to final analog output, and provides accurate rational fractional forms of refresh rates for all regional and mode combinations: (NTSC, PAL, PAL-M) × (Progressive, Interlaced) = 6 signals.

This document is not a thesis. It is a technical reference and an experiment. Precision is non-negotiable; register-level formality throughout is not. Natural contractions and informal technical shorthand (e.g. "spec", "mux") are acceptable where they are not factually wrong and reflect how engineers actually talk about this hardware.

**Philosophical guideline: every word is a liability.** If we don't know, we research. If we can't verify, we don't imply we can. No speculation. Ground everything to source material. Ask if you don't know.

A-B-C-D-E consistency mnemonic:
A) Analyze conventions
B) Be on the lookout for outliers
C) Cognitively reason about them
D) Decide on action
E) Execute and iterate

---

## 0. HOTFIX 

### 0.1 Pending Audit: "Sole True Constant" Language

The phrase "sole true constant" or equivalent appears in at least two places:

1. **Crystal Oscillator Frequency glossary entry:** "f_xtal is the sole true constant within the context of N64 video timing."
2. **§3.x body text** (suspected - unverified location): similar language asserting f_xtal's primacy.

**The problem:** The Chrominance Subcarrier Frequency entry now reads "In this document's derivations, fS serves as the starting constant from which f_xtal and all downstream timing values are established." This creates a tension: fS is the derivation entry point, f_xtal is the hardware constant. Both statements are true but they can read as contradictory without careful framing.

**Required action:**
- Locate all instances of "sole true constant" or equivalent in the document.
- Verify that each instance is scoped correctly: f_xtal is the sole true *hardware* constant; fS is the sole true *derivation entry point*.
- Ensure the two entries do not contradict each other at a casual reading.
- Consider whether a single clarifying sentence in one of the two entries resolves the apparent tension, rather than rewording both.

**Do not resolve speculatively. Human author review required.**

### 0.2 Pending Verification
- §5.2.1 (LEAP): The 5-stage B-A-B-A-B sequence enable-bit encoding (tentatively 0x15 / binary 10101)
  in VI_H_TOTAL_LEAP bits 20:16) was removed pending sourcing. If verifiable against hardware
  documentation or emulator source, it belongs in §5.2.1 with attribution.

---

## 1. Document Status & Pending Items

### 1.1 Completed This Session (2026.03.02)
- Glossary overhaul: complete pending human author final review.
- Crystal Oscillator Frequency entry corrected: X1/U7 (NTSC/PAL-M) and X2/U15 (PAL) now correctly distinguished.
- §3.4 footnote ¹ corrected: previous version incorrectly stated X2 was unrelated to video timing.
- VDC_DSYNC definition improved: free-running behavior, blanking hold behavior, and non-reset-at-HSYNC now documented.
- RDP expansion corrected to "Reality Display Processor" throughout (was "Reality Drawing Processor").
- Phase-walk values established: NTSC 2-stage, PAL 2-stage, PAL-M 3-stage.
- Zoinkity VI register reference archived and added to §7.2.
- Nintendo Introductory Manual added to §7.2.
- PAL active line count research initiated; partial results documented in §14.

### 1.2 Pending — Human Author
- Final tone/style audit.
- VDC_DSYNC find-replace pass: remove all code-blocking of VDC_DSYNC in body text (signal name, not register).
- X1/X2/U7/U15 body text audit: verify all references correctly distinguish NTSC/PAL-M (X1, U7) from PAL (X2, U15). Flag any instance carrying the old incorrect assumption that X1/U7 is universal. §3.4 footnote ¹ is now correct; body text elsewhere may not be.
- §7.2 tone/style audit: currently one of the more LLM-heavy sections. Descriptions are inconsistent in length and register; some parenthetical epistemic notes belong in copilot-instructions.md rather than a public reference list. See §14.4.
- Insert approved VI_V_VIDEO and VI_H_VIDEO register entries into §3.2.
- Insert approved 240p and 480i glossary entries.
- Insert approved M glossary entry.
- TOC: already complete. No action needed.

### 1.3 Pending — Research & Verification
- PAL active line counts: see §14.1.
- Sync leap register PAL behavior: see §14.2.
- Framebuffer scaling note (VI_X_SCALE / VI_Y_SCALE): drafted, awaiting placement decision (§3.2 vs §4).
- Nintendo Introductory Manual: citation added to §7.2; no body text changes required.

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

This means: CSYNC, BFP, HSYNC, VSYNC, FSC, FSO, FSO/5, FSEL, SCIN, VDC_DSYNC, VDC_D0–VDC_D6 are all plain text in prose.

**Known error to correct:** VDC_DSYNC appears code-blocked in several locations in the main document body. This is incorrect and must be corrected in a find-replace pass by the human author.

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
- **"Beat"**: Never used. Do not insert. "Stage" is the correct term.
- **"Frame"**: Avoid. Use risks corrupting mental half-line model alignment with hardware ground truth. Avoid in derivations and vertical timing contexts entirely.
- **"Field"**: Avoid in LEAP and vertical timing derivations. The half-line model (S) is canonical. Exception: acceptable in prose when specifically describing interlaced signals. Field is markedly less ambiguous than frame.
- **"Line" / "scanline"**: Use sparingly. Strongly prefer the atomic canonical hardware unit "half-line" (S). Scanline is acceptable where its use avoids worse repetition or ambiguity, provided the half-line model is already established in context.
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

On NUS-CPU-01 through NUS-CPU-07:
- U7 (MX8330MC) is driven by crystal X1. Handles NTSC and PAL-M. FSEL high → 17/5 multiplier.
- U15 (MX8330MC) is driven by crystal X2. Handles PAL. FSEL low → 14/5 multiplier.
- Each chip outputs FSC (input crystal ÷ 4, chroma subcarrier reference) and FSO (Rambus clock).
- FSO/5 is output from a dedicated pin on each chip and drives the video domain.

On NUS-CPU-08 onward: single MX8350 replaces twin MX8330MCs. Derived values unaffected.

**X2 is the PAL video crystal. It is not unrelated to video timing.** Any body text implying X1/U7 is universal must be corrected.

### 8.2 VDC_DSYNC Behavior

- VDC_DSYNC is a free-running clock at f_vi ÷ 4 during active video.
- It does not reset at HSYNC. Line boundaries are not aligned to its 4-stage cycle.
- When low, accompanying data lines carry synchronization and control information, not pixel color data.
- During blanking, VDC_DSYNC may be held low for multiple consecutive VI clocks to transmit control signals including HSYNC, VSYNC, colorburst clamp, and CSYNC.
- Stage 0 = VDC_DSYNC low (sync data); Stages 1–3 = Red, Green, Blue components.

**Naming:**
- `VDC_DSYNC` is the correct name throughout (RWeick schematic label).
- `!DSYNC` (Tim Worthington) appears once as a parenthetical alias only.
- "DSYNC" alone is never used.

### 8.3 Phase-Walk Values (L mod 4)

- NTSC: 3094 mod 4 = 2 (2-stage phase-walk)
- PAL: 3178 mod 4 = 2 (2-stage phase-walk)
- PAL-M: 3091 mod 4 = 3 (3-stage phase-walk)

Phase-walk is immaterial to video output.

---

## 9. Epistemic Policy for Initialisms

Body text uses expanded initialisms without qualification. The epistemic burden is carried exclusively in §7.2 References.

**Established expansions:**

- `RCP` (Reality Co-Processor): Explicit — Nintendo Introductory Manual (Nintendo of America, 1999).
- `RDP` (Reality Display Processor): Explicit — same source. Do not use "Reality Drawing Processor"; it is incorrect.
- `RSP` (Reality Signal Processor): Explicit — same source.
- `FSEL` (Frequency Select): Explicit — MX8330MC datasheet.
- `FSC` (Subcarrier Frequency): Corroborated by Nintendo diagnostics and schematics.
- `FSO` (Frequency Synthesizer Output): Inferred from functional description; corroborated by schematics.
- `FSO/5`: Schematic pin label (RWeick NUS-CPU-03). Reproduced verbatim; the `/` is part of the label, not a division operator.
- `SCIN` (Subcarrier Input): Inferred from schematic position and diagnostic logic. No datasheet definition exists.

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

### 11.2 PAL (Partially Sourced — See §14.1)

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

Status: complete in body text outside glossary. Glossary overhaul complete.

---

## 14. Open Research Questions

### 14.1 PAL Active Line Counts

NTSC active vertical spans are well-sourced (see §11.1 and §3.2 VI_V_VIDEO). PAL is not. The following is observed but not independently verified.

**Unknown:**
- Whether a PAL libultra interlaced ceiling exists equivalent to NTSC's 474.
- Whether 288 lines is fully drawable in PAL progressive (Rasky states 640×288 as conventional output; libdragon behavior unverified as of March 2026).
- Whether 576 active half-lines is achievable in PAL interlaced on retail or homebrew.
- The Dreamcast has a documented limitation of 264 lines in 288p and 512/528 lines in 576i (JunkerHQ). No equivalent N64 limitation is documented.
- Whether Blast Corps PAL's 236-line progressive reading is a VI crop/scissor artifact or a genuine framebuffer size.

**Suggested verification paths:**
- Build and test the 240p test suite for N64 (updates pending release as of March 2026).
- paraLLEl-RDP printf readout of PAL framebuffer dimensions for titles of interest.
- Expanded MiSTer signal detection pass across PAL retail library.
- Consult lidnariq or Rasky directly on PAL drawable line ceiling.

### 14.2 PAL Sync Leap Register Behavior

Zoinkity flags VI_H_SYNC_LEAP register behavior for PAL as uncertain and defers to experts. The document's LEAP Register entry covers the software-visible B-A-B-A-B sequence correctly but does not explain the underlying hardware mechanism. Needs expert verification. Lidnariq is the suggested source.

### 14.3 X1/X2/U7/U15 Body Text Audit

Following correction of §3.4 footnote ¹, a full audit pass is required on all body text references to X1, X2, U7, and U15. The old incorrect assumption was that X1/U7 is universal across all regions. The correct model is: NTSC and PAL-M use X1/U7; PAL uses X2/U15. Flag and correct any instance that does not reflect this.

### 14.4 §7.2 References Audit

§7.2 is currently one of the more LLM-heavy sections. Issues include:
- Inconsistent description length and register across entries.
- Some epistemic notes in entry descriptions that belong in copilot-instructions.md rather than a public reference list.
- The MX8330MC datasheet entry carries a long parenthetical that should be trimmed.
- Citation format not fully consistent across subsections.

Recommend a human author pass: trim to a consistent minimal format of title, link where applicable, and one-line scope note.

---

## 15. Repository Structure

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

## 16. Tiny notes

### 16.1 Document authority

The text between the following lines used to be at the end of the document (roughly. I edited it ~Elle):

---

**Document Authority Chain:** Primary Sources (Official documentation, ITU standards, datasheets, patents)  
↓  
Mathematical Derivations 
↓  
N64_Timing_Reference.md

---

I didn't like it there anymore. But I want to keep the wording here at the end of this instruction sheet.


### 16.1 README Refuse

## Hardware Specifics

Progressive modes include an extra half-line (526 for NTSC/PAL-M, 626 for PAL) to suppress interlace artifacts, resulting in a refresh rate slightly below the standard 60,000/1,001 Hz. PAL-M uses a distinct integer divisor of 3091 VI clocks per line. All NTSC derivations are based on the canonical 315/22 MHz crystal oscillator, not the commonly cited approximation of 14.318 MHz.

## Example
```cpp
// NTSC Progressive: 2,250,000 / 37,609 Hz
double frame_duration_ns = (37609.0 / 2250000.0) * 1e9; 
// Result: ~16,715,111.11 ns
```

Precision is only preserved if your implementation carries it.  
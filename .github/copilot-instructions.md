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

## 0. Recent Session Notes — 2026.03.04

### 0.1 Changes Applied This Session

- **LEAP_A / LEAP_B labels corrected throughout:** libdragon `vi.h` register presets confirm LEAP_A (upper bits 27:16) stores 3183 → effective L+6; LEAP_B (lower bits 11:0) stores 3182 → effective L+5. Sequence is A-B-A-B-A, not B-A-B-A-B. Corrected in §5.2.1 and LEAP glossary entry. The arithmetic was correct throughout; only the labels were inverted.
- **libdragon `vi.h` added to §7.2:** Primary source for PAL LEAP register values (vi_pal_p and vi_pal_i presets). Added directly beneath N64brew Video Interface entry.
- **N64brew LEAP prose error identified (not corrected in their wiki):** N64brew's explanatory note states average 5,6,5,6,5 = 5.4, yielding 27 extra clocks — which does not produce exact 15,625 Hz. Their register values are correct; their bit-assignment labels (LEAP_A / LEAP_B) are swapped. Document's arithmetic confirmed correct independently.
- **LEAP glossary sentence repaired:** Broken embedded-quote artifact removed. fH result (15,625 Hz) restored per session flag.
- **§4.1.1 `(may?)` resolved:** "randomly fails" confirmed as lidnariq's phrasing. Artifact removed.
- **§4.1.1 capitalization fixed:** "Relatedly, If" → "Relatedly, if".
- **§1.3 renamed:** "Distinctions and Hazards" → "Conventions". TOC slug updated.
- **§6 Conversion Reference:** Second paragraph and bullet combo rewritten for clarity. Sneaky em dash removed; comma substituted.

### 0.2 Previous Session Notes — 2026.03.03 (Session 2)

- **Stage → Cycle throughout:** "Stage" replaced with "cycle" (lowercase) as the canonical term for one step of the 4-cycle VDC bus group.
- **H_START:** Backtick code-blocking removed from all four occurrences. Plain ALLCAPS, consistent with N64brew convention.
- **§5.3.1 notation fix:** `f_H_ntsc` / `f_H_pal-m` corrected to `fH_NTSC` / `fH_PAL-M`.
- **VDC_DSYNC blanking behavior: resolved.** Phase-correction hypothesis retired. Source: lidnariq, N64brew.dev Video DAC page. Research obligation closed.
- **Figure 2d caption simplified.** Figure 2e caption updated: YOUT and VOUT identified and sourced.
- **Glossary trimming pass completed.**

### 0.3 Previous Session Notes — 2026.03.03 (Session 1)

- **§1.1 Terminology:** X1/X2 wording corrected.
- **§1.3:** Restructured. §1.3.3 Modes and §1.3.4 Hazards collapsed.
- **§3.4:** Substantially rewritten. "Free-running" removed throughout.
- **§3.5 / §3.6 renumbering:** All cross-references updated.
- **§5.1 fH derivation:** `× 1,000,000` mid-chain violation corrected.
- **§7.2 References:** Full formatting pass.
- **Quick-Reference-LaTeX-Tables.md:** Headers expanded.

## 1. Document Status

### 1.1 Milestone

The document has reached effective finalization: no detected language or math errors. Formatting is consistent throughout. Near-100% of remaining improvements are tag:enhancement. Preparing for:

A) Peer audit submission (Robert Peip, lidnariq, Rasky, kev4cards)
B) Spin-off draft for N64brew.dev wiki

### 1.2 Open Items

Cleared!

### 1.3 Research Obligations

**PAL LEAP behavior expansion.** Resolved. libdragon `vi.h` register presets confirm LEAP_A = L+6, LEAP_B = L+5, sequence A-B-A-B-A, producing exactly 28 extra clocks over 5 fields and exact fH = 15,625 Hz. Research obligation closed.  

**S-RGB A NUS datasheet sourcing.** The S-RGB A NUS encoder (NUS-CPU(R)-01, French market) is documented in body text via the QUAKEMASTER RGB mod guide and NFGGames forum discussion. No datasheet or primary hardware documentation has been located. One further sourcing attempt is warranted before this is formally closed as unresolvable.

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

On NUS-CPU-01 through NUS-CPU-07:
- U7 (MX8330MC) is driven by crystal X1. Handles NTSC and PAL-M. FSEL high → 17/5 multiplier.
- U15 (MX8330MC) is driven by crystal X2. Handles PAL. FSEL low → 14/5 multiplier.
- Each chip outputs FSC (input crystal ÷ 4, chroma subcarrier reference) and FSO (Rambus clock).
- FSO/5 is output from a dedicated pin on each chip and drives the video domain.

On NUS-CPU-08 onward: single MX8350 replaces twin MX8330MCs. Derived values unaffected.

**X2 is the PAL video crystal. It is not unrelated to video timing.** Any body text implying X1/U7 is universal must be corrected. The full document has been audited; the model is consistent throughout as of this handoff.

### 8.2 VDC_DSYNC Behavior — Resolved

VDC_DSYNC going low defines cycle 0 of the 4-cycle VDC bus group. During active video it asserts low once every four VI clocks. During blanking, VDC_DSYNC is held low continuously, allowing the VI to transmit control signals (VSync, HSync, colorburst clamp, CSync) on every VI clock.

Source: lidnariq, N64brew.dev Video DAC page — "The Video Interface relies on being able to send control signals (VSync, HSync, 'clamp'=colorburst, CSync) every VI clock during blanking by keeping the !DSYNC input low for multiple clocks in a row."

The phase-correction hypothesis is retired. The blanking behavior is fully accounted for by the control signal transmission requirement. Do not reintroduce phase-walk framing.

### 8.3 Naive Phase-Walk Values (L mod 4)

> Human note: This is basically bullshit. Trivia that doesn't make the cut. In actual fact, the VDC_DSYNC signal *must* remain low during blanking periods, so there is no relevance to tracking phase-walking - this isn't strictly "free-running" at all. ~Elle 

- NTSC: 3094 mod 4 = 2
- PAL: 3178 mod 4 = 2
- PAL-M: 3091 mod 4 = 3

These are arithmetic facts about line boundary alignment and remain correct. The prior framing — that VDC_DSYNC blanking behavior exists to correct this offset — is retired. The offset exists; its effect on video output is not the mechanism driving blanking behavior.

Human note: This is basically bullshit. Trivia that doesn't make the cut. In actual fact, the VDC_DSYNC signal *must* remain low during blanking periods, so there is no relevance to tracking phase-walking - this isn't strictly "free-running" at all.

### 8.4 ENC-NUS Output Identification

YOUT, VOUT, and COUT on the ENC-NUS (U5) are identified as follows:

YOUT = luminance output, S-Video Y channel
VOUT = composite video output
COUT = chrominance output, S-Video C channel

Confirmed via three independent lines of evidence:

BA7242F datasheet (Rohm): Pin table explicitly identifies pin 13 as YOUT (luminance output), pin 12 as VOUT (composite video output), pin 10 as COUT (chrominance output). Primary source — this is the actual chip.
RWeick NUS-CPU-03 schematic (Figure 2e): YOUT, VOUT, and COUT net routing traced to Multi-AV connector pins 7 (LUMINANCE), 9 (COMPOSITE VIDEO), and 8 (CHROMINANCE) respectively.
DENC-NUS pinout, Tim Worthington (Figure 2f): Equivalent successor chip labels the same functional pins VIDEO and LUMA explicitly.

SCIN (pin 8) receives U7.FSC via R13 (4.3 kΩ) / R12 (850 Ω) divider and C21. Confirmed by schematic; corroborated by BA7242F datasheet SCIN input level specification (0.45–0.60 VP-P).

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

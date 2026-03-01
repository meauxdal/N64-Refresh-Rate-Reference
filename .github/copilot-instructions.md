# N64 Video Timing Document — Style & Architecture Guide (/.github/copilot-instructions.md)

*Revision Date: 2026-03-01*

This document defines the permanent technical, stylistic, and epistemic ground truth for the N64 video timing manuscript. It is the authoritative reference for all edits.

General guidelines:
**No LaTeX. No em dashes. No en dashes. Minimal bolding. Minimal bullet points. Minimal numerical lists. Italics only for soft annotative notes. Blockquotes only for asides. Footnotes where appropriate; don't overuse. Prefer prose. All mathematical notation must conform to the canon defined herein. Fractions fully carried through all calculations. No floating-point math (decimals only used for representation and legibility).**

Philosophical guideline:
**Every word is a liability.** If we don't know, we research. If we can't verify, we don't imply we can.

A-B-C-D-E consistency mnemonic:
A) Analyze conventions
B) Be on the look out for outliers
C) Cognitively reason about them
D) Decide on action
E) Execute and iterate

Caution words:
* "Master clock" - do not re-insert. f_xtal = master crystal frequency. "System Master Clock" is used once in a header row to align with primary sources and should be left unaltered.
* "Beat" - never used in current revision, do not re-insert. "Stage" is used.
* "Line" or "scanline" is used sparingly, strongly prefer use of atomic, canonical hardware unit "half-line" (S). This is somewhat flexible as long as ambiguity is mitigated.
* "Field" - avoid in LEAP and vertical timing derivations. The half-line model (S) is canonical. "Per S half-lines" is the correct framing; "per field" introduces a broadcast-domain concept that conflicts with the hardware-native unit. Exception: acceptable in prose when describing the B-A-B-A-B sequence in plain English, provided S is already established in context.
* "Frame" - avoid wherever possible to prevent ambiguity, as above.

Guidance for LLMs specifically:
Line endings use two spaces. **Retain these when editing in-place, but never add these to newly emitted text.** This is an authorship fingerprint. Exception: when emitting figures, ensure double-spaced line endings to force newline behavior in Markdown renderers.

---

## 1. Core Notation Canon

This is the non-negotiable standard for all mathematical and technical symbols.

*   `f_xtal`: Master crystal frequency (Hz).
*   `f_vi`: VI clock frequency (~48 MHz). The underscore is retained.
*   `fH`: Horizontal scan frequency (line frequency). Replaces `f_line` universally.
*   `fV`: Vertical scan frequency (refresh rate). No underscore.
*   `fS`: Subcarrier frequency (broadcast engineering variable, used in §4.2.1 context only).
*   `f_colorburst`: The hardware derivation primitive for the same physical signal as `fS`. Used in §5 derivations. On first use in each §5 derivation, it must be annotated `(fS)`.

## 2. Derivation Convention

All frequencies inside derivation chains must be expressed in Hz.

**Rule:**
1.  Resolve MHz to Hz at the point of entry into a derivation chain.
2.  Once inside the chain, all `=` lines carry Hz without further annotation.
3.  Do not insert `× 1,000,000` mid-chain.

## 3. DSYNC and VI Pixel Group Logic

This section defines the established hardware behavior and supersedes any prior "rounding" language.

**Core Facts:**
*   `VDC_DSYNC` is a free-running clock at `f_vi ÷ 4`. It does not reset at `HSYNC`.
*   Line boundaries are not aligned to the 4-stage `DSYNC` group boundaries.
*   `HSYNC` events are communicated via data bits during an active `DSYNC` Stage 0 stage.
*   The visualization's horizontal units represent the full line duration, including any partial terminal group, reflecting the hardware reality that `L` is not always divisible by 4.

## 4. Conversion Table Semantics

The tables in §6 express **duration multipliers**, not frequency ratios. The correct semantic is:

> Multiply the source duration by the cell value at `[From row, To column]` to obtain the equivalent destination duration.

**Example:**
PAL-I `1:23:45` (5,025 s) × `37,609 / 45,000` ≈ `4,200.8` s ≈ `1:10:01` NTSC-P equivalent.

## 5. Epistemic Policy for Initialisms

Body text uses expanded initialisms without qualification. The epistemic burden (the proof of why an expansion is correct) is carried exclusively in the **§7.2 References** section.

**Established Expansions & Confidence Level:**
*   `FSEL` (Frequency Select): **Explicit** in datasheet.
*   `FSC` (Subcarrier Frequency): **Corroborated** by Nintendo diagnostics and schematics.
*   `FSO` (Frequency Synthesizer Output): **Inferred** from functional description; corroborated by schematics.
*   `SCIN` (Subcarrier Input): **Inferred** from schematic position and diagnostic logic.

## 6. Register vs. Hardware Signal Distinction

Programmer-visible register states and hardware-generated signals must not be conflated.
*   `VI_V_TOTAL` and `VI_H_TOTAL` are registers defining terminal counts.
*   `CSYNC` and `BFP` are hardware-generated signals with no register state.
*   **Rule:** Be precise. Do not mix these concepts in tables. Use prose to distinguish them where necessary. All register values are terminal-counted; clarity is required to prevent off-by-one errors.

## 7. Editorial Policy

### 7.1 Em Dashes
**No em or en dashes are permitted in the document.**
*   They are treated as a forensic marker of unreviewed LLM output. Neither `—` nor `–` may be used.
*   Use semicolons, colons, or restructure the sentence.
*   A simple space-hyphen-space (`-`) is acceptable only if structurally unavoidable for parenthetical asides.

### 7.2 Tone
*   **Technical & Declarative:** State facts directly.
*   **Objective:** No rhetorical framing or conversational asides.
*   **Precise:** No speculative language outside of explicitly marked and sourced inferences (per §5).

### 7.3 Misc
*   No LaTeX.
*   Minimal bolding, minimal bullet points, minimal numerical lists.
*   Prefer integrating loose info into prose where suitable.
*   Register names and signal names are *always* `code blocked` in prose. No exceptions.
*   Caution required regarding intermingling of register names and effective values (registers are terminal-counted; effective values are not) - both formatting consistency and clarity are key.
*   Division operators follow a context rule: `/` is used for fraction notation in derivation chains, tables, and inline mathematical expressions. `÷` is used in prose when describing hardware signal relationships in natural language (e.g., "FSO ÷ 5", "f_xtal ÷ 4"). Do not normalize these to a single symbol.

## 8. Pending Items
* Glossary insertion and finalization.
* Table of contents generation.
* Final tone/style audit by human author.

### 8.1
* Symbol audit: consistency through the following:
=, ≈, ≠, <, >, +, -, ×, ÷, ±, ∈, {,}, [,]

**Notes:**
* Prose uses `÷` for division and `/` for fractions, while tables, code blocks and derivations use `/` for both.
* Code block division identified by space-padded ` / ` pattern; fraction notation uses unpadded `/`.

## 9. Repository structure

```
N64-Refresh-Rate-Reference/
├── .github/
│   └── copilot-instructions.md       ← this file
├── docs/
│   ├── Glossary.md
│   ├── Quick-Reference-LaTeX-Tables.md
│   ├── WIP_N64-Repair-Docs-Summary.docx
│   └── [ITU-R standards PDFs]
├── figures/
│   └── fig1–fig22.*                  ← all figures and figure-PDFs
├── tools/
│   └── canonical_values.json
├── N64_Timing_Reference.md
└── README.md
```

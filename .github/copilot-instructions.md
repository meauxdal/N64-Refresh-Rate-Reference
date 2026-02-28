# Copilot Instructions: N64 Timing Reference

## Project Philosophy

This repository derives Nintendo 64 video timing constants from hardware-authoritative integers, with no floating-point values in the derivation chain. Decimals appear only as final representations. Every value must be traceable to a physical constant, register value, or irreducible fraction — not approximated from secondary sources or common knowledge.

This standard is non-negotiable. If a value cannot be derived from hardware, it does not belong in the document.

## Repository Structure

- `N64_Timing_Reference.md` — The primary document. Full derivations, hardware specifications, signal analysis, and empirical findings. Start here.
- `tools/canonical_values.json` — Machine-readable irreducible fractions for all timing constants. Authoritative source for calculations and code generation. Always prefer these over derived or approximated values.
- `docs/LaTeX-matrix.md` — Conversion matrix in LaTeX format for academic and documentation use.
- `docs/LaTeX-tables-v2.md` — Conversion tables in LaTeX format.

The LaTeX documents and JSON are correct and present but not yet formally integrated into the main document. They are authoritative companions for repository explorers and tool authors.

## Canonical Values and Fractions

All timing constants are stored and referenced as irreducible fractions. The reasoning is not stylistic — integer ratios carry no precision loss through calculation chains that floating-point representations cannot guarantee.

**Always use `tools/canonical_values.json` for calculations.** Do not derive values from the decimal representations in the markdown tables; these are display values only.

Example:
```cpp
// NTSC Progressive: 2,250,000 / 37,609 Hz
// Use canonical fraction — never the decimal approximation
frame_duration_ns = (37609.0 / 2250000.0) * 1e9;
```

## Register Naming Conventions

The document uses **N64brew naming conventions** throughout. SDK equivalents are documented in §1.3 for cross-reference. When adding content, always use N64brew names as primary with SDK names noted parenthetically if relevant.

Key registers:

| N64brew | SDK | Notes |
|---|---|---|
| `VI_V_TOTAL` | `VI_V_SYNC_REG` | Terminal count; effective = REG + 1 |
| `VI_H_TOTAL` | `VI_H_SYNC_REG` | Terminal count; effective = REG + 1 |
| `VI_H_TOTAL_LEAP` | `VI_H_SYNC_LEAP_REG` | PAL compensation; LEAP_A [27:16], LEAP_B [11:0] |

**Critical:** Registers are terminal-counted. Always add 1 when deriving effective counts. This is a common source of error.

## Mode Distinctions

Three television standards (NTSC, PAL, PAL-M) × two scan types (progressive, interlaced) = six timing configurations. Each has distinct crystal frequencies, VI clock divisors, and line counts. Do not conflate them.

### Half-Line Counting

The half-line is the atomic unit for VI registers. Progressive and interlaced modes differ by exactly one half-line in their frame structure:

- **Interlaced:** 525 half-lines (NTSC), 625 half-lines (PAL)
- **Progressive:** 526 half-lines (NTSC), 626 half-lines (PAL)

The ~0.12 Hz difference between NTSC progressive and interlaced field rates is entirely and exactly the consequence of this single additional half-line. No other factor contributes. This is derived in §6.1.

### PAL LEAP Mechanism

PAL progressive requires a hardware compensation mechanism (`VI_H_TOTAL_LEAP`) to maintain the exact 15,625 Hz line frequency. The LEAP register alternates scanline duration by ±1 VI clock in a repeating 5-field B-A-B-A-B sequence. This keeps the total half-line count constant while correcting the fractional error from integer register constraints. See §6.2.1.

### PAL-M Colorburst Precision

PAL-M timing carries a 127/143 fractional remainder from the colorburst definition (227.25 × f_H). This remainder must be preserved through the entire derivation chain. The canonical crystal frequency is **2,045,250,000 / 143 Hz** — not the rounded 14,302,444 Hz or the datasheet approximation of 14.302446 MHz. All PAL-M derivations use the colorburst-derived canonical value. See §6.3.

## Empirical Findings (§3.7.1)

The document includes empirical GBS-C telemetry data from real hardware. This section is living and will be updated as more unit data is collected. Key points for contributors:

- Measurements are taken via GBS-Control firmware reading the Tvia TV5725 ASIC's IF test bus (`IF_TEST_SEL = 3`)
- The instrument has been validated against OSSC community reports, VirtualDub capture framerate detection, and Saturn control group measurements
- Observed crystal offsets on NUS-CPU-03 units: +20 ppm and +26 ppm — within the ±30 ppm commodity AT-cut crystal tolerance
- These offsets are unit-specific crystal variance, not systematic design bias
- Do not conflate measured unit frequencies with canonical derived values — both are documented and distinct

## Derivation Standards

When adding or modifying derivations:

1. Begin from a hardware-authoritative constant (crystal frequency, colorburst frequency, register value)
2. Carry exact fractions through every step
3. Reduce fractions fully at each stage — note reductions explicitly
4. Express decimals only at the final step, to 10 significant figures (.10f)
5. Annotate with `(exact)`, `(reduced)`, `(canonical value)`, or `(≈)` as appropriate — see §1.2
6. Do not cite secondary sources for constants that can be derived from hardware

## Tone and Precision Standard

The document is a primary technical reference, not a tutorial. Prose is precise and terse. Claims are sourced or derived — never asserted. Speculation is explicitly labelled as such and scoped appropriately.

When something is unknown, say so directly. When something requires direct measurement to confirm, say that too. The document's credibility depends on the gap between what is known and what is claimed remaining zero.

---

*For questions about conventions or derivation methodology, consult `N64_Timing_Reference.md` §1–§3 before asking the user.*

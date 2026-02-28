# Copilot Instructions: N64 Timing Reference

## Project Philosophy

This repository derives Nintendo 64 video timing constants from hardware-authoritative integers, with no floating-point values in the derivation chain. Decimals appear only as final representations. Every value must be traceable to a physical constant, register value, or irreducible fraction - not approximated from secondary sources or common knowledge.

This standard is non-negotiable. If a value cannot be derived from hardware, it does not belong in the document.

## Repository Layout

```
N64-Refresh-Rate-Reference/
├── .github/
│   └── copilot-instructions.md       ← this file
├── docs/
│   ├── LaTeX-matrix.md
│   ├── LaTeX-tables-v2.md
│   └── [ITU-R standards PDFs]
├── tools/
│   └── canonical_values.json
├── fig*.png                          ← all figures at root level
├── HBI.pdf
├── VBI-625-PAL.pdf
├── N64_Timing_Reference.md
└── README.md
```

- `N64_Timing_Reference.md` - The primary document. Full derivations, hardware specifications, signal analysis, and empirical findings. Start here.
- `tools/canonical_values.json` - Machine-readable irreducible fractions for all timing constants. Authoritative source for calculations and code generation. Always prefer these over derived or approximated values.
- `docs/LaTeX-matrix.md` - Conversion matrix in LaTeX format for academic and documentation use.
- `docs/LaTeX-tables-v2.md` - Conversion tables in LaTeX format.

The LaTeX documents and JSON are correct and present but not yet formally integrated into the main document. They are authoritative companions for repository explorers and tool authors.

## Figure Inventory and Numbering

All figures referenced in the document are listed in §7.1. The repository retains figure image files even after they are removed from document references - the repo serves as a source archive. Do not infer that an image file is unused just because it lacks a current document reference.

Current figure assignment (as of 2026-02-28):

| Figure | Filename | Description |
| :--- | :--- | :--- |
| Figure 1 | `fig1_clock_gen_schematic.png` | N64 Clock Generation Circuits - U7 (NTSC/PAL-M) and U15 (PAL). RWeick, NUS-CPU-03 |
| Figure 1a | `fig6_mx8350_table.png` | MX8350 output frequencies for NTSC/PAL/MPAL. MX8350 datasheet |
| Figure 1b | `fig12_mx8330mc_rev_e.png` | MX8330MC Rev. E startup transient and feedback divider. MX8330MC datasheet |
| Figure 2 | `fig2_rcp_schematic.png` | RCP-NUS pinout - VDC timing outputs. RWeick, NUS-CPU-03 |
| Figure 2a | `fig9_rcp_vdc_schematic.png` | VDC pin assignments - 7-bit digital output. RWeick, NUS-CPU-03 |
| Figure 2b | `fig13_n64videosys.png` | N64 Video System - 4-beat VDC bus protocol and DSYNC waveform. Tim Worthington, N64RGB |
| Figure 2c | `fig14_vdc-nus.png` | VDC-NUS (BU9801F) pinout. Tim Worthington, N64RGB |
| Figure 2d | `fig18_VDC-NUS.png` | VDC-NUS (BU9801F, U4) in circuit - digital input and analog output stage. RWeick, NUS-CPU-03 |
| Figure 2e | `fig17_ENC-NUS.png` | ENC-NUS (U5) in circuit - RGB termination, SCIN subcarrier injection via U7.FSC, YOUT/VOUT outputs. RWeick, NUS-CPU-03 |
| Figure 2f | `fig15_denc-nus.png` | DENC-NUS pinout (alternate revision encoder). Tim Worthington, N64RGB |
| Figure 2g | `fig16_mav-nus.png` | MAV-NUS pinout (alternate revision encoder). Tim Worthington, N64RGB |
| Figure 3 | `fig3_n64_default_libdragon_240p_timing.png` | N64 VI Timing Diagram, NTSC Progressive. lidnariq, hardware probing |
| Figure 3alt | `fig3-alt_n64_default_libdragon_240p_timing_2x.png` | Same as Figure 3 at 2× scale |

Other image files present in the repository but not currently referenced in the document (retained as source material):

| Filename | Notes |
| :--- | :--- |
| `fig4_relationship_of_fS_to_fH.png` | fS/fH ratio table scan. Wooding, *The Amateur TV Compendium*, p. 55. Superseded by inline Markdown table in §4.2.1 |
| `fig5_mx8350_description.png` | MX8350 chip description extract. MX8350 datasheet |
| `fig7_mx8330MC_description.png` | MX8330MC chip description extract. MX8330MC datasheet |
| `fig8_mx8330MC_table.png` | MX8330MC frequency table. MX8330MC datasheet |
| `fig10_broadcast_signal_reference.png` | Broadcast signal reference material |
| `fig11_N64-diagram-copetti.org.png` | N64 system diagram. copetti.org |

Next available figure numbers: **Figure 4** (unassigned at root level), **Figure 2h** if a further NUS-CPU-01–04 encoder figure is added.

## Canonical Values and Fractions

All timing constants are stored and referenced as irreducible fractions. The reasoning is not stylistic - integer ratios carry no precision loss through calculation chains that floating-point representations cannot guarantee.

**Always use `tools/canonical_values.json` for calculations.** Do not derive values from the decimal representations in the markdown tables; these are display values only.

Example:
```cpp
// NTSC Progressive: 2,250,000 / 37,609 Hz
// Use canonical fraction - never the decimal approximation
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

PAL-M timing carries a 127/143 fractional remainder from the colorburst definition (227.25 × f_H). This remainder must be preserved through the entire derivation chain. The canonical crystal frequency is **2,045,250,000 / 143 Hz** - not the rounded 14,302,444 Hz or the datasheet approximation of 14.302446 MHz. All PAL-M derivations use the colorburst-derived canonical value. See §6.3.

## Hardware Signal Path (NUS-CPU-01 through NUS-CPU-04)

The two-stage analog output chain on early board revisions is fully illustrated in the document:

1. **U7 (MX8330MC)** generates f_xtal (master clock) and FSC (subcarrier reference)
2. **U9 (RCP-NUS)** counts VI clocks, asserts VDC_DSYNC and 7-bit VDC data
3. **U4 (VDC-NUS / BU9801F)** receives VDC bus, converts to analog RGB + CSYNC + BFP; CLK input driven by U7.FSO/5 via R28 (0 Ω) - see Figure 2d
4. **U5 (ENC-NUS)** receives analog RGB through 110 Ω termination and 1 µF coupling capacitors; receives subcarrier reference on SCIN (pin 8) from U7.FSC via R13/R12 divider and C21; outputs YOUT and VOUT - see Figure 2e

The SCIN → U7.FSC path is the hardware route by which the crystal-derived subcarrier frequency enters the analog encode stage. This ties Figure 2e directly to the fS/fH relationships in §4.2.1.

Later revisions (DENC-NUS, AVDC-NUS, MAV-NUS) consolidate U4+U5 into a single chip. This is not known to affect timing values.

## Empirical Findings (§3.7.1)

The document includes empirical GBS-C telemetry data from real hardware. This section is living and will be updated as more unit data is collected. Key points for contributors:

- Measurements are taken via GBS-Control firmware reading the Tvia TV5725 ASIC's IF test bus (`IF_TEST_SEL = 3`)
- The instrument has been validated against OSSC community reports, VirtualDub capture framerate detection, and Saturn control group measurements
- Observed crystal offsets on NUS-CPU-03 units: +20 ppm and +26 ppm - within the ±30 ppm commodity AT-cut crystal tolerance
- These offsets are unit-specific crystal variance, not systematic design bias
- Do not conflate measured unit frequencies with canonical derived values - both are documented and distinct

## Derivation Standards

When adding or modifying derivations:

1. Begin from a hardware-authoritative constant (crystal frequency, colorburst frequency, register value)
2. Carry exact fractions through every step
3. Reduce fractions fully at each stage - note reductions explicitly
4. Express decimals only at the final step, to 10 significant figures (.10f)
5. Annotate with `(exact)`, `(reduced)`, `(canonical value)`, or `(≈)` as appropriate - see §1.2
6. Do not cite secondary sources for constants that can be derived from hardware

## Tone and Precision Standard

The document is a primary technical reference, not a tutorial. Prose is precise and terse. Claims are sourced or derived - never asserted. Speculation is explicitly labelled as such and scoped appropriately.

When something is unknown, say so directly. When something requires direct measurement to confirm, say that too. The document's credibility depends on the gap between what is known and what is claimed remaining zero.

## Session History (for continuity)

**2026-02-28:**
- Removed Figure 4 (`fig4_relationship_of_fS_to_fH.png`) from document references. Image retained in repo. Source attribution ("Wooding, M., *The Amateur TV Compendium*, p. 55") preserved as table caption in §4.2.1.
- Added Figure 2d (`fig18_VDC-NUS.png`) - VDC-NUS in circuit, from RWeick NUS-CPU-03 schematic
- Added Figure 2e (`fig17_ENC-NUS.png`) - ENC-NUS in circuit, from RWeick NUS-CPU-03 schematic
- Renumbered former Figure 2d (DENC-NUS pinout) → Figure 2f; former Figure 2e (MAV-NUS pinout) → Figure 2g
- Added cross-reference note in §4.2.1 linking SCIN/U7.FSC hardware path to the subcarrier frequency discussion
- Updated §7.1 Visual References table to reflect all figure changes
- Corrected figure filenames throughout to match actual on-disk names (`fig17_ENC-NUS.png`, `fig18_VDC-NUS.png`, `fig3-alt_...`, `fig11_N64-diagram-copetti.org.png`)
- Updated this handoff sheet with correct repo layout, paths, and filename corrections

---

*For questions about conventions or derivation methodology, consult `N64_Timing_Reference.md` §1–§3 before asking the user.*

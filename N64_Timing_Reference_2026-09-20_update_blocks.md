# N64 Timing Reference — 2026-09-20 update blocks

These are drop-in revisions for `N64_Timing_Reference_rewrite_fleshed.md` on the `rewrite` branch. They update the working rewrite against the newer Clock Timing research, newer Video DAC research, the current revision sheet, and current libdragon `preview`/legacy `trunk` behavior.

The existing retail/libultra timing derivations in §§4–5 should remain. The important correction is to stop treating the old libdragon timing table as current `preview` behavior.

---

## 1. §2 Signal Path — replace the VDC-bus / output-path discussion

Keep the two opening figures, then replace the prose beginning with “The VDC bus carries” through the existing output-path discussion with the following.

### Replacement text

The VI presents a 7-bit synchronous video bus (`D0`–`D6`) plus `!DSYNC` to the video DAC. The DAC operates at four times the emitted pixel rate: four consecutive VI clock cycles form one output pixel.

* 1 emitted pixel = 4 VI clocks
* 7 bits × 3 color channels = 21-bit RGB

During active video, the four-cycle group is:

|  | Cycle 0 | Cycle 1 | Cycle 2 | Cycle 3 |
|:--|:--:|:--:|:--:|:--:|
| `!DSYNC` | **Low** | **High** | **High** | **High** |
| `D0` | `!Csync` | Red 0 | Green 0 | Blue 0 |
| `D1` | `!Hsync` | Red 1 | Green 1 | Blue 1 |
| `D2` | `!Clamp` | Red 2 | Green 2 | Blue 2 |
| `D3` | `!Vsync` | Red 3 | Green 3 | Blue 3 |
| `D4` | — | Red 4 | Green 4 | Blue 4 |
| `D5` | — | Red 5 | Green 5 | Blue 5 |
| `D6` | — | Red 6 | Green 6 | Blue 6 |

`!DSYNC` low identifies a control cycle and restarts the four-cycle sequence. During blanking, the VI can hold `!DSYNC` low across consecutive VI clocks so that control state is transmitted every clock rather than once per four-clock pixel group.

`!Clamp` is asserted during the horizontal back porch to restore the black-level reference of the AC-coupled analog signal. Colorburst is present during the same general interval, hence the common “clamp/burst” terminology.

The bus therefore carries 28 bit-times per emitted pixel (7 bits × 4 cycles). Twenty-one bit-times carry RGB data. Four bit positions in cycle 0 carry control state; the remaining three cycle-0 bit positions are unused. The resulting RGB precision is 7 bits per channel, or 21-bit RGB.

The analog implementation varies by motherboard revision, but the digital VI timing model is unchanged:

| Video output path | Board family | Region | Function / output |
|:--|:--|:--|:--|
| `VDC-NUS` / `VDC-NUS A` + `ENC-NUS` | NUS-CPU-01 through -04; NUS-CPU(M)-01 through -02 | NTSC, PAL-M | Two-stage path. VDC-NUS converts the VI bus to analog RGB and produces CSYNC/BFP; ENC-NUS encodes composite and S-Video. |
| `VDC-NUS` / `VDC-NUS A` + `S-RGB A` | NUS-CPU(R)-01 | PAL, NUS-001(FRA) | Two-stage path. S-RGB A can encode RGB, but the retail board omits the required RGB output amplification. It does not encode S-Video, leaving an unmodified console with composite output only. |
| `DENC-NUS` | NUS-CPU(P)-01 | PAL except NUS-001(FRA) | Integrated video DAC and encoder; composite and S-Video are generated internally. |
| `AVDC-NUS` | Early NUS-CPU-05 | NTSC | Integrated video DAC, video encoder, and audio DAC; composite and S-Video. |
| `MAV-NUS` | Later NUS-CPU-05 and all later revisions | All regions | Pin-compatible successor to AVDC-NUS combining video DAC, encoder, and audio DAC; composite and S-Video encoding internally. |

On PAL NUS-CPU(P)-03 and -03-1 boards, the MAV-NUS still provides the relevant encoded video signals internally, but board-level Y/C routing and supporting components to the Multi Out are omitted. These revisions therefore lack stock S-Video output; it can be restored by tapping the MAV-NUS output and restoring the missing path.

For the discrete VDC-NUS path, the signal sequence is:

1. **Source:** regional X1 drives the AV clock synthesizer.
2. **Clock synthesis:** the synthesizer produces VCLK for the VI/video DAC and FSC for the encoder; see [§3.1](#31-crystal-1-x1).
3. **Counting:** the VI uses `VI_H_TOTAL`, `VI_H_TOTAL_LEAP`, and `VI_V_TOTAL` to generate raster timing.
4. **Serialization:** the VI multiplexes control and 21-bit RGB over `D0`–`D6` and `!DSYNC` in the four-clock sequence above.
5. **Analog conversion / encoding:** VDC-NUS produces analog RGB, CSYNC, and BFP for ENC-NUS. Integrated DENC-NUS, AVDC-NUS, and MAV-NUS combine the corresponding conversion/encoding functions internally.

The component substitutions alter the physical output path, not the X1/VCLK relationship or VI register timing derived in this document.

### Keep / revise existing footnotes

Keep the existing `[^clamp]` note only if its wording does not duplicate the replacement text. Replace the existing `[^srgb-a]` note with a shorter board-specific note if desired:

```markdown
[^srgb-a]: S-RGB A is observed only on PAL NUS-CPU(R)-01 / NUS-001(FRA). The encoder is RGB-capable, but the retail motherboard leaves the required RGB amplification components unpopulated. S-RGB A does not encode S-Video.
```

A useful additional footnote for the late PAL S-Video omission is:

```markdown
[^pal-svideo]: PAL NUS-CPU(P)-03 and -03-1 omit the board-level Y/C path from MAV-NUS to the Multi Out. The traces are severed and supporting components are unpopulated; S-Video can be restored by tapping the MAV-NUS and restoring the missing path.
```

---

## 2. §3.1.3 Clock Generator Hardware Revisions — replace the current paragraph

### Replacement text

Early N64 boards use separate single-channel synthesizers for the X1 and X2 domains. X1 feeds the AV-domain synthesizer at U7; X2 feeds the RDRAM-domain synthesizer at U15. The earliest boards use MX8330MC. Intermediate revisions substitute MX9911MC at U7; because MX9911MC lacks the RSL-level `FSO` output, it is suitable for the AV/X1 position but not as a direct replacement for the X2/RDRAM synthesizer. Later boards consolidate both domains into the dual-channel MX8350 at U17.

The population change does not occur at one universal motherboard revision number across all regions:

* **NTSC:** early revisions use MX8330MC. MX9911MC is confirmed in the intermediate pre-MX8350 generation, including NUS-CPU-05/-05-1; NUS-CPU-08 and later use MX8350. Transition-era NUS-CPU-04 population should not be used as a hard boundary without a board-level observation.
* **PAL:** NUS-CPU(P)-01 spans the discrete-synthesizer era, with MX8330MC and MX9911MC populations observed. NUS-CPU(P)-02 and later use the integrated MX8350 generation.
* **PAL-M:** NUS-CPU(M)-01 and -02 are confirmed with MX8330MC; NUS-CPU(M)-03 is confirmed with MX9911MC. The currently documented M-04 and M-05 revisions lack sufficiently complete board photography to place the transition exactly; M-05-1 belongs to the later integrated-synthesizer generation.

These hardware substitutions do not change the regional X1 frequency relationships: FSC remains X1 ÷ 4 and VCLK remains X1 × 17 ÷ 5 for NTSC/PAL-M or X1 × 14 ÷ 5 for PAL.

### Small preceding edit

Change:

> Later board revisions consolidate the previously separate X1 and X2 synthesizers into this dual-channel MX8350 package...

To:

> Later board revisions consolidate the previously separate X1 and X2 synthesizers into this dual-channel MX8350 package. The transition occurs at different motherboard revisions by region; see [§3.1.3](#313-clock-generator-hardware-revisions).

---

## 3. §5 Derived Timing Reference — scope the existing tables explicitly

Do **not** replace the existing NTSC/PAL/PAL-M values in §§4–5 with current libdragon-preview values. Those sections already represent the retail/libultra timing family and remain useful as the hardware/reference derivation.

Replace the opening paragraph of §5 with:

```markdown
This section collects the nominal results derived in [§4](#4-mathematical-derivations) for the retail/libultra timing configurations. SDK-specific alternative timing presets are kept separate in [Appendix B](#appendix-b-vi-modes). In particular, current libdragon `preview` uses a different PAL-M horizontal timing preset; its values should not be read back into the retail/libultra PAL-M derivations below.
```

Change the opening sentence under **Refresh Rate Reference** from:

> The table lists refresh rates ($f_V$) for retail video modes.

To:

> The table lists nominal refresh rates ($f_V$) for the retail/libultra timing configurations derived above.

This preserves the existing PAL-M figures:

* retail/libultra progressive: ≈ 59.8370742270 Hz
* retail/libultra interlaced: ≈ 59.9702194092 Hz

while allowing the current libdragon-preview values to coexist without contradiction.

---

## 4. Appendix B.3 — replace the entire current libdragon section

### B.3 Libdragon VI Mode Definitions

libdragon has two timing families relevant to existing software: the current `preview` implementation and the older `trunk` implementation used by already-built software and stable-branch source trees. They should be documented separately rather than treating the older table as current `preview` behavior.

As of September 20, 2026, libdragon PR #1006 (“branch unity”) proposes merging the current `preview` tree into `trunk`, with the stated goal that the resulting tree be equal to current `preview`. The `preview` README has already been rewritten around a single-version model in which individual APIs are marked stable or preview, while the current `trunk` README still documents the older two-branch model. The branch names below therefore identify the source state being documented, not a permanent architectural distinction. Existing ROMs remain relevant because their VI register programming does not change unless the program is rebuilt or patched.

#### B.3.1 Current `preview` timing presets

Current `preview` separates base TV timing from framebuffer configuration. `VI_TIMING_NTSC`, `VI_TIMING_PAL`, and `VI_TIMING_MPAL` establish timing; interlace is then enabled separately by `vi_set_interlaced()`, which sets `VI_CTRL_SERRATE` and changes the low bit of `VI_V_TOTAL`.

Values below are **effective VI clocks / half-lines** after terminal-count conversion. The leap pair is shown in the rewrite's existing `(A, B)` presentation convention; libdragon's helper-macro parameter naming should not be used to silently rename the document's established A/B nomenclature. This distinction does not affect the current PAL-M preset because both leap values are equal.

| Region | Scan Type | VSYNC ($S$) | HSYNC (TOTAL, pattern) | LEAP (A, B) |
|:--|:--|--:|:--|:--|
| NTSC | Progressive | 526 | 3094, 0 | 3094, 3094 |
| NTSC | Interlaced | 525 | 3094, 0 | 3094, 3094 |
| PAL | Progressive | 626 | 3178, 21 | 3183, 3184 |
| PAL | Interlaced | 625 | 3178, 21 | 3183, 3184 |
| PAL-M | Progressive | 526 | **3091, 0** | **3098, 3098** |
| PAL-M | Interlaced | 525 | **3091, 0** | **3098, 3098** |

The current PAL-M preset is therefore neither of the older libdragon `trunk` PAL-M presets. Its source constants are:

```c
.vi_h_total      = VI_H_TOTAL_SET(0b00000, 772.75),
.vi_h_total_leap = VI_H_TOTAL_LEAP_SET(774.50, 774.50),
.vi_v_total      = VI_V_TOTAL_SET(526),
```

Because the horizontal values are expressed in quarter-pixel units, these correspond to a 3,091-VI-clock base line and 3,098-VI-clock leap line. The same horizontal preset is used for progressive and interlaced output; interlace changes the vertical count from 526 to 525 effective half-lines.

Using the exact nominal PAL-M hardware VCLK from [§3.1](#31-crystal-1-x1),

$$
f_{VI}=\frac{6{,}953{,}850{,}000}{143}\ \text{Hz},
$$

the current `preview` preset gives:

| PAL-M `preview` mode | Nominal $f_H$ | Nominal $f_V$ |
|:--|--:|--:|
| Progressive | ≈ 15,732.0941292 Hz | $\dfrac{6{,}817{,}500}{113{,}971}$ Hz ≈ **59.8178484000 Hz** |
| Interlaced | ≈ 15,732.0938712 Hz | $\dfrac{13{,}907{,}700{,}000}{232{,}058{,}827}$ Hz ≈ **59.9317861759 Hz** |

These are libdragon-`preview` timing results, not replacements for the retail/libultra PAL-M values in §§4–5.

The source currently comments that `(774.00, 774.00)` can be slightly more stable for interlaced PAL-M over composite, but the programmed preset remains `(774.50, 774.50)`.

When PAL-M interlace is active, `preview` also alternates `VI_V_BURST` between two values on successive fields. The source identifies this as a workaround for a PAL-M VI bug on older boards such as NUS-CPU-02, where a fixed `V_BURST` can produce garbled interlaced output.

#### B.3.2 Legacy `trunk` timing presets

The pre-branch-unity `trunk` source uses separate complete `vi_config_t` presets for progressive and interlaced modes. The PAL-M values are the same values previously listed in this rewrite:

| Region | Scan Type | VSYNC ($S$) | HSYNC (TOTAL, pattern) | LEAP (A, B) |
|:--|:--|--:|:--|:--|
| NTSC | Progressive | 526 | 3094, 0 | 3094, 3094 |
| NTSC | Interlaced | 525 | 3094, 0 | 3094, 3094 |
| PAL | Progressive | 626 | 3178, 21 | 3183, 3184 |
| PAL | Interlaced | 625 | 3178, 21 | 3183, 3184 |
| PAL-M | Progressive | 526 | 3090, 4 | 3099, 3098 |
| PAL-M | Interlaced | 525 | 3089, 0 | 3101, 3101 |

This code path also contains the PAL-M interlaced `VI_V_BURST` field-alternation workaround.

For archival timing analysis, the distinction matters even if `trunk` later converges with `preview`: software already compiled against the older presets continues to program the older values unless it is rebuilt or explicitly patched.

#### B.3.3 Source-state identifiers

For reproducibility, the relevant source states on September 20, 2026 are:

* `preview` branch head: `39d0d6096130836a65710da6730290701d060272`
* `trunk` branch head: `e356bf3f56f7afbf7e5246329562f145965cfdfc`
* open PR #1006: `branch unity: Merge preview into trunk`

Pinning these identifiers is preferable to describing either branch as permanently “current” or “deprecated.”

---

## 5. Glossary — surgical corrections

### Replace `$L$ (VI Clocks per Line)`

```markdown
* **$L$ (VI Clocks per Line):** Symbol for the number of VI clock cycles that constitute one full horizontal scanline, as defined by `VI_H_TOTAL` plus any applicable `VI_H_TOTAL_LEAP` adjustment. `VI_H_TOTAL` itself uses terminal-count convention. The retail/libultra base values used in §§4–5 are 3,094 (NTSC), 3,178 (PAL), and 3,090 (PAL-M progressive) / 3,089 (PAL-M interlaced). SDK-specific presets may differ; current libdragon `preview`, for example, uses a 3,091-clock PAL-M base line for both scan types. *See also: Terminal Count, VI, Appendix B.*
```

### Replace `PAL-M (MPAL)`

```markdown
* **PAL-M (MPAL):** The Brazilian System-M television standard using PAL color encoding. Its chroma subcarrier is $511{,}312{,}500/143$ Hz and the N64 X1 target is $2{,}045{,}250{,}000/143$ Hz. The retail/libultra timing family uses a 3,090-clock progressive base line and a 3,089-clock interlaced base line with distinct leap configurations; other software-defined VI presets can differ. Commonly called MPAL in N64 software and documentation. *See also: NTSC, PAL, Appendix B.*
```

### Replace `MX8350`

```markdown
* **MX8350:** Dual-channel Macronix clock synthesizer integrating the separate X1 and X2 synthesizer functions used by earlier boards. The transition is region-dependent rather than universally “NUS-CPU-08 onward”: NUS-CPU-08 is the NTSC boundary; PAL reaches the MX8350 generation by NUS-CPU(P)-02; the PAL-M transition lies after the confirmed MX9911MC-equipped NUS-CPU(M)-03, with incomplete evidence for M-04/M-05 and the later integrated generation represented by M-05-1. Derived X1/VCLK values are unchanged. *Physical chips are marked MX8350MC; datasheet part number is MX8350. See also: MX8330MC, MX9911MC.*
```

### Replace `MX9911MC`

```markdown
* **MX9911MC:** Single-channel Macronix clock synthesizer used in the intermediate AV/X1 clock-generator generation. Unlike MX8330MC, its RSL-level `FSO` pin is internally not connected; FSC, FSO/5, and FSEL behavior remain suitable for the U7 AV clock domain. Its motherboard range is region-dependent and should not be reduced to one universal revision interval. *See also: MX8330MC, MX8350, Crystal Oscillator Frequency.*
```

### Replace the video-chip-family entry

```markdown
* **VDC-NUS / VDC-NUS A / ENC-NUS / S-RGB A / DENC-NUS / AVDC-NUS / MAV-NUS:** N64 video-output components that convert the VI's 7-bit synchronous digital bus into analog video. Early NTSC and PAL-M boards use a discrete VDC-NUS + ENC-NUS path; NUS-CPU(R)-01 uses VDC-NUS + S-RGB A; NUS-CPU(P)-01 uses DENC-NUS; early NUS-CPU-05 uses AVDC-NUS; later integrated revisions use MAV-NUS. The VI sends one 21-bit RGB pixel across four VI clocks. These component changes affect the physical conversion/encoding path, not the digital VI timing derivations. *See §2.*
```

---

## 6. §8.1 References — update libdragon links

Replace the current libdragon source entries with pinned/currently descriptive ones:

```markdown
* [Libdragon](https://libdragon.dev/) - Open-source N64 SDK.
* [Libdragon - `src/vi.c`, preview source state 2026-09-20](https://github.com/DragonMinded/libdragon/blob/39d0d6096130836a65710da6730290701d060272/src/vi.c) - Current preview timing presets, interlace handling, refresh-rate helper, and PAL-M `V_BURST` workaround.
* [Libdragon - `include/vi.h`, preview source state 2026-09-20](https://github.com/DragonMinded/libdragon/blob/39d0d6096130836a65710da6730290701d060272/include/vi.h) - VI register field macros and terminal/quarter-pixel conversion.
* [Libdragon - `src/vi.h`, trunk source state 2026-09-20](https://github.com/DragonMinded/libdragon/blob/e356bf3f56f7afbf7e5246329562f145965cfdfc/src/vi.h) - Legacy trunk VI register presets, including separate PAL-M progressive/interlaced timing.
* [Libdragon - `src/display.c`, trunk source state 2026-09-20](https://github.com/DragonMinded/libdragon/blob/e356bf3f56f7afbf7e5246329562f145965cfdfc/src/display.c) - Legacy trunk display initialization and PAL-M interlaced `V_BURST` workaround.
* [Libdragon PR #1006 - branch unity: Merge preview into trunk](https://github.com/DragonMinded/libdragon/pull/1006) - September 2026 proposal to make trunk equal the current preview tree.
```

The old pinned “main branch” wording should be removed; `trunk` is the branch name used by the repository.

---

## 7. Source consistency notes

The newer Clock Timing material supports the values already used in the rewrite:

* X1-derived FSC = X1 ÷ 4.
* VCLK = X1 × multiplier ÷ 5.
* NTSC/PAL-M select 17× before the ÷5 stage; PAL selects 14×.
* Nominal VCLK: NTSC 48.68181818 MHz; PAL 49.65653 MHz; PAL-M 48.62832167 MHz.
* X2 = 250/17 MHz; RCLK = 250 MHz; MClock = 62.5 MHz; nominal VR4300 PClock = 93.75 MHz at the retail 3/2 ratio.

No change is therefore needed to the core clock equations. The update is primarily one of hardware-revision precision and SDK timing provenance.

The revision sheet should remain a confidence-aware source: rows explicitly marked inferred or revisions without board photography should not be upgraded to “confirmed” merely to simplify prose. In particular, the exact PAL-M MX9911MC→MX8350 transition should remain open until M-04/M-05 hardware is directly documented.

# N64 Video Timing Reference

Reference sheet for various N64 clock rates, primarily video clocks. Further video timing details and shown work in the [primary document](/N64_Timing_Reference.md).

---

## System Clocks

### X1 Domain

Region | X1 (f_xtal) Fraction | X1 Decimal (MHz)  | M    | VCLK (f_vi) Fraction | VCLK Decimal (MHz)
:----- | :------------------- | :---------------- | :--- | :------------------- | :-----------------
NTSC   | 315/22 MHz           | 14.3181818182     | 17/5 | 5,355/110 MHz        | 48.6818181818
PAL    | 17,734,475 Hz        | 17.734475 (exact) | 14/5 | 49,656,530 Hz        | 49.65653 (exact)
PAL-M  | 2,045,250,000/143 Hz | 14.3024475524     | 17/5 | 6,953,850,000/143 Hz | 48.6283216783


### X2 Domain (Region-Independent)

Clock           | Derivation   | Exact Value | Decimal (MHz)
:-------------- | :----------- | :---------- | :------------------------
X2              | --           | 250/17 MHz  | 14.7058823529
RCLK            | X2 × 17      | 250 MHz     | 250 (exact)
RAC / MClock    | RCLK ÷ 4     | 250/4 MHz   | 62.5 (exact)
CPU (nominal)   | MClock × 3/2 | 750/8 MHz   | 93.75 (nominal)[^divmode]
SI              | MClock ÷ 4   | 250/16 MHz  | 15.625 (exact)
Cartridge / PIF | SI ÷ 8       | 250/128 MHz | 1.953125 (exact)


[^divmode]: CPU clock is software-configurable via DivMode registers. 93.75 MHz is the nominal operating frequency.

---

## Video Timing

### Per-Mode Timing Values

Resolutions reflect standard libultra VI modes as used by retail software.[^retail]

Mode  | Scan        | Resolution | L    | S   | fH (Fraction)                   | fH (Hz, Decimal)  | fV (Fraction)                | fV (Hz, Decimal)
:---- | :---------- | :--------- | :--- | :-- | :------------------------------ | :---------------- | :--------------------------- | :---------------
NTSC  | Progressive | 640×240p   | 3094 | 526 | 2,250,000 / 143                 | 15,734.2657342657 | 2,250,000 / 37,609           | 59.8261054535
NTSC  | Interlaced  | 640×480i   | 3094 | 525 | 2,250,000 / 143                 | 15,734.2657342657 | 60,000 / 1,001               | 59.9400599401
PAL   | Progressive | 640×288p   | 3178 | 626 | 15,625 / 1                      | 15,625 (exact)    | 15,625 / 313                 | 49.9201277955
PAL   | Interlaced  | 640×576i   | 3178 | 625 | 15,625 / 1                      | 15,625 (exact)    | 50 / 1                       | 50 (exact)
PAL-M | Progressive | 640×240p   | 3090 | 526 | 4,572,156,375,000 / 290,532,671 | 15,737.1505217050 | 17,384,625,000 / 290,532,671 | 59.8370742270
PAL-M | Interlaced  | 640×480i   | 3089 | 525 | 71,583,750,000 / 4,547,257      | 15,742.1825949138 | 272,700,000 / 4,547,257      | 59.9702194092


[^retail]: L (VI clocks per line) and S (half-lines per vertical scan) are effective register values. The N64 VI is programmable at the baremetal level; these values do not represent hardware limits.

---

## Subcarrier & Crystal Reference

Standard | f_xtal (Exact)       | fS (Exact)         | fS (Hz, Decimal)     | fS : fH
:------- | :------------------- | :----------------- | :------------------- | :------------
NTSC     | 315/22 MHz           | 315/88 MHz         | 3,579,545.4545...    | 227.5 × fH
PAL      | 17,734,475 Hz        | 17,734,475/4 Hz    | 4,433,618.75 (exact) | 283.7516 × fH
PAL-M    | 2,045,250,000/143 Hz | 511,312,500/143 Hz | 3,575,611.8881...    | 227.25 × fH


---

## VI Register Reference

L and S are effective values (register + 1). LEAP(A, B) values are effective.

Mode              | VI_V_TOTAL      | L (VI_H_TOTAL+1) | LEAP Pattern | LEAP (A, B) | Notes
:---------------- | :-------------- | :--------------- | :----------- | :---------- | :--------------------------
NTSC Progressive  | 0x20D (S = 526) | 3094             | 0b00000 (0)  | 3094, 3094  | No LEAP compensation
NTSC Interlaced   | 0x20C (S = 525) | 3094             | 0b00000 (0)  | 3094, 3094  | No LEAP compensation
PAL Progressive   | 0x271 (S = 626) | 3178             | 0b10101 (21) | 3183, 3184  | SGI 1996 / pre-OS2.0H
PAL Interlaced    | 0x270 (S = 625) | 3178             | 0b10101 (21) | 3183, 3184  | SGI 1996 / pre-OS2.0H
PAL Progressive   | 0x271 (S = 626) | 3178             | 0b10111 (23) | 3182, 3184  | OS2.0H+ (from Feb 24, 1997)
PAL Interlaced    | 0x270 (S = 625) | 3178             | 0b10111 (23) | 3182, 3184  | OS2.0H+ (from Feb 24, 1997)
PAL-M Progressive | 0x20D (S = 526) | 3090             | 0b00100 (4)  | 3099, 3098  |
PAL-M Interlaced  | 0x20C (S = 525) | 3089             | 0b00000 (0)  | 3101, 3101  |


---

## Refresh Rate Conversion

Multipliers convert a time recorded on the *row* hardware to equivalent time on the *column* hardware, assuming game logic is frame-locked.

### Decimal

| From \ To | NTSC-P  | NTSC-I  | PAL-P   | PAL-I   | PAL-M-P | PAL-M-I |
| :-------- | :------ | :------ | :------ | :------ | :------ | :------ |
| NTSC-P    | 1.00000 | 0.99810 | 1.19844 | 1.19652 | 0.99982 | 0.99760 |
| NTSC-I    | 1.00190 | 1.00000 | 1.20072 | 1.19880 | 1.00172 | 0.99950 |
| PAL-P     | 0.83442 | 0.83283 | 1.00000 | 0.99840 | 0.83427 | 0.83242 |
| PAL-I     | 0.83576 | 0.83417 | 1.00160 | 1.00000 | 0.83560 | 0.83375 |
| PAL-M-P   | 1.00018 | 0.99828 | 1.19866 | 1.19674 | 1.00000 | 0.99778 |
| PAL-M-I   | 1.00241 | 1.00050 | 1.20132 | 1.19940 | 1.00223 | 1.00000 |

### Fraction

| From \ To | NTSC-P          | NTSC-I          | PAL-P               | PAL-I               | PAL-M-P             | PAL-M-I           |
| :-------- | :-------------- | :-------------- | :------------------ | :------------------ | :------------------ | :---------------- |
| NTSC-P    | 1/1             | 525/526         | 45072/37609         | 45000/37609         | 4063394/4064139     | 158995/159378     |
| NTSC-I    | 526/525         | 1/1             | 30048/25025         | 1200/1001           | 8126788/8112825     | 31799/31815       |
| PAL-P     | 37609/45072     | 25025/30048     | 1/1                 | 625/626             | 290532671/348248808 | 22736285/27313632 |
| PAL-I     | 37609/45000     | 1001/1200       | 626/625             | 1/1                 | 290532671/347692500 | 4547257/5454000   |
| PAL-M-P   | 4064139/4063394 | 8112825/8126788 | 348248808/290532671 | 347692500/290532671 | 1/1                 | 8108745/8126788   |
| PAL-M-I   | 159378/158995   | 31815/31799     | 27313632/22736285   | 5454000/4547257     | 8126788/8108745     | 1/1               |

---

## Documentation

[`N64_Timing_Reference.md`](N64_Timing_Reference.md) — Derivations, signal analysis, hardware detail, VI modes, crystal corpus  
[`canonical_values.json`](tools/canonical_values.json) — Machine-readable canonical refresh rates

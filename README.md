# N64 Video Timing Reference

Quick reference for N64 clock rates and video timing. Derivations, signal analysis, VI modes, and crystal corpus: [`N64_Timing_Reference.md`](N64_Timing_Reference.md).

---

## System Clocks

### X1 

| Region | $f_{\text{xtal}}$ | $f_{\text{xtal}}$ (MHz) | $M$ | $f_{\text{vi}}$ | $f_{\text{vi}}$ (MHz) |
| :----- | :---------------- | :---------------------- | :-- | :-------------- | :-------------------- |
| NTSC  | $\frac{315}{22}$ MHz           | 14.3181818182 | $\frac{17}{5}$ | $\frac{5{,}355}{110}$ MHz        | 48.6818181818 |
| PAL   | 17,734,475 Hz                  | 17.734475     | $\frac{14}{5}$ | 49,656,530 Hz                    | 49.65653      |
| PAL-M | $\frac{2{,}045{,}250{,}000}{143}$ Hz | 14.3024475524 | $\frac{17}{5}$ | $\frac{6{,}953{,}850{,}000}{143}$ Hz | 48.6283216783 |


### X2 

| Clock           | Derivation          | Exact                  | MHz           |
| :-------------- | :------------------ | :--------------------- | :------------ |
| X2              | —                   | $\frac{250}{17}$ MHz   | 14.7058823529 |
| RCLK            | X2 $\times$ 17      | 250 MHz                | 250           |
| MClock          | RCLK $\div$ 4       | $\frac{250}{4}$ MHz    | 62.5          |
| CPU             | MClock $\times$ 3/2 | $\frac{750}{8}$ MHz    | 93.75 (nominal)[^divmode] |
| SI              | MClock $\div$ 4     | $\frac{250}{16}$ MHz   | 15.625        |
| Cartridge / PIF | SI $\div$ 8         | $\frac{250}{128}$ MHz  | 1.953125      |



[^divmode]: CPU clock is software-configurable via DivMode registers. 93.75 MHz is the nominal operating frequency.

---

## Video Timing

| Mode  | Scan        | Resolution | $L$  | $S$ | $f_H$ (fraction)                                          | $f_H$ (Hz)        | $f_V$ (fraction)                                     | $f_V$ (Hz)    |
| :---- | :---------- | :--------- | :--- | :-- | :-------------------------------------------------------- | :---------------- | :--------------------------------------------------- | :------------ |
| NTSC  | Progressive | 640×240p   | 3094 | 526 | $\frac{2{,}250{,}000}{143}$                               | 15,734.2657342657 | $\frac{2{,}250{,}000}{37{,}609}$                     | 59.8261054535 |
| NTSC  | Interlaced  | 640×480i   | 3094 | 525 | $\frac{2{,}250{,}000}{143}$                               | 15,734.2657342657 | $\frac{60{,}000}{1{,}001}$                           | 59.9400599401 |
| PAL   | Progressive | 640×288p   | 3178 | 626 | $\frac{15{,}625}{1}$                                      | 15,625            | $\frac{15{,}625}{313}$                               | 49.9201277955 |
| PAL   | Interlaced  | 640×576i   | 3178 | 625 | $\frac{15{,}625}{1}$                                      | 15,625            | $\frac{50}{1}$                                       | 50            |
| PAL-M | Progressive | 640×240p   | 3090 | 526 | $\frac{4{,}572{,}156{,}375{,}000}{290{,}532{,}671}$      | 15,737.1505217050 | $\frac{17{,}384{,}625{,}000}{290{,}532{,}671}$       | 59.8370742270 |
| PAL-M | Interlaced  | 640×480i   | 3089 | 525 | $\frac{71{,}583{,}750{,}000}{4{,}547{,}257}$             | 15,742.1825949138 | $\frac{272{,}700{,}000}{4{,}547{,}257}$              | 59.9702194092 |

$L$: VI clocks per line (effective). $S$: half-lines per vertical scan (effective).

---

## Subcarrier & Crystal Reference

| Standard | $f_{\text{xtal}}$                    | $f_S$                              | $f_S$ (Hz)    | $f_S : f_H$          |
| :------- | :----------------------------------- | :--------------------------------- | :------------ | :------------------- |
| NTSC     | $\frac{315}{22}$ MHz                 | $\frac{315}{88}$ MHz               | 3,579,545.4545… | $227.5 \times f_H$  |
| PAL      | 17,734,475 Hz                        | $\frac{17{,}734{,}475}{4}$ Hz      | 4,433,618.75  | $283.7516 \times f_H$ |
| PAL-M    | $\frac{2{,}045{,}250{,}000}{143}$ Hz | $\frac{511{,}312{,}500}{143}$ Hz   | 3,575,611.8881… | $227.25 \times f_H$ |


---

## VI Register Reference

$L$ and $S$ are effective values (register + 1). LEAP(A, B) values are effective.

| Mode              | `VI_V_TOTAL`    | $L$  | LEAP pattern  | LEAP (A, B) | Notes                       |
| :---------------- | :-------------- | :--- | :------------ | :---------- | :-------------------------- |
| NTSC Progressive  | `0x20D` ($S$ = 526) | 3094 | `0b00000` (0)  | 3094, 3094  | No LEAP compensation        |
| NTSC Interlaced   | `0x20C` ($S$ = 525) | 3094 | `0b00000` (0)  | 3094, 3094  | No LEAP compensation        |
| PAL Progressive   | `0x271` ($S$ = 626) | 3178 | `0b10101` (21) | 3183, 3184  | SGI 1996 / pre-OS2.0H       |
| PAL Interlaced    | `0x270` ($S$ = 625) | 3178 | `0b10101` (21) | 3183, 3184  | SGI 1996 / pre-OS2.0H       |
| PAL Progressive   | `0x271` ($S$ = 626) | 3178 | `0b10111` (23) | 3182, 3184  | OS2.0H+ (from Feb 24, 1997) |
| PAL Interlaced    | `0x270` ($S$ = 625) | 3178 | `0b10111` (23) | 3182, 3184  | OS2.0H+ (from Feb 24, 1997) |
| PAL-M Progressive | `0x20D` ($S$ = 526) | 3090 | `0b00100` (4)  | 3099, 3098  |                             |
| PAL-M Interlaced  | `0x20C` ($S$ = 525) | 3089 | `0b00000` (0)  | 3101, 3101  |                             |


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

## Internal Links

[`N64_Timing_Reference.md`](N64_Timing_Reference.md) - Derivations, signal analysis, hardware detail, VI modes, crystal corpus  
[`canonical_values.json`](tools/canonical_values.json) - Machine-readable canonical refresh rates

## External Links

[N64brew.dev Wiki Video DAC page](https://n64brew.dev/wiki/Video_DAC) - Extensive rewrite on the N64brew Video DAC article.
[https://meauxdal.neocities.org/n64-converter](N64 Refresh Rate Conversion Tool) - Convert run times between different N64 regions and video modes.
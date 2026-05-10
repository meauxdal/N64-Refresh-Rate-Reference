# N64 Video Timing Reference

Quick reference for N64 clock rates and video timing. Derivations, signal analysis, VI modes, and crystal corpus: [`N64_Timing_Reference.md`](N64_Timing_Reference.md).

---

## System Clocks

### X1 

| Region |         $f_{\text{XTAL}}$                     | $f_{\text{XTAL}}$ (MHz) |    $M$          |          $f_{\text{VI}}$                      | $f_{\text{VI}}$ (MHz)
| :----: | :-------------------------------------------: | :---------------------: | :-------------: | :-------------------------------------------: | :-------------------:
|  NTSC  |         $\dfrac{315}{22} \text{ MHz}$         |      14.3181818182      | $\dfrac{17}{5}$ |      $\dfrac{5{,}355}{110} \text{ MHz}$       |     48.6818181818
|  PAL   |          $17{,}734{,}475 \text{ Hz}$          |        17.734475        | $\dfrac{14}{5}$ |          $49{,}656{,}530 \text{ Hz}$          |       49.65653
| PAL-M  | $\dfrac{2{,}045{,}250{,}000}{143} \text{ Hz}$ |      14.3024475524      | $\dfrac{17}{5}$ | $\dfrac{6{,}953{,}850{,}000}{143} \text{ Hz}$ |     48.6283216783


### X2 

|      Clock       |             Derivation              | Frequency (MHz)           | Frequency (MHz)
| :--------------: | :---------------------------------: | :-----------------------: | :----------------------:
|        X2        |                 -                   |     $\dfrac{250}{17}$     |      14.7058823529
|       RCLK       |        $\text{X2} \times 17$        |           $250$           |           250
|      MClock      |        $\text{RCLK} \div 4$         |     $\dfrac{125}{2}$      |           62.5
|       CPU        | $\text{MClock} \times \dfrac{3}{2}$ |     $\dfrac{375}{4}$      |     93.75[^divmode]
| Serial Interface |       $\text{MClock} \div 4$        |     $\dfrac{125}{8}$      |          15.625
| Cartridge / PIF  |         $\text{SI} \div 8$          |     $\dfrac{125}{64}$     |         1.953125


[^divmode]: CPU clock ratio is configurable via DivMode pins. 93.75 MHz is the nominal operating frequency.

---

## Video Timing

| Standard | Scan Type   | Resolution | $L$  | $S$ |                 $f_H$ (Hz)                           | $f_H$ (Hz)        |               $f_V$ (Hz)                        |  $f_V$ (Hz)
| :------: | :---------: | :--------: | :--: | :-: | :--------------------------------------------------: | :---------------: | :---------------------------------------------: | :-----------:
|   NTSC   | Progressive |  640×240p  | 3094 | 526 |             $\dfrac{2{,}250{,}000}{143}$             | 15,734.2657342657 |        $\dfrac{2{,}250{,}000}{37{,}609}$        | 59.8261054535
|   NTSC   | Interlaced  |  640×480i  | 3094 | 525 |             $\dfrac{2{,}250{,}000}{143}$             | 15,734.2657342657 |           $\dfrac{60{,}000}{1{,}001}$           | 59.9400599401
|   PAL    | Progressive |  640×288p  | 3178 | 626 |                     ${15{,}625}$                     |      15,625       |             $\dfrac{15{,}625}{313}$             | 49.9201277955
|   PAL    | Interlaced  |  640×576i  | 3178 | 625 |                     ${15{,}625}$                     |      15,625       |                     ${50}$                      |      50
|  PAL-M   | Progressive |  640×240p  | 3090 | 526 | $\dfrac{4{,}572{,}156{,}375{,}000}{290{,}532{,}671}$ | 15,737.1505217050 | $\dfrac{17{,}384{,}625{,}000}{290{,}532{,}671}$ | 59.8370742270
|  PAL-M   | Interlaced  |  640×480i  | 3089 | 525 |    $\dfrac{71{,}583{,}750{,}000}{4{,}547{,}257}$     | 15,742.1825949138 |    $\dfrac{272{,}700{,}000}{4{,}547{,}257}$     | 59.9702194092


See [Note](/N64_Timing_Reference.md#note).

$L$: VI clocks per line (effective). $S$: half-lines per vertical scan (effective).

---

# Subcarrier & Crystal Reference

| Standard |              $f_{\text{XTAL}}$                |                  $f_{SC}$                 |    $f_{SC}$ (Hz)  |    $f_{SC} : f_H$
| :------: | :------------------------------------------:  | :--------------------------------------:  | :---------------: | :-------------------:
| NTSC     |         $\dfrac{315}{22} \text{ MHz}$         |       $\dfrac{315}{88} \text{ MHz}$       | 3,579,545.4545... |  $227.5 \times f_H$
| PAL      |         $17{,}734{,}475 \text{ Hz}$           |  $\dfrac{17{,}734{,}475}{4} \text{ Hz}$   |   4,433,618.75    | $283.7516 \times f_H$
| PAL-M    | $\dfrac{2{,}045{,}250{,}000}{143} \text{ Hz}$ | $\dfrac{511{,}312{,}500}{143} \text{ Hz}$ | 3,575,611.8881... |  $227.25 \times f_H$

---

## VI Register Reference

$L$ and $S$ are effective values (register + 1). LEAP(A, B) values are effective.

| Mode              | `VI_V_TOTAL`        | $L$  | LEAP pattern   | LEAP (A, B) | Notes
| :---------------- | :------------------ | :--- | :------------- | :---------- | :--------------------------
| NTSC Progressive  | `0x20D` ($S$ = 526) | 3094 | `0b00000` (0)  | 3094, 3094  | No LEAP compensation
| NTSC Interlaced   | `0x20C` ($S$ = 525) | 3094 | `0b00000` (0)  | 3094, 3094  | No LEAP compensation
| PAL Progressive   | `0x271` ($S$ = 626) | 3178 | `0b10101` (21) | 3183, 3184  | SGI 1996 / pre-OS2.0H
| PAL Interlaced    | `0x270` ($S$ = 625) | 3178 | `0b10101` (21) | 3183, 3184  | SGI 1996 / pre-OS2.0H
| PAL Progressive   | `0x271` ($S$ = 626) | 3178 | `0b10111` (23) | 3182, 3184  | OS2.0H+ (from Feb 24, 1997)
| PAL Interlaced    | `0x270` ($S$ = 625) | 3178 | `0b10111` (23) | 3182, 3184  | OS2.0H+ (from Feb 24, 1997)
| PAL-M Progressive | `0x20D` ($S$ = 526) | 3090 | `0b00100` (4)  | 3099, 3098  |
| PAL-M Interlaced  | `0x20C` ($S$ = 525) | 3089 | `0b00000` (0)  | 3101, 3101  |

See [Note](/N64_Timing_Reference.md#note).

---

## Refresh Rate Conversion

Multipliers convert a time recorded on the *row* hardware to equivalent time on the *column* hardware, assuming game logic is frame-locked. The [N64 Refresh Rate Conversion Tool](https://meauxdal.neocities.org/n64-converter) can do this for you automatically.

### Decimal

| From \ To | NTSC-P  | NTSC-I  | PAL-P   | PAL-I   | PAL-M-P | PAL-M-I
| :-------- | :------ | :------ | :------ | :------ | :------ | :------
| NTSC-P    | 1.00000 | 0.99810 | 1.19844 | 1.19652 | 0.99982 | 0.99760
| NTSC-I    | 1.00190 | 1.00000 | 1.20072 | 1.19880 | 1.00172 | 0.99950
| PAL-P     | 0.83442 | 0.83283 | 1.00000 | 0.99840 | 0.83427 | 0.83242
| PAL-I     | 0.83576 | 0.83417 | 1.00160 | 1.00000 | 0.83560 | 0.83375
| PAL-M-P   | 1.00018 | 0.99828 | 1.19866 | 1.19674 | 1.00000 | 0.99778
| PAL-M-I   | 1.00241 | 1.00050 | 1.20132 | 1.19940 | 1.00223 | 1.00000

See [Note](/N64_Timing_Reference.md#note).


### Fraction

| From \ To | NTSC-P                     | NTSC-I                     | PAL-P                          | PAL-I                          | PAL-M-P                        | PAL-M-I
| :-------: | :-----------------------:  | :-----------------------:  | :---------------------------:  | :---------------------------:  | :---------------------------:  | :-------------------------:
| NTSC-P    | $1$                        | $\dfrac{525}{526}$         | $\dfrac{45072}{37609}$         | $\dfrac{45000}{37609}$         | $\dfrac{4063394}{4064139}$     | $\dfrac{158995}{159378}$
| NTSC-I    | $\dfrac{526}{525}$         | $1$                        | $\dfrac{30048}{25025}$         | $\dfrac{1200}{1001}$           | $\dfrac{8126788}{8112825}$     | $\dfrac{31799}{31815}$
| PAL-P     | $\dfrac{37609}{45072}$     | $\dfrac{25025}{30048}$     | $1$                            | $\dfrac{625}{626}$             | $\dfrac{290532671}{348248808}$ | $\dfrac{22736285}{27313632}$
| PAL-I     | $\dfrac{37609}{45000}$     | $\dfrac{1001}{1200}$       | $\dfrac{626}{625}$             | $1$                            | $\dfrac{290532671}{347692500}$ | $\dfrac{4547257}{5454000}$
| PAL-M-P   | $\dfrac{4064139}{4063394}$ | $\dfrac{8112825}{8126788}$ | $\dfrac{348248808}{290532671}$ | $\dfrac{347692500}{290532671}$ | $1$                            | $\dfrac{8108745}{8126788}$
| PAL-M-I   | $\dfrac{159378}{158995}$   | $\dfrac{31815}{31799}$     | $\dfrac{27313632}{22736285}$   | $\dfrac{5454000}{4547257}$     | $\dfrac{8126788}{8108745}$     | $1$

See [Note](/N64_Timing_Reference.md#note).

---

## Internal Links

* [`N64_Timing_Reference.md`](N64_Timing_Reference.md) - Derivations, signal analysis, hardware detail, VI modes, crystal corpus  
* [`canonical_values.json`](tools/canonical_values.json) - Machine-readable canonical refresh rates

## External Links

* [N64brew.dev Wiki Video DAC page](https://n64brew.dev/wiki/Video_DAC) - Extensive rewrite of the Video DAC article for the N64brew.dev wiki
* [N64brew.dev Clock Timing DAC page](https://n64brew.dev/wiki/Video_DAC) - New article on N64 Clock Timing for the N64brew.dev wiki
* [N64 Refresh Rate Conversion Tool](https://meauxdal.neocities.org/n64-converter) - Convert run times between different N64 regions and video modes
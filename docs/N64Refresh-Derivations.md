# N64 Refresh Rate Derivations

## **NTSC Derivation**

**Constants:**

```
Color burst frequency: f_colorburst = 315/88 MHz  (≈ 3.5795454545 MHz)
Crystal frequency: f_xtal = 4 × f_colorburst = 315/22 MHz  (≈ 14.3181818182 MHz)
VI clock multiplier: M = 17 / 5
VI clocks per scanline: L = 3,094
Progressive scanlines: S_prog = 526
Interlaced scanlines: S_int = 525
```

**Video clock frequency:**

```
f_vi = f_xtal × M
     = (315/22 MHz) × (17/5)
     = (315 × 17)/(22 × 5) MHz
     = 5,355/110 MHz
     ≈ 48.6818181818 MHz
```

**Horizontal scan frequency:**

```
f_line = f_vi / L
       = (5,355/110 MHz) / 3,094
       = 5,355,000,000 / (110 × 3,094) Hz
       = 5,355,000,000 / 340,340 Hz
       = 591,750,000 / 37,609 Hz (reduced)
       ≈ 15,734.2657342657 Hz
```

**Refresh rate (Progressive):**

Progressive mode: 526 scanlines per vertical scan cycle, scanned sequentially.

```
refresh_rate = f_line / (S_prog / 2)
             = (591,750,000 / 37,609) / (526 / 2)
             = (591,750,000 / 37,609) / 263
             = 591,750,000 / (37,609 × 263)
             = 591,750,000 / 9,891,167
             = 2,250,000 / 37,609  (exact fraction)
             ≈ 59.8261054535 Hz
```

**Refresh rate (Interlaced):**

Interlaced mode: 525 scanlines per vertical scan cycle, alternating between odd and even fields (262.5 scanlines each).

```
refresh_rate = f_line / (S_int / 2)
             = (591,750,000 / 37,609) / (525 / 2)
             = (591,750,000 / 37,609) / 262.5
             = (591,750,000 × 2) / (37,609 × 525)
             = 1,183,500,000 / 19,744,725
             = 60,000 / 1,001  (exact fraction)
             ≈ 59.9400599401 Hz
```

---

## **PAL Derivation**

**Constants:**

```
Color burst frequency: f_colorburst = 17,734,475 / 4 Hz  (≈ 4.4336187500 MHz)
Crystal frequency: f_xtal = 4 × f_colorburst = 17,734,475 Hz  (≈ 17.7344750000 MHz)
VI clock multiplier: M = 14 / 5
VI clocks per scanline: L = 3,178
Progressive scanlines: S_prog = 626
Interlaced scanlines: S_int = 625
```

**Video clock frequency:**

```
f_vi = f_xtal × M
     = 17,734,475 Hz × (14/5)
     = (17,734,475 × 14) / 5 Hz
     = 248,282,650 / 5 Hz
     = 49,656,530 Hz
     = 49.6565300000 MHz  (exact decimal)
```

**Horizontal scan frequency:**

Without LEAP compensation, the theoretical line frequency would be:

```
f_line (theoretical) = f_vi / L
                     = 49,656,530 / 3,178 Hz
                     ≈ 15,625.0881057269 Hz
```					 

The LEAP register compensates for this ~5.6 ppm error by adding fractional VI clocks during vsync, achieving:

```
f_line = 4,890,625 / 313 Hz  (exact fraction)
       = 15,625 Hz  (exact decimal)
```

**Refresh rate (Progressive):**

```
refresh_rate = f_line / (S_prog / 2)
             = (4,890,625 / 313) / (626 / 2)
             = (4,890,625 / 313) / 313
             = 4,890,625 / (313 × 313)
             = 4,890,625 / 97,969
             = 15,625 / 313  (exact fraction)
             ≈ 49.9201277955 Hz
```

**Refresh rate (Interlaced):**

```
refresh_rate = f_line / (S_int / 2)
             = (4,890,625 / 313) / (625 / 2)
             = (4,890,625 × 2) / (313 × 625)
             = 9,781,250 / 195,625
             = 50 / 1  (exact fraction)
             = 50.0000000000 Hz
```

**Notes on LEAP pattern:**

* PAL modes use the VI LEAP register to alternate between two scanline lengths during vsync
* A 5-field repeating pattern alternates between LEAP_A and LEAP_B to add fractional VI clocks and maintain exact PAL broadcast timing (B-A-B-A-B)
* NTSC and PAL-M do not use LEAP (LEAP = 0x00, always uses LEAP_A)

---

## **PAL-M (MPAL) Derivation**

**Constants:**

```
Color burst frequency: f_colorburst = 3,575,611 Hz
Crystal frequency: f_xtal = 4 × f_colorburst = 14,302,444 Hz
VI clock multiplier: M = 17 / 5
VI clocks per scanline: L = 3,091
Progressive scanlines: S_prog = 526
Interlaced scanlines: S_int = 525
```

**Video clock frequency:**

```
f_vi = f_xtal × M
     = 14,302,444 Hz × 3.4
     = 48,628,309.6 Hz
     = 243,141,548 / 5 Hz
     = 48,628,309.6 Hz
     = 48.6283096000 MHz  (exact decimal)
```

**Horizontal scan frequency:**

```
f_line = 243,141,548 / 15,455 Hz  (exact fraction)
       ≈ 15,732.2256874798 Hz
```

**Refresh rate (Progressive):**

```
refresh_rate = f_line / (S_prog / 2)
             = (243,141,548 / 15,455) / (526 / 2)
             = (243,141,548 / 15,455) / 263
             = 243,141,548 / (15,455 × 263)
             = 243,141,548 / 4,064,665  (exact fraction)
             ≈ 59.8183486216 Hz
```

**Refresh rate (Interlaced):**

```
refresh_rate = f_line / (S_int / 2)
             = (243,141,548 / 15,455) / (525 / 2)
             = (243,141,548 × 2) / (15,455 × 525)
             = 486,283,096 / 8,113,875  (exact fraction)
             ≈ 59.9323738480 Hz
```

**Notes:**

* PAL-M does not use LEAP compensation
* Expected VI clocks per scanline is 3090.6 (non-integer), but hardware requires integer divisor

---

## **Summary Table**

| Mode    | Crystal / VI Mult | VI Clocks | Scanlines | Line Freq (Hz) | Refresh Rate (Hz) | Line Freq (Fraction) | Refresh Rate (Fraction) |
| ------- | ----------------- | --------- | --------- | -------------- | ----------------- | -------------------- | ----------------------- |
| NTSC-P  | 4x NTSC × 3.4     | 3,094     | 526       | 15,734.265734  | 59.8261054535     | 591,750,000 / 37,609 | 2,250,000 / 37,609      |
| NTSC-I  | 4x NTSC × 3.4     | 3,094     | 525       | 15,734.265734  | 59.9400599401     | 591,750,000 / 37,609 | 60,000 / 1,001          |
| PAL-P   | 4x PAL × 2.8      | 3,178     | 626       | 15,625.000000  | 49.9201277955     | 4,890,625 / 313      | 15,625 / 313            |
| PAL-I   | 4x PAL × 2.8      | 3,178     | 625       | 15,625.000000  | 50.0000000000     | 4,890,625 / 313      | 50 / 1                  |
| PAL-M-P | 4x MPAL × 3.4     | 3,091     | 526       | 15,732.225687  | 59.8183486216     | 243,141,548 / 15,455 | 243,141,548 / 4,064,665 |
| PAL-M-I | 4x MPAL × 3.4     | 3,091     | 525       | 15,732.225687  | 59.9322883333     | 243,141,548 / 15,455 | 486,283,096 / 8,113,875 |

---

## **Mathematical Relationships**

**General Formula:**

For any video mode:
```
Horizontal scan frequency: f_line = (f_xtal × M) / L

Refresh rate = f_line / (S / 2)
```

Where:
- `f_xtal` = Crystal oscillator frequency (4× color subcarrier)
- `M` = VI clock multiplier (17/5 for NTSC/MPAL, 14/5 for PAL)
- `L` = VI clocks per scanline (3094 for NTSC, 3178 for PAL, 3091 for MPAL)
- `S` = Total scanlines per frame

Division by 2 accounts for the historical broadcast convention where line frequency is defined as scanlines per field period.

**Progressive vs Interlaced:**

- Progressive: All scanlines scanned sequentially in one vertical scan cycle
- Interlaced: Scanlines alternated across two fields (odd field, then even field)
- Both use the same line frequency; different scanline counts yield different refresh rates

**LEAP Pattern (PAL only):**

PAL modes use the LEAP register to alternate scanline lengths during vsync:
- Compensates for PAL's non-integer chroma period to VI clock ratio
- Adds fractional scanline lengths during vsync to achieve exact broadcast timing
- NTSC and PAL-M use LEAP = 0 (no alternation)

---

## **Annotations**

- **(exact fraction)** - Final result expressed as a fraction in lowest terms; stored in canonical_values.json for verification.
- **(exact decimal)** - Decimal representation with no rounding.
- **(reduced)** - Fraction reduced to lowest terms.

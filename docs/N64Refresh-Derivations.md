# N64 Refresh Rate Derivations

## **NTSC Derivation**

**Constants:**

```
Crystal frequency: f_xtal = 4 × f_colorburst_NTSC
VI clock multiplier: M = 17 / 5 = 3.4
VI clocks per scanline: L_prog = 3,094
Progressive scanlines: S_prog = 526
Interlaced scanlines: S_int = 525
```

**Line frequency (fractional):**

```
f_line = (f_xtal × M) / L_prog
       = 591,750,000 / 37,609  (exact fraction)
```

**Refresh Rate (Progressive):**

```
refresh_rate = f_line / S_prog × 2   # doubled per-field to full frame
             = (591,750,000 / 37,609) ÷ 526 × 2
             = (591,750,000 × 2) / (37,609 × 526)
             = 1,183,500,000 / 19,762,934  (exact fraction)
             ≈ 59.8114333002 Hz
```

**Refresh Rate (Interlaced):**

```
refresh_rate = f_line / S_int × 2
             = (591,750,000 / 37,609) ÷ 525 × 2
             = (591,750,000 × 2) / (37,609 × 525)
             = 1,183,500,000 / 19,724,725  (exact fraction)
             ≈ 59.9220529640 Hz
```

---

## **PAL Derivation (after LEAP compensation)**

**Constants:**

```
Crystal frequency: f_xtal = 4 × f_colorburst_PAL
VI clock multiplier: M = 14 / 5 = 2.8
VI clocks per scanline: L_prog = 3,178
Progressive scanlines: S_prog = 626
Interlaced scanlines: S_int = 625
```

**Line frequency (fractional):**

```
f_line = (f_xtal × M) / L_prog
       = 4,890,625 / 313  (exact fraction)
```

**Refresh Rate (Progressive):**

```
refresh_rate = f_line / S_prog × 2
             = (4,890,625 / 313) ÷ 626 × 2
             = (4,890,625 × 2) / (313 × 626)
             = 9,781,250 / 195,638  (exact fraction)
             ≈ 50.0002558884 Hz
```

**Refresh Rate (Interlaced):**

```
refresh_rate = f_line / S_int × 2
             = (4,890,625 / 313) ÷ 625 × 2
             = (4,890,625 × 2) / (313 × 625)
             = 9,781,250 / 195,625  (exact fraction)
             ≈ 50.0000000000 Hz
```

**Notes on LEAP register:**

* The N64 Video Interface LEAP register allows inserting of additional VI clocks to more closely adhere to broadcast standards.
* Small deviation (6 ppm) compensated via LEAP registers without altering L_prog.

---

## **PAL-M (MPAL) Derivation**

**Constants:**

```
Crystal frequency: f_xtal = 4 × f_colorburst_MPAL
VI clock multiplier: M = 17 / 5 = 3.4
VI clocks per scanline: L_prog = 3,091
Progressive scanlines: S_prog = 526
Interlaced scanlines: S_int = 525
```

**Line frequency (fractional):**

```
f_line = (f_xtal × M) / L_prog
       = 243,141,548 / 15,455  (exact fraction)
```

**Refresh Rate (Progressive):**

```
refresh_rate = f_line / S_prog × 2
             = (243,141,548 / 15,455) ÷ 526 × 2
             = (243,141,548 × 2) / (15,455 × 526)
             = 486,283,096 / 8,126,930  (exact fraction)
             ≈ 59.8056780890 Hz
```

**Refresh Rate (Interlaced):**

```
refresh_rate = f_line / S_int × 2
             = (243,141,548 / 15,455) ÷ 525 × 2
             = (243,141,548 × 2) / (15,455 × 525)
             = 486,283,096 / 8,116,375  (exact fraction)
             ≈ 59.8647476960 Hz
```

* PAL-M does not use LEAP compensation
* Expected VI clocks per scanline is 3090.6, but only integers are allowed, so best-fit 3091 is used (~129ppm error)

---

## **Summary Table**

| Mode    | Crystal / VI Mult | VI Clocks | Scanlines | Line Freq (Hz) | Refresh Rate (Hz) | Line Freq (Fraction)  | Refresh Rate (Fraction) |
| ------- | ----------------- | --------- | --------- | -------------- | ----------------- | --------------------- | ----------------------- |
| NTSC-P  | 4x NTSC × 3.4     | 3,094     | 526       | 15,734.265734  | 59.8114333002     | 591,750,000 / 37,609  | 2,250,000 / 37,609      |
| NTSC-I  | 4x NTSC × 3.4     | 3,094     | 525       | 15,734.265734  | 59.9220529640     | 591,750,000 / 188,045 | 4,500,000 / 75,075      |
| PAL-P   | 4x PAL × 2.8      | 3,178     | 626       | 15,625.000000  | 50.0002558884     | 4,890,625 / 313       | 15,625 / 313            |
| PAL-I   | 4x PAL × 2.8      | 3,178     | 625       | 15,625.000000  | 50.0000000000     | 4,890,625 / 313       | 50 / 1                  |
| PAL-M-P | 4x MPAL × 3.4     | 3,091     | 526       | 15,732.225959  | 59.8056780890     | 243,141,548 / 15,455  | 243,141,548 / 4,064,665 |
| PAL-M-I | 4x MPAL × 3.4     | 3,091     | 525       | 15,732.225959  | 59.8647476960     | 243,141,548 / 15,455  | 486,283,096 / 8,113,875 |
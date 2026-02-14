### PAL-M First-Principles Derivation

**Constants:**

```
C      = 1,260,000,000 / 88      ; VI clock constant
M      = 17 / 5                  ; VI multiplier
L      = 3,091                   ; Horizontal pixel unit (PAL-M adjusted)
S_prog = 263                      ; Lines per progressive frame
S_int  = 525 / 2                  ; Lines per interlaced field
```

> **Note:** PAL-M uses NTSC vertical scan (525 lines, 60 Hz) with PAL color encoding. L is slightly different from NTSC to target PAL-M color line frequency accurately.

---

**Line frequency:**

```
f_line = (C × M) / L
       = ((1,260,000,000 / 88) × (17 / 5)) / 3,091
       = 21,420,000,000 / 1,293,080
       = 15,732.224783... Hz  ; exact fraction: 21,420,000,000 / 1,293,080
```

---

**Progressive refresh frequency:**

```
f_refresh_prog = f_line / S_prog
               = (21,420,000,000 / 1,293,080) / 263
               = 21,420,000,000 / (1,293,080 × 263)
               = 21,420,000,000 / 340,072,040
               = 243,141,548 / 4,064,665  ; exact fraction
               ≈ 59.817987218 Hz
```

---

**Interlaced refresh frequency:**

```
f_refresh_int = f_line / S_int
              = (21,420,000,000 / 1,293,080) / (525 / 2)
              = 21,420,000,000 × 2 / (1,293,080 × 525)
              = 42,840,000,000 / 678,801,000
              = 486,283,096 / 8,113,875  ; exact fraction
              ≈ 59.932374437 Hz
```

---

**Time conversion multipliers:**

```
T_int = T_prog × (f_refresh_prog / f_refresh_int)
      = T_prog × (243,141,548 / 4,064,665) ÷ (486,283,096 / 8,113,875)
      = T_prog × (243,141,548 × 8,113,875) / (4,064,665 × 486,283,096)
      = T_prog × 8,128,332 / 8,113,875  ; exact fraction

T_prog = T_int × (f_refresh_int / f_refresh_prog)
       = T_int × (486,283,096 / 8,113,875) ÷ (243,141,548 / 4,064,665)
       = T_int × (486,283,096 × 4,064,665) / (8,113,875 × 243,141,548)
       = T_int × 8,113,875 / 8,128,332  ; exact fraction
```
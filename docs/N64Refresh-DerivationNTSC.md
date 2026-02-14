### NTSC First-Principles Derivation

**Constants:**

```
C      = 1,260,000,000 / 88      ; VI clock constant
M      = 17 / 5                  ; VI multiplier
L      = 3,094                   ; Horizontal pixel unit
S_prog = 263                       ; Lines per progressive frame
S_int  = 525 / 2                   ; Lines per interlaced field
```

**Line frequency:**

```
f_line = (C × M) / L
       = ((1,260,000,000 / 88) × (17 / 5)) / 3,094
       = 21,420,000,000 / 1,361,360
       = 15,734.265734... Hz
```

**Progressive refresh frequency:**

```
f_refresh_prog = f_line / S_prog
               = (21,420,000,000 / 1,361,360) / 263
               = 21,420,000,000 / 357,568,880
               = 2,250,000 / 37,609  ; exact fraction
```

**Interlaced refresh frequency:**

```
f_refresh_int = f_line / S_int
              = (21,420,000,000 / 1,361,360) / (525 / 2)
              = 21,420,000,000 × 2 / (1,361,360 × 525)
              = 42,840,000,000 / 714,240,000
              = 4,500,000 / 75,075  ; exact fraction
```

**Time conversion multipliers:**

```
T_int = T_prog × (f_refresh_prog / f_refresh_int)
      = T_prog × (2,250,000 / 37,609) ÷ (4,500,000 / 75,075)
      = T_prog × (2,250,000 × 75,075) / (4,500,000 × 37,609)
      = T_prog × 75,218 / 75,075  ; exact fraction

T_prog = T_int × (f_refresh_int / f_refresh_prog)
       = T_int × (4,500,000 / 75,075) ÷ (2,250,000 / 37,609)
       = T_int × (4,500,000 × 37,609) / (2,250,000 × 75,075)
       = T_int × 75,075 / 75,218  ; exact fraction
```
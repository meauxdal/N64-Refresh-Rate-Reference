### PAL First-Principles Derivation

**Constants:**

```
C      = 125,000,000 / 1        ; VI clock constant
M      = 1 / 1                  ; VI multiplier
L      = 313                    ; Horizontal pixel unit
S_prog = 50                     ; Lines per progressive frame
S_int  = 100 / 1                ; Lines per interlaced field
```

**Line frequency:**

```
f_line = (C × M) / L
       = (125,000,000 / 1) / 313
       = 125,000,000 / 313
```

**Progressive refresh frequency:**

```
f_refresh_prog = f_line / S_prog
               = (125,000,000 / 313) / 50
               = 125,000,000 / (313 × 50)
               = 125,000,000 / 15,650
               = 15,625 / 313  ; exact fraction
```

**Interlaced refresh frequency:**

```
f_refresh_int = f_line / S_int
              = (125,000,000 / 313) / (100 / 1)
              = 125,000,000 / (313 × 100)
              = 125,000,000 / 31,300
              = 50 / 1  ; exact fraction
```

**Time conversion multipliers:**

```
T_int = T_prog × (f_refresh_prog / f_refresh_int)
      = T_prog × (15,625 / 313) ÷ (50 / 1)
      = T_prog × (15,625 × 1) / (313 × 50)
      = T_prog × 9,765,625 / 9,781,250  ; exact fraction

T_prog = T_int × (f_refresh_int / f_refresh_prog)
       = T_int × (50 / 1) ÷ (15,625 / 313)
       = T_int × (50 × 313) / 15,625
       = T_int × 9,781,250 / 9,765,625  ; exact fraction
```
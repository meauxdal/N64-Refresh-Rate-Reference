# N64 Refresh Rate – Complete Reference

## Legend

- **Lines**: canonical JSON value
- **Line frequency (f_line)**: canonical line frequency from JSON
- **Refresh rate**: derived vertical refresh rate from JSON fraction (~48–61 Hz)

## NTSC-P

### Constants / Canonical Values
- Lines: 526
### Derived Values
- Line frequency: 2250000/143
- Refresh rate: 2250000/37609 ≈ 59.8261054535 Hz
- Notes: 4×NTSC crystal × 3.4, 3094 VI clocks/scanline; exact spec timing

## NTSC-I

### Constants / Canonical Values
- Lines: 525
### Derived Values
- Line frequency: 450000/143
- Refresh rate: 60000/1001 ≈ 59.9400599401 Hz
- Notes: 4×NTSC crystal × 3.4, 3094 VI clocks/scanline; exact spec timing

## PAL-P

### Constants / Canonical Values
- Lines: 626
### Derived Values
- Line frequency: 15625/1
- Refresh rate: 15625/313 ≈ 49.9201277955 Hz
- Notes: 4×PAL crystal × 2.8, 3178 VI clocks/scanline; LEAP applied for exact 50 Hz

## PAL-I

### Constants / Canonical Values
- Lines: 625
### Derived Values
- Line frequency: 7825/1
- Refresh rate: 50/1 ≈ 50.0000000000 Hz
- Notes: 4×PAL crystal × 2.8, 3178 VI clocks/scanline; LEAP applied

## PAL-M-P

### Constants / Canonical Values
- Lines: 526
### Derived Values
- Line frequency: 243141548/15455
- Refresh rate: 243141548/4064665 ≈ 59.8183486216 Hz
- Notes: 4×MPAL crystal × 3.4, 3091 VI clocks/scanline; integer scanline divisor, no LEAP

## PAL-M-I

### Constants / Canonical Values
- Lines: 525
### Derived Values
- Line frequency: 243141548/15455
- Refresh rate: 486283096/8113875 ≈ 59.9322883333 Hz
- Notes: 4×MPAL crystal × 3.4, 3091 VI clocks/scanline; integer divisor, no LEAP

## Master Conversion LUT (Fractions)

| From \ To | NTSC-P | NTSC-I | PAL-P | PAL-I | PAL-M-P | PAL-M-I |
|---|---|---|---|---|---|---|
| NTSC-P | 1/1 | 526/525 | 37609/45072 | 37609/45000 | 790210031/790312500 | 207825238153/207457031250 |
| NTSC-I | 525/526 | 1/1 | 25025/30048 | 1001/1200 | 5531470217/5542725000 | 790210031/790312500 |
| PAL-P | 45072/37609 | 30048/25025 | 1/1 | 626/625 | 76103304524/63510390625 | 152206609048/126779296875 |
| PAL-I | 45000/37609 | 1200/1001 | 625/626 | 1/1 | 121570774/101616625 | 243141548/202846875 |
| PAL-M-P | 790312500/790210031 | 5542725000/5531470217 | 63510390625/76103304524 | 101616625/121570774 | 1/1 | 526/525 |
| PAL-M-I | 207457031250/207825238153 | 790312500/790210031 | 126779296875/152206609048 | 202846875/243141548 | 525/526 | 1/1 |
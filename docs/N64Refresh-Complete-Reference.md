# Complete N64 Refresh Rate

## Quick Reference Conversion Lookup Table (QRCLUT)

| FROM ↓ / TO → | NTSC-P | NTSC-I | PAL-P | PAL-I | PAL-M-P | PAL-M-I |
| ------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| **NTSC-P** | 1. | 1.00190476190476 | 0.8344204827831 | 0.83575555555556 | 1.00048339367299 | 1.00555351895514 |
| **NTSC-I** | 0.99809885931559 | 1. | 0.83000088276836 | 0.41787777777778 | 1. | 1. |
| **PAL-P** | 1.19843654444415 | 1.20481799569252 | 1. | 1.0016 | 1197.99068102170372 | 1199.40737362305981 |
| **PAL-I** | 1.19652210906964 | 2.39304421813928 | 0.99840255591054 | 1. | 0.00083473103409 | 0.00083374508277 |
| **PAL-M-P** | 0.99951683988355 | 1. | 0.00083473103409 | 1.19636697243192 | 1. | 1.00178176272126 |
| **PAL-M-I** | 0.99447715228433 | 1. | 0.00083374508277 | 0.83586393058582 | 0.99822140631067 | 1. |

## NTSC

### Exact Refresh Rates Summary
| Mode        | Exact Fraction | Decimal           |
| ----------- | --------------- | ----------------- |
| Progressive | 2250000 / 37609 | 59.82610545348188 |
| Interlaced  | 4500000 / 75075 | 59.94005994005994 |

### Matrix / Golden Table
| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |
| ------------- | --------------- | --------------- | --------------- | --------------- |
| 591750000 / 37609 | 2250000 / 37609 | 4500000 / 75075 | 75218 / 75075 | 75075 / 75218 |

### Timing Sheet Summary
| Parameter         | Value           | Notes           |
| ----------------- | --------------- | --------------- |
| Lines per frame   | 525 | Derived / JSON |
| Progressive lines | 263 | Derived         |
| Interlaced lines  | 262 | Derived         |
| f_line            | 591750000 / 37609 | Calculated      |
| f_prog            | 2250000 / 37609 | Calculated      |
| f_int             | 4500000 / 75075 | Calculated      |

## PAL

### Exact Refresh Rates Summary
| Mode        | Exact Fraction | Decimal           |
| ----------- | --------------- | ----------------- |
| Progressive | 15625 / 313 | 49.92012779552716 |
| Interlaced  | 50 / 1 | 50.00000000000000 |

### Matrix / Golden Table
| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |
| ------------- | --------------- | --------------- | --------------- | --------------- |
| 4890625 / 313 | 15625 / 313 | 50 / 1 | 626 / 625 | 625 / 626 |

### Timing Sheet Summary
| Parameter         | Value           | Notes           |
| ----------------- | --------------- | --------------- |
| Lines per frame   | 625 | Derived / JSON |
| Progressive lines | 313 | Derived         |
| Interlaced lines  | 312 | Derived         |
| f_line            | 4890625 / 313 | Calculated      |
| f_prog            | 15625 / 313 | Calculated      |
| f_int             | 50 / 1 | Calculated      |

## PAL-M

### Exact Refresh Rates Summary
| Mode        | Exact Fraction | Decimal           |
| ----------- | --------------- | ----------------- |
| Progressive | 243141548 / 4064665 | 59.81834862159612 |
| Interlaced  | 486283096 / 8113875 | 59.93228833325630 |

### Matrix / Golden Table
| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |
| ------------- | --------------- | --------------- | --------------- | --------------- |
| 63946227124 / 4064665 | 243141548 / 4064665 | 486283096 / 8113875 | 8128332 / 8113875 | 8113875 / 8128332 |

### Timing Sheet Summary
| Parameter         | Value           | Notes           |
| ----------------- | --------------- | --------------- |
| Lines per frame   | 525 | Derived / JSON |
| Progressive lines | 263 | Derived         |
| Interlaced lines  | 262 | Derived         |
| f_line            | 63946227124 / 4064665 | Calculated      |
| f_prog            | 243141548 / 4064665 | Calculated      |
| f_int             | 486283096 / 8113875 | Calculated      |

---

### Source and Authority

All refresh rates, conversion multipliers, and derived timing values are computed directly from the canonical JSON:

```
tools/canonical_values.json
```

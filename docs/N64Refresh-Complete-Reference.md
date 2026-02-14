# Complete N64 Refresh Rate

| FROM ↓ / TO → | NTSC-P  | NTSC-I  | PAL-P   | PAL-I   | PAL-M-P | PAL-M-I |
| ------------- | ------- | ------- | ------- | ------- | ------- | ------- |
| **NTSC-P**    | 1.00000 | 1.00190 | 0.83442 | 0.83576 | 1.00048 | 1.00555 |
| **NTSC-I**    | 0.99810 | 1.00000 | 0.83000 | 0.41788 | 1.00000 | 1.00000 |
| **PAL-P**     | 1.19844 | 1.20482 | 1.00000 | 1.00160 | 0.99840 | 0.99831 |
| **PAL-I**     | 1.19652 | 0.99841 | 0.99840 | 1.00000 | 0.99822 | 0.99822 |
| **PAL-M-P**   | 0.99952 | 1.00000 | 1.00160 | 1.19637 | 1.00000 | 1.00178 |
| **PAL-M-I**   | 0.99448 | 1.00000 | 0.99831 | 0.83586 | 0.99822 | 1.00000 |


## NTSC-P

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


## NTSC-I

### Exact Refresh Rates Summary
| Mode        | Exact Fraction | Decimal           |
| ----------- | --------------- | ----------------- |
| Progressive | 4500000 / 75075 | 59.94005994005994 |
| Interlaced  | 4500000 / 75075 | 59.94005994005994 |

### Matrix / Golden Table
| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |
| ------------- | --------------- | --------------- | --------------- | --------------- |
| 591750000 / 37609 | 4500000 / 75075 | 4500000 / 75075 | 75218 / 75075 | 75075 / 75218 |

### Timing Sheet Summary
| Parameter         | Value           | Notes           |
| ----------------- | --------------- | --------------- |
| Lines per frame   | 525 | Derived / JSON |
| Progressive lines | 263 | Derived         |
| Interlaced lines  | 262 | Derived         |
| f_line            | 591750000 / 37609 | Calculated      |
| f_prog            | 4500000 / 75075 | Calculated      |
| f_int             | 4500000 / 75075 | Calculated      |


## PAL-P

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


## PAL-I

### Exact Refresh Rates Summary
| Mode        | Exact Fraction | Decimal           |
| ----------- | --------------- | ----------------- |
| Progressive | 50 / 1 | 50.00000000000000 |
| Interlaced  | 50 / 1 | 50.00000000000000 |

### Matrix / Golden Table
| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |
| ------------- | --------------- | --------------- | --------------- | --------------- |
| 4890625 / 313 | 50 / 1 | 50 / 1 | 626 / 625 | 625 / 626 |

### Timing Sheet Summary
| Parameter         | Value           | Notes           |
| ----------------- | --------------- | --------------- |
| Lines per frame   | 625 | Derived / JSON |
| Progressive lines | 313 | Derived         |
| Interlaced lines  | 312 | Derived         |
| f_line            | 4890625 / 313 | Calculated      |
| f_prog            | 50 / 1 | Calculated      |
| f_int             | 50 / 1 | Calculated      |


## PAL-M-P

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


## PAL-M-I

### Exact Refresh Rates Summary
| Mode        | Exact Fraction | Decimal           |
| ----------- | --------------- | ----------------- |
| Progressive | 486283096 / 8113875 | 59.93228833325630 |
| Interlaced  | 486283096 / 8113875 | 59.93228833325630 |

### Matrix / Golden Table
| f_line        | f_prog          | f_int           | mul_prog_to_int | mul_int_to_prog |
| ------------- | --------------- | --------------- | --------------- | --------------- |
| 63946227124 / 4064665 | 486283096 / 8113875 | 486283096 / 8113875 | 8128332 / 8113875 | 8113875 / 8128332 |

### Timing Sheet Summary
| Parameter         | Value           | Notes           |
| ----------------- | --------------- | --------------- |
| Lines per frame   | 525 | Derived / JSON |
| Progressive lines | 263 | Derived         |
| Interlaced lines  | 262 | Derived         |
| f_line            | 63946227124 / 4064665 | Calculated      |
| f_prog            | 486283096 / 8113875 | Calculated      |
| f_int             | 486283096 / 8113875 | Calculated      |


---

### Source and Authority

All refresh rates, conversion multipliers, and derived timing values are computed directly from the canonical JSON:
`tools/canonical_values.json`

# N64 Refresh Rate Timing Sheet

## NTSC

**NTSC-P**
- Lines: 526
- Line frequency: 2250000/143
- Refresh rate: 2250000/37609 ≈ 59.8261054535 Hz
- Notes: 4×NTSC crystal × 3.4, 3094 VI clocks/scanline; exact spec timing

**NTSC-I**
- Lines: 525
- Line frequency: 450000/143
- Refresh rate: 60000/1001 ≈ 59.9400599401 Hz
- Notes: 4×NTSC crystal × 3.4, 3094 VI clocks/scanline; exact spec timing

## PAL

**PAL-P**
- Lines: 626
- Line frequency: 15625/1
- Refresh rate: 15625/313 ≈ 49.9201277955 Hz
- Notes: 4×PAL crystal × 2.8, 3178 VI clocks/scanline; LEAP applied for exact 50 Hz

**PAL-I**
- Lines: 625
- Line frequency: 7825/1
- Refresh rate: 50/1 ≈ 50.0000000000 Hz
- Notes: 4×PAL crystal × 2.8, 3178 VI clocks/scanline; LEAP applied

## PAL-M

**PAL-M-P**
- Lines: 526
- Line frequency: 243141548/15455
- Refresh rate: 243141548/4064665 ≈ 59.8183486216 Hz
- Notes: 4×MPAL crystal × 3.4, 3091 VI clocks/scanline; integer scanline divisor, no LEAP

**PAL-M-I**
- Lines: 525
- Line frequency: 243141548/15455
- Refresh rate: 486283096/8113875 ≈ 59.9322883333 Hz
- Notes: 4×MPAL crystal × 3.4, 3091 VI clocks/scanline; integer divisor, no LEAP

## Quick Conversion (Decimal, 5 digits)

| From \ To | NTSC-P | NTSC-I | PAL-P | PAL-I | PAL-M-P | PAL-M-I |
|---|---|---|---|---|---|---|
| NTSC-P | 1.00000 | 1.00190 | 0.83442 | 0.83576 | 0.99987 | 1.00177 |
| NTSC-I | 0.99810 | 1.00000 | 0.83283 | 0.83417 | 0.99797 | 0.99987 |
| PAL-P | 1.19844 | 1.20072 | 1.00000 | 1.00160 | 1.19828 | 1.20056 |
| PAL-I | 1.19652 | 1.19880 | 0.99840 | 1.00000 | 1.19637 | 1.19865 |
| PAL-M-P | 1.00013 | 1.00203 | 0.83453 | 0.83586 | 1.00000 | 1.00190 |
| PAL-M-I | 0.99823 | 1.00013 | 0.83294 | 0.83427 | 0.99810 | 1.00000 |

## System Constants / Notes

| Parameter | NTSC-P | NTSC-I | PAL-P | PAL-I | PAL-M-P | PAL-M-I | Notes / Source |
|---|---|---|---|---|---|---|---||
| Lines per frame | 526 | 525 | 626 | 625 | 526 | 525 | BT.470-6 |
| Pixel clock (typical DAC) | ~13.5 MHz | ~13.5 MHz | ~13.5 MHz | ~13.5 MHz | ~13.5 MHz | ~13.5 MHz | MX8350 datasheet |
| Horizontal active video | ~52.7 μs | ~52.7 μs | ~52.7 μs | ~52.7 μs | ~52.7 μs | ~52.7 μs | Derived from VI addendums |
| Horizontal sync pulse | 4.7 μs | 4.7 μs | 4.7 μs | 4.7 μs | 4.7 μs | 4.7 μs | BT.1700/1701 & Addendums |
| Front porch | ~1.5 μs | ~1.5 μs | ~1.5 μs | ~1.5 μs | ~1.5 μs | ~1.5 μs | VI timing register mapping |
| Back porch | ~5.5 μs | ~5.5 μs | ~6 μs | ~6 μs | ~6 μs | ~6 μs | Includes color burst |
| Vertical sync pulse | 2 lines | 2 lines | 2 lines | 2 lines | 2 lines | 2 lines | VI_V_SYNC register |
| Vertical back porch | 18 lines | 18 lines | 20 lines | 20 lines | 20 lines | 20 lines | BT.470-6 / Addendums |
| Vertical front porch | 1 line | 1 line | 1 line | 1 line | 1 line | 1 line | Addendum tables |
| Color subcarrier | 3.579545 MHz | 3.579545 MHz | 4.43361875 MHz | 4.43361875 MHz | 4.43361875 MHz | 4.43361875 MHz | BT.470-6 |
| VI registers mapping | VI_WIDTH, VI_H_SYNC, VI_V_SYNC, VI_BURST | VI_WIDTH, VI_H_SYNC, VI_V_SYNC, VI_BURST | Same | Same | Same | Same | Ultra64 Addendum |
| Active pixels per line | 320–640 | 320–640 | 320–640 | 320–640 | 320–640 | 320–640 | VI allows horizontal scaling |
# N64 Video Timing Reference

Documenting exact refresh rates for Nintendo 64 hardware. Values are derived from targeted broadcast standards, oscillator math, and register logic. Fractions are carried through all calculations for maximum precision.  

## Quick Reference

| Mode  | Scan Type   | Resolution | Refresh Rate (Hz) | Exact Refresh Rate (Hz)      |  
| ---   | ---         | ---        | ---               | ---                          |  
| NTSC  | Progressive | 640x240p   | 59.8261054535     | 2,250,000 / 37,609           |   
| NTSC  | Interlaced  | 640x480i   | 59.9400599401     | 60,000 / 1,001               |  
| PAL   | Progressive | 640x288p   | 49.9201277955     | 15,625 / 313                 |  
| PAL   | Interlaced  | 640x576i   | 50 (exact)        | 50 / 1                       |  
| PAL-M | Progressive | 640x240p   | 59.8370742270     | 17,384,625,000 / 290,532,671 |  
| PAL-M | Interlaced  | 640x480i   | 59.9702194092     | 272,700,000 / 4,547,257      |   

---

[`N64_Timing_Reference.md`](N64_Timing_Reference.md): Primary document  
[`Quick-Reference-LaTeX-Tables.md`](docs/Quick-Reference-LaTeX-Tables.md): LaTeX formatting for more legible fractions  
[`canonical_values.json`](tools/canonical_values.json): Exact refresh rates  

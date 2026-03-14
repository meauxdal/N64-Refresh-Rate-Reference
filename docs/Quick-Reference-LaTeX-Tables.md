<h2 align=center>Quick Reference (/docs/Quick-Reference-LaTeX-Tables.md)</h2>

<h3 align=center>Fundamental Constants</h3>

$$\begin{array}{|l|c|c|c|c|}
\hline
\text{Mode} & f_{\text{xtal}} & \text{M} & \text{L} & \text{S} \\
\hline
\text{NTSC Progressive}  & 315/22 \text{ MHz} & 17/5 & 3094 & 526 \\
\text{NTSC Interlaced}   & 315/22 \text{ MHz} & 17/5 & 3094 & 525 \\
\text{PAL Progressive}   & 17{,}734{,}475 \text{ Hz} & 14/5 & 3178 & 626 \\
\text{PAL Interlaced}    & 17{,}734{,}475 \text{ Hz} & 14/5 & 3178 & 625 \\
\text{PAL-M Progressive} & 2{,}045{,}250{,}000/143 \text{ Hz} & 17/5 & 3090 & 526 \\
\text{PAL-M Interlaced}  & 2{,}045{,}250{,}000/143 \text{ Hz} & 17/5 & 3089 & 525 \\
\hline
\end{array}$$

<h3 align=center>Derived Timing Values</h3>

$$\begin{array}{|l|c|c|}
\hline
\text{Mode} & f_H \text{ (Hz)} & f_V \text{ (Hz)} \\
\hline
\text{NTSC Progressive}  & 2{,}250{,}000/143                     & 2{,}250{,}000/37{,}609       \\
\text{NTSC Interlaced}   & 2{,}250{,}000/143                     & 60{,}000/1{,}001             \\
\text{PAL Progressive}   & 15{,}625/1                            & 15{,}625/313                 \\
\text{PAL Interlaced}    & 15{,}625/1                            & 50/1                         \\
\text{PAL-M Progressive} & 4{,}572{,}156{,}375{,}000/290{,}532{,}671 & 17{,}384{,}625{,}000/290{,}532{,}671 \\
\text{PAL-M Interlaced}  & 71{,}583{,}750{,}000/4{,}547{,}257   & 272{,}700{,}000/4{,}547{,}257 \\
\hline
\end{array}$$

<h3 align=center>Subcarrier Frequency Relationships</h3>

$$\begin{array}{|l|c|}
\hline
\text{Standard} & f_S : f_H \\
\hline
\text{PAL}   & f_S = 283.7516 \times f_H \\
\text{SECAM} & f_S = 282 \times f_H \\
\text{PAL-N} & f_S = 229.2516 \times f_H \\
\text{PAL-M} & f_S = 227.25 \times f_H \\
\text{NTSC}  & f_S = 227.5 \times f_H \\
\hline
\end{array}$$

<h3 align=center>Decimal Conversions</h3>

$$\begin{array}{|l|c|c|c|c|c|c|}
\hline
\text{From} \backslash \text{To} & \text{NTSC-P} & \text{NTSC-I} & \text{PAL-P} & \text{PAL-I} & \text{PAL-M-P} & \text{PAL-M-I} \\
\hline
\text{NTSC-P}  & 1.00000 & 0.99810 & 1.19844 & 1.19652 & 0.99982 & 0.99760 \\
\text{NTSC-I}  & 1.00190 & 1.00000 & 1.20072 & 1.19880 & 1.00172 & 0.99950 \\
\text{PAL-P}   & 0.83442 & 0.83283 & 1.00000 & 0.99840 & 0.83427 & 0.83242 \\
\text{PAL-I}   & 0.83576 & 0.83417 & 1.00160 & 1.00000 & 0.83560 & 0.83375 \\
\text{PAL-M-P} & 1.00018 & 0.99828 & 1.19866 & 1.19674 & 1.00000 & 0.99778 \\
\text{PAL-M-I} & 1.00241 & 1.00050 & 1.20132 & 1.19940 & 1.00223 & 1.00000 \\
\hline
\end{array}$$

<h3 align=center>Exact Fractional Conversions</h3>

$$\begin{array}{|l|c|c|c|c|c|c|}
\hline
\text{From} \backslash \text{To} & \text{NTSC-P} & \text{NTSC-I} & \text{PAL-P} & \text{PAL-I} & \text{PAL-M-P} & \text{PAL-M-I} \\
\hline
\text{NTSC-P}  & 1/1             & 525/526         & 45072/37609         & 45000/37609         & 4063394/4064139     & 158995/159378   \\
\text{NTSC-I}  & 526/525         & 1/1             & 30048/25025         & 1200/1001           & 8126788/8112825     & 31799/31815     \\
\text{PAL-P}   & 37609/45072     & 25025/30048     & 1/1                 & 625/626             & 290532671/348248808 & 22736285/27313632 \\
\text{PAL-I}   & 37609/45000     & 1001/1200       & 626/625             & 1/1                 & 290532671/347692500 & 4547257/5454000 \\
\text{PAL-M-P} & 4064139/4063394 & 8112825/8126788 & 348248808/290532671 & 347692500/290532671 & 1/1                 & 8108745/8126788 \\
\text{PAL-M-I} & 159378/158995   & 31815/31799     & 27313632/22736285   & 5454000/4547257     & 8126788/8108745     & 1/1             \\
\hline
\end{array}$$

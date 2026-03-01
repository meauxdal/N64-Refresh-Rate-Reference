<h1 align=center>Quick Reference (/docs/LaTeX-tables.md)</h1>

<h3 align=center> Fundamental Constants</h3>

$$\begin{array}{|l|c|c|c|c|}
\hline
\text{Mode} & \text{f\_xtal} & \text{M} & \text{L} & \text{S} \\
\hline
\text{NTSC Progressive}  & 315/22 \text{ MHz} & 17/5 & 3094 & 526 \\
\text{NTSC Interlaced}   & 315/22 \text{ MHz} & 17/5 & 3094 & 525 \\
\text{PAL Progressive}   & 17{,}734{,}475/4 \text{ Hz} & 14/5 & 3178 & 626 \\
\text{PAL Interlaced}    & 17{,}734{,}475/4 \text{ Hz} & 14/5 & 3178 & 625 \\
\text{PAL-M Progressive} & 2{,}045{,}250{,}000/143 \text{ Hz} & 17/5 & 3091 & 526 \\
\text{PAL-M Interlaced}  & 2{,}045{,}250{,}000/143 \text{ Hz} & 17/5 & 3091 & 525 \\
\hline
\end{array}$$

<h3 align=center>Derived Timing Values</h3>

$$\begin{array}{|l|c|c|c|c|}
\hline
\text{Mode} & \text{fH (Hz)} & \text{fV Progressive (Hz)} & \text{fV Interlaced (Hz)} \\
\hline
\text{NTSC}  & 2{,}250{,}000/143       & 2{,}250{,}000/37{,}609       & 60{,}000/1{,}001     \\
\text{PAL}   & 15{,}625/1              & 15{,}625/313                 & 50/1                 \\
\text{PAL-M} & 6{,}953{,}850{,}000/442{,}013 & 6{,}953{,}850{,}000/116{,}249{,}419 & 185{,}436{,}000/3{,}094{,}091 \\
\hline
\end{array}$$

<h3 align=center>Subcarrier Frequency Relationships</h3>

$$\begin{array}{|l|c|}
\hline
\text{Standard} & \text{fS : fH} \\
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
\text{NTSC-P}  & 1.00000 & 0.99810 & 1.19844 & 1.19652 & 1.00013 & 0.99823 \\
\text{NTSC-I}  & 1.00190 & 1.00000 & 1.20072 & 1.19880 & 1.00203 & 1.00013 \\
\text{PAL-P}   & 0.83442 & 0.83283 & 1.00000 & 0.99840 & 0.83453 & 0.83294 \\
\text{PAL-I}   & 0.83576 & 0.83417 & 1.00160 & 1.00000 & 0.83586 & 0.83427 \\
\text{PAL-M-P} & 0.99987 & 0.99797 & 1.19828 & 1.19637 & 1.00000 & 0.99810 \\
\text{PAL-M-I} & 1.00178 & 0.99987 & 1.20056 & 1.19865 & 1.00190 & 1.00000 \\
\hline
\end{array}$$

<h3 align=center>Exact Fractional Conversions</h3>

$$\begin{array}{|l|c|c|c|c|c|c|}
\hline
\text{From} \backslash \text{To} & \text{NTSC-P} & \text{NTSC-I} & \text{PAL-P} & \text{PAL-I} & \text{PAL-M-P} & \text{PAL-M-I} \\
\hline
\text{NTSC-P}  & 1/1             & 525/526         & 45072/37609         & 45000/37609         & 15455/15453         & 2704625/2709426     \\
\text{NTSC-I}  & 526/525         & 1/1             & 30048/25025         & 1200/1001           & 1625866/1622565     & 15455/15453         \\
\text{PAL-P}   & 37609/45072     & 25025/30048     & 1/1                 & 625/626             & 581247095/696497616 & 386761375/464331744 \\
\text{PAL-I}   & 37609/45000     & 1001/1200       & 626/625             & 1/1                 & 116249419/139077000 & 3094091/3708720     \\
\text{PAL-M-P} & 15453/15455     & 1622565/1625866 & 696497616/581247095 & 139077000/116249419 & 1/1                 & 525/526             \\
\text{PAL-M-I} & 2709426/2704625 & 15453/15455     & 464331744/386761375 & 3708720/3094091     & 526/525             & 1/1                 \\
\hline
\end{array}$$

# SpyBOAT - Spatial pyBOAT

Small pipeline for the time-frequency analysis of 3D-Stacks (time,Y,X) based on the tools provided by [pyBOAT](https://github.com/tensionhead/pyBOAT). The supplied input movie gets analyzed pixel by pixel along the time axis, yielding up to four output movies:

- phase movie
- period movie
- amplitude movie
- power movie

This is the complete 2D-analogue to the results for univariate time-series provided by pyBOAT.
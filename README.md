# lewin-rhythms
Implementation of Lewin's 1981 "Some Investigations into Foreground Rhythmic and Metric Patterning"

this folder contains some tools implementing the diagrams suggested in Lewin's 1981 "Reflections on Foreground Rhythmic Patterning"

the four files with dates are earlier drafts before I refactored everything.

main_svg and main_table are the two files that generate anything useful. They both output (ie print to stdout, redirect with >foo.html) standard html files that can be opened in a browser. svg generates brackets showing alignments, table generates tables showing the accumulation of rythmic alignments over time. Both have many options, run with -h to see instructions

stretti_lewin is the core of the intelligent stuff. It contains the basic offsets counter as well as some more finicky tools for building tables, making "peaks" bold, etc

the two "tests" files contains some basic tests

"themes" defines theme1 and theme2 as in Canons 1a and 1b of Abrahamsen's Schnee.

Much of the code here is not remotely bulletproof. It all works for its intended purpose when generated from the included theme definitions, but I have not included any type-checks or input validity checks, so things could very easily blow up.

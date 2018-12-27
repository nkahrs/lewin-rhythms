# string all of this together
# according to user arguments, combine the themes, look for common rhythmic alignments, and make an svg

import argparse
from themes import *
from stretti_lewin import *
from svg import *


if __name__ != '__main__':
    exit()

# much of this heavily draws on the python argparse tutorial
parser = argparse.ArgumentParser()

offset = parser.add_mutually_exclusive_group()
offset.add_argument('-X', '--xthemeonly', action="store_true",
                    help="only include theme 1")
offset.add_argument('-Y', '--ythemeonly', action="store_true",
                    help="only include theme 2")
offset.add_argument('-x', '--xthemeoffset', type=int,
                    help="offset for theme 1")
offset.add_argument('-y', '--ythemeoffset', type=int,
                    help="offset for theme 2")

combos = parser.add_mutually_exclusive_group()
combos.add_argument('-d', '--includeduplicates', action="store_true",
                    help="aggregate->aggregate, include duplicates (default)")
combos.add_argument('-e', '--excludeduplicates', action="store_true",
                    help="aggregate->aggregate, exclude duplicates")
combos.add_argument('-s', '--sameonly', action="store_true",
                    help="only theme1->theme1, theme2->theme2")
combos.add_argument('-o', '--otheronly', action="store_true",
                    help="only theme1->theme2, theme2->theme1")

toplot = parser.add_mutually_exclusive_group()
toplot.add_argument('-a', '--plotall', action="store_true",
                    help="plot all common offsets (default)")
toplot.add_argument('-l', '--plotlist',
                    help='plot from list after arg (ie "1,2,3")')
toplot.add_argument('-t', '--threshold', type=int,
                    help="plot if count is above specified threshold")

args = parser.parse_args()

# tests that argument parsing works correctly, can/should be commented out
# print("<!--")
# if args.xthemeoffset:
#     print("x offset", args.xthemeoffset)
# elif args.ythemeoffset:
#     print("y offset", args.ythemeoffset)

# if args.excludeduplicates:
#     print("exclude duplicates")
# elif args.sameonly:
#     print("same only")
# elif args.otheronly:
#     print("other only")
# else:
#     print("include duplicates")

# if args.plotlist:
#     thelist = args.plotlist
#     thelist = thelist.split(',')
#     thelist = list(map(int, thelist))
#     print("plot list", thelist)
# elif args.threshold:
#     print("plot threshold", thelist)
# else:
#     print("plot all")
# print("-->")


# offset themes and plot accordingly
if args.xthemeoffset:
    theme1 = shift_theme(theme1, args.xthemeoffset)
elif args.ythemeoffset:
    theme2 = shift_theme(theme2, args.ythemeoffset)

# plot themes and bars
print('<body> <svg height="4000" width="2000">')
print("<!-- bar numbers -->")
theme2svg(bars, 0, 0, 200, 1, 'silver')
if (not args.xthemeonly):
    print("<!-- theme 2 -->")
    theme2svg(theme2, 0, 50, 50, 1, 'black')
if (not args.ythemeonly):
    print("<!-- theme 1 -->")
    theme2svg(theme1, 0, 100, 50, 1, 'black')


# calculate common offsets
distanceDict = {}
if args.sameonly:
    distanceDict = lewin_count(theme1, theme1)
    distanceDict = lewin_count(theme2, theme2, distanceDict)
elif args.otheronly:
    distanceDict = lewin_count(theme1, theme2)
    distanceDict = lewin_count(theme2, theme1, distanceDict)
elif args.xthemeonly:
    distanceDict = lewin_count(theme1, theme1)
elif args.ythemeonly:
    distanceDict = lewin_count(theme2, theme2)
else:
    entranceTimes = combine_themes(theme1, theme2, args.excludeduplicates)
    distanceDict = lewin_count(entranceTimes, entranceTimes)
    
# extract list of keys, work accordingly
thekeys = list(distanceDict.keys())
# sort by number of occurences, from most to least
thekeys.sort(key=(lambda i: len(distanceDict[i])))
thekeys.reverse()

# initialize y-starting position for alignmentbrackets
y_start = 200
# conditional arguments
if args.plotlist:
    # get list of alignment durations to plot (ignore others)
    thelist = args.plotlist
    thelist = thelist.split(',')
    thelist = list(map(int, thelist))
    for i in thekeys:
        if i in thelist:
            print("<!--", len(distanceDict[i]), "x", i, "-->")
            drawsegments(distanceDict[i], 0, y_start, 1, 'black')
            y_start = y_start + 2*len(distanceDict[i]) + 2
elif args.threshold:
    for i in thekeys:
        if len(distanceDict[i]) < args.threshold:
            break
        else:
            print("<!--", len(distanceDict[i]), "x", i, "-->")
            drawsegments(distanceDict[i], 0, y_start, 1, 'black')
            y_start = y_start + 2*len(distanceDict[i]) + 2
else:
    # plot all
    for i in thekeys:
        print("<!--", len(distanceDict[i]), "x", i, "-->")
        drawsegments(distanceDict[i], 0, y_start, 1, 'black')
        y_start = y_start + 2*len(distanceDict[i]) + 2

# print("<!-- some segments -->")
# drawsegments(segments, 0, 210, 1, 'black')
print("</svg> </body>")
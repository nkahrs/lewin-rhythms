import argparse, copy, functools
from themes import *
from stretti_lewin import *
from class_equiv import *
from svg import *

    
# adapt to use flag syntax from main_svg
# duplicates?

if __name__ != '__main__':
    exit()
    
# set up flagging
# much of this heavily draws on the python argparse tutorial
parser = argparse.ArgumentParser()

offset = parser.add_mutually_exclusive_group()
offset.add_argument('-x', '--xthemeoffset', type=int,
                help="offset for theme 1")
offset.add_argument('-y', '--ythemeoffset', type=int,
                help="offset for theme 2")
offset.add_argument('-X', '--xthemeonly', action="store_true",
                    help="only include theme 1")
offset.add_argument('-Y', '--ythemeonly', action="store_true",
                    help="only include theme 2")

combos = parser.add_mutually_exclusive_group()
combos.add_argument('-d', '--includeduplicates', action="store_true",
                help="aggregate->aggregate, include duplicates (default)")
combos.add_argument('-e', '--excludeduplicates', action="store_true",
                help="aggregate->aggregate, exclude duplicates")

toplot = parser.add_argument_group("which to plot (all by default)")
toplot.add_argument('-l', '--plotlist',
                    help='plot from list after arg (ie "1,2,3")')
toplot.add_argument('-t', '--threshold', type=int,
                    help="plot if count is above specified threshold (also applies to list)")
toplot.add_argument('-c', '--beatclass', action="store_true",
                    help="account for beat-class equivalence across barlines")

bold = parser.add_argument_group("only plotting bold columns")
bold.add_argument('-b', '--boldonly', action="store_true",
                  help="only show columns with a bold element")
bold.add_argument('-r', '--boldthreshold', type=int,
                  help="in combination with -b, specify min number of bold elements to be sufficient for column inclusion")

args = parser.parse_args()

if args.xthemeoffset:
    theme1 = shift_theme(theme1, args.xthemeoffset)
elif args.ythemeoffset:
    theme2 = shift_theme(theme2, args.ythemeoffset)

if args.xthemeonly:
    entranceTimes = theme1
elif args.ythemeonly:
    entranceTimes = theme2
else:
    entranceTimes = combine_themes(theme1, theme2, args.excludeduplicates)
    
thetable = lewin_allcounts(entranceTimes)

if args.beatclass:
    thetable = bcequiv_allcounts(thetable, 216)

# make HTML table, only include specific values

# adapt with flag syntax here

if args.plotlist:
    # get list of alignment durations to plot (ignore others)
    thelist = args.plotlist
    thelist = thelist.split(',')
    thelist = list(map(int, thelist))
    thelist.sort()
else:
    thelist = None
    
formatted = liststobold(
    countstolists(entranceTimes, thetable, thelist, args.threshold)
)

if args.boldonly:
    if args.boldthreshold:
        formatted = boldcolsonly(formatted, args.boldthreshold)
    else:
        formatted = boldcolsonly(formatted)

formatted = formatlabels(formatted)

print('<style>td {border: 1px solid black;}</style>')

print('<table>')

# need to allow capacity for bold

for i in formatted:
    print('<tr>')
    for j in i:
        # check if it's a "peak"
        if j[1]:
            print('<td><b>', j[0], '</b></td>')
        else:
            print('<td>', j[0], '</td>')
    print('</tr>')
print('</table>')

# string all of this together
# according to user arguments, combine the themes, look for common rhythmic alignments, and make an svg

from themes import *
from stretti_lewin import *
from svg import *


if __name__ != '__main__':
    exit()

# encode full form as a series of offsets applied to theme 2 (negative = applied to theme 1)
form = list(map(lambda i: i*216, [5, 3, 1, -1, -3, -5]))  # for now without repetitions

# go from form to overall themes
# input: form as above (list of offsets in units), themes 1 and 2 as from themes module (lists of onsets in units), theme length in units (5*216)
# output: themes as lists of onsets in units
def formtothemes(form, theme1, theme2, length):
    x0 = 0 # initial offset for either theme
    toreturn1 = []
    toreturn2 = []
    for i in form:
        if (i > 0):
            offset1 = 0
            offset2 = i
        else:
            offset1 = -i
            offset2 = 0
        toreturn1 += shift_theme(theme1, x0+offset1)
        toreturn2 += shift_theme(theme2, x0+offset2)
        x0 += (length + abs(i))
    return (toreturn1, toreturn2, x0)

theme1, theme2, total = formtothemes(form, theme1, theme2, 5*216)

# redefine bars from themes, for longer situation
bars = list(map(lambda i: i * 216, range(int(total/216)+1)))

# plot themes and bars
print('<body> <svg height="5000" width="'+str(total+216)+'">')
print("<!-- bar numbers -->")
theme2svg(bars, 0, 0, 200, 1, 'silver')
print("<!-- theme 2 -->")
theme2svg(theme2, 0, 50, 50, 1, 'black')
print("<!-- theme 1 -->")
theme2svg(theme1, 0, 100, 50, 1, 'black')


# main_svg but without controls---for now I'm going to have to create an imaginary "args" object
args = type('', (), {})()
args.sameonly = 0
args.otheronly = 0
args.xthemeonly = 0
args.ythemeonly = 0
args.plotlist = "186,124,80,110,156,180,192,168,128,24,30" #"80,30,110,24,156,180,216,186,184,124" #"80,156" 
args.threshold = 0 #70 #50
args.excludeduplicates = 0


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
else: # same theme or one to other
    entranceTimes = combine_themes(theme1, theme2, args.excludeduplicates)
    distanceDict = lewin_count(entranceTimes, entranceTimes)
    
# extract list of keys, work accordingly
thekeys = list(distanceDict.keys())

# only keep IOIs with length of at most 2*216
thekeys = list(filter(lambda x: x <= 2*216, thekeys))

# sort by number of occurences, from most to least
thekeys.sort(key=(lambda i: len(distanceDict[i])))
thekeys.reverse()

# initialize y-starting position for alignmentbrackets
y_start = 200

# determine requisite conditional "showkeyp"
if args.plotlist:
    # get list of alignment durations to plot (ignore others)
    thelist = args.plotlist
    thelist = thelist.split(',')
    thelist = list(map(int, thelist))
    showkeyp = (lambda x: x in thelist)
elif args.threshold:
    showkeyp = (lambda x: len(distanceDict[x]) >= args.threshold)
else:
    showkeyp = (lambda x: 1)

# assign color based on Section 5 figures
def thecolor(ioi):
    if ioi==24:
        return 'red'
    elif ioi==80:
        return 'orange'
    elif ioi==156:
        return 'green'
    elif ioi==30:
        return 'blue'
    elif ioi==180:
        return 'purple'
    elif ioi==110:
        return 'brown'
    else:
        return 'black'

for i in thekeys:
    if showkeyp(i):
        print("<!--", len(distanceDict[i]), "x", i, "-->")
        distanceDict[i].sort() # new addition
        # add prefatory text: another new addition
        print('<text x="' + str(distanceDict[i][0][0] - 20) + '" y="'
              + str(y_start - 5) + '" size="16"> '
              + str(len(distanceDict[i])) + ' x ' + str(i) + ' </text>')
        drawsegments(distanceDict[i], 0, y_start, 1, thecolor(i))
        y_start += len(distanceDict[i]) + 2 # previously 2*len, etc; shortened because there's a lot now


# print("<!-- some segments -->")
# drawsegments(segments, 0, 210, 1, 'black')
print("</svg> </body>")

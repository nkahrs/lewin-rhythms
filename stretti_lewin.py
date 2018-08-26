import copy, functools

# stretti: given 2 themes, shift and combine them
# lewin: count distances from one rhythm to another, and make tables

# shift_theme: add the shift amount to each member of the theme
def shift_theme(theme, shift):
    return list(map(lambda i: i + shift, theme))

# combine themes: take two themes (already staggered) and superimpose them
# nodups: if true, eliminate duplicates
def combine_themes(theme1, theme2, nodups):
    entranceTimes = theme1+theme2
    if nodups:
        entranceTimes = list(set(entranceTimes))
    entranceTimes.sort()
    return entranceTimes


# lewin_count: count all possible positive distances from rhythm1 to rhythm2
# rhythms should be given as arrays of time-points
# the proper count as proposed in Lewin's essay would be from a single rhythm to itself, which is an obvious special case here
# returns a dictionary of form {offset amount: [pairs with that offset]}
# distanceDict argument lets you append values to an older dict
def lewin_count(rhythm1, rhythm2, distanceDict = {}):
#    distanceDict = {}
    for i in rhythm1:
        for j in rhythm2:
            diff = j-i
            if diff>0:
                if diff in distanceDict.keys():
                    distanceDict[diff].append([i,j])
                else:
                    distanceDict[diff] = [(i,j)]
    return distanceDict



# 8/3/18: upon rereading the Lewin article, it turns out that what's important is how the count progresses over time. This requires a slightly different function, in which we keep track of all intermediate results


# lewin_allcounts: return an array of distancedicts, one for each point in rhythm (in order)
# differences from stretti_lewin.lewin_count:
#   input:
#      only takes one rhythm as input (table format doesn't make sense otherwise)
#      doesn't let you specify initial values for output
#   output:
#      instead of single distancedict, it's an array of distancedicts
#      (single dict of array of dicts might be more efficient, but it doesn't matter at this scale)
#      specifically output is [{Int: [[Int]]}]
def lewin_allcounts(rhythm):
    # iterate over rhythm and a slowly-being-replace clone simultaneously
    # but replace each value with distancedict at current stage
    distanceDict = {}
    toreturn = copy.deepcopy(rhythm)
    for ipointer in range(len(rhythm)):
        i = rhythm[ipointer]
        for j in rhythm[0:ipointer]:
            diff = i - j
            if diff>0:
                if diff in distanceDict.keys():
                    distanceDict[diff].append([i,j])
                else:
                    distanceDict[diff] = [(i,j)]
        toreturn[ipointer] = copy.deepcopy(distanceDict)
    return toreturn

# countstolist: [Int] [{Int: [[Int]]}] (Maybe [Int]) (Maybe Int)  -> [[Int]]
# convert output from lewin_allcounts to a nice table, as list of rows, each of which is a list of columns
# rows: timepoints, columns: rhythmic intervals, values: counts at that point
# input: therhythm (the rhythm itself), thetable (output from lewin_allcounts), thelist (which to include as columns, or None for all), thethreshold (min value to consider)
# output: list of lists, to be formatted later
def countstolists(therhythm, thetable, thelist=None, threshold=None):
    # "thelist" is which rhythmic offsets to look at
    # if not specified, look at all of them
    if (not thelist):
        thelist = list(thetable[-1].keys())
        thelist.sort()
    # if a threshold is specified, only look at elements of the list more common than said min value
    if (threshold):
        # 8/8: this is broken somewhere, since it's cutting things it shouldn't.
        thelist = list(filter(
            lambda i: len(thetable[-1][i]) >= threshold,
            # this is not entirely safe---if we're given a list that isn't in thetable[-1].keys() we get a KeyError
            thelist
        ))
    
    # initialize first row (display)
    toreturn = [[""] + thelist]
    # fill in values
    for ipointer in range(len(therhythm)):
        # label
        thisrow = [therhythm[ipointer]]
        # counts
        for j in thelist:
            if j in thetable[ipointer].keys():
                thisrow.append(len(thetable[ipointer][j]))
            else:
                thisrow.append("")
        toreturn.append(thisrow)
    return toreturn

# liststobold: [[Int]] -> [[(Int, Bool)]]
# replace each Int with a tuple: x->(x, True) if x is accented and thus should be bold in table, x->(x, False) otherwise
def liststobold(thetable):
    toreturn = copy.deepcopy(thetable)
    # first, set all items of the first row to not be bold
    for jpointer in range(len(thetable[0])):
        toreturn[0][jpointer] = (thetable[0][jpointer], False)
    # iterate over the table, ignoring the first row
    for ipointer in range(1, len(thetable)):
        # should adjust so that leftmost is only bold if anything in the rest of the row is
        # ignore leftmost column (labels)
        for jpointer in range(1, len(thetable[ipointer])):
            # find item above
            if (ipointer > 0):
                itemabove = thetable[ipointer-1][jpointer]
                if itemabove == '':
                    itemabove = 0
            else:
                itemabove = 0
            # find next nonzero to left
            thisjpointer = copy.deepcopy(jpointer) - 1
            itemtoleft = 0
            while (thisjpointer > 0):
                thisitem = thetable[ipointer][thisjpointer]
                if thisitem:
                    itemtoleft = copy.deepcopy(thisitem)
                    break
                else:
                    thisjpointer -= 1
            # find next nonzero to right
            thisjpointer = copy.deepcopy(jpointer) + 1
            itemtoright = 0
            while (thisjpointer < len(thetable[ipointer])):
                thisitem = thetable[ipointer][thisjpointer]
                if thisitem:
                    itemtoright = copy.deepcopy(thisitem)
                    break
                else:
                    thisjpointer += 1                    
            # check if this item is a peak
            thisitem = thetable[ipointer][jpointer]
            
            if ( (type(thisitem) == int) and # item isn't ''
                 (thisitem > 1) and
                 (thisitem > itemabove) and
                 (thisitem > itemtoleft) and
                 (thisitem > itemtoright)
            ):
                toreturn[ipointer][jpointer] = (thisitem, True)
            else:
                toreturn[ipointer][jpointer] = (thisitem, False)
        # no bold for leftmost
        toreturn[ipointer][0] = (thetable[ipointer][0], False)
    return toreturn

# boldcolsonly: [[(Int, Bool)]] Int -> [[(Int, Bool)]]
# strip all columns that don't have a bold element
# also, mark row labels (in column zero) with bold iff there's a bold element later in the row
# first argument: the table to strip columns from
# second argument: min number of bolds to not strip column (default: 1)
def boldcolsonly(theboldtable, threshold = 1):
    # first, figure out which columns to keep
    whichcols = [0]
    # indices start at 1 to ignore labels at sides of table
    # this might be more succinct if I did a tranpose and filter and transpose again, but transpose is needlessly expensive
    # consider revising as a reduce of a map
    for jpointer in range(1, len(theboldtable[0])): # iterate over columns
        boldcount = 0
        for ipointer in range(1, len(theboldtable)): # iterate over rows
            if theboldtable[ipointer][jpointer][1]:
                boldcount += 1
                if (boldcount >= threshold):
                    whichcols.append(jpointer)
                    break
                continue
            continue
    # thanks, stackexchange
    toreturn = [ [theboldtable[i][j] for j in whichcols]
                 for i in range(len(theboldtable)) ]
    return toreturn

# formatlabels: [[(Int, Bool)]] Int -> [[(Int, Bool)]]
# format first column and first row: bold only if a later item is
def formatlabels(toreturn):
    # make leftmost of row bold iff rest of row has something
    for ipointer in range(len(toreturn)):
        if functools.reduce(lambda x, y: x or y,
                  map(lambda x: x[1], toreturn[ipointer][1:])):
            toreturn[ipointer][0] = (toreturn[ipointer][0][0], True)
    # make topmost of column bold iff rest of column has something
    for jpointer in range(len(toreturn[0])):
        if functools.reduce(lambda x, y: x or y,
                  map(lambda ipointer: toreturn[ipointer][jpointer][1],
                      range(1,len(toreturn)))):
            toreturn[0][jpointer] = (toreturn[0][jpointer][0], True)
    # and return
    return toreturn

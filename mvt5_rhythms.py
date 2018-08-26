# create the rhythms of the two hands in movement 5
# then make an svg out of them

from svg import *
import copy

# example: ([3,4],[2,1]) -> [0,2,4,6,7,8,9]
def makerhythm(phrasedurs, notedurs):
    toreturn = [0]
    for i in range(len(phrasedurs)):
        for j in range(phrasedurs[i]):
            toreturn.append(toreturn[-1] + notedurs[i % len(notedurs)])
    return toreturn[0:-1]

# basic cell for generating stuff
cell = [3,4,5,5,4]
# llec = cell backwards
llec = copy.deepcopy(cell)
llec.reverse()

# parts 1 and 2, and bars behind
p1 = makerhythm(2*cell + 2*llec, [1,2])
p2 = makerhythm(2*llec + 2*cell, [2,1])
bars = [i*9 for i in range(15)] #list(map(lambda i: i * 9, range(15)))

# thicken: replace each time point by width-many, with spacing-many pixels until the next
# this way we can see individual articulations but they take up most of the space available
def thicken(timepoints, spacing, width):
    toreturn = []
    timepoints = [i*spacing for i in timepoints]
    for i in range(width):
        toreturn += timepoints
        timepoints = [i+1 for i in timepoints]
    return toreturn

# thicken everything we want to plot
p1 = thicken(p1, 4, 3)
p2 = thicken(p2, 4, 3)
bars = thicken(bars, 4, 3)
# note midpoint in red
mid = thicken([7*9], 4, 3)

# plot themes and bars
print('<body> <svg height="4000" width="2000">')
print("<!-- bar numbers -->")
theme2svg(bars, 0, 0, 200, 1, 'silver')
print("<!-- midpoint -->")
theme2svg(mid, 0, 0, 200, 1, 'red')
print("<!-- part 1 -->")
theme2svg(p1, 0, 50, 50, 1, 'black')
print("<!-- part 2 -->")
theme2svg(p2, 0, 100, 50, 1, 'black')
print("</svg> </body>")

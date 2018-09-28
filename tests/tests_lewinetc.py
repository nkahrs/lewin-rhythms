# some tests, in this case of the lewin module, based on "07 25 stretti and lewin.py"

from themes import *
from stretti_lewin import *

entranceTimes = combine_themes(theme1, theme2, True)

distanceDict = lewin_count(entranceTimes, entranceTimes)

distanceList = list(map(
    lambda i: (len(distanceDict[i]), i, distanceDict[i]),
    distanceDict.keys()
))

distanceList.sort()
distanceList.reverse()

if __name__ == '__main__':
    for i in distanceList:
        if i[1] in [216, 80, 30, 110, 156, 24, 180]:
            print(i[0],'\t',i[1],'\t',i[2])


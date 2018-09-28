entranceTimes = """0
216
340
432
496
556
616
648
680
712
742
772
802
832
848
864
880
896
912
928
943
958
973
988
1003
1018
1048""".split('\n')

### theme 2
##entranceTimes = """0
##54
##86
##108
##128
##140
##152
##162
##172
##182
##188
##194
##200
##206
##211
##216
##221
##226
##231
##236
##239
##242
##245
##248
##251
##254
##260""".split('\n')

entranceTimes = list(map(lambda i: int(i), entranceTimes))

# now that we have entrance times, find distances between them
distanceDict = {}
for i in entranceTimes:
    for j in entranceTimes:
        diff = j-i
        if diff>0:
            if diff in distanceDict.keys():
                distanceDict[diff].append([i,j])
            else:
                distanceDict[diff] = [(i,j)]

distanceList = list(map(
    lambda i: (len(distanceDict[i]), i, distanceDict[i]),
    distanceDict.keys()
    ))

distanceList.sort()
distanceList.reverse()

for i in distanceList:
	print (i[0],'\t',i[1],'\t',i[2])

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
1018""".split('\n')
#1048 #this would be full circle

theme1 = list(map(lambda i: int(i)+32, entranceTimes))

### theme 2
entranceTimes = """0
54
86
108
128
140
152
162
172
182
188
194
200
206
211
216
221
226
231
236
239
242
245
248
251
254""".split('\n')
#260 would be full circle

theme2 = list(map(lambda i: (int(i)*4)+40, entranceTimes))

# offset by some number of measures. 1 measure=216 units
# close stretti: everything in theme 2 is later by 1 bar (now earlier, changed + to -)
theme2 = list(map(lambda i: i - 216, theme2))

# concatenate, then sort to combine
entranceTimes = theme1+theme2
#entranceTimes = list(set(entranceTimes))
entranceTimes.sort()

# now that we have entrance times, find distances between them
distanceDict = {}
# for i in entranceTimes:
#     for j in entranceTimes:
for i in theme1:
    for j in theme2:
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
    if i[1] in [216, 80, 30, 110, 156, 24, 180]:
        print (i[0],'\t',i[1],'\t',i[2])

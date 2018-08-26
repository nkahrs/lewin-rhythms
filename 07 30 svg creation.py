# copy-pasted definitions of basic variables

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
theme2 = list(map(lambda i: i + 216, theme2))

# bar endpoints

bars = list(map(lambda i: i * 216, range(7)))

## theme2svg: given theme, output svg rectangles to mark points
def theme2svg(theme, x_offset, y_offset, height, width, color):
    for i in theme:
        print('<rect x="', (x_offset+i), '" y="', y_offset,
              '" height="', height, '" width="', width,
              '" fill="', color, '" />')


# a few line segments to plot as a test
# for e, segments = [(-176, 40), [32, 248], [40, 256], [168, 384], [248, 464], [256, 472], [336, 552], [372, 588], [384, 600], [432, 648], [432, 648], [464, 680], [472, 688], [512, 728], [528, 744], [552, 768], [576, 792], [588, 804], [588, 804], [600, 816], [624, 840], [648, 864], [648, 864], [680, 896], [712, 928], [728, 944], [744, 960], [774, 990], [804, 1020], [804, 1020], [834, 1050], (168, 248), [256, 336], [384, 464], [432, 512], [472, 552], [588, 668], [600, 680], [648, 728], [648, 728], [668, 748], [688, 768], [712, 792], [748, 828], [816, 896], [864, 944], [880, 960], (528, 552), [552, 576], [576, 600], [600, 624], [624, 648], [624, 648], [688, 712], [744, 768], [768, 792], [780, 804], [780, 804], [792, 816], [804, 828], [804, 828], [816, 840], [840, 864], (372, 528), [432, 588], [512, 668], [552, 708], [588, 744], [624, 780], [648, 804], [648, 804], [648, 804], [648, 804], [708, 864], [804, 960], [804, 960], [834, 990], [864, 1020], (372, 552), [528, 708], [588, 768], [600, 780], [624, 804], [624, 804], [648, 828], [648, 828], [748, 928], [780, 960], [840, 1020], (744, 774), [774, 804], [774, 804], [804, 834], [804, 834], [834, 864], [960, 990], [975, 1005], [990, 1020], [1005, 1035], [1020, 1050], (834, 944), [880, 990]]
# well, maybe more than a few
# for d
segments = [(32, 248), [248, 464], [256, 472], [372, 588], [464, 680], [472, 688], [528, 744], [588, 804], [600, 816], [648, 864], [680, 896], [688, 904], [712, 928], [744, 960], [768, 984], [774, 990], [804, 1020], [816, 1032], [834, 1050], [864, 1080], [904, 1120], [944, 1160], [984, 1200], [1008, 1224], [1020, 1236], [1032, 1248], [1056, 1272], (688, 712), [744, 768], [880, 904], [904, 928], [960, 984], [984, 1008], [1008, 1032], [1032, 1056], [1056, 1080], [1200, 1224], [1212, 1236], [1224, 1248], [1236, 1260], [1248, 1272], (600, 680), [688, 768], [816, 896], [864, 944], [880, 960], [904, 984], [928, 1008], [1020, 1100], [1080, 1160], [1100, 1180], [1120, 1200], [1180, 1260], (372, 528), [588, 744], [648, 804], [804, 960], [834, 990], [864, 1020], [944, 1100], [984, 1140], [1056, 1212], [1080, 1236], (744, 774), [774, 804], [804, 834], [834, 864], [960, 990], [975, 1005], [990, 1020], [1005, 1035], [1020, 1050], [1050, 1080], (588, 768), [804, 984], [960, 1140], [1020, 1200], [1032, 1212], [1056, 1236], [1080, 1260], (834, 944), [880, 990], [990, 1100], [1050, 1160]]


def drawsegment(segment, x_offset, y_start, y_height, color):
    print('<rect x="', x_offset + segment[0], '" y=', y_start+1,
          '" height="', y_height, '" width="', 1+segment[1]-segment[0],
          '" fill="', color, '" />')
    # add handles
    print('<rect x="', x_offset + segment[0], '"y=', y_start,
          '" height="1" width="1" fill="', color, '" />')
    print('<rect x="', x_offset + segment[1], '"y=', y_start,
          '" height="1" width="1" fill="', color, '" />')

def drawsegments(segments, x_offset, y_start, y_height, color):
    for i in segments:
        drawsegment(i, x_offset, y_start, y_height, color)
        y_start = y_start + 2*y_height
        
if __name__=='__main__':
    print('<body> <svg height="2000" width="2000">')
    print("<!-- bar numbers -->")
    theme2svg(bars, 0, 0, 200, 1, 'silver')
    print("<!-- theme 2 -->")
    theme2svg(theme2, 0, 50, 50, 1, 'black')
    print("<!-- theme 1 -->")
    theme2svg(theme1, 0, 100, 50, 1, 'black')
    print("<!-- some segments -->")
    drawsegments(segments, 0, 210, 1, 'black')
    print("</svg> </body>")

    # we'd change the 0 after "variable name" to "216" for the E rather than D case

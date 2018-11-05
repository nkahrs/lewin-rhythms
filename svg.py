# refactored "07 30 svg creation.py", svg generation only

## theme2svg: given theme, output svg rectangles to mark points
def theme2svg(theme, x_offset, y_offset, height, width, color):
    for i in theme:
        print('<rect x="', (x_offset+i), '" y="', y_offset,
              '" height="', height, '" width="', width,
              '" fill="', color, '" />', sep='')

def drawsegment(segment, x_offset, y_start, y_height, color):
    print('<rect x="', x_offset + segment[0], '" y="', y_start+1,
          '" height="', y_height, '" width="', 1+segment[1]-segment[0],
          '" fill="', color, '" />', sep='')
    # add handles
    print('<rect x="', x_offset + segment[0], '" y="', y_start,
          '" height="1" width="1" fill="', color, '" />', sep='')
    print('<rect x="', x_offset + segment[1], '" y="', y_start,
          '" height="1" width="1" fill="', color, '" />', sep='')

def drawsegments(segments, x_offset, y_start, y_height, color):
    for i in segments:
        drawsegment(i, x_offset, y_start, y_height, color)
        y_start = y_start + 2*y_height
        

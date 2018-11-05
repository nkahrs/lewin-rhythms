# This file pushes out the rhythms for the wind and string
# accompaniments to the piano themes in Canon 1b. All dotted-eighths.
# there are 6 dotted eighths per measure, so 1 is 216/6=36
# plots against the piano themes for easy comparison

from svg import *
import themes

theme1 = [1,
          6, 9, 11,
          14, 15,
          20, 22, 23,
          25, 26, 27, 29]

theme2 = [1,
          6, 9, 11,
          14, 15,
          20, 22, 23,
          24, 25, 26, 27, 29]

wstheme1 = list(map(lambda i: i * 36, theme1))
wstheme2 = list(map(lambda i: i * 36, theme2))

if __name__=='__main__':
    # plot themes and bars
    print('<body> <svg height="4000" width="2000">')

    print("<!-- theme 1 -->")
    print("<!-- bars -->")
    theme2svg(themes.bars, 0, 0, 200, 1, 'silver')
    print("<!-- piano -->")
    theme2svg(themes.theme1, 0, 50, 50, 1, 'black')
    print("<!-- strings -->")
    theme2svg(wstheme1, 0, 100, 50, 1, 'black')

    print("\n<!-- theme 2 -->")
    print("<!-- bars -->")
    theme2svg(themes.bars, 0, 300, 200, 1, 'silver')
    print("<!-- piano -->")
    theme2svg(themes.theme2, 0, 350, 50, 1, 'black')
    print("<!-- winds -->")
    theme2svg(wstheme2, 0, 400, 50, 1, 'black')

    
    print("</svg> </body>")

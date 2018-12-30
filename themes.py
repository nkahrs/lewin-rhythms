## define initial themes here
## in the future, I could replace this with text processing of a file or of stdin, but why bother for now?

# theme1, theme2 are the two important variables to come from here
# both of these are arrays of integers; integers represent timepoint offset of entrance from a fixed zero point (which is usually the begin-repeat sign)

theme1 = """0
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
# 1048 would be full circle
# perhaps I should include the end of the last note?

theme1 = list(map(lambda i: int(i)+32, theme1))

### theme 2
theme2 = """0
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
# 260 would be full circle
# *4 is because we have a larger quantum unit for this theme
theme2 = list(map(lambda i: (int(i)*4)+40, theme2))


# some bar endpoints
bars = list(map(lambda i: i * 216, range(11)))

# 10/19/18: adapting to also work with beat-classes

import copy

# combine_lictdist_equiv: ({Int: []}, Int) -> {Int: []}
# inputs: thedict (dict with integer indices and list entries)
#         modulus (modulus for equivalence)
# outputs: thedict, with lists equal mod modulus concatenated together
def combine_listdict_equiv(thedict, modulus):
    newdict = {}
    for i in thedict.keys():
        im = i % modulus
        if im in newdict.keys():
            newdict[im] += thedict[i]
        else:
            newdict[im] = copy.deepcopy(thedict[i])
    return newdict

# bcequiv_lists: applies beat-class equivalence to output from all-counts
def bcequiv_allcounts(allcounts, modulus):
    for i in range(len(allcounts)):
        allcounts[i] = combine_listdict_equiv(allcounts[i], modulus)
    return allcounts


# tests itself automatically if run directly
if __name__=="__main__":
    foo = {5: [1,2,3], 7: [4,5,6], 10: [7,8,9]}
    print("expecting {0: [7,8,9], 1: [1,2,3,4,5,6]}")
    print(combine_listdict_equiv(foo, 2))
    print("expecting {0: [1,2,3,7,8,9], 2: [4,5,6]}")
    print(combine_listdict_equiv(foo, 5))

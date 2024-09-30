'''
Binning functions to reduce the quantity of labels in a 
Gaifman structure as labeling with frequencies may be
too rigid.
'''

ident = lambda x: x

# binary binning labels 0/1 give, essentially, a standard Gaifman graph
binary = lambda x: int(x > 0)

# binary binning labels for a thresholded Gaifman graph
# ~ def t(x):
    # ~ if x < 23: return 0 # just forgets about the 6 children in 1st class
    # ~ return 1
# ~ def t(x):
    # ~ if x < 212: return 0 # there is a bend there hitting some exp-like
    # ~ return 1
    # marks that few children overall, and that few people in 1st and 2nd class
def t(x):
    if x < 1000: return 0 
    return 1

# manually decided for Titanic on the basis of increase over 20% to next one
# ~ def t(x):
    # ~ if x < 5: return 0
    # ~ if x < 10: return 1
    # ~ if x < 30: return 2
    # ~ if x < 70: return 3
    # ~ if x < 100: return 4
    # ~ if x < 250: return 5
    # ~ if x < 300: return 6
    # ~ if x < 700: return 7
    # ~ if x < 1000: return 8
    # ~ return 9
# leads to only one total primitive clan

# manually decided for Titanic on the basis of:
# select value, duplicate, find next larger value and keep it (?), go on until two consecutive increases beyond 10%, recurse
# (maybe zeros/start should be handled differently)
# ~ def t(x):
    # ~ if x < 52: return 0
    # ~ if x < 167: return 1
    # ~ if x < 510: return 2
    # ~ return 3
# leads to only one total primitive clan

# ~ by multiples of the 10 root of 6 so that lines meet at 6, they also meet at 367, see file toplot.txt
# ~ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 23, 24, 45, 52, 57, 64, 79, 106, 118, 122, 126, 145, 167, 178, 179, 180, 196, 203, 212, 261, 319, 344, 367, 425, 510, 528, 627, 654, 673, 862, 885, 1364, 1438, 1667]
# ~                                ^               ^                                         ^                                                           ^
# ~
# ~ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 23, 24, 45, 52, 57, 64, 79, 106, 118, 122, 126, 145, 167, 178, 179, 180, 196, 203, 212, 261, 319, 344, 367, 425, 510, 528, 627, 654, 673, 862, 885, 1364, 1438, 1667]
# ~                                ^                                                                                                           ^                                                           ^

# ~ by multiples of the i-th root of i-th value so that lines meet at that value, where do they also meet/cross?
# ~ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 23, 24, 45, 52, 57, 64, 79, 106, 118, 122, 126, 145, 167, 178, 179, 180, 196, 203, 212, 261, 319, 344, 367, 425, 510, 528, 627, 654, 673, 862, 885, 1364, 1438, 1667]
# ~                                ^               ^                                         ^                                                           ^

# example with i = 31:
# ~ def t(x):
    # ~ if x < 23: return 0
    # ~ if x < 212: return 1
    # ~ return 2
# leads to only one total primitive clan

# example with i = 42:
# ~ def t(x):
    # ~ if x < 6: return 0
    # ~ if x < 654: return 1 # just separates the traveling classes
    # ~ return 2

# example with i = 37:
# ~ def t(x):
    # ~ if x < 6: return 0
    # ~ if x < 627: return 1 # just separates the small 1st/2nd traveling classes
    # ~ return 2

# example with i = 18:
# ~ def t(x):
    # ~ if x < 23: return 0
    # ~ if x < 79: return 1 # just separates the survived nodes
    # ~ return 2

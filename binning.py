'''
Binning functions to reduce the quantity of labels in a 
Gaifman structure as labeling with frequencies may be
too rigid.
'''

ident = lambda x: x

# binary binning labels 0/1 give, essentially, a standard Gaifman graph
binary = lambda x: int(x > 0)

# manually decided for Titanic on the basis of increase over 20% to next one
def t(x):
    if x < 5: return 0
    if x < 10: return 1
    if x < 30: return 2
    if x < 70: return 3
    if x < 100: return 4
    if x < 250: return 5
    if x < 300: return 6
    if x < 700: return 7
    if x < 1000: return 8
    return 9

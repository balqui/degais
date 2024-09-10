'''
Binning functions to reduce the quantity of labels in a 
Gaifman structure as labeling with frequencies may be
too rigid.
'''

ident = lambda x: x

# binary binning labels 0/1 give, essentially, a standard Gaifman graph
binary = lambda x: int(x > 0)

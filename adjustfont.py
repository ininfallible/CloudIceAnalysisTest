import matplotlib as mpl

def adjfont():
    font = {
            'family' : 'normal',
            'weight' : 'normal',
            'size' : 18
            }
    mpl.rc('font', **font)

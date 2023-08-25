import sys
sys.path += ['.']

import os

from pytexutils.graphs.bar_chart import bar_chart

if __name__ == '__main__':


    data = {
        'men' : {
            'x'     : [2012,   2011,   2010,   2009],
            'y'     : [408184, 408348, 414870, 412156],
            'color' : [0.54, 0, 0],
        },
        'women' : {
            'x'     : [2012,   2011,   2010,   2009],
            'y'     : [388950, 393007, 398449, 395972],
            'color' : [0, 0.50, 0.50],
        }
        }
    latex_bar_chart = bar_chart(data, caption='My bar chart 1', label='bar1', preamble=True)
    print(latex_bar_chart)

    save_folder = os.path.join('tmp', 'test_bar_chart')
    os.makedirs(save_folder, exist_ok=True)
    
    with open(os.path.join(save_folder, 'main-1.tex'), 'w') as texfile:
        texfile.writelines(latex_bar_chart)
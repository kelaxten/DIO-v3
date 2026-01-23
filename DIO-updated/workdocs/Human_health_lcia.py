"""
Create an impact method for occupational health
"""

import pandas as pd

import lciafmt
from lciafmt.util import store_method

# from pathlib import Path

# filepath = Path(__file__).parent.parent
# datapath = filepath / 'data'

def main():
    data = {
        'Flowable': ['Injury and illness'],
        'Context': [''],
        'Unit': ['DALY'],
        'Characterization Factor': [1],
        'Indicator': ['Injury and illness'],
        }
    method = (pd.DataFrame(data)
              .assign(Method='Occupational health')
              .assign(**{'Indicator unit': 'DALY'})
              )

    df = lciafmt.custom.get_custom_method(input_df=method)

    store_method(df, method_id=None, name='OccupationalHealth_LCIA')

if __name__ == "__main__":
    main()
    df = lciafmt.get_mapped_method('OccupationalHealth_LCIA')

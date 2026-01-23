import pandas as pd

import lciafmt
from lciafmt.util import store_method

from pathlib import Path

filepath = Path(__file__).parent.parent
datapath = filepath / 'data'

def main():

    file = pd.read_csv(datapath / 'DIO_valuation.csv')
    methods = lciafmt.generate_endpoints(file=file, name = 'DIO Valuation')
    
    store_method(methods, method_id = None)

if __name__ == "__main__":
    main()
    df = lciafmt.get_mapped_method('DIO Valuation')

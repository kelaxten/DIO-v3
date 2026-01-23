# -*- coding: utf-8 -*-
"""
Clean A and B matrix
"""

import pandas as pd
import numpy as np

from pathlib import Path

filepath = Path(__file__).parent.parent
datapath = filepath / 'data'

A = pd.read_csv(datapath/'A_matrix_DIO.csv')
B = pd.read_csv(datapath/'B_matrix_DIO.csv')


#%% Replace Flowable with name from federal flow list
import fedelemflowlist as fed
fl = fed.get_flows()

B = (B
     .merge(fl[['Flowable','Flow UUID']],
            how='left',
            left_on='FlowUUID',
            right_on='Flow UUID',
            suffixes=('','_x')
            )
     .assign(fedefl_missing=lambda x: x['Flow UUID'].isna())
     .assign(Flowable=lambda x: x['Flowable_x'].fillna(x.Flowable))
     .drop(columns=['Flow UUID', 'Flowable_x'])
     )

cols = ['Flowable','Context','Unit','FlowUUID']
missing = (B
           .query('fedefl_missing == True')
           .drop_duplicates(subset=cols)
           .drop(columns=[c for c in B.columns if c not in cols])
           )
print(f"UUID not found for \n {missing.to_markdown(index=False)}")

#%% Fix two locations for single processes, where all but one of the records
# Shows global/unspecified while the last one shows the actual location
locations = (B
             .groupby(['ProcessID', 'Location']).size().reset_index()
             .rename(columns={0:'count'})
             .sort_values(by=['count'])
             .assign(duplicate=lambda x: x.duplicated(subset=['ProcessID'],
                                                      keep='first'))
             .query('duplicate == False')
             )
locations = dict(zip(locations.ProcessID, locations.Location))
B['Location'] = B['ProcessID'].map(locations)
B['Location'] = B['Location'].replace({'Global / Unspecified': 'Global'})

#%%
A['Location'] = A['Location'].replace({'United States': 'US'})
A['Location'] = A['Location'].str.strip()

# align locations from A matrix to B matrix
B['Location'] = B['ProcessID'].map(dict(zip(A.ProcessID, A.Location)))

#%% Upload revised csv
(A.to_csv(datapath/'A_matrix_DIO.csv', index=False)
 )
(B
 .drop(columns=['fedefl_missing'], errors='ignore')
 .to_csv(datapath/'B_matrix_DIO.csv', index=False)
 )


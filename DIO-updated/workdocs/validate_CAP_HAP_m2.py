"""
Generates and validates CAP_HAP_national_m2 flow-by-sector model
"""

import flowsa
import pandas as pd
from flowsa.settings import plotoutputpath

# Re-generate methods
# flowsa.flowby.FlowBySector.generateFlowBySector(method='CAP_HAP_national_2017_m2',
#                                                 download_sources_ok=True)
# flowsa.flowby.FlowBySector.generateFlowBySector(method='CAP_HAP_national_2017_m1',
#                                                 download_sources_ok=True)

m2 = flowsa.getFlowBySector("CAP_HAP_national_2017_m2_v2.0.0_a52db57")
m1 = flowsa.getFlowBySector("CAP_HAP_national_2017_m1_v2.0.0_a52db57")

#%% Validate against m1
# pd.testing.assert_frame_equal(m1, m2)

m2.Context.unique()
m1.Context.unique()

rename_flow_cols = {"FlowAmount_x":"m1","FlowAmount_y":"m2"}


# compare flow totals
f2 = m2.groupby(['Flowable']).agg({'FlowAmount':'sum'})
f1 = m1.groupby(['Flowable']).agg({'FlowAmount':'sum'})
# pd.testing.assert_frame_equal(f1, f2, rtol=0.0001)
f_merge = (pd.merge(f1.reset_index(), f2.reset_index(), how='outer',
                    on='Flowable')
           .assign(Rel=lambda x: x['FlowAmount_x'] / x['FlowAmount_y'])
           )
f_merge = f_merge.rename(columns=rename_flow_cols)
f_merge.to_csv("Flow_total_CAP_HAP_m1_vs_m2.csv",index=False)

# compare sector totals
s2 = m2.groupby(['SectorProducedBy']).agg({'FlowAmount':'sum'})
s1 = m1.groupby(['SectorProducedBy']).agg({'FlowAmount':'sum'})
# pd.testing.assert_frame_equal(s1, s2, rtol=0.03)
s_merge = (pd.merge(s1.reset_index(), s2.reset_index(), how='outer',
                    on='SectorProducedBy')
           .assign(Rel=lambda x: x['FlowAmount_x'] / x['FlowAmount_y'])
           )

s2 = m2.groupby(['SectorProducedBy','Flowable']).agg({'FlowAmount':'sum'})
s1 = m1.groupby(['SectorProducedBy','Flowable']).agg({'FlowAmount':'sum'})
# pd.testing.assert_frame_equal(s1, s2, rtol=0.03)
s_merge = (pd.merge(s1.reset_index(), s2.reset_index(), how='outer',
                    on=['SectorProducedBy','Flowable'])
           .assign(Rel=lambda x: x['FlowAmount_x'] / x['FlowAmount_y'])
           .query('Rel >= 1.01 or Rel <= 0.99'))
s_merge = s_merge.rename(columns=rename_flow_cols)
s_merge.to_csv("Sector+Flow_total_CAP_HAP_m1_vs_m2.csv",index=False)

#%% Compare methods by sector by indicator
import lciafmt

indicator = 'Human toxicity non-cancer, short term'

impacts1 = (lciafmt.apply_lcia_method(m1, 'ImpactWorld+'))
impacts2 = (lciafmt.apply_lcia_method(m2, 'ImpactWorld+'))
groupby = ['SectorProducedBy','Indicator','Indicator unit']
impacts = (impacts1.groupby(groupby).agg({'Impact':'sum'})
           .merge(impacts2.groupby(groupby).agg({'Impact':'sum'}),
                  how='outer', on=groupby)
           .rename(columns={'Impact_x':'m1',
                            'Impact_y':'m2'})
           .query('Indicator == @indicator')
           .reset_index()
           .sort_values(by='SectorProducedBy'))
impacts['comp'] = impacts['m2'] / impacts['m1']

#%% Data Viz
from flowsa.validation import calculate_industry_coefficients
import seaborn as sns
method = 'ImpactWorld+'
# print(lciafmt.supported_indicators(lciafmt.Method.ImpactWorld))
indicator = 'Particulate matter formation'
# IW has duplicate names sometimes for midpoint and endpoint
indicator_unit = 'kg PM2.5 eq'
level = 'detail'
year = '2012' if level == 'detail' else '2017'

coeff_1 = (calculate_industry_coefficients(m1, year, "national", io_level=level,
                                          impacts=method)
           .query('Indicator == @indicator')
           .query('`Indicator unit` == @indicator_unit')
           .assign(method='Original')
           )

coeff_2 = (calculate_industry_coefficients(m2, year, "national", io_level=level,
                                           impacts=method)
           .query('Indicator == @indicator')
           .query('`Indicator unit` == @indicator_unit')
           .assign(method='Secondary Contexts')
           )
df = pd.concat([coeff_1, coeff_2], ignore_index=True)

## Adapted from flowsa plot_state_coefficients()
sns.set_style("whitegrid")
axis_var = 'Sector'
g = (sns.relplot(data=df, x="Coefficient", y=axis_var,
                 hue="method", alpha=0.7, style="method",
                 palette="colorblind")
     )
g._legend.set_title('Method')
g.set_axis_labels(f"{df['Indicator'][0]} ({df['Indicator unit'][0]} / $)",
                  "")
g.tight_layout()
g.figure.set_size_inches(10.5, 50)
# Save to local/flows/Plots
l = f'_{level}' if level != 'summary' else ''
g.savefig(plotoutputpath / 'CAP_HAP_'
          f'{indicator.replace(" ","_").replace(",","")}{l}.png')

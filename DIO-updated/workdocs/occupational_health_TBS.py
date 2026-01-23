"""
Generate TBS for Occupational Health data
Huang et al 2023: https://doi.org/10.1021/acs.est.3c00188
System Approach for Characterizing and Evaluating Factors for
Occupational Health Impacts Due to Nonfatal Injuries and Illnesses
for the Use in Life Cycle Assessment
"""
import pandas as pd
import flowsa

repo = 'https://github.com/ZhehanHuang/Occupational-health-calculation'
file = 'raw/main/data/developed_dataset/Dataset%20of%20direct%20impact%20factors%20of%20occupational%20health%20impacts.xlsx'

years = ['2014', '2015', '2016', '2017', '2018'] # average across 5 years

## USEEIO TBS format
cols = [
    'Sector',
    'SectorName',
    'Flowable',
    'Year',
    'FlowAmount',
    'DataReliability',
    'TemporalCorrelation',
    'GeographicalCorrelation',
    'TechnologicalCorrelation',
    'DataCollection',
    'Location',
    'Context',
    'Unit',
    'FlowUUID',
    'MetaSources',
    ]


def generate_OH_totals(file, years):
    df_total = pd.DataFrame()
    for year in years:
        df = (pd.read_excel(file, sheet_name=year)
              .filter(['USEEIO Code', 'Total Impact'])
              .assign(Sector = lambda x: x['USEEIO Code'].apply(str))
              .rename(columns={'Total Impact': year})
              .assign(Unit = 'DALY / $ output')
              # .assign(Year = year)
              .assign(Flowable = 'Injury and illness')
              .assign(Context = '')
              .assign(MetaSources = 'Huang et al. 2023')
              .assign(Location = 'US'))

        fba = (flowsa.getFlowByActivity('BEA_GDP_GrossOutput', year)
               .filter(['FlowAmount', 'ActivityProducedBy'])
               .rename(columns={'ActivityProducedBy': 'Sector',
                                'FlowAmount': 'Output'})
               )

        ## Multiply OH data (coefficients) by industry output
        df2 = (df.merge(fba, on='Sector')
               .assign(FlowAmount = lambda x: x[year]*x['Output'])
               .drop(columns=[year, 'Output', 'USEEIO Code'])
               .rename(columns={'FlowAmount': year})
               .assign(Unit = 'DALY')
               )
        if len(df_total) == 0:
            df_total = df2.copy()
        else:
            df_total = pd.concat([df_total, df2[year]], axis=1)

    # Average across all years
    df_total['FlowAmount'] = df_total[years].mean(axis=1)
    df_total = df_total.assign(Year=years[-1])

    return df_total.reindex(columns=cols)

df_illness = generate_OH_totals(file=f'{repo}/{file}', years=years)
df_illness.to_csv('data/Huang_Occupational_Health_illness.csv', index=False)

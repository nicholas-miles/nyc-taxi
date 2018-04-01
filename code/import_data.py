import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

# subway_data_list = ['../data/turnstile_17{}.txt'.format(x) 
#                   for x in [1125,1202,1209,1223,1230]
#                  ]

dfs = {'taxi': pd.read_csv('../data/yellow_tripdata_2017-12.csv', index_col='tpep_pickup_datetime', parse_dates=True, infer_datetime_format=True),
       # 'subway': pd.concat([pd.read_csv(file) for file in subway_data_list]),
       'weather': pd.read_csv('../data/1260113.csv', index_col='DATE', parse_dates=True, infer_datetime_format=True)
       # 'shapes': geo.read_file('../data/zones/taxi_zones.shp')
      }

dfs['taxi'] = dfs['taxi']['2017-12-01':'2018-01-01']
                              dfs['taxi'].total_amount < 300]
dfs['taxi_agg'] = dfs['taxi'][['tpep_dropoff_datetime', 'total_amount']]
dfs['taxi_agg'] = dfs['taxi_agg'].resample('1H').count()['total_amount']

dfo = pd.DataFrame(pd.date_range('2017-12-01', '2017-12-31', freq='H'))

raise SystemExit
dfs['taxi']['hour'] = dfs['taxi'].tpep_pickup_datetime.apply(lambda x: x[11:13])\
                                                      .astype('uint8')
taxi_dfo = dfs['taxi'][['PULocationID','hour','total_amount']]\
                .groupby(['PULocationID', 'hour'])\
                .count()\
                .reset_index()
taxi_dfo.set_index('PULocationID')

dfo = dfs['shapes'].merge(taxi_dfo, left_on='LocationID', right_index=True)

for frame in range(0,25):
    base = dfo[['geometry']].plot(alpha=0.2)
    dfo[['geometry', 'hour', 'total_amount']]\
            .loc[lambda df: df.hour == frame][['geometry','total_amount']]\
            .plot(ax=base, column='total_amount')
    plt.axis('off')
    plt.savefig('../out/{}_taxi.png'.format(frame), format='png')
    plt.close()
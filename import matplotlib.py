import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Load the data efficiently using pandas
df1 = pd.read_csv('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', delimiter=';', usecols=[0, 1, 2, 3, 4], names=['navn', 'stasjon', 'dato1', 'temp1', 'trykk1'], skiprows=1)
df2 = pd.read_csv('trykk_og_temperaturlogg_rune_time.csv.txt', delimiter=';', usecols=[0, 1, 2, 3, 4], names=['dato2', 'tid_siden_start', 'trykk2', 'abs_trykk2', 'temp2'], skiprows=1)

# Replace commas with dots and convert columns to float
df1['temp1'] = df1['temp1'].str.replace(',', '.').astype(float)
df1['trykk1'] = df1['trykk1'].str.replace(',', '.').astype(float)
df2['temp2'] = df2['temp2'].str.replace(',', '.').astype(float)
df2['abs_trykk2'] = df2['abs_trykk2'].str.replace(',', '.').astype(float) * 10  # Multiply abs_trykk2 by 10 directly

# Process dates in df1
df1['dato1'] = pd.to_datetime(df1['dato1'], format='%d.%m.%Y %H:%M')

# Process dates in df2
def convert_date(date):
    if '00' in date and 'am' in date:
        date = date.replace('00', '12', 1)
    if "/" in date:
        return datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p').strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.strptime(date, '%m.%d.%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')

df2['dato2'] = df2['dato2'].apply(convert_date)
df2['dato2'] = pd.to_datetime(df2['dato2'], format='%Y-%m-%d %H:%M:%S')

# Remove duplicates from df2 (to avoid ValueError when reindexing)
df_ten_seconds = df2[['dato2', 'temp2']].drop_duplicates(subset='dato2').set_index('dato2').rename(columns={'temp2': 'Ten Seconds'})

# Prepare data for plotting
df_hourly = df1[['dato1', 'temp1']].set_index('dato1').rename(columns={'temp1': 'Hourly'})

# Align indexes and interpolate hourly data
common_index = df_hourly.index.union(df_ten_seconds.index)
df_hourly_reindexed = df_hourly.reindex(common_index).interpolate()
df_ten_seconds_reindexed = df_ten_seconds.reindex(common_index)

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(df_hourly_reindexed.index, df_hourly_reindexed['Hourly'], label='Hourly Data', color='green')
plt.plot(df_ten_seconds_reindexed.index, df_ten_seconds_reindexed['Ten Seconds'], label='10 Second Data', color='blue', alpha=0.5)

# Adding titles and labels
plt.title('Hourly vs 10-Second Measurements')
plt.xlabel('Time')
plt.ylabel('Measurements')
plt.legend()
plt.grid()

# Show plot
plt.show()

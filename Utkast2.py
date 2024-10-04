import matplotlib.pyplot as plt 
import csv
import numpy as np
import pandas as pd
from datetime import datetime

navn = []
stasjon = []
dato1 = []
temp1 = []
trykk1 = []
with open('temperatur_trykk_met_samme_rune_time_datasett.csv.txt', 'r') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader) #Hopper over første linje
    for row in reader:
        navn.append(row[0])
        stasjon.append(row[1])
        dato1.append(row[2])
        temp1.append(row[3])
        trykk1.append(row[4])
        
dato2 = []
tid_siden_start = []
trykk2 = []
abs_trykk2 = []
temp2 = []
with open('trykk_og_temperaturlogg_rune_time.csv.txt', 'r') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader) #Hopper over første linje
    for row in reader:
        dato2.append(row[0])
        tid_siden_start.append(row[1])
        trykk2.append(row[2])
        abs_trykk2.append(row[3])
        temp2.append(row[4])
        
temp1_ = [s.replace(',', '.') for s in temp1] #Bytter ut , med . i temp1
temp1_float = [float(num) for num in temp1_ if num] #Endrer temp1 fra str til float

dato1_ = [s for s in dato1 if s] #Fjerner tom string
dato1_2 = [s for s in dato1 if s] #Fjerner tom string

trykk1_ = [s.replace(',', '.') for s in trykk1] #Bytter ut , med . i trykk1
trykk1_float = [float(num) for num in trykk1_ if num] #Endrer trykk1 fra str til float

temp2_ = [s.replace(',', '.') for s in temp2] #Bytter ut , med . i trykk1
temp2_float = [float(num) for num in temp2_ if num] #Endrer trykk1 fra str til float

abs_trykk2_ = [s.replace(',', '.') for s in abs_trykk2] #Bytter ut , med . i trykk1
abs_trykk2_float = [float(num) for num in abs_trykk2_ if num] #Endrer trykk1 fra str til float



Dato_2Form = []

for date in dato2:
    if '00' in date and 'am' in date:
        date = date.replace('00', '12', 1) 
     
    if "/" in date:
        formatert_dato1 = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p').strftime('%Y-%m-%d %H:%M:%S')
        Dato_2Form.append(formatert_dato1)
    else:
        formatert_dato1 = datetime.strptime(date, '%m.%d.%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
        Dato_2Form.append(formatert_dato1)

dato1_2 = [] 

for date in dato1_:
    formatert_dato3 = datetime.strptime(date, '%d.%m.%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    dato1_2.append(formatert_dato3)

abs_trykk2_float10 = []
for i in abs_trykk2_float:
    abs_trykk2_float10.append(i*10)
    

hourly_index =pd.to_datetime(dato1_2)
hourly_data = temp1_float  # Replace with your actual data
df_hourly = pd.DataFrame(hourly_data, index=hourly_index, columns=['Hourly'])
    
# Create 10-second data from 11.06.2021 14:23 to 13.06.2021 22:34
ten_second_index = pd.to_datetime(Dato_2Form)
ten_second_data = temp2_float  # Replace with your actual data
df_ten_seconds = pd.DataFrame(ten_second_data, index=ten_second_index, columns=['Ten Seconds'])

# Optional: Remove duplicates if any (not expected in this generation)
df_ten_seconds = df_ten_seconds[~df_ten_seconds.index.duplicated(keep='first')]

# Reindex to a common frequency
common_index = df_hourly.index.union(df_ten_seconds.index)
df_hourly_reindexed = df_hourly.reindex(common_index).interpolate()  # Forward fill for hourly data
df_ten_seconds_reindexed = df_ten_seconds.reindex(common_index)

# Plotting
plt.figure(figsize=(14, 7))

# Plotting hourly data
plt.plot(df_hourly_reindexed.index, df_hourly_reindexed['Hourly'], label='Hourly Data', color='green',)

# Plotting 10-second data
plt.plot(df_ten_seconds_reindexed.index, df_ten_seconds_reindexed['Ten Seconds'], label='10 Second Data', color='blue', alpha=0.5)

# Adding titles and labels
plt.title('Hourly vs 10-Second Measurements')
plt.xlabel('Time')
plt.ylabel('Measurements')
plt.legend()
plt.grid()

# Show plot
plt.show()
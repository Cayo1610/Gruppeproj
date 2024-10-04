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
        formatert_dato1 = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p').strftime('%d.%m.%Y %H:%M')
        Dato_2Form.append(formatert_dato1)
    else:
        formatert_dato1 = datetime.strptime(date, '%m.%d.%Y %H:%M').strftime('%d.%m.%Y %H:%M')
        Dato_2Form.append(formatert_dato1)
       
 

abs_trykk2_float10 = []
for i in abs_trykk2_float:
    abs_trykk2_float10.append(i*10)
    
# Create DataFrames for both datasets
df_hourly = pd.DataFrame({'Temperature': temp1_float}, index=dato1_)
df_second = pd.DataFrame({'Temperature': temp2_float}, index=Dato_2Form)

# Combine the two datasets using an outer join (preserves all data points)
combined_index = df_hourly.index.union(df_second.index)

#df_Dato_2Form = df_Dato_2Form[~df_Dato_2Form.index.duplicated(keep="first")]
df_second_d = df_second[~df_second.index.duplicated(keep="first")]


# Reindex both datasets without interpolation for missing data
df_hourly_reindexed = df_hourly.reindex(combined_index)
df_second_reindexed = df_second_d.reindex(combined_index)

# Plotting both datasets on the same plot
plt.figure(figsize=(10, 6))

# Plot hourly data (with NaN where there is no data)
plt.plot(df_hourly_reindexed.index, df_hourly_reindexed['Temperature'], color='green', label="Hourly Data")

# Plot second-interval data (with NaN where there is no data)
plt.plot(df_second_reindexed.index, df_second_reindexed['Temperature'], color='blue', label="10-second Data", alpha=0.6)

# Label the plot
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title('Temperature Comparison: Hourly vs 10-second Interval')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

# Adjust layout
plt.tight_layout()

# Show the figure
plt.show()
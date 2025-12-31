#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ### Load dataset

# In[4]:


data = pd.read_csv("Public_Transport_Trips_EDA.csv")


# ### Data Understanding

# In[5]:


data.head()


# In[7]:


data.tail()


# ### The table above contains 'NAN', which indicate the presence of missing data.

# In[8]:


data.info()


# ### Table contains 1000 rows and 11 columns. Columns 5, 6, and 7 contain missing values, representing a total of 100 data points. Additionally, Columns 10 and 11, which are unnamed and contain a significant amount of missing data, should be removed from the dataset.

# ### Remove Irrelevant Colunms including Trip ID, Unnamed:10, Unamed:11

# In[9]:


data.drop("Trip_ID", axis=1, inplace=True)
data.drop("Unnamed: 10", axis=1, inplace=True)
data.drop("Unnamed: 11", axis=1, inplace=True)


# In[10]:


data.info()


# ### Table contains 1000 rows and 8 columns

# ### Confimring  Missing Values

# In[11]:


data.isnull().sum()


# In[12]:


### Percentage of missing Value
data.isnull().mean() * 100


# In[15]:


### Missing value visualization
##Install Missingno
import missingno as msn


# In[16]:


msn.bar(data, color="blue")


# In[14]:


### Statistical Summary of the numerical data
data.describe()


# In[23]:


### Statistical Summary for the  categorical data
cat_data = data.select_dtypes(include=["object", "category", "bool"])
cat_data.describe()


# ### Replacing missing data with the median

# In[86]:


data["Passenger_Count"] = data["Passenger_Count"].fillna(data["Passenger_Count"].median())
data["Fare_Amount"] = data["Fare_Amount"].fillna(data["Fare_Amount"].median())
data["Trip_Duration_Minutes"] = data["Trip_Duration_Minutes"].fillna(data["Trip_Duration_Minutes"].median())
data["Trip_Date"] = data["Trip_Date"].fillna(data["Trip_Date"].median())


# In[84]:


data.isnull().sum()


# ### Change Departure_time and Trip_date to Pandas date time

# In[21]:


data["Departure_Time"] = pd.to_datetime(data["Departure_Time"])
data["Trip_Date"] = pd.to_datetime(data["Trip_Date"])


# In[82]:


data.info()


# ### Checking for Duplicates

# In[25]:


data.duplicated().sum()


# ### Checking for outliers 

# In[26]:


### Numerical coulumns
numerical_columns = data.select_dtypes(include="number")
numerical_columns


# In[27]:


fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 6))
ax = ax.flatten()

for idx, col in enumerate(numerical_columns):
    sns.histplot(data[col], ax=ax[idx], kde=True, color="skyblue")
    ax[idx].set_title(f"Histogram for {col}", fontsize=14)

plt.tight_layout()
plt.show()


# In[28]:


import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 3, figsize=(20, 6))
ax = ax.flatten()

for i, col in enumerate(["Passenger_Count", "Fare_Amount", "Trip_Duration_Minutes"]):
    sns.boxplot(data=data, y=col, ax=ax[i], color="lightblue")
    ax[i].set_title(f"Boxplot for {col}")

plt.tight_layout()
plt.show()


# ### Data has no outliers, histplot show a normal distribution and box blot show no outliers

# ### Viewing unique variables for categorical Data and adjusting for speling inconsistencies

# In[31]:


data["Mode_of_Transport"].value_counts()


# In[32]:


### Spelling adjutment for the varrious mode of Transport
data["Mode_of_Transport"] = data["Mode_of_Transport"].str.lower()


# In[33]:


data["Mode_of_Transport"] = data["Mode_of_Transport"].str.capitalize()


# In[34]:


data["Mode_of_Transport"].value_counts()


# In[35]:


data["Departure_Station"].value_counts()


# In[36]:


### Spelling adjutment for the Departure station
data["Departure_Station"] = data["Departure_Station"].str.strip()
data["Departure_Station"].value_counts()


# In[37]:


data["Arrival_Station"].value_counts()


# In[39]:


### Spelling adjutment for the Arrival station
data["Arrival_Station"] = data["Arrival_Station"].str.lower()
data["Arrival_Station"] = data["Arrival_Station"].str.title()
data["Arrival_Station"].value_counts()


# In[66]:


### Converting depature Time to Pandas date time
data["Trip_Date"] = pd.to_datetime(data["Trip_Date"])


# In[49]:


data.head(10)


# In[87]:


cat_data = data.select_dtypes(include=["object", "category", "bool"])
cat_data.describe()


# ### Statistical analysis

# In[51]:


#### Number of Passengers per mode of Transport
passengers_per_mode = data.groupby('Mode_of_Transport')['Passenger_Count'].sum().sort_values(ascending=False)
print(passengers_per_mode)


# In[53]:


### Total passengers per mode of transport
plt.figure(figsize=(8,5))
plt.bar(passengers_per_mode.index, passengers_per_mode.values, color=['skyblue','orange','green','red'])
plt.title('Total Passengers by Mode of Transport')
plt.xlabel('Mode of Transport')
plt.ylabel('Total Passengers')
plt.show()


# ### Bus is the dominant mode of transport, follwoed by Ferry and Train  while Tram is the least mode of Transport

# In[54]:


### Average fare per mode of transport
avg_fare_per_mode = data.groupby('Mode_of_Transport')['Fare_Amount'].mean()
plt.figure(figsize=(8,5))
plt.bar(avg_fare_per_mode.index, avg_fare_per_mode.values, color='lightgreen')
plt.title('Average Fare per Mode of Transport')
plt.xlabel('Mode of Transport')
plt.ylabel('Average Fare')
plt.show()


# ### Average fare is almost similar for all types of transport except for the ferry which is slightly lower

# In[59]:


###Total revenue per day of the week
data['Revenue'] = data['Passenger_Count'] * data['Fare_Amount']
revenue_per_day = data.groupby('Day_of_Week')['Revenue'].sum()

plt.figure(figsize=(8,5))
plt.bar(revenue_per_day.index, revenue_per_day.values, color='salmon')
plt.title('Total Revenue per Day of the Week')
plt.xlabel('Day of Week')
plt.ylabel('Revenue')
plt.show()


# ### A slidely higher revenue is generated on Sunday,Tuesday, Saturday and Monday. 

# In[60]:


###Busiest departure stations
busiest_departure = data.groupby('Departure_Station')['Passenger_Count'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,5))
plt.bar(busiest_departure.index, busiest_departure.values, color='teal')
plt.title('Total Passengers per Departure Station')
plt.xlabel('Departure Station')
plt.ylabel('Total Passengers')
plt.xticks(rotation=45)
plt.show()


# ### For departure, Central station has the highest number of customers

# In[61]:


###Busiest arrival stations
busiest_arrival = data.groupby('Arrival_Station')['Passenger_Count'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,5))
plt.bar(busiest_arrival.index, busiest_arrival.values, color='purple')
plt.title('Total Passengers per Arrival Station')
plt.xlabel('Arrival Station')
plt.ylabel('Total Passengers')
plt.xticks(rotation=45)
plt.show()


# ### For arrival, the airport has the highest numberof arrivals

# In[72]:


### Average trip duration by mode
avg_duration_mode = data.groupby('Mode_of_Transport')['Trip_Duration_Minutes'].mean()
plt.figure(figsize=(8,5))
plt.bar(avg_duration_mode.index, avg_duration_mode.values, color='skyblue')
plt.title('Average Trip Duration by Mode of Transport')
plt.xlabel('Mode of Transport')
plt.ylabel('Trip Duration (Minutes)')
plt.show()


# ### There is no significant difference in trip duration across the four modes of transportation

# In[69]:


### Correlation between fare and trip duration
plt.figure(figsize=(8,5))
sns.scatterplot(data=data, x='Trip_Duration_Minutes', y='Fare_Amount', hue='Mode_of_Transport')
plt.title('Fare vs Trip Duration')
plt.xlabel('Trip Duration (Minutes)')
plt.ylabel('Fare Amount')
plt.show()


# ### There is no correlation between the fare amonut and the trip duration

# In[71]:


###Top 10 high-revenue trips
high_revenue_trips = data.sort_values(by='Revenue', ascending=False).head(10)
plt.figure(figsize=(12,6))
plt.bar(high_revenue_trips['Route'], high_revenue_trips['Revenue'], color='gray')
plt.title('Top 10 High-Revenue Trips')
plt.xlabel('Route')
plt.ylabel('Revenue')
plt.xticks(rotation=90)
plt.show()


# ### These are the top 10 high revenue trips, with the North Station to Airport route being the highest revenue generated route

# In[73]:


data['Route'] = data['Departure_Station'] + " → " + data['Arrival_Station']


# In[75]:


route_summary = data.groupby('Route').agg({
    'Passenger_Count': 'sum',
    'Fare_Amount': 'sum'
}).reset_index()


# In[76]:


top10_passengers = route_summary.sort_values('Passenger_Count', ascending=False).head(10)
top10_revenue = route_summary.sort_values('Fare_Amount', ascending=False).head(10)


# In[77]:


plt.figure(figsize=(12,6))
plt.barh(top10_passengers['Route'], top10_passengers['Passenger_Count'], color='skyblue', label='Passenger Count')
plt.title('Top 10 Most Popular Routes (by Passenger Count)')
plt.xlabel('Total Passengers')
plt.ylabel('Route')
plt.gca().invert_yaxis()  
plt.tight_layout()
plt.show()


# ### These are the top10 most popular routes.

# In[78]:


top10_combined = route_summary.sort_values('Passenger_Count', ascending=False).head(10)
plt.figure(figsize=(12,6))
plt.bar(top10_combined['Route'], top10_combined['Passenger_Count'], color='skyblue', label='Passenger Count')
plt.bar(top10_combined['Route'], top10_combined['Fare_Amount'], bottom=top10_combined['Passenger_Count'], color='orange', label='Fare Amount')
plt.title('Top 10 Routes: Passenger Count + Fare Amount (Stacked)')
plt.xlabel('Route')
plt.ylabel('Value')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()


# In[96]:


# --- Calculate Average Fare and Duration per Transport Mode ---
summary = data.groupby('Mode_of_Transport')[['Fare_Amount', 'Trip_Duration_Minutes']].mean().reset_index()
x = np.arange(len(summary['Mode_of_Transport']))  
width = 0.35  
plt.figure(figsize=(10, 6))
plt.bar(x - width/2, summary['Fare_Amount'], width, label='Average Fare ($)', color='skyblue')
plt.bar(x + width/2, summary['Trip_Duration_Minutes'], width, label='Avg Duration (Minutes)', color='orange')
plt.title('Average Fare and Trip Duration by Mode of Transport', fontsize=14, weight='bold')
plt.xlabel('Mode of Transport', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.xticks(x, summary['Mode_of_Transport'])
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# ### The fare amount and the duration of the trip does not determine the choice of transport mode by the customers.

# In[101]:


# Passenger count by mode of transport on top10 busiest route
data['Route'] = data['Departure_Station'] + " → " + data['Arrival_Station']
route_passengers = data.groupby('Route')['Passenger_Count'].sum().reset_index()
top_routes = route_passengers.sort_values(by='Passenger_Count', ascending=False).head(10)
top_routes_data = data[data['Route'].isin(top_routes['Route'])]
grouped = top_routes_data.groupby(['Route', 'Mode_of_Transport'])['Passenger_Count'].sum().unstack(fill_value=0)
grouped['Total_Passengers'] = grouped.sum(axis=1)
grouped = grouped.sort_values(by='Total_Passengers', ascending=False)
grouped = grouped.drop(columns='Total_Passengers')  
plt.figure(figsize=(14,7))
grouped.plot(kind='bar', stacked=True, colormap='tab20', edgecolor='black')
plt.title('Passenger Count by Transport Mode on Top 10 Busiest Routes (Sorted)', fontsize=16)
plt.xlabel('Route', fontsize=14)
plt.ylabel('Total Passengers', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Mode of Transport')
plt.tight_layout()
plt.show()



# In[102]:


# Passenger count by day of the week on top 10 passenger count
data['Route'] = data['Departure_Station'] + " → " + data['Arrival_Station']
route_passengers = data.groupby('Route')['Passenger_Count'].sum().reset_index()
top_routes = route_passengers.sort_values(by='Passenger_Count', ascending=False).head(10)
top_routes_data = data[data['Route'].isin(top_routes['Route'])]
grouped = top_routes_data.groupby(['Route', 'Day_of_Week'])['Passenger_Count'].sum().unstack(fill_value=0)
grouped['Total_Passengers'] = grouped.sum(axis=1)
grouped = grouped.sort_values(by='Total_Passengers', ascending=False)
grouped = grouped.drop(columns='Total_Passengers')  # remove helper column
plt.figure(figsize=(14,7))
grouped.plot(kind='bar', stacked=True, colormap='tab20', edgecolor='black')
plt.title('Passenger Count by Day of the Week on Top 10 Busiest Routes', fontsize=16)
plt.xlabel('Route', fontsize=14)
plt.ylabel('Total Passengers', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Day of the Week')
plt.tight_layout()
plt.show()


# In[104]:


###Total Passengercount per hour of the day
df = pd.DataFrame(data, columns=["Mode_of_Transport", "Departure_Station", "Arrival_Station", "Departure_Time", "Passenger_Count", "Fare_Amount", "Trip_Duration_Minutes", "Trip_Date", "Day_of_Week"])
df['Departure_Time'] = pd.to_datetime(df['Departure_Time'], format='%H:%M:%S')
df['Hour'] = df['Departure_Time'].dt.hour
hourly_passenger_count = df.groupby('Hour')['Passenger_Count'].sum()
plt.figure(figsize=(10,6))
plt.plot(hourly_passenger_count.index, hourly_passenger_count.values, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)
plt.title("Passenger Count per Hour of the Day", fontsize=14)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Total Passenger Count", fontsize=12)
plt.xticks(hourly_passenger_count.index)  # Show each hour
plt.grid(True)


# ## Given the observed decline in passenger traffic between the hours of 11:00–12:00 and 20:00–22:00, we recommend offering discounted tickets during these periods. This initiative will help encourage greater customer engagement and utilization of Metromove services during off-peak hours.

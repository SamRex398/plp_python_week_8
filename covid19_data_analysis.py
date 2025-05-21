#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Global Data Analysis and Reporting
# 
# This notebook analyzes global COVID-19 trends including cases, deaths, recoveries, and vaccinations across countries and time. It includes data cleaning, exploratory data analysis (EDA), visualizations, and narrative insights.

# ## 1. Data Collection
# 
# Download the latest cleaned COVID-19 dataset from Our World in Data:
# - [Our World in Data COVID-19 Dataset (CSV)](https://covid.ourworldindata.org/data/owid-covid-data.csv)
# 
# Save the file as `owid-covid-data.csv` in the same folder as this notebook.

# In[ ]:


# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
sns.set(style="whitegrid")


# ## 2. Data Loading & Exploration

# In[ ]:


# Load the dataset
df = pd.read_csv('owid-covid-data.csv')

# Preview columns
print(df.columns)

# Preview first 5 rows
df.head()


# In[ ]:


# Check for missing values
df.isnull().sum()


# ## 3. Data Cleaning

# In[ ]:


# Filter countries of interest
countries = ['Kenya', 'United States', 'India']
df_countries = df[df['location'].isin(countries)].copy()

# Drop rows with missing dates or critical values
df_countries = df_countries.dropna(subset=['date', 'total_cases', 'total_deaths'])

# Convert date column to datetime
df_countries['date'] = pd.to_datetime(df_countries['date'])

# Fill missing numeric values with interpolation
numeric_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']
for col in numeric_cols:
    if col in df_countries.columns:
        df_countries[col] = df_countries[col].interpolate(method='linear')


# ## 4. Exploratory Data Analysis (EDA)

# In[ ]:


# Plot total cases over time for selected countries
plt.figure(figsize=(12,6))
for country in countries:
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)
plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.show()


# In[ ]:


# Plot total deaths over time
plt.figure(figsize=(12,6))
for country in countries:
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['total_deaths'], label=country)
plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.show()


# In[ ]:


# Compare daily new cases between countries
plt.figure(figsize=(12,6))
for country in countries:
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['new_cases'], label=country)
plt.title('Daily New COVID-19 Cases')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend()
plt.show()


# In[ ]:


# Calculate death rate
df_countries['death_rate'] = df_countries['total_deaths'] / df_countries['total_cases']

# Plot death rate over time
plt.figure(figsize=(12,6))
for country in countries:
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['death_rate'], label=country)
plt.title('COVID-19 Death Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Death Rate')
plt.legend()
plt.show()


# ## 5. Visualizing Vaccination Progress

# In[ ]:


# Plot cumulative vaccinations over time for selected countries
plt.figure(figsize=(12,6))
for country in countries:
    subset = df_countries[df_countries['location'] == country]
    if 'total_vaccinations' in subset.columns:
        plt.plot(subset['date'], subset['total_vaccinations'], label=country)
plt.title('Total COVID-19 Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.show()


# ## 6. Optional: Choropleth Map of Cases by Country
# 
# This section requires `plotly` to be installed. You can install it via `pip install plotly`.
# 
# It visualizes the latest total cases by country on a world map.

# In[ ]:


import plotly.express as px

# Prepare data for latest date
latest_date = df.groupby('location')['date'].max().reset_index()
latest_data = pd.merge(df, latest_date, on=['location', 'date'], how='inner')

# Filter out entries without iso_code or total_cases
latest_data = latest_data.dropna(subset=['iso_code', 'total_cases'])

# Plot choropleth map
fig = px.choropleth(latest_data, locations='iso_code', color='total_cases', hover_name='location',
                    color_continuous_scale='Reds',
                    title='Global COVID-19 Total Cases by Country (Latest)')
fig.show()


# ## 7. Insights & Reporting
# 
# ### Key Insights
# - The United States has had the highest total cases and deaths among the selected countries.
# - India experienced significant waves of new cases, especially in mid-2021.
# - Kenya shows a slower but steady increase in cases and vaccinations.
# - Death rates vary over time and between countries, reflecting different healthcare responses.
# - Vaccination rollouts have progressed at different paces, with the US leading among the selected countries.
# 
# ### Anomalies & Patterns
# - Sudden spikes in new cases often correspond to new variants or changes in testing/reporting.
# - Some missing data points were interpolated to maintain continuity.
# 
# ### Conclusion
# This analysis provides a snapshot of the COVID-19 pandemic's progression and vaccination efforts in selected countries. Further analysis could include more countries, additional metrics, and deeper statistical modeling.

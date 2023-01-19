#!/usr/bin/env python
# coding: utf-8

# ## Importing the libraries.

# In[1]:


import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


# ## Loading the datasets.

# In[2]:


observations = pd.read_csv('observations.csv')
species = pd.read_csv('species_info.csv')


# ## Exploring both datasets.

# ### Species.

# In[3]:


print(species.head())


# #### The `species_info.csv` contains information on the different species in the National Parks. 
# #### The columns in the data set include:
# #### `category` - The category of taxonomy for each species;
# #### `scientific_name` - The scientific name of each species;
# #### `common_names` - The common names of each species;
# #### `conservation_status` - The species conservation status.

# ### Observations.

# In[4]:


print(observations.head())


# #### The `Observations.csv` contains information from recorded sightings of different species throughout the national parks in the past 7 days. 
# #### The columns included are:
# #### `scientific_name` - The scientific name of each species;
# #### `park_name`- The name of the national park;
# #### `observations` - The number of observations in the past 7 days.

# ### Checking datasets dimentions.

# In[5]:


print(f'species shape: {species.shape}')
print(f'observations shape: {observations.shape}')


# #### The `species` dataset has 5,824 rows, and 4 columns, while `observations` has 23,2296 rows, and 3 columns. 

# ## Exploring ```species``` dataset more in depth.

# ### Dataset structure.

# In[6]:


print(f'Total number of species: {species.scientific_name.nunique()}')
print(f'Total number of category: {species.category.nunique()}')
print(f'Names of categories: {species.category.unique()}')


# #### The `species` dataset contains 5541 different species, distribuited in 7 types of categories.

# ### Exploring the ```category``` column.

# In[7]:


species.groupby('category').size()


# #### We can see that by far `Vascular Plant` is the most commun one and `Reptile` is the most rare.

# ### Exploring the ```conservation_status``` column.

# In[8]:


print(f'Number of conservation statuses: {species.conservation_status.nunique()}')
print(f'Conservation statuses names: {species.conservation_status.unique()}')


# #### The `conservation_status` column shows 4 different types of status and a 'nan' value. 

# In[9]:


print(species.groupby('conservation_status').size())
print(f'The data shows {species.conservation_status.isna().sum()} NaNs values')


# #### There are 5,633 NaNs values which, in this case, means that they are species without concerns. 
# #### On the other hand there are 161 species of concern, 16 endangered, 10 threatened, and 4 in recovery.

# ### Checking for duplicates.

# In[10]:


print(species.duplicated().sum())


# #### There is no duplicated values. 

# ## Looking at the `observations` dataset.

# In[11]:


print(f'The data shows a total of {observations.park_name.nunique()} parks')
print(f'The parks names are the following: {observations.park_name.unique()}')


# #### We can see that the data was captured on four different parks.

# ### Checking the total number of observations recored.

# In[12]:


print(f'Observations: {observations.observations.sum()}')


# #### The dataset has a total of 3314739 observations divided amoung four parks.

# ### Taking a closer look at the `scientific_name` column.

# In[13]:


print(f'Scientific names: {observations.scientific_name.nunique()}')


# #### The `observations` dataset shows a total of 5541 different scientific names registered. The same as the `species` dataset. 

# ### Checking for duplicates.

# In[14]:


print(observations.duplicated().sum())


# #### There is 15 duplicated rows in the `observations` dataset.

# ### Deleting the duplicates.

# In[15]:


observations = observations.drop_duplicates()


# ### Checking for NaNs.

# In[16]:


print(observations.isnull().sum())


# #### There is no NaNs values in this dataset.

# ### Filling the NaNs in the `species` dataset.

# #### The possible values for this column are the following: 
# #### `Species of Concern`: declining or appear to be in need of conservation
# #### `Threatened`: vulnerable to endangerment in the near future
# #### `Endangered`: seriously at risk of extinction
# #### `In Recovery`: formerly `Endangered`, but currently neither in danger of extinction throughout all or a significant portion of its range
# 
# #### In the exploration, a lot of `nan` values were detected. These values will need to be converted to `No Intervention` as this species are not in concern 

# In[17]:


species.fillna('No Intervention', inplace = True)
species.groupby('conservation_status').size()


# ## Analyzing the dataset

# ### Taking a look at how the species are distributed on the 'conservation_status' column

# In[18]:


# Grouping the data to get a better understand of distribution of species among the conservation_status column.
conservationCategory = species[species.conservation_status != 'No Intervention'].groupby(['conservation_status', 'category'])['scientific_name'].count().unstack()
print(conservationCategory)


# In[19]:


# Plotting a bar chart to visualize the distribution of species among the conservation_status column.
ax = conservationCategory.plot(kind = 'bar', figsize=(8,6), stacked = True)


# #### It is possible to see that the biggest number of species are classified as `Species of Concern`. Having that the `Bird` category is the one with the biggest volume of species in this classification. 

# ### Analyzing the volume and distribution of each animal categories amoung the parks.

# In[20]:


# Joining the observations with the species dataset.
outer = observations.merge(species, on = 'scientific_name', how = 'outer')

# Dorpping the plants categories from the dataset
criteria1 = outer['category'] == 'Vascular Plant'
outer = outer.drop(outer[criteria1].index) 

criteria2 = outer['category'] == 'Nonvascular Plant'
outer = outer.drop(outer[criteria2].index) 

# Grouping the data in the necessary order. 
outer_cate = outer.groupby(['park_name','category'])['observations'].sum().unstack()

# Plotting a bar char that shows the distribution and volume of each category among the parks.
ax = outer_cate.plot(kind = 'bar', figsize = (14,10))
plt.title('Volume and Distribution of Animals Categories Among the Parks')
plt.ylabel('Number of Observations')
plt.xlabel("Park Name")
plt.show()


# #### It is possible to conclude that `Yellowstone National Park` has the biggest volume of animals for every category, and specially `birds`. 

# ## Checking the mammal population density among the parks.

# ### Creating a dataset with each park the total area (km²).

# In[21]:


# Creating a new dataset.
data = [('Great Smoky Mountains National Park', 2144.10), ('Yosemite National Park', 3027.81),('Bryce National Park', 1342.57),('Yellowstone National Park', 8983.18)]
park_area = pd.DataFrame(data, columns=["park_name", "area_(km²)"])

print(park_area.head())

# The data was provided by ChatGPT.


# ### Getting the total area of the parks combined. 

# In[22]:


# Summing the total area of the four parks
total_area = park_area['area_(km²)'].sum()
print(f'Total area: {total_area}km²')


# #### The four parks have a total area of 15497.66km².

# ### Counting the total mammal observations among the four pakrs. 

# In[23]:


# Grouping the data to get the sum of mammal observations.
total_mammal_obs = outer[outer.category == 'Mammal'].groupby('category')['observations'].sum().reset_index()

# Transforming the total_mammal_obs in a df. 
m_obs_result = pd.DataFrame(total_mammal_obs)

print(f'Total observations: {m_obs_result.iloc[0,1]}')


# #### Was recored 162608 observations of mammals in the four parks combined.

# ### Encountering the general mammal population density among the four parks combined. 

# In[24]:


# Isoleting the sum of observations from total_mammal_obs.
t_m_obs =  m_obs_result.iloc[0,1]

# Calculating the general mammal density.
general_m_density = round((t_m_obs / total_area),2)
print(f'General mammal density: {general_m_density}')


# #### The General mammal population density is 10 mammals per each km².

# ### Joining the `park_area` dataset with the `outer` dataset.  

# In[25]:


# Joining the tables.
outer_area = outer.merge(park_area, on ='park_name', how = 'outer')
print(outer_area.head(2))


# #### Now each park has the indication of its area in km².

# ### Counting the total number of mammals on each park and checking the density of its population by km². 

# In[26]:


# Grouping the data to show the total population of mammals in each park and its total area.
outer_density = outer_area[outer_area.category == 'Mammal'].groupby(['park_name','area_(km²)', 'category'])['observations'].sum().reset_index().rename(columns ={'observations':'total_observations'})

# Chenging the outer_density to a df. 
outer_density = pd.DataFrame(outer_density)

# Finding the mammal population density for each park.
outer_density['population_density'] = outer_density['total_observations'] / outer_density['area_(km²)']
# print(outer_density)

# Plotting a bar chart to analyze the mammal population density by each park. 
ax = outer_density['population_density'].plot(kind = 'bar', figsize = (14,10))
ax = plt.gca()
ax.set_xticklabels(outer_density['park_name'])
plt.xlabel('Park Name')
plt.ylabel('Number of Mammals per km²')
plt.title('Mammal Population Density per km² Among U.S. National Parks')
plt.show()


# #### Though the Yellowstone national park is the one with the biggest number mammals observations registered the Bryce National is the US national park with the higher probability of observing mammals as it is the park with a higher mammal population density.

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


all_data = pd.read_csv("F:/Sales_Data/all_data.csv")
all_data.head()


# ### Clean Up the Data!

# #### Drops Rows of Nan

# In[3]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()


# In[4]:


all_data = all_data.dropna(how='all')


# #### Augment Data with additional Columns

# #### First we separate month from the Order Date

# #### Separated Datapoints contains 'Or' string. So,

# #### Find 'Or' and Delete it 

# In[5]:


temp_df = all_data[all_data['Order Date'].str[0:2] == 'Or']
temp_df.head()


# #### Remove datapoints that contains 'Or'

# In[6]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']


# #### After Cleaning the data we now add the Month Column

# In[9]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# #### Convert columns to the correct type

# In[11]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each']) 


# #### Add a city column to the dataset

# In[22]:


# Let's use .apply() 
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")


all_data.head()


# In[ ]:





# ### Question 1: What was the best month for sales? How much was earned that month?

# #### We have Qty ordered and Price column, with we create additional column 'Sales'

# In[12]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# #### We can use Groupby function with sum to find the answer

# In[14]:


result = all_data.groupby('Month').sum()
print(result)


# #### Here we can see that 12th month i.e. December month has the hoghest of sales

# #### Now Let's Visualize the data for quick insights

# In[16]:


import matplotlib.pyplot as plt

months = range(1,13)

plt.bar(months, result['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# ###  Question 2 : Which City had a highest number of Sales?

# In[24]:


results = all_data.groupby('City').sum()
results


# #### Here we can see that San Fransisco has the highest of Sales

# #### Let's visualize data for quick insights

# In[29]:


import matplotlib.pyplot as plt

cities = all_data['City'].unique()

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation = 'vertical', size =8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City')
plt.show()


# ###  Question 3 : What time should we display advertisements to maximize the likelihood of customer's buying product?

# In[52]:


all_data.head()


# In[34]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

all_data.head()


# In[35]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute

all_data.head()


# In[41]:


hours  = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show


# #### 11 A.M (11) or 7 P.M (19) will be the best time to place an advertisement

# ###  Question 4 : What products are most often sold together?

# In[42]:


all_data.head()


# In[43]:


# From the above data with the Order ID 176560 we can see that Gphone and Wired headphones are sold together!


# In[47]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

df = df[['Order ID', 'Grouped']].drop_duplicates()

df.head()


# In[49]:


# Referenced: https://stackoverflow.com/questions/52195887/counting-unique-pairs-of-numbers-into-a-python-dictionary

from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))
    
for key, value in count.most_common(10):
    print(key,value)


# #### We can see that Iphone and Lightning Charging cable are mostly bought together

# ###  Question 5 : What product sold the most? and why do you think it sold the most?

# In[50]:


all_data.head()


# In[56]:


product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]

plt.bar(products, quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.xticks(products, rotation='vertical', size=8)
plt.show()


# #### Here we can see that AAA Batteries are sold the most and LG Dryer and Washing machnie the least,  this could be beacuse the price of the  batteries are cheap, so now let's compare the prices, to prove this, let's plot "prices" in secondary y axis

# In[72]:


prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color = 'g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)

plt.show()


# #### Here we can see that the price and the quantity ordered are correlated, so our assumption is true

# In[ ]:





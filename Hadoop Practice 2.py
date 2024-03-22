#!/usr/bin/env python
# coding: utf-8

# ### Part 2

# SELECT lo_quantity, MAX(lo_revenue) \
# FROM (SELECT lo_revenue, MAX(lo_quantity) as lo_quantity, \
# MAX(lo_discount) as lo_discount \
# FROM lineorder \
# WHERE lo_orderpriority LIKE '%URGENT' \
# GROUP BY lo_revenue) \
# WHERE lo_discount BETWEEN 5 AND 8 \
# GROUP BY lo_quantity;

# #### Break down query:

# Inner Query - 1st MR: \
# SELECT lo_revenue, MAX(lo_quantity) as lo_quantity, MAX(lo_discount) as lo_discount \
# FROM lineorder \
# WHERE lo_orderpriority LIKE '%URGENT' \
# GROUP BY lo_revenue 
# 
# Outter Query - 2nd MR: \
# SELECT lo_quantity, MAX(lo_revenue) \
# FROM Inner Query \
# WHERE lo_discount BETWEEN 5 AND 8 \
# GROUP BY lo_quantity;

# In[1]:


#Sample for simplified code.
sample1 = ['1|1|7381|155190|828|19960102|1-URGENT|0|17|2116823|17366547|4|2032150|74711|2|19960212|TRUCK|',            '1|2|7381|67310|163|19960102|1-URGENT|0|36|4598316|17366547|9|4184467|76638|6|19960228|MAIL|',            '1|3|7381|63700|71|19920106|1-URGENT|0|8|1330960|17366547|2|1197864|99822|2|19960305|REG AIR|',            '1|4|7381|2132|943|19960102|1-URGENT|0|28|2895564|17366547|8|2634963|62047|6|19960330|AIR|',            '1|5|7381|24027|1625|19960102|1-URGENT|0|24|2282448|17366547|10|2054203|57061|4|19960314|FOB|',            '1|6|7381|15635|1368|19920102|1-URGENT|0|17|4962016|17366547|3|4614674|93037|2|19960207|MAIL|',            '1|1|7381|155190|828|19960102|1-URGENT|0|17|2116823|17366547|5|2032150|74711|2|19960212|TRUCK|',            '1|2|7381|67310|163|19960102|1-URGENT|0|36|4598316|17366547|10|4184467|76638|6|19960228|MAIL|',            '1|3|7381|63700|71|19920106|1-URGENT|0|8|1330960|17366547|6|1197864|99822|2|19960305|REG AIR|',            '1|4|7381|2132|943|19960102|1-URGENT|0|8|2895564|17366547|7|2634963|62047|6|19960330|AIR|',            '1|5|7381|24027|1625|19960102|1-URGENT|0|24|2282448|17366547|11|2054203|57061|4|19960314|FOB|',            '1|6|7381|15635|1368|19920102|1-URGENT|0|10|4962016|17366547|7|4614674|93037|2|19960207|MAIL|']


# In[2]:


#Mapper1 - Extract column name using index and filtered by indicated column.
#!/usr/bin/python
import sys
import re

for line in sys.stdin:
    columnName = line.strip().split('|', 17)
    lo_revenue = int(columnName[12])
    lo_quantity = int(columnName[8])
    lo_discount = int(columnName[11])
    lo_orderpriority = columnName[6]
    #Using regular expression for 'URGENT' value. 
    pattern = r'.*URGENT.*'
    if re.search(pattern, lo_orderpriority):
        print(f"{lo_revenue}|{lo_quantity}|{lo_discount}")


# In[3]:


sample2 = ['2032150|17|4', '4184467|36|9', '1197864|8|2', '2634963|28|8', '2054203|24|10',            '4614674|17|3', '2032150|17|5', '4184467|36|10', '1197864|8|6', '2634963|8|7',            '2054203|24|11', '4614674|10|7']


# In[4]:


#Reducer1
#!/usr/bin/python
import sys

#Dictionary with lo_revenue as key and lo_quantity/lo_discount as values.
revenueDict = {}

for line in sys.stdin:
    lo_revenue, lo_quantity, lo_discount = map(int, line.strip().split('|'))
    
    if lo_revenue in revenueDict:
        #Retrieve current quantity/discount values.
        max_lo_quantity, max_lo_discount = revenueDict[lo_revenue]
        
        #Get max value by comparing with current iterated values.
        max_lo_quantity = max(max_lo_quantity, lo_quantity)
        max_lo_discount = max(max_lo_discount, lo_discount)
        
        #Overwrite max values.
        revenueDict[lo_revenue] = (max_lo_quantity, max_lo_discount)
    else:
        #Initialize for new lo_revenue.
        revenueDict[lo_revenue] = (lo_quantity, lo_discount)

for lo_revenue, (max_lo_quantity, max_lo_discount) in revenueDict.items():
    print(f"{lo_revenue}|{max_lo_quantity}|{max_lo_discount}")


# In[5]:


sample3 = ['2032150|17|5', '4184467|36|10', '1197864|8|6', '2634963|8|8', '2054203|24|11',            '4614674|17|7']


# In[6]:


#Mapper2 - Extract column name using index and filtered by indicated column.
#!/usr/bin/python
import sys

for line in sys.stdin:
    lo_revenue, lo_quantity, lo_discount = map(int, line.strip().split('|'))
    if 5 <= lo_discount <= 8: 
        print(f"{lo_revenue}|{lo_quantity}")


# In[7]:


sample4 = ['2032150|17', '1197864|8', '2634963|8', '4614674|17']


# In[8]:


#Reducer2
#!/usr/bin/python
import sys

#Dictionary with lo_quantity as key and maximum value of lo_revenue as value. 
quantityDict = {}
print('lo_quantity|MAX(lo_revenue)')
for line in sys.stdin:
    lo_revenue, lo_quantity = map(int, line.strip().split('|'))
    
    if lo_quantity in quantityDict:
        #Get max value by comparing with current iterated values.
        max_lo_revenue = max(quantityDict[lo_quantity], lo_revenue)
    else:
        #If new lo_quantity key, initialize lo_revenue as maximum value. 
        max_lo_revenue = lo_revenue
    quantityDict[lo_quantity] = max_lo_revenue

for lo_quantity, max_lo_revenue in quantityDict.items():
    print(f"{lo_quantity}|{max_lo_revenue}")

create table lineorder (
  lo_orderkey          int,
  lo_linenumber        int,
  lo_custkey           int,
  lo_partkey           int,
  lo_suppkey           int,
  lo_orderdate         int,
  lo_orderpriority     varchar(15),
  lo_shippriority      varchar(1),
  lo_quantity          int,
  lo_extendedprice     int,
  lo_ordertotalprice   int,
  lo_discount          int,
  lo_revenue           int,
  lo_supplycost        int,
  lo_tax               int,
  lo_commitdate         int,
  lo_shipmode          varchar(10)    
);

#!/usr/bin/env python
# coding: utf-8

# #### Student Name: Mai Ngo
# #### Course Name and Number: CSC 555 Big Data Mining
# #### Assignment 2
# #### Date: 10/10/2023

# Note: My coding logic, the first column out from mapper is 'dictionary key'.

# #### Query 1

# SELECT s_suppkey, s_name, s_city, s_nation, s_phone \
# FROM supplier

# In[1]:


#Sample for simplified code. 
supplierLine = '1|Supplier#000000001|sdrGnXCDRcfriBvY0KL,i|PERU     0|PERU|AMERICA|27-989-741-2988|'


# In[2]:


#Mapper - Extract column name using index.
#!/usr/bin/python
import sys
for line in sys.stdin:
    columnName = line.strip().split('|', 7)
    s_suppkey = columnName[0]
    s_name = columnName[1]
    s_city = columnName[3]
    s_nation = columnName[4]
    s_phone = columnName[6]
    print(f"{s_suppkey}|{s_name}|{s_city}|{s_nation}|{s_phone}")


# In[3]:


#Reducer
#!/usr/bin/python
import sys
print('s_suppkey|s_name|s_city|s_nation|s_phone')
for line in sys.stdin:
    print(line)


# #### Query 2

# SELECT lo_quantity, lo_linenumber \
# FROM lineorder \
# WHERE lo_discount < 7 AND lo_tax > 3

# In[4]:


#Sample for simplified code.
line_orderLine = ['1|1|7381|155190|828|19960102|5-LOW|0|17|2116823|17366547|4|2032150|74711|4|19960212|TRUCK']


# In[5]:


#Mapper - Extract column name using index and filtered by indicated column.
#!/usr/bin/python
import sys
for line in sys.stdin:
    columnName = line.strip().split('|', 17)
    lo_discount = int(columnName[11])
    lo_tax = int(columnName[14])     
    lo_quantity = int(columnName[8])
    lo_linenumber = int(columnName[1])
    if lo_discount < 7 and lo_tax > 3:
        print(f"{lo_quantity}|{lo_linenumber}")


# In[6]:


#Reducer
#!/usr/bin/python
import sys
print('lo_quantity|lo_linenumber')
for line in sys.stdin:
    print(line)


# #### Query 3

# SELECT p_category, COUNT(p_type) \
# FROM part \
# GROUP BY p_category

# In[7]:


#Sample for simplified code.
partLines = ['1|lace spring|MFGR#1|MFGR#11|MFGR#1121|goldenrod|PROMO BURNISHED COPPER|7|JUMBO PKG|',              '2|rosy metallic|MFGR#4|MFGR#11|MFGR#4318|blush|LARGE BRUSHED BRASS|1|LG CASE|'] 


# In[8]:


#Mapper - Extract column name using index.
#!/usr/bin/python
import sys
for line in sys.stdin:
    columnName = line.strip().split('|', 8)
    p_category = columnName[3]
    p_type = columnName[6] 
    print(f"{p_category}|{p_type}")


# In[9]:


lineRes = ['MFGR#11|PROMO BURNISHED COPPER', 'MFGR#11|LARGE BRUSHED BRASS'] #Sample for simplified code.


# In[10]:


#Reducer
#!/usr/bin/python
import sys

#Initiate iterated category placeholder and counter for each p_category.
currentCategory = None
counter = 0
print('p_category|COUNT(p_type)')

for line in sys.stdin:
    p_category, p_type = line.strip().split('|')
    if currentCategory is None: #Assign first p_category.
        currentCategory = p_category
    elif p_category != currentCategory: #Next cateogry, output current category and reset counter.
        print(f"{currentCategory}|{counter}")
        currentCategory = p_category
        counter = 0
    counter += 1
    
if currentCategory is not None:
    print(f"{currentCategory}|{counter}")


# #### Query 4

# SELECT lo_suppkey, lo_discount \
# FROM lineorder \
# WHERE lo_quantity < 12 \
# GROUP BY lo_suppkey , lo_discount \
# ORDER BY lo_discount

# In[11]:


#Sample for simplified code.
line_orderLines = ['1|1|7381|155190|828|19960102|5-LOW|0|10|2116823|17366547|4|2032150|74711|4|19960212|TRUCK|',                    '1|2|7381|67310|163|19960102|5-LOW|0|11|4598316|17366547|9|4184467|76638|6|19960228|MAIL|',                   '1|1|7381|155190|828|19960102|5-LOW|0|10|2116823|17366547|4|2032150|74711|4|19960212|VAN|']


# In[12]:


#Mapper - Extract column name using index and filtered by indicated column.
#!/usr/bin/python
import sys
for line in sys.stdin:
    columnName = line.strip().split('|', 17)
    lo_quantity = int(columnName[8])
    lo_discount = int(columnName[11])
    lo_suppkey = int(columnName[4])     
    if lo_quantity < 12:
        print(f"{lo_suppkey}|{lo_discount}")


# In[13]:


lineRes = ['828|4', '163|9', '200|1', '828|1', '828|4' ] #Sample for simplified code.


# In[14]:


#Reducer
#!/usr/bin/python
import sys

#Initiate dictionary with lo_suppkey as key. Tackle this statement: GROUP BY lo_suppkey , lo_discount.
suppkeyDict = {}
print('lo_suppkey|lo_discount')

for line in sys.stdin:
    lo_suppkey, lo_discount = line.strip().split('|')
    if lo_suppkey in suppkeyDict:
        if lo_discount not in suppkeyDict[lo_suppkey]:
            #Keep appending lo_discount value(s) associated to corresponding lo_suppkey key.
            suppkeyDict[lo_suppkey].append(lo_discount) 
    else:
        suppkeyDict[lo_suppkey] = [lo_discount]

lo_discountList = [] #List contains all unique lo_discount values of each lo_suppkey.
for lo_suppkey, lo_discounts in suppkeyDict.items():
    lo_discountList.extend(lo_discounts) 

#Sort all lo_discount values in ascending order.
lo_discountList = sorted(set(lo_discountList), key=int)

#Print sorted lo_discount and corresponding lo_suppkey.
for discount in lo_discountList:
    for lo_suppkey, lo_discounts in suppkeyDict.items():
        if discount in lo_discounts:
            print(f"{lo_suppkey}|{discount}")


# #### Query 5

# SELECT lo_discount, AVG(lo_extendedprice) \
# FROM lineorder \
# GROUP BY lo_discount

# In[15]:


#Mapper - Extract column name using index.
#!/usr/bin/python
import sys
for line in sys.stdin:
    columnName = line.strip().split('|', 17)
    lo_discount = int(columnName[11])
    lo_extendedprice = int(columnName[9])    
    print(f"{lo_discount}|{lo_extendedprice}")


# In[16]:


lineRes = ['9|4598316', '10|1330960', '9|2895564', '10|2282448', '7|4962016', '0|4469446', '6|5405805',            '10|4679647', '6|3989088', '1|261876', '4|3298652', '10|2873364', '3|3069090', '2|2367855', '7|5072392',            '8|7342650', '8|6199831', '7|1360860'] #Sample for simplified code.


# In[17]:


#Reducer
#!/usr/bin/python
import sys

#Dictionary with lo_discount as key and lo_extendedprice as values.
discountDict = {}
print('lo_discount|AVG(lo_extendedprice)')

for line in sys.stdin:
    lo_discount, lo_extendedprice = line.strip().split('|')
    if lo_discount in discountDict:
        discountDict[lo_discount].append(int(lo_extendedprice))
    else:
        discountDict[lo_discount] = [int(lo_extendedprice)]

#For each dictionary item, calculate the average.
for lo_discount, lo_extendedprices in discountDict.items():
    avg_lo_extendedprices = sum(lo_extendedprices)/len(lo_extendedprices) 
    print(f"{lo_discount}|{avg_lo_extendedprices}")


# #### Query 6

# SELECT lo_custkey, SUM(lo_extendedprice) AS revenue \
# FROM lineorder \
# WHERE lo_quantity < 12 \
# GROUP BY lo_custkey

# In[18]:


#Mapper - Extract column name using index and filtered by indicated column.
#!/usr/bin/python
import sys
for line in sys.stdin:
    columnName = line.strip().split('|', 17)
    lo_custkey = int(columnName[2])
    lo_extendedprice = int(columnName[9])   
    lo_quantity = int(columnName[8]) 
    if lo_quantity < 12:
        print(f"{lo_custkey}|{lo_extendedprice}")


# In[19]:


lineRes = ['7381|2116823', '7381|4598316', '7999|456799','7999|11111']


# In[20]:


#Reducer
#!/usr/bin/python
import sys

#Dictionary with lo_custkey as key and lo_extendedprice as values. 
custkeyDict = {}
print('lo_custkey|revenue')
for line in sys.stdin:
    lo_custkey, lo_extendedprice = line.strip().split('|')
    if lo_custkey in custkeyDict:
        custkeyDict[lo_custkey].append(int(lo_extendedprice))
    else:
        custkeyDict[lo_custkey] = [int(lo_extendedprice)]

#For each dictionary item, get values count.
for lo_custkey, lo_extendedprices in custkeyDict.items():
    sum_lo_extendedprices = sum(lo_extendedprices)
    print(f"{lo_custkey}|{sum_lo_extendedprices}")


# #### Query 7

# SELECT d_datekey FROM dwdate \
# WHERE d_datekey NOT IN( \
# SELECT lo_orderdate FROM lineorder)

# In[21]:


#Sample for simplified code.
lines = ['19920101|January 1, 1992|Thursday|January|1992|199201|Jan1992|5|1|1|1|1|Winter|0|1|1|1|',          '19920102|January 2, 1992|Friday|January|1992|199201|Jan1992|6|2|2|1|1|Winter|0|1|0|1|',          '19920103|January 3, 1992|Saturday|January|1992|199201|Jan1992|7|3|3|1|1|Winter|1|1|0|0|',          '19920104|January 4, 1992|Sunday|January|1992|199201|Jan1992|1|4|4|1|1|Winter|0|1|0|0|',          '19920105|January 5, 1992|Monday|January|1992|199201|Jan1992|2|5|5|1|1|Winter|0|1|0|1|',          '19920106|January 6, 1992|Tuesday|January|1992|199201|Jan1992|3|6|6|1|1|Winter|0|1|0|1|',          '19920103|January 2, 1992|Friday|January|1992|199201|Jan1992|6|2|2|1|1|Winter|0|1|0|1|',          '1|1|7381|155190|828|19960102|5-LOW|0|17|2116823|17366547|4|2032150|74711|2|19960212|TRUCK|',          '1|2|7381|67310|163|19960102|5-LOW|0|36|4598316|17366547|9|4184467|76638|6|19960228|MAIL|',          '1|3|7381|63700|71|19960102|5-LOW|0|8|1330960|17366547|10|1197864|99822|2|19960305|REG AIR|',          '1|4|7381|2132|943|19960102|5-LOW|0|28|2895564|17366547|9|2634963|62047|6|19960330|AIR|',          '1|5|7381|24027|1625|19960102|5-LOW|0|24|2282448|17366547|10|2054203|57061|4|19960314|FOB|',          '1|6|7381|15635|1368|19960102|5-LOW|0|32|4962016|17366547|7|4614674|93037|2|19960207|MAIL|']


# In[22]:


#Mapper - Extract column name using index.
#!/usr/bin/python
import sys

#Identify each table by using second to last character.
for line in sys.stdin:
    columnName = line.strip().split('|') #Since both tables have 17 columns.
    if columnName[-2] == '0' or columnName[-2] == '1': 
        d_datekey = columnName[0]
        print(f"dwdate|{d_datekey}")
    else:
        lo_orderdate = columnName[5]
        print(f"lineorder|{lo_orderdate}")


# In[23]:


#Sample for simplified code.
res = ['dwdate|10', 'dwdate|30', 'lineorder|10', 'lineorder|40']


# In[24]:


#Reducer
#!/usr/bin/python
import sys
print('d_datekey')

#Make sure it's unquie for comparison.
dwdateKey = set()
lineorderKey = set()

for line in sys.stdin:
    fileSource, value = line.strip().split('|')
    if fileSource == "dwdate":
        dwdateKey.add(value)
    elif fileSource == "lineorder":
        lineorderKey.add(value)

#Find key that are not in lineorder.
missingKey = dwdateKey - lineorderKey
for d_datekey in missingKey:
    print(d_datekey)


# #### Query 8

# Note: I tried to do join on the mapper side. My code was working on Jupyter Notebook but not in Hadoop Streaming. Also tweak mapper code here and there, still got the same result. So I did filter on mapper side, and join on reducer side and it worked.  

# SELECT lo_orderdate, AVG(lo_extendedprice) AS revenue \
# FROM lineorder, dwdate \
# WHERE lo_orderdate = d_datekey \
# AND d_year = 1998 \
# AND lo_discount BETWEEN 5 AND 7 \
# AND lo_quantity < 12 \
# GROUP BY lo_orderdate;

# In[25]:


#Sample for simplified code.
lines = ['19920101|January 1, 1992|Thursday|January|1992|199201|Jan1992|5|1|1|1|1|Winter|0|1|1|1|',          '19920102|January 2, 1992|Friday|January|1992|199201|Jan1992|6|2|2|1|1|Winter|0|1|0|1|',          '19920103|January 3, 1992|Saturday|January|1998|199201|Jan1992|7|3|3|1|1|Winter|1|1|0|0|',          '19920104|January 4, 1992|Sunday|January|1998|199201|Jan1992|1|4|4|1|1|Winter|0|1|0|0|',          '19920102|January 5, 1992|Monday|January|1998|199201|Jan1992|2|5|5|1|1|Winter|0|1|0|1|',          '19920106|January 6, 1992}Tuesday|January|1992|199201|Jan1992|3|6|6|1|1|Winter|0|1|0|1|',          '19920103|January 2, 1992|Friday|January|1992|199201|Jan1992|6|2|2|1|1|Winter|0|1|0|1|',          '1|1|7381|155190|828|19960102|5-LOW|0|17|2116823|17366547|4|2032150|74711|2|19960212|TRUCK|',          '1|2|7381|67310|163|19960102|5-LOW|0|36|4598316|17366547|9|4184467|76638|6|19960228|MAIL|',          '1|3|7381|63700|71|19920106|5-LOW|0|8|1330960|17366547|10|1197864|99822|2|19960305|REG AIR|',          '1|4|7381|2132|943|19960102|5-LOW|0|28|2895564|17366547|9|2634963|62047|6|19960330|AIR|',          '1|5|7381|24027|1625|19960102|5-LOW|0|24|2282448|17366547|10|2054203|57061|4|19960314|FOB|',          '1|6|7381|15635|1368|19920102|5-LOW|0|10|4962016|17366547|7|4614674|93037|2|19960207|MAIL|']


# In[26]:


#Mapper - Extract column name using index and filtered by indicated column.
#!/usr/bin/python
import sys
for line in sys.stdin:
    columnName = line.strip().split('|', 17)
    if columnName[-2] == '0' or columnName[-2] == '1':
        d_datekey = columnName[0]
        d_year = int(columnName[4])
        if d_year == 1998: 
            print(f"dwdate|{d_datekey}") 
    else:
        lo_orderdate = columnName[5]
        lo_extendedprice = columnName[9]
        lo_quantity = int(columnName[8])
        lo_discount = int(columnName[11])
        if lo_quantity < 12 and 5 <= int(lo_discount) <= 7:
            print(f"lineorder|{lo_orderdate}|{lo_extendedprice}")


# In[27]:


#Sample for simplified code.
res = ['dwdate|19920103', 'dwdate|19920104', 'dwdate|19920102', 'lineorder|19920102|20', 'lineorder|19920102|20', 'lineorder|19920104|10', 'lineorder|19920104|10']


# In[28]:


#Reducer
#!/usr/bin/python
import sys

#Initiate counters to calculate average revenue for each lo_orderdate. 
print('lo_orderdate|revenue')
revSum = 0
revCount = 0

#Dictionaries for each table. Tackle this statement: WHERE lo_orderdate = d_datekey.
#Note: Could you set data structure as well for dwdateDict. But in term of generalize use code, dictionary is better.
dwdateDict = {}
lineorderDict = {}

for line in sys.stdin:
    columnName = line.strip().split('|')
    fileSource = columnName[0]
    if fileSource == "dwdate":
        d_datekey = columnName[1]
        dwdateDict[d_datekey] = None #No values, just store d_datekey for comparison.
    elif fileSource == "lineorder":
        lo_orderdate = columnName[1]
        lo_extendedprice = int(columnName[2])
    
        if lo_orderdate in dwdateDict: #Equivalent to WHERE lo_orderdate = d_datekey.
            if lo_orderdate not in lineorderDict: #If new lo_orderdate.
                lineorderDict[lo_orderdate] = {'revSum': 0, 'revCount': 0}
            
            #Keep appending.
            lineorderDict[lo_orderdate]['revSum'] += lo_extendedprice
            lineorderDict[lo_orderdate]['revCount'] += 1

#For each item, average revenue output is already calculated here.
for lo_orderdate, revenue in lineorderDict.items():
    avgRev = revenue['revSum'] / revenue['revCount']
    print(f"{lo_orderdate}|{avgRev}")


# #### Schema
create table part (
  p_partkey     int,
  p_name        varchar(22),
  p_mfgr        varchar(6),
  p_category    varchar(7),
  p_brand1      varchar(9),
  p_color       varchar(11),
  p_type        varchar(25),
  p_size        int,
  p_container   varchar(10)    
);

create table supplier (
  s_suppkey     int,
  s_name        varchar(25),
  s_address     varchar(25),
  s_city        varchar(10),
  s_nation      varchar(15),
  s_region      varchar(12),
  s_phone       varchar(15)    
);

create table customer (
  c_custkey     int,
  c_name        varchar(25),
  c_address     varchar(25),
  c_city        varchar(10),
  c_nation      varchar(15),
  c_region      varchar(12),
  c_phone       varchar(15),
  c_mktsegment  varchar(10)    
);

create table dwdate (
  d_datekey            int,
  d_date               varchar(19),
  d_dayofweek          varchar(10),
  d_month              varchar(10),
  d_year               int,
  d_yearmonthnum       int,
  d_yearmonth          varchar(8),
  d_daynuminweek       int,
  d_daynuminmonth      int,
  d_daynuminyear       int,
  d_monthnuminyear     int,
  d_weeknuminyear      int,
  d_sellingseason      varchar(13),
  d_lastdayinweekfl    varchar(1),
  d_lastdayinmonthfl   varchar(1),
  d_holidayfl          varchar(1),
  d_weekdayfl          varchar(1)     
);

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
# In[ ]:





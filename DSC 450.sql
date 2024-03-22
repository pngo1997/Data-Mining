
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
  lo_commitdate        int,
  lo_shipmode          varchar(10), 
  lo_last             varchar(5)
);

drop table lineorder;
SELECT COUNT(*) FROM lineorder;
SELECT * from supplier;

SELECT s_suppkey, s_name, s_city, s_nation, s_phone
FROM supplier

SELECT lo_quantity, lo_linenumber
FROM lineorder
WHERE lo_discount < 7 AND lo_tax > 3


SELECT p_category, COUNT(p_type)
FROM part
GROUP BY p_category

SELECT lo_suppkey, lo_discount
FROM lineorder
WHERE lo_quantity < 12
GROUP BY lo_suppkey , lo_discount
ORDER BY lo_discount


SELECT lo_discount, AVG(lo_extendedprice)
FROM lineorder
GROUP BY lo_discount

SELECT lo_custkey, SUM(lo_extendedprice) AS revenue
FROM lineorder
WHERE lo_quantity < 12
GROUP BY lo_custkey

SELECT d_datekey FROM dwdate
WHERE d_datekey NOT IN(
SELECT lo_orderdate FROM lineorder)


SELECT lo_orderdate AS revenue
FROM lineorder, dwdate
WHERE lo_orderdate = d_datekey
AND d_year = 1998
AND lo_discount BETWEEN 5 AND 7
AND lo_quantity < 12
--GROUP BY lo_orderdate;


create table test
( 
id INT,
amount INT
);
INSERT INTO test VALUES(828,4);
INSERT INTO test VALUES(163,9);
INSERT INTO test VALUES(200,1);
INSERT INTO test VALUES(828,1);
INSERT INTO test VALUES(828,4);

SELECT id, amount
FROM test
GROUP BY id , amount
order by amount
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    # database="mysql",
    password="1234"
)

###############################################
#Q1

cur = conn.cursor()

cur.execute("""SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema = 'TEST'""")

tables = [table_name for (table_name,) in cur]

col_num = []

print(tables)

for t in tables:
    cur.execute(
        """select column_name from information_schema.columns where table_schema = 'TEST' and table_name = '%s'""" % t)
    b = cur.fetchall()
    col_num.append(len(b))

answer1 = sum(col_num) / len(col_num)

#print(col_num)
print('sum of column numbers is {0}'.format(sum(col_num)))
print('number of tables is {0}'.format(len(col_num)))

print('Answer1 is {:.2f}'.format(answer1))

###############################################################################
#Q3

answer3 = 0

for t in tables:
  cur.execute("""select count(1) from TEST.%s""" % t)
  row_num = cur.fetchone()[0]
  answer3 += row_num

print('Answer3 is {0}'.format(answer3))

################################################################################
#Q2

d = {}
result = {}

for t in tables:
    d[t] = col_num[tables.index(t)]

#print(d)

for t in tables:
    cur.execute("""select * from TEST.%s""" % t)
    records = cur.fetchall()
    for row in records:
        for i in range(d[t]):
            words = str(row[i]).split(" ")
            for a in words:
                if a in result:
                    result[a] += 1
                else:
                    result[a] = 1

df = pd.DataFrame.from_dict(result,orient='index',columns=['count'])
df=df.sort_values(by='count',ascending=False)
print(df)

#################################################################################
#TEST for Q2

# result = {}
#
# cur.execute("""select * from TEST.countries_aggregated""" )
# records = cur.fetchall()
# for row in records:
#     for i in range(5):
#         words = str(row[i]).split(" ")
#         for a in words:
#             if a in result:
#                 result[a] += 1
#             else:
#                 result[a] = 1
#
# df = pd.DataFrame.from_dict(result,orient='index',columns=['count'])
# df=df.sort_values(by='count',ascending=False)
# #print(df.head(1000))
# print(df)
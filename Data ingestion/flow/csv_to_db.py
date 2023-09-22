# FLOW FROM THE SKY - CSV TO DB (IN DEVELOPMENT...)
# CAM 93.102.140.115
# EMANUEL FERREIRA - OCT2022
# emanuel.ferreira@cm-maia.pt

# IMPORTS
# -------------------------------------------------------------------------------------------------------------
import pandas as pd
import sys
import config
import mysql.connector as mysql
from sqlite3 import Error
import datetime
# -------------------------------------------------------------------------------------------------------------

# DATAFRAME CREATIONS FROM .CSV FILES
df1 = pd.read_csv('C115_G1_Distribution_export_2022-10-25-14_16_04.csv', delimiter=';', names=['END_TIMESTAMP'])
#df1.iloc[:,1].apply(lambda x: (x - datetime.datetime(1970, 1, 1)).total_seconds())
print(df1)

#df1 = pd.DataFrame(df1) # Gate 1

#g2 = pd.read_csv(r'/home/eferreira/D4CMM/Yunex/Docs/C115_G2_Distribution_export_2022-10-25-14_16_42.csv', delimiter=';')
#df2 = pd.DataFrame(g2) # Gate 2

#g3 = pd.read_csv(r'/home/eferreira/D4CMM/Yunex/Docs/C115_G3_Distribution_export_2022-10-25-14_17_06.csv', delimiter=';')
#df3 = pd.DataFrame(g3) # Gate 3

#g4 = pd.read_csv(r'/home/eferreira/D4CMM/Yunex/Docs/C115_G4_Distribution_export_2022-10-25-14_17_27.csv', delimiter=';')
#df4 = pd.DataFrame(g4) # Gate 4

#print(df1)
#print(df2)
#print(df3)
#print(df4)

# CREDENTIALS FILE LOCATION
sys.path.insert(0, 'home/eferreira/D4CMM/Yunex/config.py')

    
# DATABASE CONNECTION TRY
try: 
    conn = mysql.connect(
    user = config.mdb_user,
    password = config.mdb_pwd,
    host = "localhost",
    #host = "195.23.9.32",
    port = 3306, 
    database = "BAZE",
    auth_plugin = 'mysql_native_password')
    #conn.is_connected():
    cursor = conn.cursor()

except Error as e:
      print("Error connecting to MariaDB platform: \n{e}")
      sys.exit(-1)

# INSERT DATAFRAME TO DATABASE    
for row in df1.itertuples():
  query = cursor.execute('''
                        INSERT INTO Flow_Distribution (START_TIMESTAMP, END_TIMESTAMP, BICYCLE, BUS, CAR, HEAVY, LIGHT, MOTORCYCLE, DATA_VALIDITY_STATUS)
                        VALUES (?,?,?,?,?,?,?,?,?)
                        ''',
                        row.START_TIMESTAMP,
                        row.END_TIMESTAMP,
                        row.BICYCLE,
                        row.BUS,
                        row.CAR,
                        row.HEAVY,
                        row.LIGHT,
                        row.MOTORCYCLE,
                        row.DATA_VALIDITY_STATUS,
                  )
conn.commit()

# print("SQL for Flow_Distribution: %d registo." % (cursor.rowcount))
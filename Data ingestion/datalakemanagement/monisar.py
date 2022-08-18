import os
import time
import sys
import datetime
import config
from pathlib import Path

ficheiro= "/home/ppimenta/sar_stat.txt"



leitura = False
leitura = True

if leitura:
	f = open(ficheiro,"r")
	lines = f.readlines()
else:
	lines = [
'07:30:01 PM     all      4.44      0.06      1.08      0.04      0.00     94.39\n'
	]

print ("linha:", lines)
#print ("data:%s" % lines[0][0:12])
#timst = datetime.datetime.strptime(lines[0][0:12], '%H:%M:%S %p')

puser = float (lines[0][22:30])
pnice = float (lines[0][32:40])
psystem = float (lines[0][42:50])
piowait = float (lines[0][52:60])
psteal = float (lines[0][62:70])
pidle = float (lines[0][72:80])

#print ("%s ->%5.2f" % (lines[0][22:30], puser))

#INSERT INTO `BAZE`.`datalakesize` (`datafile`, `discousado`) VALUES ('2022-06-13 17:30:00', '2434');

sqlcmd = "INSERT INTO `BAZE`.`datalakesize` (`puser`, `pnice`, `psystem`, `piowait`, `psteal`, `pidle`) VALUES\
 ("+"{}, {}, {}, {}, {}, {} ".format(puser, pnice, psystem, piowait, psteal, pidle)+");"
print (sqlcmd)


persiste=False
persiste=True

if persiste:
	import mysql.connector
	from mysql.connector import Error

	try:
		conn = mysql.connector.connect(
                user=config.MariaUser,
                password=config.MariaUpwd,
                host="localhost",
                port=3306,
                database="BAZE")

		cur = conn.cursor()
    
 
		sql=sqlcmd

		#print("sql:", sql)
		cur.execute(sql)
		conn.commit()

	except Error as e:
		print(f"Error connecting to MariaDB Platform: {e}")
		sys.exit(-3)
    
else:
	print ("----- Valores não persistidos (persiste=",persiste,").")
	sys.exit(-2)


print ("done.")
f.close()
sys.exit(-1)

import os
import time
import sys
import config
from pathlib import Path

#ficheiro="~ppimenta/baze/opendatasoft/datalakemanagement/"+"dlsize.txt"
#print ("Vou tentar abrir o ficheiro %s" % ficheiro)
#print ("no Path %s" % Path(ficheiro))
ficheiro= "/home/ppimenta/baze/opendatasoft/datalakemanagement/"+"dlsize.txt"



#(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(os.path.abspath(ficheiro))
(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(Path(ficheiro))

print("ctime: %s " % time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ctime)))
print("mtime: %s " % time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime+3600)))
print("atime: %s " % time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(atime)))

leitura = False
leitura = True

if leitura:
	f = open(ficheiro,"r")
	lines = f.readlines()
else:
	lines = ['16K\t/var/lib/mysql/aria_log.00000001\n', '4.0K\t/var/lib/mysql/aria_log_control\n', '320M\t/var/lib/mysql/BAZE\n', '4.0K\t/var/lib/mysql/databaseteste\n', '8.0K\t/var/lib/mysql/ib_buffer_pool\n', '76M\t/var/lib/mysql/ibdata1\n', '48M\t/var/lib/mysql/ib_logfile0\n', '48M\t/var/lib/mysql/ib_logfile1\n', '12M\t/var/lib/mysql/ibtmp1\n', '0\t/var/lib/mysql/multi-master.info\n', '1.3M\t/var/lib/mysql/mysql\n', '0\t/var/lib/mysql/mysql.sock\n', '4.0K\t/var/lib/mysql/mysql_upgrade_info\n', '4.0K\t/var/lib/mysql/performance_schema\n', '24K\t/var/lib/mysql/tc.log\n', '505M\ttotal\n']

#INSERT INTO `BAZE`.`datalakesize` (`datafile`, `discousado`) VALUES ('2022-06-13 17:30:00', '2434');

sqlcmd = "INSERT INTO `BAZE`.`datalakesize` (`datafile`, `discousado`) VALUES ('"+time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime+3600))+"', "+lines[-1].split("M")[0]+");"
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

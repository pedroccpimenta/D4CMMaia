# INE V.3
import requests
import json
import sys
import datetime
import mysql.connector
from mysql.connector import Error
import time

start_time = time.clock()

import configUBaMariaDB



print ("Ine on ", sys.platform)
if sys.platform=="win32":
  from sshtunnel import SSHTunnelForwarder


leitura=False
leitura=True

"""
simul=[{'IndicadorCod': '0008417', 'IndicadorDsg':\
 'Caixas multibanco em 31 de Dezembro (N.º) por Localização geográfica (NUTS - 2013);\
  Anual - SIBS, Estatísticas das instituições de crédito e sociedades financeiras',\
 'MetaInfUrl': 'https://www.ine.pt/bddXplorer/htdocs/minfo.jsp?var_cd=0008417&lingua=PT',\
 'DataExtracao': '2022-08-08T22:18:13.389+01:00', 'DataUltimoAtualizacao': '2022-06-23',\
 'UltimoPref': '2021', 'Dados': {'2015': [{'geocod': '11A1306', 'geodsg': 'Maia', 'valor': '151'}]}}]

simul=[{'IndicadorCod': '0008234', 'IndicadorDsg': 'Nados-vivos (N.º) por Local de residência da mãe \
(NUTS - 2013) e Sexo; Anual - INE, Nados-vivos',\
 'MetaInfUrl':\
 'https://www.ine.pt/bddXplorer/htdocs/minfo.jsp?var_cd=0008234&lingua=PT', 'DataExtracao':\
 '2022-08-09T00:15:15.421+01:00', 'DataUltimoAtualizacao': '2022-04-27',\
 'UltimoPref': '2021', 'Dados': {'2021': [{'geocod': '11A1306',\
 'geodsg': 'Maia', 'dim_3': '1', 'dim_3_t': 'H', 'valor': '508'},\
 {'geocod': '11A1306', 'geodsg': 'Maia',\
 'dim_3': 'T', 'dim_3_t': 'HM', 'valor': '974'},\
 {'geocod': '11A1306', 'geodsg': 'Maia', 'dim_3': '2',\
	 'dim_3_t': 'M', 'valor': '466'}]}}]

for t in simul[0]['Dados'].keys():
	print (t)

print (list(simul[0]['Dados'].keys())[0])
print (simul[0]['Dados'][list(simul[0]['Dados'].keys())[0]] )

print (simul[0]['Dados'][list(simul[0]['Dados'].keys())[0]][1]['valor'] )

for j in simul[0]['Dados'][list(simul[0]['Dados'].keys())[0]]:
	if j['dim_3_t']=="HM":
		print (" ----> The value:", j['valor'])

print ("Código: ",simul[0]['IndicadorCod'])
print ("Descri: ",simul[0]['IndicadorDsg'])
print ("DataUltimoAtualizacao: ",simul[0]['DataUltimoAtualizacao'])
print ("UltimoPref: ",simul[0]['UltimoPref'])
print ("MetaInfUrl: ",simul[0]['MetaInfUrl'])

#sys.exit(8)
"""

if leitura==True:

	try:
	    print('Connecting to the MariaDB Database...')

	    if sys.platform=="win32":
	      ssh_tunnel = SSHTunnelForwarder("195.23.9.30",
	          ssh_username="ppimenta",
	          ssh_private_key=r"C:\Users\Pedro\.ssh\id_rsa",
	          remote_bind_address=("localhost", 3306)
	      )
	      ssh_tunnel.start()
	      print(ssh_tunnel.local_bind_address)
	      porta =  ssh_tunnel.local_bind_port

	    else:
	      porta = 3306 

	    connection = mysql.connector.connect(
	        user=configUBaMariaDB.MariaUser,
	        password=configUBaMariaDB.MariaUpwd,
	        host="127.0.0.1",
	        port = porta,
	        database="BAZE"
	    )

	    cursor = connection.cursor(dictionary = True)
	    cursor = connection.cursor(buffered=True)

	    print ("... connection successful.", end="")
	except Error as e:
	    print('Connection Has Failed: ', e)
	    sys.exit(0)

	print ("Database ready...")

	with open("listadeindicadores.txt") as f: # open the file for reading
		for line in f: # iterate over each line
			cod = line.split()[0] # split it by whitespace
			print("»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»  Código: ",cod)
			if cod[0][0]=="#":
				print ("BREAK")
			
			else:	
				nmc = 0
				# Ano de inicio, ano de fim
				for ano in range(2011, 2023):
					print ("=================================================",ano , cod)
					url="https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&varcd="+cod+"&Dim1=S7A"+str(ano)+"&Dim2=11A1306&lang=PT"
					print ("CHAMADA:",url)
					s=requests.Session()
					b=s.get(url, allow_redirects=True)
					r=b.content
					
					r=s.get(url, allow_redirects=True).content
					

					try:				
					
						d=json.loads(r)

					
						sql = "SHOW COLUMNS FROM baze21RA LIKE 'C"+d[0]['IndicadorCod']+"';"
						print(sql, end ="")
						cursor.execute(sql)
						cursor.fetchall()
						connection.commit()
						print (" => ", cursor.rowcount, " regs", end="")
						if cursor.rowcount == 0:
							decimal = "0"
							if cod=="0009787":
								decimal="2"
							sql = "alter table baze21RA add column C"+d[0]['IndicadorCod']+" decimal (10, "+decimal+");";
							print (" - a Coluna não existe, adding column ->",sql)
							cursor.execute(sql)
							connection.commit()
						else:
							print ("- a Coluna existe.")

						ano = list(d[0]['Dados'].keys())[0]
						sql="select C"+d[0]['IndicadorCod']+" from baze21RA where ano="+ano +";" #+" and C"+d[0]['IndicadorCod']+" is not null;"
						print ("Existindo a coluna, procuramos (ano, C"+d[0]['IndicadorCod']+") ->",sql, end="")
						cursor.execute(sql)
						h=cursor.fetchall()
						connection.commit()
						print ("Cursor:rowcount(A): ", cursor.rowcount)	
						if cursor.rowcount == 0 :
							if d[0]['IndicadorCod']=="0008234":
								for j in d[0]['Dados'][list(simul[0]['Dados'].keys())[0]]:
									if j['dim_3_t']=="HM":
										#print (j['valor'])							
										sql ="insert into baze21RA (ano, C"+d[0]['IndicadorCod']+") values ("+ano+", "+\
								j['valor']  +");"

							else:
								sql ="insert into baze21RA (ano, C"+d[0]['IndicadorCod']+") values ("+ano+", "+\
								d[0]['Dados'][list(d[0]['Dados'].keys())[0]][0]['valor']  +");"
						else:
							print ("Existe o valor ",h[0][0],", opção update para ",d[0]['IndicadorCod'] ," ->")
					

							if 	d[0]['IndicadorCod'] in ("0008234", "0008349"):
								for j in d[0]['Dados'][list(d[0]['Dados'].keys())[0]]:
									print ("»»»»» j:", j)
									if j['dim_3_t'] in ("HM", "Total"):
										print (" + + + h[0][0]:", h[0][0]," =", j['valor'], type(h[0][0]), type(j['valor']))
										if h[0][0]==None or float(j['valor'])!=float(h[0][0]): 
											sql ="update baze21RA set C"+d[0]['IndicadorCod']+" = "+ j['valor'] +\
													" where ano="+ano+";"
										else:
											sql ="nothing"

							else:
								print (" + + + + + + h[0][0]:", h[0][0])
								if  h[0][0]==None or float(h[0][0])!=float(d[0]['Dados'][list(d[0]['Dados'].keys())[0]][0]['valor']):
									sql ="update baze21RA set C"+d[0]['IndicadorCod']+" = "+ d[0]['Dados'][list(d[0]['Dados'].keys())[0]][0]['valor'] +\
										" where ano="+ano+";"
								else:
									sql ="nothing"

						if sql=="nothing":
							print ("do nothing...")
						else:
							print ("INSERT / UPDATE ->",sql)
							cursor.execute (sql)
							connection.commit()
							nmc=nmc+1
						
		
					except:
						print ("no json data")
					
				#sys.exit(5) # Todos os Anos para uma variável
				print (" Para a variável ", cod, " foram efectuadas", nmc, "alterações =====================")
				agora = str(datetime.datetime.now())
				sql = "select * from fonte where nome='"+cod+"';"
				cursor.execute(sql)
				connection.commit()
				if cursor.rowcount==0:
					print("Ainda não existe entrada em 'fonte' para esta variável.")				
					sql = "insert into fonte (origem, nome, descri, DescriPlus, DataUltimaActual,"+\
					 "UltimoPref, MetaInfUrl, DataUltimaActuaLocal, DataUltimaVerifica,"+\
					 "editor, `status`) values ("+\
						"'INE', '"+cod+"', '"+d[0]['IndicadorDsg']+"', 'geocod:11A1306, geodsg: Maia', '"+d[0]['DataUltimoAtualizacao']+"', "\
						+d[0]['UltimoPref']+", '"+d[0]['MetaInfUrl']+"', '"+\
						agora+"', '"+agora+"', 'PCP (ppimenta@cm-maia.pt)', 'disponível'"+\
					")"
				

				else:
					print ("Já existe entrada em 'fonte' para esta variável, deverá ser actualizada.")
					if nmc==0:
						sql = "update fonte set DataUltimaVerifica='"+agora+"' where nome='"+cod+"';"
					else:
						sql = "update fonte set DataUltimaActuaLocal='"+agora+"',\
						 DataUltimaVerifica='"+agora+"' where nome='"+cod+"';" 

				print ("To go...:", sql)
				cursor.execute(sql)
				connection.commit()

		#sys.exit(3) # Todos os anos para todos os indicadores
	if connection:
		connection.close()

else:
	print("done")

print(time.clock() - start_time, "seconds")

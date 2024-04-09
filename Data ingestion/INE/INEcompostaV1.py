
"""
INE Composta
Exemplo de script em python para cálculo de séries compostas no data lake D4Maia
Pedro Pimenta, Abril 2024

"""
import datetime
agora = str(datetime.datetime.now())[0:19]
import time
import socket
hostname=socket.gethostname()

print ("Execução de ", __file__, " - ", agora, 'em ', hostname)

iniciop = time.process_time()
iniciot = time.time()

def perf(sql):
	global nmc
	print ("SQL:", sql)
	cursor.execute (sql)
	connection.commit()

import argparse

parser = argparse.ArgumentParser(description="Cálculo de séries compostas - V1, Abril de 2024.",
	epilog='Para mais informação, consulte https://bit.ly/PPL-INE')
parser.add_argument("-n",  type=str, help="nome (datalake D4Maia) da série a calcular")
#parser.add_argument("-m",  type=str, help="mail if new data is harvested (True) or no email(False)")
#parser.add_argument("-d",  type=str, help="option to add debug output (True) or ommit it (False)")
args = parser.parse_args()

nomeserie  = 'NObitos' if args.n  == None else args.n  # valor default 0008235


print ('Parâmetros:',nomeserie)


"""
Ligação à base de dados

"""

import mysql.connector
from mysql.connector import Error

"""
	Esta script está feita para poder correr sem alterações em máquinas de teste e no servidor de produção.
	Neste caso, a máquina win32 tem as credenciais de acesso guardadas no ficheiro configdbX230, e o servidor tem as credenciais de acesso guardadas em configdbbaze1
"""

if (hostname=="DESKTOP-O5TUSN4"):
	import configdbX230 as configdb
elif (hostname=="baze.cm-maia.pt"):
	import configdbbaze as configdb	
else:
	print ("host", hostname, " not recognized.")
	exit(8)

username=configdb.username
passwd=configdb.password

try:
    print('Connecting to the MariaDB Database..', end="")
    porto = 3306 

    connection = mysql.connector.connect(
        user=username,
        password=passwd,
        host="localhost",
        port = porto,
        database="BAZE"
    )

    cursor = connection.cursor(dictionary = True)
    cursor = connection.cursor(buffered=True)

    print (". successful. ")
except Error as e:
    print('. failed: ', e)
    exit(0)
finally:
	pass

#print ("Database ready.")
print ("Ligação à base de dados: %.1f sec, %.3f sec de processador." % (time.time()-iniciot, time.process_time()-iniciop))

#exit(1)
"""
Verificação da existência da série

Podemos usar na tabela fonte o mesmo´código utilizado pelo INE ou mapear esse código na tabela 'fonte'.
No exemplo seguinte, usamos a segunda alternativa.
"""

sql = "select * from fonte where nome='"+nomeserie+"'"
cursor.execute(sql)
lu=cursor.fetchall()
if lu==[]:
	print ("=> A série",nomeserie, "ainda não está definida em `fonte` - reporte a suporte.dados@cm-maia.pt.")
	exit(8)
else:
	assunto="Composição de "+nomeserie 
	tabela=lu[0][1]
	curadoremail=lu[0][13]
	FormaCalculo = "adição das séries NObitosF e NObitosM"

if (nomeserie=="NObitos"): 
	sql = "select ano, CNObitosM, CNObitosF, CNObitos from baze21RA order by ano;"
	print("sql:", sql)
	cursor.execute(sql)
	lu=cursor.fetchall()
	nn= cursor.rowcount
	#print(nn,lu, lu[0])	
	print("Leitura da base de dados em %.1f sec, %.3f sec de processador." % (time.time()-iniciot, time.process_time()-iniciop))

	repo="<table border=1 cellspacing=0 cellpadding=5><tr><td align=center>Ano<td align=center>NObitosM<td align=center>NObitosF<td align=center>NObitos (total)<td align=center>Status"
	actua = False
	for i in range(0,nn):
		print(lu[i])

		repo+="<tr><td align=right>"+str(lu[i][0])+"<td align=right>"+str(lu[i][1])+"<td align=right>"+str(lu[i][2])+"<td align=right>"+str(lu[i][3])
		if lu[i][1]!=None and lu[i][2]!=None:
			if lu[i][3]==None or lu[i][3]!=lu[i][1]+lu[i][2]:
				actua = True
				sql ="update baze21RA set CNObitos="+str(lu[i][1]+lu[i][2])+" where ano="+str(lu[i][0])
				print ("! -> ", sql)
				cursor.execute(sql)
			
				repo+=" / <b><font color=orange>"+str(lu[i][1]+lu[i][2])
				repo+="<td align=center><font color=orange><B>Calculado</b>"
			else:			
				repo+="<td align=center><font color=green><B>OK!</b>"
		elif (lu[i][1]==None and lu[i][2]!=None) or (lu[i][1]!=None and lu[i][2]==None):
			repo+="<td align=center><font color=orange><B>Dados em falta</b>"
		else:
			repo+="<td align=center>NA"
	connection.commit()
	repo+="</table>"
	repo+="NObitosF: <a href=https://baze.cm-maia.pt/BaZe/gstat.htm?e0=NObitosF>https://baze.cm-maia.pt/BaZe/gstat.htm?e0=NObitosF</a><br>"
	repo+="NObitosM: <a href=https://baze.cm-maia.pt/BaZe/gstat.htm?e0=NObitosM>https://baze.cm-maia.pt/BaZe/gstat.htm?e0=NObitosM</a><br>"
	repo+="NObitos: <a href=https://baze.cm-maia.pt/BaZe/gstat.htm?e0=NObitos>https://baze.cm-maia.pt/BaZe/gstat.htm?e0=NObitos</a>"

	sql  = "update fonte set DataUltimaVerifica='"+agora+"', FormaCalculo='"+FormaCalculo+"'"
	sql  += ", comm='Esta série é calculada automáticamente por "+__file__+"'"
	sql  += ", `licença`='Creative Commons CCZero', `licençaURL`='http://opendefinition.org/licenses/cc-zero/'"
	
	if actua: 	
		sql += ", DataUltimaActuaLocal='"+agora+"'"
	sql += ", fonte='INE', Descri='Nº de Óbitos', Descriplus='Série calculada como soma de NObitosF e NObitosM ("+__file__+").', status='dispo' where nome='"+nomeserie+"';"
	print("sql:", sql)
	cursor.execute(sql)
	connection.commit()

	print("Actualização da base de dados em %.1f sec, %.3f sec de processador." % (time.time()-iniciot, time.process_time()-iniciop))
	email=repo
else:
	print("Não está definido o cálculo da série composta ", nomeserie)
	exit(8)

# Envio de email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

import configGMail

try:
    message = MIMEMultipart("alternative")
    message["Subject"] = assunto
    
    message["From"]=configGMail.UserFrom

    toadd=[ "pedroccpimenta@gmail.com", curadoremail ]
    message["To"]=", ".join(toadd)

    message["Reply-To"]="ppimenta@ipmaia.pt"
    
	# Create the plain-text and HTML version of your message
    text = email+"\nEsta é uma mensagem automática."

    html = "<html><body style='font-family:montserrat'>"+email+ "<hr color=orange>Tempo de execução %.1f sec, %.2f sec de processador" % (time.time()-iniciot, time.process_time()-iniciop)
    html = html +"<br>Esta mensagem automática foi gerada por "+ __file__ +"</body></html>"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    #port=587 # TLS
    port=465 # SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    	server.login(configGMail.UserName, configGMail.UserPwd)
    	sender_email = configGMail.UserFrom
    	server.sendmail(sender_email,toadd, message.as_string())
except Error as e:
    print('A notificação não foi enviada:', e)
finally:
    pass


print("Conclusão em %.1f sec, %.3f sec de processador." % (time.time()-iniciot, time.process_time()-iniciop))

exit(0)

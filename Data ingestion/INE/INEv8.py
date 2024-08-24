
"""
INE V.8
Exemplo de script em python para operacionalizar a recolha de dados do endpoint disponibilizado pelo INE (Instituto Nacional de Estatística) e para armazenamento no data lake D4Maia.
Pedro Pimenta, Março 2024

O INE disponibiliza uma interface REST para acesso aos dados, disponível em https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api&INST=322751522&ine_smenu.boui=357197120&ine_smenu.selected=357197822&ine_smenu.boui=357197120&ine_smenu.selected=357197822. Os parâmetros necessários são:

- código do indicador
- código da dimensão temporal (ano?)
- código da dimensão geográfica (NUTS)
- Código opcional, em função da série (ver mais à frente)
- Língua (EN ou PT)
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

parser = argparse.ArgumentParser(description="Recolha de dados INE - V8, Março 2024.",
	epilog='Para mais informação, consulte https://bit.ly/PPL-INE')
parser.add_argument("-c",  type=str, help="código (000xxx) da série")
parser.add_argument("-d1", type=str, help="ano (Dim1 = S7A<ano>).")
parser.add_argument("-d2", type=str, help="Dim2 - código territorial (11A1306 - Maia)")
parser.add_argument("-d3", type=str, help="Dim3 - código opcional")
#parser.add_argument("-m",  type=str, help="mail if new data is harvested (True) or no email(False)")
#parser.add_argument("-d",  type=str, help="option to add debug output (True) or ommit it (False)")
args = parser.parse_args()

code  = '0008235' if args.c  == None else args.c  # valor default 0008235
ano   =      2015 if args.d1 == None else args.d1 # valor default 2015
Dim2  = '11A1306' if args.d2 == None else args.d2 # valor default '11A1306' (Concelho da Maia)
Dim3  =       'T' if args.d3 == None else args.d3 # valor default 'T' - total

Dim1 = "S7A"+ str(ano)

print ('Parâmetros:',code, ano, Dim1, Dim2, Dim3)

import requests
import json

"""
O URL seguinte foi construído a partir das variáveis ano, code e ugeo para antecipar a reutilização do resto da script em outras situações.
"""

# Com este URL, obtemos só o número de óbitos de H ou M, conforme especifiquemos Dim3=1 (H) ou Dim3=2 (M) 
url="https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&varcd="+code+"&Dim1="+Dim1+"&Dim2="+Dim2+"&Dim3="+Dim3+"&lang=PT"
print("url:", url)

s=requests.Session()

"""
A directiva allow_redirects=True foi utilizada porque o INE devolve a resposta (texto JSON) sob o protocolo ftp, de modo que especificamos a permissão de redireccionamento para acedermos à resposta nesta script.
"""

r=s.get(url, allow_redirects=True).content

print ("Recolha de dados: %.1f sec, %.3f sec de processador." % (time.time()-iniciot, time.process_time()-iniciop))

#print(r)
dd=json.loads(r)
#print (dd)


"""
Para uma leitura mais fácil, podemos imprimir o objecto 'dd' da forma seguinte:
"""

print(json.dumps(dd, indent=4))

if 'Verdadeiro' in dd[0]['Sucesso']:
	print ("Acesso ao endpoint INE com sucesso:",dd[0]['Sucesso']['Verdadeiro'][0]['Msg'])
elif 'Falso' in dd[0]['Sucesso']:
	print ("Erro no acesso ao endpoint INE:",dd[0]['Sucesso']['Falso'][0]['Msg'])
	exit(8)

"""
Inspeccionando a resposta, percebemos que o endpoint devolve o número de óbitos separado por sexo (H / M), bem como o número total.
Sendo o nosso propósito, em termos de estrutura de data lake, o de guardar as variáveis ao maior nível de desagregação possível, o que iremos fazer é utilizar esta resposta para verificar / actualizar as séries óbitos H e óbitos M que existem no data lake.

Os passos seguintes serão:

1.   Verificar se no data lake já existem os valores respeitantes aos parâmetros ano, code (série), ugeo (unidade geográfica), e, neste caso, séries primárias (H / M);
2.   Se já existem, verificar se os valores são iguais aos recebidos agora através do endpoint;
2.1. Se são iguais, não altera os valores;
2.2. Se são diferentes, altera os valores e prepara um email de notificação para o/a Curador dos dados;
3. Se não existem, adiciona os novos valores à base de dados e prepara um email de notificação para o/a Curador dos dados;
4. Em qualquer dos casos, actualiza os dados relativos à 'última tentativa de actualização da série';
5. Se algum email estiver preparado, envia esse email (para o Curador)

"""

"""
Verificação da existência dos valores no data lake

Ligação à base de dados

"""

#import sys
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
	print ("host", hostname, " não reconhecido.")
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
if (code=="0008235"): 
	if Dim3=="T":
		nomeserie="NObitos"
	elif Dim3=="1":
		nomeserie="NObitosM"
		descriplus="Número de óbitos de indivíduos do sexo masculino, como reportado pelo INE."
		comm = "Esta série é sincronizada a partir do INE, com número de óbitos desagregado por sexo."
	elif Dim3=="2":
		nomeserie="NObitosF"
		descriplus="Número de óbitos de indivíduos do sexo feminino, como reportado pelo INE."
		comm = "Esta série é sincronizada a partir do INE, com número de óbitos desagregado por sexo."
	else:
		print("Dim3 / serie não definida.")
		exit(1)
	tema="Demografia"

	"""
	D
	"""
	sql = "select * from fonte where nome='"+nomeserie+"'"
	cursor.execute(sql)
	lu=cursor.fetchall()
	if lu==[]:
		print ("=> A série",nomeserie, "ainda não está definida em `fonte` - reporte a suporte.dados@cm-maia.pt.")
		exit(8)
	else:
		#print (lu)
		#print (lu[0][0], lu[0][1], lu[0][2], lu[0][13], lu[0][34], lu[0][35], " - ok!", len(lu[0]))
		
		#baze1
		#tabela=lu[0][..]
		#curador=lu[0][..]
		#curadoremail=lu[0][..]

		# X230
		tabela=lu[0][1]
		curadoremail=lu[0][13]

		print(nomeserie, lu[0][0], "tabela:", tabela, ", email do Curador:", curadoremail)

	sql = "SHOW COLUMNS FROM `"+tabela+"` LIKE 'C"+nomeserie+"';"
	cursor.execute(sql)
	cursor.fetchall()
	#connection.commit()
	nn= cursor.rowcount
	if nn!=1:
		print ("=>", cursor.rowcount, "regs. A série 'C"+nomeserie+ "' ainda não está definida em '"+tabela+"' - reporte a suporte.dados@cm-maia.pt.")
		exit(8)
	else:
		print ("A série 'C"+nomeserie+ "' está definida em '"+tabela+"', o curador é "+ curadoremail+" - ok!")
		sql="select C"+nomeserie+" from `"+tabela+"` where ano="+str(ano) +";" 
		print("sql:", sql)
		cursor.execute(sql)
		kk=cursor.fetchall()
		nn= cursor.rowcount
		print ("==>", nn, kk, "(actual) vs", dd[0]['Dados'][str(ano)][0]['valor'] , " (recolhido no INE).")
		ultimopref = dd[0]['UltimoPref']
		assunto="\U0001F557 Pipeline INE "+ code +" Dim1: %s Dim2: %s Dim3: %s \u2192 %s" % ( Dim1, Dim2, Dim3, nomeserie )
		email = "pipeline INE "+ code +" Dim1: %s Dim2: %s Dim3: %s &rarr; %s<br>" % ( Dim1, Dim2, Dim3, nomeserie )

		if Dim3=="1":
			desc = "Nº Óbitos (M)"
		elif Dim3=="2":
			desc = "Nº Óbitos (F)"
		else:
			print("Dim3 não definido ou incoerente.")
			exit(0)

		if kk[0][0]==None:
			sql = "update `"+tabela+"` set C"+nomeserie+"="+dd[0]['Dados'][str(ano)][0]['valor'] + ' where ano='+str(ano);
			sqlf = "update fonte set descri='"+desc+"', DataUltimaVerifica='"+agora+"', DataUltimaActuaLocal='"+ agora+\
			"', UltimoPref='"+ultimopref+"', fonte='INE', `status`='dispo'\
			, DescriPlus='"+descriplus+"'\
			, FormaCalculo='Série primária', `licença`='Creative Commons CCZero'\
			, `licençaURL`='http://opendefinition.org/licenses/cc-zero/'\
			, `comm`='"+comm+"'\
			, tema='"+tema+"'  where nome='"+nomeserie+"';"
			email = email + "novo valor inserido na base de dados:" + " ano: "+ str(ano)+", valor:"+dd[0]['Dados'][str(ano)][0]['valor']
			print ("Novo valor inserido no data lake.")

		else:
			if int(kk[0][0])==int(dd[0]['Dados'][str(ano)][0]['valor']): # Válido para variáveis int
				sql=""
				sqlf = "update fonte set DataUltimaVerifica='"+agora+"' where nome='"+nomeserie+"';"
				email= email + "Dados coincidentes, não será efectuada nenhuma alteração."
				print ("Nada a fazer...")
			else:	
				sql = "update `"+tabela+"` set C"+nomeserie+"="+dd[0]['Dados'][str(ano)][0]['valor'] + ' where ano='+str(ano);
				sqlf = "update fonte set DataUltimaVerifica='"+agora+"', DataUltimaActuaLocal='"+ agora+"', UltimoPref='"+ultimopref+"' where nome='"+nomeserie+"';"
				email = email + "valor alterado:<bR>Ano:"+str(ano)+" valor anterior:"+str(kk[0][0])+", novo valor: "+str(dd[0]['Dados'][str(ano)][0]['valor'])
				assunto="[Alarme] " + assunto 
				print ("Valor actualizado / alterado!")				
		
		print ("sql:", sql)
		print ("sqlf:", sqlf)

		cursor.execute(sqlf)
		if sql!="":
			cursor.execute(sql)
		
		connection.commit()
		print ("Actualização da base de dados: %.1f sec, %.3f sec de processador." % (time.time()-iniciot, time.process_time()-iniciop))
		#exit(8)
		

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
		    print ("Notificação enviada.")
		except Error as e:
		    print('A notificação não foi enviada:', e)
		finally:
		    pass

else:
	print("Indicador sem processador / pipeline definido.")
	exit(1)

print("Conclusão em %.1f sec, %.3f sec de processador." % (time.time()-iniciot, time.process_time()-iniciop))

exit(9)

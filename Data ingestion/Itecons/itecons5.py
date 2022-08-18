import mysql.connector
from mysql.connector import Error
import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib, ssl

import sys
import requests

import configItecons
import configUBaMariaDB
import configGMail

def Decimal(s):
    return(float(s))


leitura=True
#leitura=False

if leitura==True:

    try:
        connection = mysql.connector.connect(host='62.28.1.84',
                                         port='1689',
										 charset='utf8',
                                         user=configItecons.User,
                                         password=configItecons.Upwd
                                         )
        """
        user='ForumMaiaRO',
        password='kae2yeeee-Me'
        """

        if connection.is_connected():
            cursor = connection.cursor(dictionary = True)
#        cursor.execute("SELECT  datahora, radiacao, pressao_atm, temperatura, velocidade_vento,  direcao_vento, precipitacao, humidade FROM ForumMaia.Registos WHERE datahora = (SELECT MAX(datahora) FROM ForumMaia.Registos)")
#""""
#        cursor.execute ("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='ForumMaia' AND `TABLE_NAME`='Registos'")
#        result=cursor.fetchall()
#        for x in result:
#            print (x)
#"""

            cursor.execute("SELECT * FROM ForumMaia.Registos WHERE datahora = (SELECT MAX(datahora) FROM ForumMaia.Registos)")
            result = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
else:
    print ("LEITURA OFF - SIMUL")
    result=[{'datahora': datetime.datetime(2021, 11, 24, 23, 32), 'radiacao': Decimal('0.00'), 'pressao_atm': Decimal('100.40'), 'pressao_vapor': Decimal('0.80'), 'temperatura': Decimal('8.80'), 'velocidade_vento': Decimal('1.70'), 'direcao_vento': Decimal('303.90'), 'gust_vento': Decimal('4.50'), 'trovoes': Decimal('0.00'), 'dist_trovoes': Decimal('0.00'), 'precipitacao': Decimal('0.00'), 'humidade': Decimal('70.00'), 'temperatura_SH': Decimal('8.10'), 'orientacaoX': Decimal('-0.40'), 'orientacaoY': Decimal('1.30'), 'TC1': Decimal('14.80'), 'TC2': Decimal('11.60'), 'TC3': Decimal('15.10'), 'TC4': Decimal('10.70'), 'TC5': Decimal('23.60'), 'TC6': Decimal('11.70'), 'TC7': Decimal('8.50'), 'TC8': Decimal('9.10'), 'TC9': Decimal('7.10'), 'TC10': Decimal('20.70'), 'TC11': Decimal('2.80'), 'TC12': Decimal('9.30'), 'TC13': Decimal('14.40'), 'TC14': Decimal('22.90'), 'TC15': Decimal('19.30'), 'TC16': Decimal('15.50'), 'TC17': Decimal('18.70'), 'TC18': Decimal('9.50'), 'TC19': Decimal('15.50'), 'TC20': Decimal('2.90'), 'TF1': Decimal('-3424.66'), 'TF2': Decimal('-1592.10'), 'TF3': Decimal('-8032.13'), 'SH1': Decimal('41.30'), 'SH2': Decimal('31.60')}]

for x in result:
    print(x)

print(30*"=")
print (result)
lvar=""
lves=""

for i in result[0].keys():
    print (i, end=", ")
print()
for i in result[0].values():
    print (i, end=", ")
print()

datamedida=str(result[0]['datahora'])

lvar=lvar +"fonte, regdata, data, local, radiacao, pressao, pressao_vapor, temp"
lvar=lvar + ",vento, ventodir, gust_vento, trovoes, dist_trovoes, precipitacao, humidade" 
lvar=lvar + ",orientacaoX, orientacaoY, SH1, SH2"
lves=lves+"'Itecons','"+str(datetime.datetime.now())+"','"+str(result[0]['datahora'])+"'"
lves=lves +",'Cobertura Verde'"
lves=lves+","+str(result[0]['radiacao'])+","+str(result[0]['pressao_atm'])
lves=lves+","+str(result[0]['pressao_vapor'])+","+str(result[0]['temperatura'])
lves=lves+","+str(result[0]['velocidade_vento'])+","+str(result[0]['direcao_vento'])
lves=lves+","+str(result[0]['gust_vento'])+","+str(result[0]['trovoes'])
lves=lves+","+str(result[0]['dist_trovoes'])+","+str(result[0]['precipitacao'])
lves=lves+","+str(result[0]['humidade'])
lves=lves+","+str(result[0]['orientacaoX'])+","+str(result[0]['orientacaoY'])
lves=lves+","+str(result[0]['SH1'])+","+str(result[0]['SH2'])


sql="insert into baze21r ("+lvar+") values("+lves+")"

print("sql:", sql)

persiste=False
persiste=True

if persiste:
    print("Para a Bdados:")
    #print("r:",r)
    import mysql.connector
    from mysql.connector import Error

    try:
        conn = mysql.connector.connect(
                user = configUBaMariaDB.MariaUser,
                password=configUBaMariaDB.MariaUpwd,
                host="localhost",
                #host="195.23.9.30",
                port=3306,
                database="BAZE")

        """
        user="ppimenta",
        password="pim53enta",
        """

    
    except Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(-1)
        
    # Get Cursor
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print(cur.rowcount)

else:
    print ("----- Valores não persistidos (persiste=",persiste,").")
    sys.exit(0)


enviaemail=True

if enviaemail==False:
    print("Sem email")
else:
    print("Com email")
    minSH1=47.3 # valor mínimo "normal"
    minSH2=42.3 # valor mínimo "normal"
    minSH2=43.3 # valor mínimo para testar o envio de email

    SH1=result[0]['SH1']
    SH2=result[0]['SH2']
    print ("SH1:%.2f e SH2:%2.f" % ( SH1, SH2))
    if (SH1<minSH1) or  (SH2<minSH2):

        message = MIMEMultipart("alternative")
        message["Subject"] = "Cobertura Verde necessita de rega"
        
        message["From"]=configGMail.UserFrom
        message["To"]="ppimenta@ucp.pt;pimenta@dsi.uminho.pt"
        message["ReplyTo"]="ppimenta@cm-maia.pt"
        """
        message["From"] = "pedroccpimenta@gmail.com"
        message["To"] = "ppimenta@cm-maia.pt"
        """
        # emanuel.ferreira@cm-maia.pt emanuel.ferreira91@gmail.com
        # bruno.figueiredo@cm-maia.pt brunomaf75@gmail.com
        
    # Create the plain-text and HTML version of your message
        text = """\
    Esta é uma mensagem automática e de teste.<br>
    (Emanuel, Bruno, vou enviar este email tb para os Vs. gmails como teste)
    <hr color=green>
    O sistema de monitorazação da humidade no solo da Cobertura Verde reporta, a esta data ("""+ datamedida +""")
        um valor de """+str(SH1)+"""% (minímo para alarme de """+str(minSH1)+"""%) para SH1 e de """+str(SH2)+\
         """% (mínimo para alarme de """+str(minSH2)+"""%).</p>
        <br>
        Para mais informações, consulte <a href='baze.cm-maia.pt/BaZe/cverde3.htm'>baze.cm-maia.pt/BaZe/cverde3.htm</a>.
      </body>
    </html>
    """    

        html = text

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        #port=587 # TLS
        port=465 # SSL

        #password="etnitjozlptdtged"
        # Create a secure SSL context
        context = ssl.create_default_context()

        #with smtplib.SMTP("smtp.gmail.com", port, context=context) as server:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            """
            server.login("pedroccpimenta@gmail.com", password)
            """
            server.login(configGMail.UserName, configGMail.UserPwd)

            sender_email = configGMail.UserFrom
            receiver_email = "ppimenta@cm-maia.pt;ppimenta@ipmaia.pt"

            qa=server.sendmail(sender_email, receiver_email, message.as_string())
            #qa=server.sendmail(message.as_string())

            print("qa:",qa)
        print ("Valores de SH1 ou SH2 baixos:\n", message)

    else:
        print ("Valores de SH1 e SH2 normais, alarme não enviado.")

print("done.")



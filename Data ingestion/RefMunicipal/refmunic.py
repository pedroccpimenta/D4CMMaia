# 
import sys
import json
import pprint
from sshtunnel import SSHTunnelForwarder
import mysql.connector
from mysql.connector import Error



#linha=open("ementa.txt", "r", encoding="utf-8").read().split("\n")
#linha=open("ementa12a16.txt", "r", encoding="utf-8").read().split("\n")
#linha=open("ementa18a23.txt", "r", encoding="utf-8").read().split("\n")
linha=open("ementa26a30desetembro.txt", "r", encoding="utf-8").read().split("\n")

print (linha)

print ("-")
semana=linha[0].split(" ")[1] +" "+ linha[len(linha)-1].split(" ")[0] +" "+ linha[0].split(" ")[0] +" "+\
linha[len(linha)-1].split(" ")[1] +" "+linha[len(linha)-1].split(" ")[2]
print (semana)

print (linha[1])

menuhtml="<p style=""font-family:montserrat""><table border=1 cellspacing=0 style=""font-family:montserrat""><tr><td colspan=6 align=center><b>Semana de "+semana
menuhtml=menuhtml+"<tr><td>Dia<td>Sopa<td>normal<td>dieta<td>opção<td>sobremesa"

morada="Rua Dr. Carlos Pires Felgueiras<br>4470-157 Maia Pt"
day=[]
for i in range(0, 5):
	menu={}
	print ("day:",linha[1+6*i], end=", ")
	print("sopa:",linha[31+4*i], end=", " )
	print("normal:",linha[32+4*i], end=", " )
	print("dieta:",linha[33+4*i], end=", " )
	print("opção:"," ", end=", " )
	print("sobremesa:",linha[34+4*i], end=", " )
	print()
  """
	menu["sopa"]=linha[31+4*i]
	menu["normal"]=linha[32+4*i]
	menu["dieta"]=linha[33+4*i]
	menu["opção"]=linha[34+4*i]
	menu["sobremesa"]=linha[35+4*i]
	day.append({"weekday":linha[1+6*i], "menu":menu})
"""
	menuhtml=menuhtml+"<tr><td>"+linha[1+6*i]
	menuhtml=menuhtml+"<td>"+linha[31+5*i]
	menuhtml=menuhtml+"<td>"+linha[32+5*i]
	menuhtml=menuhtml+"<td>"+linha[33+5*i]
	menuhtml=menuhtml+"<td>"+linha[34+5*i]
	menuhtml=menuhtml+"<td>"+linha[35+5*i]


week={"start":"2022-09-5", "end":"2022-09-5"}
coordinates={"Lat":41.23,"Lon":-8.6227, "alt":78}

name="Refeitório Municipal"
author={"name":"Albertina Ferreira", "email":"albertina.ferreira@smasmaia.pt", "telef":"<a href=tel:+351229430800>+351229430800</a>"}
img ={"url":"https://lh5.googleusercontent.com/p/AF1QipOTIJPwwlGvG81XUPYsnT1iQVeE0lLJfffBxyNV=w480-h257-p-k-no", "description":"Descrição"}
menuhtml=menuhtml+"</table>"
menuhtml=menuhtml+"<hr color=lime><p style=""font-family:montserrat"">Fonte: Albertina Ferreira<br>email: <a href=mailto:albertina.ferreira@smasmaia.pt?subject=""pedido de reserva"">albertina.ferreira@smasmaia.pt</a><br>telef: <a href=tel:+351229430800>+351229430800</a>"
menuhtml=menuhtml+"<br>vcard:<a href=""Albertina Ferreira (iOS).vcf"" title=""iOS vacard"">VCard</a> | <a href=""Albertina Ferreira (Google).csv"" title=""Google contact card"">Google</a> |<a href=""Albertina Ferreira (Outlook).csv"" title=""Outlook contact card"">Outlook</a> | "

menuhtml=menuhtml+"<br>"+morada
menuhtml=menuhtml+"<br>Maps: <a href=https://www.google.com/maps/@41.23,-8.6227,19z target=gm>Google</a>"
menuhtml=menuhtml+" | <a href=https://www.bing.com/maps?cp=41.23~-8.6227&lvl=19 target=bm>Bing</a>"
menuhtml=menuhtml+" | <a href=https://www.openstreetmap.org/#map=19/41.2300/-8.6227 target=osm>Open Street</a>"
menuhtml=menuhtml+" | <a href=https://maps.openrouteservice.org/#/place/@-8.6227,41.2300,19 target=orm>Open Route</a>"





menuhtml=menuhtml+"<center><img src="+img["url"]+" width=80% title="+img["description"]+">"


pprint.pprint (json.dumps(day,ensure_ascii=False))
print("------------------------------------------------")

print(json.dumps(day, ensure_ascii=False))
print("------------------------------------------------")

erm={
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
    	"name":name,  
        "weekmenu":day,
        "editor":author,
        "picture":img
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          -8.62277,
          41.23005
        ]
      }
    }
  ]
}


refeitorio={
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -8.622839972376823,
              41.23010991357515
            ],
            [
              -8.622833266854286,
              41.230073603869315
            ],
            [
              -8.622945249080658,
              41.230064022138016
            ],
            [
              -8.62293653190136,
              41.229940468108744
            ],
            [
              -8.622713908553122,
              41.22996114451357
            ],
            [
              -8.622709214687347,
              41.22992231321128
            ],
            [
              -8.622638806700706,
              41.22993088635793
            ],
            [
              -8.622660264372826,
              41.230064022138016
            ],
            [
              -8.622719272971153,
              41.230059987724424
            ],
            [
              -8.622723296284676,
              41.23011495658825
            ],
            [
              -8.622839972376823,
              41.23010991357515
            ]
          ]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "marker-color": "cyan",
        "marker-size": "large",
        "marker-symbol": "restaurant"

      },
      "geometry": {
        "type": "Point",
        "coordinates": [
         -8.62277,
          41.23005
         ]
      }
    }
  ]
}


refeitorio={"type":"FeatureCollection","features":[{"type":"Feature","properties":{
        "stroke": "blue",
        "stroke-width": 4,
        "stroke-opacity": 1,
        "fill": "aqua",
        "fill-opacity": 0.2,
        "popupContent":menuhtml,
},"geometry":{"type":"Polygon","coordinates":[[[-8.6228776,41.2301069],[-8.6228695,41.2300383],[-8.6229674,41.2300297],[-8.6229573,41.229947],[-8.6227528,41.2299632],[-8.6227461,41.2299218],[-8.6226764,41.2299279],[-8.6226979,41.230061],[-8.6227293,41.2300595],[-8.6227387,41.230119],[-8.6228776,41.2301069]]]}},

{"type":"Feature","properties":{
    "marker-color": "cyan",
    "marker-size": "large",
    "marker-symbol": "restaurant",
    "popupContent":menuhtml,
    "icon":"http://baze.cm-maia.pt/BaZe/pics/restaurant-icon-transparent-18.png",

    "style":{
    }
},"geometry":{"type":"Point","coordinates":[-8.62277,41.23005]}}]}

refeitorio['features'][0]["properties"]={"name":name,"week":week, "menu":day, "author":author}

k=json.dumps(refeitorio, ensure_ascii=False)
print(k)

import os

print(os.name)

persiste=False
persiste=True

if persiste:
  if os.name=="nt":
    try:
        print('Connecting to the MariaDB Database...')

        ssh_tunnel = SSHTunnelForwarder("195.23.9.30",
            ssh_username="ppimenta",
            ssh_private_key=r"C:\Users\Pedro\.ssh\id_rsa",
            remote_bind_address=("localhost", 3306)
        )

        ssh_tunnel.start()
        print(ssh_tunnel.local_bind_address) 
        porta = ssh_tunnel.local_bind_port
    except Error as e:
        print('Connection Has Failed: ', e)
        sys.exit(0)

  else:
    try:
        porta=3306
        connection = mysql.connector.connect(
		        user="ppimenta",
		        password="pim53enta",
		        host="127.0.0.1",
		        port = porta,
		        database="BAZE"
		    )

        cursor = connection.cursor(dictionary = True)
        cursor = connection.cursor(buffered=True)

        print ("... connection successful.")

        sql = "update GJSON set valor='"+k+ "' where nome='RefeitorioMunicipal';"
        print(sql)
        cursor.execute(sql)
        connection.commit()
        print (cursor.rowcount, " registos alterados.")
    except Error as e:
        print('Connection Has Failed: ', e)


sys.exit(0)

"""
import urllib.parse
safe_string = urllib.parse.quote_plus(k)
#print (safe_string)


http://geojson.io/#data=data:application/json,%7B%22type%22%3A%22LineString%22%2C%22coordinates%22%3A%5B%5B0%2C0%5D%2C%5B10%2C10%5D%5D%7D


http://geojson.io/#data=data:application/json,%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%22name%22%3A%22Refeit%C3%B3rioMunicipal%22%2C%22week%22%3A%7B%22start%22%3A%222022-09-5%22%2C%22end%22%3A%222022-09-5%22%7D%2C%22menu%22%3A%5B%7B%22weekday%22%3A%22Segunda-feira%22%2C%22menu%22%3A%7B%22sopa%22%3A%22Legumes%22%2C%22normal%22%3A%22Carne%C3%A0Jardineira%22%2C%22dieta%22%3A%22Peixeespadagrelhado%22%2C%22op%C3%A7%C3%A3o%22%3A%22%22%2C%22sobremesa%22%3A%22FrutaeouDoce%22%7D%7D%2C%7B%22weekday%22%3A%22Ter%C3%A7a-feira%22%2C%22menu%22%3A%7B%22sopa%22%3A%22Nabi%C3%A7as%22%2C%22normal%22%3A%22Raiafritacomarrozprimavera%22%2C%22dieta%22%3A%22Costeletasgrelhadas%22%2C%22op%C3%A7%C3%A3o%22%3A%22%22%2C%22sobremesa%22%3A%22FrutaeouDoce%22%7D%7D%2C%7B%22weekday%22%3A%22Quarta-feira%22%2C%22menu%22%3A%7B%22sopa%22%3A%22Espinafres%22%2C%22normal%22%3A%22Frango%C3%A0Passarinho%22%2C%22dieta%22%3A%22Alasdepescadacozidas%22%2C%22op%C3%A7%C3%A3o%22%3A%22%22%2C%22sobremesa%22%3A%22FrutaeouDoce%22%7D%7D%2C%7B%22weekday%22%3A%22Quinta-feira%22%2C%22menu%22%3A%7B%22sopa%22%3A%22Penca%22%2C%22normal%22%3A%22Filetesdepescadacomsaladarussa%22%2C%22dieta%22%3A%22Bifedefrangogrelhado%22%2C%22op%C3%A7%C3%A3o%22%3A%22%22%2C%22sobremesa%22%3A%22FrutaeouDoce%22%7D%7D%2C%7B%22weekday%22%3A%22Sexta-feira%22%2C%22menu%22%3A%7B%22sopa%22%3A%22Legumes%22%2C%22normal%22%3A%22Feijoada%C3%A0Lavrador%22%2C%22dieta%22%3A%22Robalogrelhado%22%2C%22op%C3%A7%C3%A3o%22%3A%22%22%2C%22sobremesa%22%3A%22FrutaeouDoce%22%7D%7D%5D%2C%22author%22%3A%7B%22name%22%3A%22AlbertinaFerreira%22%2C%22email%22%3A%22albertina.ferreira%40smasmaia.pt%22%2C%22telef%22%3A%22%3Cahref%3Dtel%3A%2B351229430800%3E%2B351229430800%3C%2Fa%3E%22%7D%7D%2C%22geometry%22%3A%7B%22type%22%3A%22Polygon%22%2C%22coordinates%22%3A%5B%5B%5B-8.6228776%2C41.2301069%5D%2C%5B-8.6228695%2C41.2300383%5D%2C%5B-8.6229674%2C41.2300297%5D%2C%5B-8.6229573%2C41.229947%5D%2C%5B-8.6227528%2C41.2299632%5D%2C%5B-8.6227461%2C41.2299218%5D%2C%5B-8.6226764%2C41.2299279%5D%2C%5B-8.6226979%2C41.230061%5D%2C%5B-8.6227293%2C41.2300595%5D%2C%5B-8.6227387%2C41.230119%5D%2C%5B-8.6228776%2C41.2301069%5D%5D%5D%7D%7D%2C%7B%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%22marker-color%22%3A%22cyan%22%2C%22marker-size%22%3A%22large%22%2C%22marker-symbol%22%3A%22restaurant%22%2C%22popupContent%22%3A%22%3Cpstyle%3Dfont-family%3Amontserrat%3E%3Ctableborder%3D1cellspacing%3D0style%3Dfont-family%3Amontserrat%3E%3Ctr%3E%3Ctdcolspan%3D6align%3Dcenter%3E%3Cb%3ESemanadede05-Seta09-Set2022%3Ctr%3E%3Ctd%3EDia%3Ctd%3ESopa%3Ctd%3Enormal%3Ctd%3Edieta%3Ctd%3Eop%C3%A7%C3%A3o%3Ctd%3Esobremesa%3Ctr%3E%3Ctd%3ESegunda-feira%3Ctd%3ELegumes%3Ctd%3ECarne%C3%A0Jardineira%3Ctd%3EPeixeespadagrelhado%3Ctd%3E%3Ctd%3EFrutaeouDoce%3Ctr%3E%3Ctd%3ETer%C3%A7a-feira%3Ctd%3ENabi%C3%A7as%3Ctd%3ERaiafritacomarrozprimavera%3Ctd%3ECosteletasgrelhadas%3Ctd%3E%3Ctd%3EFrutaeouDoce%3Ctr%3E%3Ctd%3EQuarta-feira%3Ctd%3EEspinafres%3Ctd%3EFrango%C3%A0Passarinho%3Ctd%3EAlasdepescadacozidas%3Ctd%3E%3Ctd%3EFrutaeouDoce%3Ctr%3E%3Ctd%3EQuinta-feira%3Ctd%3EPenca%3Ctd%3EFiletesdepescadacomsaladarussa%3Ctd%3EBifedefrangogrelhado%3Ctd%3E%3Ctd%3EFrutaeouDoce%3Ctr%3E%3Ctd%3ESexta-feira%3Ctd%3ELegumes%3Ctd%3EFeijoada%C3%A0Lavrador%3Ctd%3ERobalogrelhado%3Ctd%3E%3Ctd%3EFrutaeouDoce%3C%2Ftable%3E%3Chrcolor%3Dlime%3EFonte%3AAlbertinaFerreira%3Cbr%3Eemail%3A%3Cahref%3Dmailto%3Aalbertina.ferreira%40smasmaia.pt%3Fsubject%3D%27pedidodereserva%27%3Ealbertina.ferreira%40smasmaia.pt%3C%2Fa%3E%3Cbr%3Etelef%3A%3Cahref%3Dtel%3A%2B351229430800%3E%2B351229430800%3C%2Fa%3E%3Cbr%3ERuaDr.CarlosPiresFelgueiras%3Cbr%3E4470-157MaiaPt%3Cbr%3Evcard%3A%3Cahref%3DAlbertinaFerreira%28iOS%29.vcftitle%3DiOSvacard%3EVCard%3C%2Fa%3E%7C%3Cahref%3DAlbertinaFerreira%28Google%29.csvtitle%3DGooglecontactcard%3EGoogle%3C%2Fa%3E%7C%3Cahref%3DAlbertinaFerreira%28Outlook%29.csvtitle%3DOutlookcontactcard%3EOutlook%3C%2Fa%3E%7C%22%2C%22icon%22%3A%22http%3A%2F%2Fbaze.cm-maia.pt%2FBaZe%2Fpics%2Frestaurant-icon-transparent-18.png%22%2C%22style%22%3A%7B%7D%7D%2C%22geometry%22%3A%7B%22type%22%3A%22Point%22%2C%22coordinates%22%3A%5B-8.62277%2C41.23005%5D%7D%7D%5D%7D
"""
# Bird V.3
import requests
import json
import sys
import datetime

import tokenBird
import configUBaMariaDB

leitura=True
#leitura=False

if leitura==True:
	s = requests.Session()

	key=tokenBird.token # Esta chave está guardada no ficheiro tokenBird.py

	s.headers.update({'Authorization': 'Bearer '+key})

	#url = 'https://mds.bird.co/gbfs/v2/private/maia-portugal/gbfs.json'
	url = 'https://mds.bird.co/gbfs/v2/private/maia-portugal/free_bike_status.json'

	resposta=s.get(url)

	r=resposta.json()
else:
	r={"version":"2.2","data":{"bikes":[{"bike_id":"a3a47d4c-56ef-442a-9e08-3ab5883cdb43","lat":41.233128333333326,"lon":-8.63456,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272361,"current_range_meters":10179,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3Da3a47d4c-56ef-442a-9e08-3ab5883cdb43%26lat%3D41.23311999999999%26lon%3D-8.634538333333333%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=a3a47d4c-56ef-442a-9e08-3ab5883cdb43&lat=41.23311999999999&lng=-8.634538333333333"}},{"bike_id":"ef31ac5f-2c88-42fa-896b-21da661f01e0","lat":41.225604999999995,"lon":-8.615573333333334,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272430,"current_range_meters":13572,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3Def31ac5f-2c88-42fa-896b-21da661f01e0%26lat%3D41.225640000000006%26lon%3D-8.615535%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=ef31ac5f-2c88-42fa-896b-21da661f01e0&lat=41.225640000000006&lng=-8.615535"}},{"bike_id":"78206339-24ac-48a2-b58a-db22957aa3fb","lat":41.23764500000001,"lon":-8.624988333333333,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272310,"current_range_meters":21924,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3D78206339-24ac-48a2-b58a-db22957aa3fb%26lat%3D41.23763666666667%26lon%3D-8.624991666666666%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=78206339-24ac-48a2-b58a-db22957aa3fb&lat=41.23763666666667&lng=-8.624991666666666"}},{"bike_id":"ad3279f0-533a-4641-a77f-90aa99c1f6f4","lat":41.23763999999999,"lon":-8.624985,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272191,"current_range_meters":23229,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3Dad3279f0-533a-4641-a77f-90aa99c1f6f4%26lat%3D41.23773500000001%26lon%3D-8.625043333333334%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=ad3279f0-533a-4641-a77f-90aa99c1f6f4&lat=41.23773500000001&lng=-8.625043333333334"}},{"bike_id":"6143d0ad-b723-4793-8731-d80ff907f5a8","lat":41.190334316666664,"lon":-8.5947237,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272197,"current_range_meters":15300,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3D6143d0ad-b723-4793-8731-d80ff907f5a8%26lat%3D41.191806799999995%26lon%3D-8.594705583333333%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=6143d0ad-b723-4793-8731-d80ff907f5a8&lat=41.191806799999995&lng=-8.594705583333333"}},{"bike_id":"a9158745-29ff-4906-a4c3-ffc7824332fc","lat":41.23683166666667,"lon":-8.609726666666667,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272271,"current_range_meters":16443,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3Da9158745-29ff-4906-a4c3-ffc7824332fc%26lat%3D41.23653833333333%26lon%3D-8.614338333333334%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=a9158745-29ff-4906-a4c3-ffc7824332fc&lat=41.23653833333333&lng=-8.614338333333334"}},{"bike_id":"be5ad6b0-17a4-469f-806d-5d160c7dc186","lat":41.142417666666674,"lon":-8.647562166666667,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272379,"current_range_meters":32850,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3Dbe5ad6b0-17a4-469f-806d-5d160c7dc186%26lat%3D41.23686250000001%26lon%3D-8.617172166666668%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=be5ad6b0-17a4-469f-806d-5d160c7dc186&lat=41.23686250000001&lng=-8.617172166666668"}},{"bike_id":"1bf5f433-bc4b-481c-9919-43692ee73786","lat":41.23153333333333,"lon":-8.623741666666666,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272393,"current_range_meters":21663,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3D1bf5f433-bc4b-481c-9919-43692ee73786%26lat%3D41.23148%26lon%3D-8.623746666666667%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=1bf5f433-bc4b-481c-9919-43692ee73786&lat=41.23148&lng=-8.623746666666667"}},{"bike_id":"3b7db44f-dd7f-46a7-ae31-08e4c8ceaeb2","lat":41.23139166666667,"lon":-8.623738333333334,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272344,"current_range_meters":21924,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3D3b7db44f-dd7f-46a7-ae31-08e4c8ceaeb2%26lat%3D41.231498333333334%26lon%3D-8.623731666666666%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=3b7db44f-dd7f-46a7-ae31-08e4c8ceaeb2&lat=41.231498333333334&lng=-8.623731666666666"}},{"bike_id":"9f1dcd52-d070-46ab-bebc-7c52762cf679","lat":41.23120833333334,"lon":-8.624031666666667,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272343,"current_range_meters":21663,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3D9f1dcd52-d070-46ab-bebc-7c52762cf679%26lat%3D41.23146499999999%26lon%3D-8.623761666666667%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=9f1dcd52-d070-46ab-bebc-7c52762cf679&lat=41.23146499999999&lng=-8.623761666666667"}},{"bike_id":"55a9edc6-3c6d-4cb0-a8dc-254f39f53730","lat":41.244193333333335,"lon":-8.62867,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272373,"current_range_meters":21924,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3D55a9edc6-3c6d-4cb0-a8dc-254f39f53730%26lat%3D41.244216666666674%26lon%3D-8.628703333333334%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=55a9edc6-3c6d-4cb0-a8dc-254f39f53730&lat=41.244216666666674&lng=-8.628703333333334"}},{"bike_id":"562d2234-5f00-4346-9c2e-9f8dc5ea34f8","lat":41.23763666666667,"lon":-8.624948333333332,"is_disabled":"False","is_reserved":"False","vehicle_type_id":"bae2102b-56ba-42ba-9097-720e5990b4b2","last_reported":1654272419,"current_range_meters":19575,"pricing_plan_id":"5c469505-2249-4383-9f13-8e4fd1430b0d","rental_uris":{"android":"https://go.bird.co/navigate?link=https%3A%2F%2Fgo.bird.co%2Fmap%3FbirdId%3D562d2234-5f00-4346-9c2e-9f8dc5ea34f8%26lat%3D41.23763666666667%26lon%3D-8.624985%26apn%3Dco.bird.android%26isi%3D1260842311%26ibi%3Dco.bird.Ride%26efr%3D1","ios":"https://go.bird.co?birdId=562d2234-5f00-4346-9c2e-9f8dc5ea34f8&lat=41.23763666666667&lng=-8.624985"}}]},"last_updated":1654272535,"ttl":60}

print(r)
#print("")

sepa="+"+5*"-"+"+"+40*"-"+"+"+12*"-"+"+"+12*"-"+"+"+9*"-"+"+"+9*"-"+"+"+24*"-"+"+"+10*"-"+"+"
print (sepa)
k=1

nbikes=0
kmsdisp=0
bikesdisp=0
isdisab = 0
isreserv=0
print('|{0:^4} | {1:^38} |  {2:^9} |  {3:^9} | {4:^7} | {5:>7} | {6:>22} | {7:^8} |'.format("N", 
	"BikeId", "Lat", "Lng", "Disab.", "Resr.", "last_report", "Auton"))

print (sepa)
for i in r['data']['bikes']:
	#print()
	#print (i[i]['bike_id'])
	print('{0:>5} | {1:>38} |  {2:.6f} |  {3:.6f} | {4:>7} | {5:>7} | {6:>22} | {7:>8.0f} |'.format(k,i['bike_id'], i['lat'], i['lon'], \
	 str(i['is_disabled']), str(i['is_reserved']), 
	 str(datetime.datetime.fromtimestamp(i['last_reported'])), i['current_range_meters'] ))
	k=k+1
	nbikes=nbikes+1
	if i['is_disabled']:
		isdisab=isdisab+1
	else:
		if i['is_reserved']:
			isreserv = isreserv+1
		else:
			kmsdisp= kmsdisp+i['current_range_meters']/1000
			bikesdisp=bikesdisp+1
#	if (i['current_range_meters'])

print (sepa)

print (datetime.datetime.now())
print ("-- Indicadores")
print (" Nº de scooters:", nbikes)
print (" Bikes disp:", bikesdisp)
print (" Bikes disab:", isdisab)
print (" Bikes reserv:", isreserv)
print (" Kms disp:", kmsdisp)


print ("------------------")

persiste=False
persiste=True

if persiste:
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


		cur = conn.cursor()
    
    # Get Cursor
		kregs=0
		for i in r['data']['bikes']:
			lvar = ""
			lves = ""
			lvar = lvar + " regdata, last_reported, lat, lon, is_reserved, is_disabled, current_range_meters, bike_id"
			lves = lves + "'" + str(datetime.datetime.now()) +"', '"+str(datetime.datetime.fromtimestamp(i['last_reported']))+"'"
			lves = lves + ", " + str(round(i['lat'],6))+", "+str(round(i['lon'],6))
			lves = lves + ", " + str(i['is_reserved'])+", "+str(i['is_disabled'])
			lves = lves + ", " + str(round(i['current_range_meters'],0))
			lves = lves + ", '" + i['bike_id'] +"'"

			sql="insert into scooter ("+lvar+") values ("+lves+")"

			#print("sql:", sql)
			cur.execute(sql)
			conn.commit()
			kregs=kregs+cur.rowcount
			print("Registados ", cur.rowcount, " registos [STotal:",kregs,"].")

			sql="truncate table lastScooters;"
			#print("sql:", sql)
			cur.execute(sql)
			conn.commit()

		for i in r['data']['bikes']:
			lvar = ""
			lves = ""
			lvar = lvar + " regdata, last_reported, lat, lon, is_reserved, is_disabled, current_range_meters, bike_id"
			lves = lves + "'" + str(datetime.datetime.now()) +"', '"+str(datetime.datetime.fromtimestamp(i['last_reported']))+"'"
			lves = lves + ", " + str(round(i['lat'],6))+", "+str(round(i['lon'],6))
			lves = lves + ", " + str(i['is_reserved'])+", "+str(i['is_disabled'])
			lves = lves + ", " + str(round(i['current_range_meters'],0))
			lves = lves + ", '" + i['bike_id'] +"'"

			sql="insert into lastScooters ("+lvar+") values ("+lves+")"

			#print("sql:", sql)
			cur.execute(sql)
			conn.commit()


			lves = ""
			lves = lves + "'" + str(datetime.datetime.now()) +"'"
			lves = lves + ", " + str(nbikes)+", "+str(isreserv)
			lves = lves + ", " + str(kmsdisp)+", "+'{0:.2f}'.format(bikesdisp/nbikes)

		sql = "insert into scooterindi1 (regdata, nbikes, reserved, kmsdisp, dispercent) values ("+lves+")"
		print (sql)
		cur.execute(sql)
		conn.commit()

	except Error as e:
		print(f"Error connecting to MariaDB Platform: {e}")
		sys.exit(-1)
    

	#cur = conn.cursor()
	#cur.execute(sql)
	#conn.commit()
	#print("Registados ", cur.rowcount, " registos.")

else:
	print ("----- Valores não persistidos (persiste=",persiste,").")
	sys.exit(0)


	



sys.exit(-1)


print ("done.")

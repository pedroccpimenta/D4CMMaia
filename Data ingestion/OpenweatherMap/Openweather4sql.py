# Recolha de dados de https://openweathermap.org/current

import pprint
import requests
import json
import sys
import datetime
import time
import mysql.connector

# Caminho do ficheiro config.py -> onde está as acredenciais do mySQL e da KEY da API
sys.path.insert(0, 'D4CMMaia/Openweather/config.py')

import config


# Dicionario de coordenadas a importar os dados biometricos
pontos = []

pontos.append({'lat':41.2936, 'lon':-8.6196})  # Parque de Avioso - São Pedro
pontos.append({'lat':41.2712, 'lon':-8.6494})  # Monte do Viso
pontos.append({'lat':41.2712, 'lon':-8.6196})  # Anta
pontos.append({'lat':41.2712, 'lon':-8.5897})  # Santa Maria de Avioso
pontos.append({'lat':41.2712, 'lon':-8.5598})  # São Romão do Coronado
pontos.append({'lat':41.2712, 'lon':-8.5300})  # Folgosa
pontos.append({'lat':41.2487, 'lon':-8.6793})  # Aeroporto - Vila Nova da Telha
pontos.append({'lat':41.2487, 'lon':-8.6494})  # Moreira
pontos.append({'lat':41.2487, 'lon':-8.6196})  # Barca
pontos.append({'lat':41.2487, 'lon':-8.5897})  # Nogueira
pontos.append({'lat':41.2487, 'lon':-8.5598})  # São Pedro de Afins
pontos.append({'lat':41.2487, 'lon':-8.5300})  # Santa Cristina
pontos.append({'lat':41.2263, 'lon':-8.6793})  # Freixieiro
pontos.append({'lat':41.2263, 'lon':-8.6494})  # Lipor II
pontos.append({'lat':41.2263, 'lon':-8.6196})  # Escola EB1 - Maia
pontos.append({'lat':41.2263, 'lon':-8.5897})  # Condomínio Natura Park
pontos.append({'lat':41.2263, 'lon':-8.5598})  # Sampaio
pontos.append({'lat':41.2038, 'lon':-8.6196})  # Parque A. da Ribeira de Picoutos
pontos.append({'lat':41.2038, 'lon':-8.5897})  # Pav. Mun. de Águas Santas III
pontos.append({'lat':41.2038, 'lon':-8.5598})  # Horta Biológica da Palmilheira
pontos.append({'lat':41.1814, 'lon':-8.5897})  # Escola EB1/JI Pedrouços

pontos.append({'lat':41.2378, 'lon':-8.6183})  # Centro de Compostagem
pontos.append({'lat':41.2583, 'lon':-8.5570})  # Pto Qart em São Frutuoso
pontos.append({'lat':41.2601, 'lon':-8.6167})  # Pto Qart Trav. da Escola Prep.

# Tentativa de abertura do ficheiro contadorwb.txt -> este ficheiro vai ser o contador dos pontos
# Como estamos a pedir os dados 1 a 1 (a cada 30 mim pede um ponto diferente),
# temos que anotar no ficheiro qual foi o ultimo a ser pedido, para depois pedir o seguinte
try:
    if sys.argv[1]:
        FName = str(sys.argv[1])
except:
    dum = 0
    FName = "/home/bfigueiredo/D4CMMaia/Openweather/contadorwb.txt"

print("Argumento:", FName, end="")
fh = open(FName, "r")
dice = int(fh.read())

# Caso chegue ao final dos pontos, começa do inicio (zero - 0)
if dice >= len(pontos):
     dice = 0

print("dice:", dice, " de um total de", len(pontos), ".")
fh.close

# Importa a KEY (campo -> token) da API do ficheiro config.py
chave = config.token

fonte = "OpenWeatherMap" # nome da API
readapi = False
readapi = True

if readapi == True:

    # URL da API
    url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + str(pontos[dice]['lat']) + '&lon=' + str(
        pontos[dice]['lon']) + '&appid=' + chave


    print("url:", url)
    start_time = time.time()
    resposta = requests.get(url)
    r = resposta.json()
    print("***** From API")
else:
    print("----- Testing data (readapi=", readapi, ").")
    r = {"data": [{"rh": 93, "pod": "n", "lon": -8.62, "pres": 1014.2, "timezone": "Europe\/Lisbon",
                   "ob_time": "2021-12-29 23:00", "country_code": "PT", "clouds": 62, "ts": 1640818800,
                   "solar_rad": 0, "state_code": "17", "city_name": "Maia", "wind_spd": 3.6,
                   "wind_cdir_full": "east-southeast", "wind_cdir": "ESE", "slp": 1023,
                   "vis": 5, "h_angle": -90, "sunset": "17:15", "dni": 0,
                   "dewpt": 13.9, "snow": 0, "uv": 0, "precip": 0, "wind_dir": 110, "sunrise": "07:59",
                   "ghi": 0, "dhi": 0, "aqi": 23, "lat": 41.24,
                   "weather": {"icon": "c02n", "code": 802, "description": "Scattered clouds"},
                   "datetime": "2021-12-29:23", "temp": 15, "station": "LPPR", "elev_angle": -62.79, "app_temp": 15}],
         "count": 1}

    #   r=JSON.parse(r)

local = r['name']
print(local);

latitude = r['coord']['lat']
longitude = r['coord']['lon']

print(latitude, longitude)

# Inserção do nome correto do local da medição

if (latitude==round(41.2936, 4) and longitude==round(-8.6196, 4)): local="Parque de Avioso - São Pedro";
if (latitude==round(41.2712, 4) and longitude==round(-8.6494, 4)): local="Monte do Viso";
if (latitude==round(41.2712, 4) and longitude==round(-8.6196, 4)): local="Anta";
if (latitude==round(41.2712, 4) and longitude==round(-8.5897, 4)): local="Santa Maria de Avioso";
if (latitude==round(41.2712, 4) and longitude==round(-8.5598, 4)): local="São Romão do Coronado";
if (latitude==round(41.2712, 4) and longitude==round(-8.5300, 4)): local="Folgosa";
if (latitude==round(41.2487, 4) and longitude==round(-8.6793, 4)): local="Aeroporto - Vila Nova da Telha";
if (latitude==round(41.2487, 4) and longitude==round(-8.6494, 4)): local="Moreira";
if (latitude==round(41.2526, 4) and longitude==round(-8.6508, 4)): local="Moreira"; # API -> Pedido 41.2487 -8.6494 // Resposta -> 41.2526 -8.6508

if (latitude==round(41.2487, 4) and longitude==round(-8.6196, 4)): local="Barca";
if (latitude==round(41.2487, 4) and longitude==round(-8.5897, 4)): local="Nogueira";
if (latitude==round(41.2487, 4) and longitude==round(-8.5598, 4)): local="São Pedro de Afins";
if (latitude==round(41.2487, 4) and longitude==round(-8.5300, 4)): local="Santa Cristina";
if (latitude==round(41.2263, 4) and longitude==round(-8.6793, 4)): local="Freixieiro";
if (latitude==round(41.2263, 4) and longitude==round(-8.6494, 4)): local="Lipor II";
if (latitude==round(41.2263, 4) and longitude==round(-8.6196, 4)): local="Escola EB1 - Maia";
if (latitude==round(41.2279, 4) and longitude==round(-8.6206, 4)): local="Escola EB1 - Maia"; # API -> Pedido 41.2263 -8.6196 // Resposta -> 41.2279 -8.6206
if (latitude==round(41.2273, 4) and longitude==round(-8.6170, 4)): local="Escola EB1 - Maia"; # API -> Pedido 41.2263 -8.6196 // Resposta -> 41.2273 -8.6170
if (latitude==round(41.2274, 4) and longitude==round(-8.6170, 4)): local="Escola EB1 - Maia"; # API -> Pedido 41.2263 -8.6196 // Resposta -> 41.2274 -8.6170

if (latitude==round(41.2263, 4) and longitude==round(-8.5897, 4)): local="Condomínio Natura Park";
if (latitude==round(41.2263, 4) and longitude==round(-8.5598, 4)): local="Sampaio";
if (latitude==round(41.2038, 4) and longitude==round(-8.6196, 4)): local="Parque A. da Ribeira de Picoutos";
if (latitude==round(41.2038, 4) and longitude==round(-8.5897, 4)): local="Pav. Mun. de Águas Santas III";
if (latitude==round(41.2038, 4) and longitude==round(-8.5598, 4)): local="Horta Biológica da Palmilheira";
if (latitude==round(41.1814, 4) and longitude==round(-8.5897, 4)): local="Escola EB1/JI Pedrouços";
if (latitude==round(41.1809, 4) and longitude==round(-8.5909, 4)): local="Escola EB1/JI Pedrouços"; # API -> Pedido 41.1814 -8.5897 // Resposta -> 41.1809 -8.5909

if (latitude==round(41.2378, 4) and longitude==round(-8.6183, 4)): local="Centro de Compostagem";
if (latitude==round(41.2583, 4) and longitude==round(-8.5570, 4)): local="Pto Qart em São Frutuoso";
if (latitude==round(41.2601, 4) and longitude==round(-8.6167, 4)): local="Pto Qart Trav. da Escola Prep.";

enulo="null" # variavel NULL

# Matching dos campo da BD com os da API
temp = r['main']['temp']
max_temp = r['main']['temp_max']
min_temp = r['main']['temp_min']
pressao = r['main']['pressure']
humidade = r['main']['humidity']
data = r['dt']
nebulosidade = r['clouds']['all']
uv = enulo
ts = enulo
vento = r['wind']['speed']
ventodir = r['wind']['deg']
gust_vento = enulo
if 'gust' in r['wind'] : gust_vento = r['wind']['gust'] # Verificação se o campo existe. Se existir, atribui o seu valor
precipitacao = enulo
if 'rain' in r : precipitacao = r['rain']['1h'] # Verificação se o campo existe. Se existir, atribui o seu valor
snow = enulo
if 'snow' in r : snow = r['rain']['1h'] # Verificação se o campo existe. Se existir, atribui o seu valor
solar_rad = enulo
slp = enulo
vis = r['visibility']
h_angle = enulo
dni = enulo
wt_icon = r['weather'][0]['icon']
wt_desc = r['weather'][0]['description']
aqi = enulo
sunset = r['sys']['sunset']
sunrise = r['sys']['sunrise']
timezone = r['timezone']

# Conserção de GDH UNIX UTC -> GDH Y-m-d H:M:S PT
data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data))
sunset = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sunset))
sunrise = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sunrise))

pprint.pprint(r)

agora = str(datetime.datetime.now())
agora = agora[0:19:1]
print("{} / {} {} ({},{}) {}ºC {} dir {}º {}mbar {}% {}% {} {} {} {} {} {} {} {}".format(agora[0:19:1], \
                                                                                         data, local, latitude,
                                                                                         longitude, temp, vento,
                                                                                         ventodir, pressao,
                                                                                         nebulosidade, \
                                                                                         uv, timezone, solar_rad, slp,
                                                                                         vis, h_angle, dni, aqi,
                                                                                         sunrise))
# Abre escreve e fecha
# Abre o ficheiro contadorwb.txt, escreve o ultimo ponto a ser pedido e fecha o ficheiro
open(FName, "w").write(str(dice + 1))

# Inserção dos dados recebidos na BD
persiste = True
#persiste = False

# Construção da Query
sql = "insert into baze21r (fonte, regdata, data, local, lat, lon, temp, max_temp, min_temp, pressao, humidade"
sql = sql + ", nebulosidade, uv, ts, vento, ventodir, gust_vento, precipitacao, snow, solar_rad, slp, vis, h_angle"
sql = sql + ", dni, wt_icon, wt_desc"
sql = sql + ", sunrise, sunset"
sql = sql + ",  aqi, createdby) \n values ('" + fonte + "','" + agora + "', '" + data + "'"
sql = sql + ", '" + local + "', " + str(latitude) + ", " + str(longitude) + ", " + str(temp)
sql = sql + ", " + str(max_temp) + "," + str(min_temp) + "," + str(pressao) + "," + str(humidade)
sql = sql + ", " + str(nebulosidade) + "," + str(uv) + "," + str(ts) + "," + str(vento)
sql = sql + ", " + str(ventodir) + "," + str(gust_vento) + "," + str(precipitacao) + "," + str(snow)
sql = sql + ", " + str(solar_rad) + "," + str(slp) + "," + str(vis) + "," + str(h_angle)
sql = sql + ", " + str(dni) + ", '" + wt_icon + "', '" + wt_desc + "'"
sql = sql + ", '" + sunrise + "', '" + sunset + "'"
sql = sql + ", " + str(aqi) + ", '" + config.MariaUser + "'"
sql = sql + ");"

print()
print('sql:', sql)

if persiste:
    print("Para a Bdados:")
    import mysql.connector
    from mysql.connector import Error

    try:    # Tentativa de Conexão à BD
        conn = mysql.connector.connect(
            user=config.MariaUser,
            password=config.MariaUpwd,
            host="localhost",
            # host="195.23.9.32",
            port=3306,
            database="BAZE")

    except Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(-1)

    # Get Cursor
    # Inserção dos dados na BD
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("sql for baze21r: %d registo." % (cur.rowcount))

else:
    print("----- Valores não persistidos (persiste=", persiste, ").")
    sys.exit(0)

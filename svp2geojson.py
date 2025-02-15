import json
import geojson
from shapely.geometry import shape, Point, mapping
from shapely.ops import transform
import pyproj

# Função para criar um círculo
def create_circle(lat, lon, radius_meters):
    local_azimuthal_projection = pyproj.Proj(
        proj='aeqd',
        lat_0=lat,
        lon_0=lon
    )
    project = lambda x, y: pyproj.transform(pyproj.Proj(proj='latlong'), local_azimuthal_projection, x, y)
    inverse_project = lambda x, y: pyproj.transform(local_azimuthal_projection, pyproj.Proj(proj='latlong'), x, y)

    point = Point(lon, lat)
    point_transformed = transform(project, point)
    buffer = point_transformed.buffer(radius_meters)
    circle = transform(inverse_project, buffer)
    return circle

# Exemplo de coordenadas das lojas (latitude, longitude) e nomes
lojas = [
{"nome":"Loja 1","coordenadas": (38.7737250,-9.0981250)},
{"nome":"Loja 2","coordenadas": (38.7431080,-9.1333980),},
{"nome":"Loja 3","coordenadas": (38.7813059,-9.1260222),},
{"nome":"Loja 4","coordenadas": (38.7606230,-9.1673160),},
{"nome":"Loja 5","coordenadas": (38.7359125,-9.1477441),},
{"nome":"Loja 6","coordenadas": (38.7737250,-9.0981250),},
{"nome":"Loja 7","coordenadas": (38.7244080,-9.1459050),},
{"nome":"Loja 8","coordenadas": (38.7114109,-9.1593650),},
{"nome":"Loja 9","coordenadas": (38.7114343,-9.1288499),},
{"nome":"Loja 10","coordenadas": (38.7059020,-9.1867970),},
{"nome":"Loja 11","coordenadas": (38.7023270,-9.1808710),},
{"nome":"Loja 12","coordenadas": (38.7177750,-9.1349820),},
{"nome":"Loja 13","coordenadas": (38.7463390,-9.1468940),},
{"nome":"Loja 14","coordenadas": (38.7019750,-9.2021170),},
{"nome":"Loja 15","coordenadas": (38.7665880,-9.1549910),},
{"nome":"Loja 16","coordenadas": (38.7633240,-9.1205480),},
{"nome":"Loja 17","coordenadas": (38.7270360,-9.1567020),},
{"nome":"Loja 18","coordenadas": (38.7168170,-9.1284350),},
{"nome":"Loja 19","coordenadas": (38.7119300,-9.1377000),},
{"nome":"Loja 20","coordenadas": (38.7499020,-9.1943870),},
{"nome":"Loja 21","coordenadas": (38.7539810,-9.1670260),},
{"nome":"Loja 22","coordenadas": (38.7316640,-9.1497990),},
{"nome":"Loja 23","coordenadas": (38.7356300,-9.1333380),},
{"nome":"Loja 24","coordenadas": (38.7641300,-9.1571010),},
{"nome":"Loja 25","coordenadas": (38.7255120,-9.1340380),},
{"nome":"Loja 26","coordenadas": (38.7470660,-9.1886960),},
{"nome":"Loja 27","coordenadas": (38.7280170,-9.1427220),},
{"nome":"Loja 28","coordenadas": (38.7555690,-9.1176720),},
{"nome":"Loja 29","coordenadas": (38.7117793,-9.1575020),},
{"nome":"Loja 30","coordenadas": (38.7329300,-9.1429930),},
{"nome":"Loja 31","coordenadas": (38.7640488,-9.1818569),},
{"nome":"Loja 32","coordenadas": (38.7376956,-9.1441710),},
{"nome":"Loja 33","coordenadas": (38.7163589,-9.1374102),},
{"nome":"Loja 34","coordenadas": (38.7740275,-9.1531396),},
{"nome":"Loja 35","coordenadas": (38.7814755,-9.1484129),},
{"nome":"Loja 36","coordenadas": (38.7232138,-9.1303488),},
{"nome":"Loja 37","coordenadas": (38.7422297,-9.1480066),},
{"nome":"Loja 38","coordenadas": (38.7202701,-9.1375588),},
{"nome":"Loja 39","coordenadas": (38.7551641,-9.1421857),},
{"nome":"Loja 40","coordenadas": (38.7194252,-9.1642098),},
{"nome":"Loja 41","coordenadas": (38.7481854,-9.1416354),},
{"nome":"Loja 42","coordenadas": (38.7113840,-9.1427998),},
{"nome":"Loja 43","coordenadas": (38.7432101,-9.1420508),},
{"nome":"Loja 44","coordenadas": (38.7175399,9.1349877),},
{"nome":"Loja 45","coordenadas": (38.7180774,-9.1349279),},
{"nome":"Loja 46","coordenadas": (38.7144452,-9.1621291),},
{"nome":"Loja 47","coordenadas": (38.7159263,-9.1328267),}

]

# Raio do círculo em metros
raio = 400

# Lista para armazenar os círculos
features = []

for loja in lojas:
    nome = loja["nome"]
    lat, lon = loja["coordenadas"]
    circle = create_circle(lat, lon, raio)
    
    # Adicionar o círculo como uma Feature com o nome da loja
    feature = geojson.Feature(
        geometry=mapping(circle),
        properties={
            "name": nome,  # Nome da loja
            "description": f"Círculo de 200m ao redor da {nome}"  # Descrição opcional
        }
    )
    features.append(feature)

# Criar o ficheiro GeoJSON
feature_collection = geojson.FeatureCollection(features)

# Salvar o ficheiro GeoJSON
with open('lojas_circulos.geojson', 'w') as f:
    json.dump(feature_collection, f, indent=4)  # Usar indent=4 para melhor legibilidade

print("Ficheiro GeoJSON criado com sucesso!")
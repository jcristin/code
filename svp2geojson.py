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

# Exemplo de coordenadas das lojas (latitude, longitude)
lojas = [
(38.7737250,-9.0981250),
(38.7431080,-9.1333980),
(38.7813059,-9.1260222),
(38.7606230,-9.1673160),
(38.7359125,-9.1477441),
(38.7737250,-9.0981250),
(38.7244080,-9.1459050),
(38.7114109,-9.1593650),
(38.7114343,-9.1288499),
(38.7059020,-9.1867970),
(38.7023270,-9.1808710),
(38.7177750,-9.1349820),
(38.7463390,-9.1468940),
(38.7019750,-9.2021170),
(38.7665880,-9.1549910),
(38.7633240,-9.1205480),
(38.7270360,-9.1567020),
(38.7168170,-9.1284350),
(38.7119300,-9.1377000),
(38.7499020,-9.1943870),
(38.7539810,-9.1670260),
(38.7316640,-9.1497990),
(38.7356300,-9.1333380),
(38.7641300,-9.1571010),
(38.7255120,-9.1340380),
(38.7470660,-9.1886960),
(38.7280170,-9.1427220),
(38.7555690,-9.1176720),
(38.7117793,-9.1575020),
(38.7329300,-9.1429930),
(38.7640488,-9.1818569),
(38.7376956,-9.1441710),
(38.7163589,-9.1374102),
(38.7740275,-9.1531396),
(38.7814755,-9.1484129),
(38.7232138,-9.1303488),
(38.7422297,-9.1480066),
(38.7202701,-9.1375588),
(38.7551641,-9.1421857),
(38.7194252,-9.1642098),
(38.7481854,-9.1416354),
(38.7113840,-9.1427998),
(38.7432101,-9.1420508),
(38.7175399,9.1349877),
(38.7180774,-9.1349279),
(38.7144452,-9.1621291),
(38.7159263,-9.1328267)
]

# Raio do círculo em metros
raio = 200

# Lista para armazenar os círculos
features = []

for lat, lon in lojas:
    circle = create_circle(lat, lon, raio)
    feature = geojson.Feature(geometry=mapping(circle), properties={"name": f"Loja {lat},{lon}"})
    features.append(feature)

# Criar o ficheiro GeoJSON
feature_collection = geojson.FeatureCollection(features)

# Salvar o ficheiro GeoJSON
with open('lojas_circulos.geojson', 'w') as f:
    json.dump(feature_collection, f)

print("Ficheiro GeoJSON criado com sucesso!")
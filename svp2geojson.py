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
{"nome":"MAIS OPTICA VIANA DO CASTELO","coordenadas": (41.6934261,-8.8297534)},
{"nome":"MAIS OPTICA BARCELOS","coordenadas": (41.530299,-8.6208376)},
{"nome":"CLINIC STORM VALADARES","coordenadas": (41.088828,-8.6280841)},
{"nome":"MAIS OPTICA LIXA","coordenadas": (41.3246331,-8.1495042)},
{"nome":"EUROZONE TELEMOVEIS","coordenadas": (41.4072459,-8.5207196)},
{"nome":"PRINK SEIXAL","coordenadas": (38.6181531,-9.1055673)},
{"nome":"JOAQUIM FERNANDES & CRUZ LDA","coordenadas": (41.1514466,-8.6211642)},
{"nome":"DISTANCIA REVERSIVEL UNIP LDA","coordenadas": (41.1859271,-8.5849819)},
{"nome":"BAIWHO LISBOA","coordenadas": (38.7144452,-9.1621291)},
{"nome":"Cycling Spot","coordenadas": (38.7597634,-9.0952436)},
{"nome":"BNF LOJA SANTO TIRSO","coordenadas": (41.3377681,-8.4970742)},
{"nome":"MAIS OPTICA SAO JOAO DA MADEIRA","coordenadas": (40.8943476,-8.493875)},
{"nome":"GAIABIKE PORTO BESSA","coordenadas": (41.158474,-8.6447581)},
{"nome":"GAIABIKE ARRIFANA","coordenadas": (40.9160342,-8.4961252)},
{"nome":"GAIABIKE MAIA","coordenadas": (41.2456656,-8.6483147)},
{"nome":"GAIABIKE PACOS DE FERREIRA","coordenadas": (41.2746866,-8.3949676)},
{"nome":"OPTICALIA VIEIRA DO MINHO","coordenadas": (41.6366212,-8.1444313)},
{"nome":"OPTICALIA AMARES","coordenadas": (41.6278027,-8.3654199)},
{"nome":"OPTINOVA CRUZ","coordenadas": (41.4424878,-8.4957256)},
{"nome":"FRANCISCO ARANDA E VIEGAS LDA","coordenadas": (38.6493319,-9.0632713)},
{"nome":"PAPELARIA PEROLA","coordenadas": (40.494691,-7.592975)},
{"nome":"Tabacaria Danevi","coordenadas": (37.1018778,-8.2291597)},
{"nome":"USEMAIS TINTEIROS","coordenadas": (39.091303,-9.253638)},
{"nome":"USEMAIS TINTEIROS","coordenadas": (39.4707542,-8.5336846)},
{"nome":"INFORECO A-DOS-CUNHADOS","coordenadas": (39.1517035,-9.2986325)},
{"nome":"USEMAIS TINTEIROS","coordenadas": (40.1403392,-7.4985469)},
{"nome":"Pap. Livraria Arco Iris","coordenadas": (37.1924906,-7.420335)},
{"nome":"TEKPHONE REBORDOSA","coordenadas": (41.2248172,-8.4091271)},
{"nome":"VitalGeste","coordenadas": (40.194393,-8.417735)},
{"nome":"ITE Informática","coordenadas": (40.194393,-8.417735)},
{"nome":"CMC","coordenadas": (41.4445055,-8.3051016)},
{"nome":"ESPOALUGA UNIPESSOAL LDA","coordenadas": (41.5365059,-8.7544328)},
{"nome":"SKYZONE 2","coordenadas": (38.7180774,-9.1349279)},
{"nome":"SKYZONE","coordenadas": (38.7175399,9.1349877)},
{"nome":"SILVIA FERREIRA","coordenadas": (41.3794301,-8.5174262)},
{"nome":"HELPMOBILE","coordenadas": (41.1929564,-8.6346066)},
{"nome":"Rajas Mobile","coordenadas": (37.1402496,-8.5374594)},
{"nome":"USEMAIS TINTEIROS","coordenadas": (39.8192878,-7.496522)},
{"nome":"DHL PT","coordenadas": (40.2906394,-7.4816121)},
{"nome":"LIVRARIA JARDIM","coordenadas": (40.5356237,-7.2693257)},
{"nome":"IRIS ESTUDIO","coordenadas": (41.346934,-8.4808309)},
{"nome":"USEMAIS TINTEIROS","coordenadas": (39.8192878,-7.496522)},
{"nome":"USEMAIS TINTEIROS","coordenadas": (40.1403392,-7.4985469)},
{"nome":"TAB. CCE","coordenadas": (40.277865,-7.497648)},
{"nome":"PAPELARIA XAPATI","coordenadas": (39.8168033,-7.4851919)},
{"nome":"PAPELARIA A3","coordenadas": (40.5395151,-7.273346)},
{"nome":"RC DIGITEC","coordenadas": (40.5470964,-7.2525602)},
{"nome":"DUQUE PASTELARIA","coordenadas": (41.5604085,-8.413819)},
{"nome":"INES CUNHA & PEDRO TIAGO LDA","coordenadas": (41.5354652,-8.6174435)},
{"nome":"VITOR DANIEL OLIVEIRA SILVA","coordenadas": (41.5718884,-8.4526427)},
{"nome":"MISSION TO ESCAPE LISBOA","coordenadas": (38.7603438,-9.1392961)},
{"nome":"FAUSTO E DINIS COM E SERV LDA","coordenadas": (40.753595,-8.5682107)},
{"nome":"VER OU NAO VER LDA","coordenadas": (40.2109897,-8.4318585)},
{"nome":"BIOHOME GARDEN","coordenadas": (40.5622997,-8.7693742)},
{"nome":"VANDA MARIA ACURCIO","coordenadas": (40.1663407,-8.8438188)},
{"nome":"PAPELARIA DESTAKE","coordenadas": (41.2521767,-8.6511885)}
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
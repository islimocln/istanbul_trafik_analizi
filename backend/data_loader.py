import requests
import json
import pandas as pd
from sqlalchemy import create_engine

# OpenStreetMap (OSM) API URL'si
overpass_url = "http://overpass-api.de/api/interpreter"
query = """
[out:json];
area["name"="İstanbul"]->.searchArea;
(
  way(area.searchArea)["highway"~"motorway|primary|secondary|tertiary"];
  node(w)->.nodes;
);
out body;
"""

response = requests.get(overpass_url, params={"data": query})

# Yanıtı detaylı inceleyelim
print("="*50)
print("📌 HTTP Yanıt Kodu:", response.status_code)
print("📌 API Yanıtı İlk 500 Karakter:", response.text[:500])
print("="*50)

if response.status_code == 200:
    data = response.json()

    # JSON olarak kaydet
    with open("data/istanbul_yollar.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Veri başarıyla kaydedildi! ({len(data['elements'])} öğe)")

    # 📌 Eklenen verileri terminalde gösterelim
    for element in data["elements"][:10]:  # İlk 10 veriyi yazdıralım
        if element["type"] == "node":
            osm_id = element["id"]
            lat = element["lat"]
            lon = element["lon"]
            print(f"Eklenen Veri: OSM ID: {osm_id}, Lat: {lat}, Lon: {lon}")

else:
    print(f"⚠ Hata oluştu! HTTP Yanıt Kodu: {response.status_code}")
    print(f"Yanıt: {response.text}")

# -------------------------------  CSV'yi PostgreSQL Veritabanına Aktarma -----------------------------

# CSV dosyasını pandas ile oku
file_path = "data/fuel_station.csv"  # Veritabanına aktarılacak CSV dosyasının yolu
df = pd.read_csv(file_path)

# Veritabanı bağlantısı kurma (PostgreSQL)
db_engine = create_engine('postgresql://postgres:Software.23@localhost:5432/traffic_verisi')  # Veritabanı bağlantı dizesini buraya ekle

# Veritabanına veri ekleme (fuel_stations tablosuna)
df.to_sql('fuel_stations', db_engine, if_exists='replace', index=False)

print("✅ Benzin istasyonu verisi başarıyla veritabanına eklendi!")

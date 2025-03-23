import psycopg2
import json

# PostgreSQL Bağlantısı (Trafik Verisi Veritabanı)
conn = psycopg2.connect(
    dbname="trafik_verisi",  # Veritabanı adını kontrol et
    user="postgres",
    password="Software.23",  # PostgreSQL şifreni yaz
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# JSON Dosyasını Oku
with open("../data/istanbul_yollar.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Veriyi PostgreSQL'e Kaydet
eklenen_veri_sayisi = 0
for element in data["elements"]:
    if element["type"] == "node":  # Sadece yolların noktalarını kaydediyoruz
        osm_id = element["id"]
        lat = element["lat"]
        lon = element["lon"]

        try:
            # PostGIS için coğrafi nokta oluştur ve veriyi ekle
            cursor.execute(
                "INSERT INTO istanbul_yollar (osm_id, latitude, longitude, geom) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))",
                (osm_id, lat, lon, lon, lat)
            )
            print(f"Eklenen Veri: OSM ID: {osm_id}, Lat: {lat}, Lon: {lon}")

            eklenen_veri_sayisi += 1
            print(f"✅ Veri Eklendi: OSM ID: {osm_id}, Lat: {lat}, Lon: {lon}")
        except Exception as e:
            print(f"⚠ Hata! {e}")

# Değişiklikleri Kaydet
conn.commit()
cursor.close()
conn.close()           

print(f"🎯 Toplam {eklenen_veri_sayisi} veri PostgreSQL'e eklendi!")
print("Aktarım tamamlandı, toplam kayıt sayısı:", cursor.rowcount)


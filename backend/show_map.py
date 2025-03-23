import pandas as pd

# CSV dosyanın yolunu belirt
csv_dosyasi = "../data/fuel_station.csv"  # Eğer başka bir konumdaysa doğru yolu yaz

# CSV'yi oku
df = pd.read_csv(csv_dosyasi)

# İlk birkaç satırı göster
print(df.head())

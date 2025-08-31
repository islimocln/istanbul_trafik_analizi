# İstanbul Trafik Analizi

*Ağ Programlama* dersi kapsamında geliştirilen bu proje, İstanbul’daki **trafik ve şehir içi mekân verilerini** harita üzerinde görselleştirir. Amaç; kullanıcıların benzin istasyonları, AVM’ler, hastaneler, eczaneler, oteller ve restoranlar gibi noktaları hızlıca keşfetmesi, **yakınındaki yerleri** bulması ve **yoğunluk/rota** bilgileriyle karar vermesini kolaylaştırmaktır.

## 🎯 Neyi Vadediyor?
- **Anlaşılır görselleştirme:** İstanbul’daki önemli nokta türlerini (Eczane, Benzin, Otel, Restoran, Hastane, AVM) tek harita üzerinde, ikonlarıyla birlikte sunar.
- **Konum tabanlı keşif:** Kullanıcı konumuna göre **en yakın yerleri** ve **mesafe bilgisini** gösterir.
- **Filtreleme ve seçim:** Bir veya birden çok mekân türünü seçip belirli sayıda sonuç (5, 10 vb.) listeleyebilirsin.
- **Analiz görünümü:** Otel/restoran listeleri ve puanlarıyla **en iyi seçenekleri** öne çıkarır.
- **Genişletilebilir mimari:** Trafik yoğunluğu/alternatif rota ve makine öğrenimi tabanlı analizler eklenerek kapsam büyütülecektir.

> Harita altyapısı **Leaflet** ve **OpenStreetMap** katkıcılarını kullanır.

## ✨ Ana Özellikler
- 📍 Konum seçme ve koordinat görüntüleme  
- 🧮 “Mekân sayısı” ile sonuç sayısını belirleme  
- 🧭 Seçili mekânların haritada **mesafe** bilgisiyle gösterimi  
- 🧰 Çoklu filtre (eczane, benzin, otel, restoran, hastane, AVM)  
- ⭐ Otel/restoran için puan bazlı “en iyi” listeleri (analiz sayfası)  
- 🗺️ Kullanıcı dostu arayüz (Ana sayfa, Harita, Analiz, Hakkında)

## 🖼️ Ekran Görüntüleri

> Görselleri repoda `docs/screens/` klasörüne kaydet ve aşağıdaki isimlerle eşleştir.

| Ana Sayfa (Hero) | Kategori Filtreleri | Tip Seçim Modalı |
|---|---|---|
| ![](./docs/screens/home-hero.png) | ![](./docs/screens/map-filters.png) | ![](./docs/screens/type-select-modal.png) |

| Seçili Tipler & İkonlar | Yakın Mekânlar (Mesafe) | AVM Yoğunluk Katmanı |
|---|---|---|
| ![](./docs/screens/markers-mixed.png) | ![](./docs/screens/popup-distance.png) | ![](./docs/screens/avm-layer.png) |

| En İyi Oteller | En İyi Restoranlar | Konum Paneli |
|---|---|---|
| ![](./docs/screens/top-hotels.png) | ![](./docs/screens/top-restaurants.png) | ![](./docs/screens/location-panel.png) |

> İstersen dosya adlarını şu şekilde eşleyebilirsin:  
> `Ekran görüntüsü 2025-06-07 161530.png → location-panel.png`  
> `… 162013.png → map-filters.png`  
> `… 173749.png → top-hotels.png`  
> `… 173757.png → top-restaurants.png`  
> `… 002242.png → home-hero.png`  
> `… 002324.png → type-select-modal.png`  
> `… 002415.png → markers-mixed.png`  
> `… 002435.png → popup-distance.png`  
> `… 002533.png → markers-alt.png (opsiyonel)`  
> `… 002616.png → avm-layer.png`

## 🗺️ Veri ve Harita
- Harita: **Leaflet** + **OpenStreetMap** (© OSM contributors)  
- Nokta ikonları: tür bazlı özelleştirilmiş marker’lar  
- (Opsiyonel) Dış veri kaynakları ve lisans bilgileri bu bölümde listelenir.


---




import googlemaps
import json
import time
from datetime import datetime
import requests
import os
import logging

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fetch_reviews.log'),
        logging.StreamHandler()
    ]
)

# Google API anahtarınızı buraya ekleyin
API_KEY = 'AIzaSyDvtQ5w7m2FIKycb0QBeFGxQJXI9tBF6Ts'

# Mutlak yol tanımı (Windows veya Linux fark etmez)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PHOTO_DIR = os.path.join(DATA_DIR, 'photos')

# Klasörleri oluştur
try:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PHOTO_DIR, exist_ok=True)
    logging.info(f"Klasörler oluşturuldu: {DATA_DIR}, {PHOTO_DIR}")
except Exception as e:
    logging.error(f"Klasör oluşturma hatası: {e}")
    raise

def initialize_gmaps():
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        # API'yi test et
        test_result = gmaps.places('test', location=(41.0082, 28.9784), radius=1000)
        if 'results' in test_result:
            logging.info("Google Maps API başarıyla başlatıldı")
            return gmaps
        else:
            logging.error("Google Maps API testi başarısız")
            raise Exception("API testi başarısız")
    except Exception as e:
        logging.error(f"Google Maps API başlatma hatası: {e}")
        raise

def search_places_all(gmaps, query, location, radius=5000, max_results=50):
    results = []
    page_token = None
    try:
        while len(results) < max_results:
            if page_token:
                places_result = gmaps.places(
                    query=query,
                    location=location,
                    radius=radius,
                    page_token=page_token
                )
            else:
                places_result = gmaps.places(
                    query=query,
                    location=location,
                    radius=radius
                )
            
            if 'results' not in places_result:
                logging.error(f"API yanıtında 'results' bulunamadı: {places_result}")
                break
                
            logging.info(f"API'dan dönen sonuç sayısı: {len(places_result.get('results', []))}")
            results.extend(places_result.get('results', []))
            page_token = places_result.get('next_page_token')
            if not page_token:
                break
            time.sleep(2)
        
        logging.info(f"Toplam çekilen mekan: {len(results)}")
        return results[:max_results]
    except Exception as e:
        logging.error(f"Mekan arama hatası: {e}")
        return []

def get_place_details(gmaps, place_id):
    try:
        place_details = gmaps.place(
            place_id,
            fields=[
                'name', 'rating', 'reviews', 'formatted_address', 
                'price_level', 'photo', 'website', 'formatted_phone_number',
                'opening_hours', 'type', 'geometry', 'url', 'user_ratings_total',
                'editorial_summary', 'business_status'
            ]
        )
        if 'result' not in place_details:
            logging.error(f"Detay yanıtında 'result' bulunamadı: {place_details}")
            return {}
            
        logging.info(f"Detay çekilen mekan: {place_details.get('result', {}).get('name', 'BULUNAMADI')}")
        return place_details.get('result', {})
    except Exception as e:
        logging.error(f"Detay hatası: {e}")
        return {}

def download_photo(gmaps, photo_reference, max_width=1200):
    try:
        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={API_KEY}"
        response = requests.get(photo_url)
        if response.status_code == 200:
            safe_name = photo_reference[:100]  # Çok uzun dosya adlarını kısalt
            photo_path = os.path.join(PHOTO_DIR, f"{safe_name}.jpg")
            with open(photo_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Fotoğraf indirildi: {photo_path}")
            return photo_path
        logging.error(f"Fotoğraf indirme başarısız: {response.status_code}")
        return None
    except Exception as e:
        logging.error(f"Fotoğraf indirme hatası: {e}")
        return None

def process_places(places, gmaps):
    processed_places = []
    
    for place in places:
        try:
            place_id = place.get('place_id')
            if not place_id:
                logging.warning("Place ID bulunamadı")
                continue
                
            details = get_place_details(gmaps, place_id)
            if not details:
                logging.warning(f"Detaylar çekilemedi: {place.get('name', 'İsimsiz')}")
                continue
            
            # Daha fazla fotoğraf çek (10'a kadar)
            photos = []
            for photo in details.get('photos', [])[:10]:
                photo_path = download_photo(gmaps, photo.get('photo_reference'))
                if photo_path:
                    photos.append(photo_path)
            
            processed_place = {
                'name': details.get('name', ''),
                'location': details.get('formatted_address', ''),
                'rating': details.get('rating', 0),
                'user_ratings_total': details.get('user_ratings_total', 0),
                'price_level': details.get('price_level', 0),
                'website': details.get('website', ''),
                'phone': details.get('formatted_phone_number', ''),
                'opening_hours': details.get('opening_hours', {}).get('weekday_text', []),
                'types': details.get('type', []),
                'business_status': details.get('business_status', ''),
                'google_maps_url': details.get('url', ''),
                'coordinates': {
                    'lat': details.get('geometry', {}).get('location', {}).get('lat'),
                    'lng': details.get('geometry', {}).get('location', {}).get('lng')
                },
                'photos': photos,
                'reviews': [],
                'editorial_summary': details.get('editorial_summary', {}).get('overview', '')
            }
            
            # Tüm yorumları çek
            for review in details.get('reviews', []):
                processed_review = {
                    'user': review.get('author_name', ''),
                    'stars': review.get('rating', 0),
                    'comment': review.get('text', ''),
                    'time': review.get('time', 0),
                    'relative_time': review.get('relative_time_description', ''),
                    'profile_photo': review.get('profile_photo_url', ''),
                    'likes': review.get('likes', 0)
                }
                processed_place['reviews'].append(processed_review)
            
            processed_places.append(processed_place)
            logging.info(f"Mekan işlendi: {processed_place['name']}")
            time.sleep(2)  # API limitini aşmamak için bekle
            
        except Exception as e:
            logging.error(f"Mekan işleme hatası: {e}")
            continue
    
    return processed_places

def merge_with_existing(new_data, filename):
    """Mevcut dosyadaki verilerle birleştir, tekrar edenleri atla."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing = json.load(f)
            except Exception:
                existing = []
    else:
        existing = []
    
    existing_ids = {item.get('google_maps_url') or item.get('name') for item in existing}
    # google_maps_url yoksa name ile kontrol (eski veri uyumluluğu için)
    merged = existing[:]
    for item in new_data:
        key = item.get('google_maps_url') or item.get('name')
        if key not in existing_ids:
            merged.append(item)
            existing_ids.add(key)
    return merged

def main():
    try:
        ISTANBUL_CENTER = (41.0082, 28.9784)
        gmaps = initialize_gmaps()
        
        # Restoranları çek
        logging.info("Restoranlar aranıyor...")
        restaurants = search_places_all(gmaps, 'restaurant', ISTANBUL_CENTER, max_results=25)
        processed_restaurants = process_places(restaurants, gmaps)
        
        # Otelleri çek
        logging.info("Oteller aranıyor...")
        hotels = search_places_all(gmaps, 'hotel', ISTANBUL_CENTER, max_results=25)
        processed_hotels = process_places(hotels, gmaps)
        
        # Verileri birleştir ve kaydet
        logging.info("Veriler birleştiriliyor ve kaydediliyor...")
        
        # Restoranları birleştir
        merged_restaurants = merge_with_existing(processed_restaurants, 'restaurants_with_reviews.json')
        with open(os.path.join(DATA_DIR, 'restaurants_with_reviews.json'), 'w', encoding='utf-8') as f:
            json.dump(merged_restaurants, f, ensure_ascii=False, indent=2)
        
        # Otelleri birleştir
        merged_hotels = merge_with_existing(processed_hotels, 'hotels_with_reviews.json')
        with open(os.path.join(DATA_DIR, 'hotels_with_reviews.json'), 'w', encoding='utf-8') as f:
            json.dump(merged_hotels, f, ensure_ascii=False, indent=2)
        
        logging.info("İşlem tamamlandı!")
        
    except Exception as e:
        logging.error(f"Ana işlem hatası: {e}")
        raise

if __name__ == "__main__":
    main()

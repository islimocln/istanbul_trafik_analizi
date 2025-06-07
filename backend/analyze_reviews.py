import spacy
import json
from textblob import TextBlob
import pandas as pd

# spaCy modelini yükle
nlp = spacy.load('en_core_web_md')

# Analiz edilecek başlıklar ve ilgili anahtar kelimeler (İngilizce ve Türkçe)
ASPECTS = {
    'temizlik': [
        # İngilizce
        'clean', 'hygiene', 'dirty', 'filthy', 'tidy', 'neat',
        # Türkçe
        'temiz', 'hijyen', 'kirli', 'pis', 'düzenli', 'bakımlı'
    ],
    'fiyat': [
        # İngilizce
        'price', 'expensive', 'cheap', 'value', 'cost', 'affordable',
        # Türkçe
        'fiyat', 'pahalı', 'ucuz', 'değer', 'maliyet', 'uygun'
    ],
    'lezzet': [
        # İngilizce
        'taste', 'delicious', 'flavor', 'food', 'meal', 'cuisine',
        # Türkçe
        'lezzet', 'nefis', 'yemek', 'tat', 'güzel', 'harika'
    ],
    'servis': [
        # İngilizce
        'service', 'staff', 'waiter', 'waitress', 'attentive', 'friendly',
        # Türkçe
        'servis', 'personel', 'garson', 'ilgi', 'dostça', 'yardımcı'
    ],
    'konfor': [
        # İngilizce
        'comfort', 'comfortable', 'cozy', 'spacious', 'room', 'bed',
        # Türkçe
        'rahat', 'konfor', 'ferah', 'geniş', 'oda', 'yatak'
    ]
}

def sentiment_to_stars(sentiment):
    """Duygu analizi puanını (-1 ile 1) 0-5 yıldıza çevirir"""
    # -1 ile 1 arasındaki puanı 0-5 arasına dönüştür
    return (sentiment + 1) * 2.5

def analyze_sentiment(text):
    """Metnin duygu analizini yapar"""
    blob = TextBlob(text)
    return blob.sentiment.polarity  # -1 ile 1 arasında bir değer döner

def analyze_aspects(text):
    """Metni başlıklara göre analiz eder"""
    doc = nlp(text.lower())
    aspect_scores = {aspect: 0 for aspect in ASPECTS}
    aspect_counts = {aspect: 0 for aspect in ASPECTS}
    
    # Her başlık için puan hesapla
    for aspect, keywords in ASPECTS.items():
        for keyword in keywords:
            if keyword in text.lower():
                # Anahtar kelime bulunduğunda, o başlığın puanını güncelle
                sentiment = analyze_sentiment(text)
                aspect_scores[aspect] += sentiment
                aspect_counts[aspect] += 1
    
    # Ortalama puanları hesapla ve yıldıza çevir
    final_scores = {}
    for aspect in ASPECTS:
        if aspect_counts[aspect] > 0:
            avg_sentiment = aspect_scores[aspect] / aspect_counts[aspect]
            final_scores[aspect] = round(sentiment_to_stars(avg_sentiment), 1)
        else:
            final_scores[aspect] = 0.0
    
    return final_scores

def analyze_reviews(file_path):
    """JSON dosyasındaki yorumları analiz eder"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = []
    for item in data:
        name = item['name']
        total_scores = {aspect: 0 for aspect in ASPECTS}
        review_count = 0
        
        for review in item['reviews']:
            comment = review['comment']
            stars = review['stars']
            
            # Yorumu analiz et
            aspect_scores = analyze_aspects(comment)
            
            # Puanları topla
            for aspect in ASPECTS:
                total_scores[aspect] += aspect_scores[aspect]
            
            review_count += 1
        
        # Ortalama puanları hesapla
        if review_count > 0:
            avg_scores = {aspect: round(score/review_count, 1) for aspect, score in total_scores.items()}
            results.append({
                'name': name,
                'scores': avg_scores,
                'review_count': review_count
            })
    
    return results

def print_results(results, title):
    """Sonuçları güzel bir şekilde yazdırır"""
    print(f"\n{title}")
    print("=" * 50)
    
    for result in results[:5]:  # İlk 5 sonucu göster
        print(f"\n{result['name']}")
        print("-" * 30)
        for aspect, score in result['scores'].items():
            stars = "★" * int(score) + "☆" * (5 - int(score))
            print(f"{aspect:8}: {score:.1f} {stars}")
        print(f"Yorum Sayısı: {result['review_count']}")

def main():
    # Test için otel ve restoran yorumlarını analiz et
    hotel_results = analyze_reviews('data/hotels_with_reviews.json')
    restaurant_results = analyze_reviews('data/restaurants_with_reviews.json')
    
    # Sonuçları göster
    print_results(hotel_results, "🏨 Otel Analizleri")
    print_results(restaurant_results, "🍽️ Restoran Analizleri")

if __name__ == "__main__":
    main() 
import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
from textblob import TextBlob
import re

def setup_driver():
    """Selenium web driver'ı ayarlar"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def get_hotel_reviews(hotel_name, location):
    """Google'dan otel yorumlarını çeker"""
    driver = setup_driver()
    search_query = f"{hotel_name} {location} reviews"
    url = f"https://www.google.com/search?q={search_query}"
    
    try:
        driver.get(url)
        # Yorumların yüklenmesini bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "review-snippet"))
        )
        
        # Sayfadaki yorumları topla
        reviews = []
        review_elements = driver.find_elements(By.CLASS_NAME, "review-snippet")
        
        for element in review_elements[:10]:  # İlk 10 yorumu al
            review_text = element.text
            if review_text:
                reviews.append({
                    "text": review_text,
                    "sentiment": analyze_sentiment(review_text)
                })
        
        return reviews
    
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return []
    
    finally:
        driver.quit()

def analyze_sentiment(text):
    """Metin duygu analizi yapar"""
    analysis = TextBlob(text)
    # -1 ile 1 arasında bir değer döndürür (-1: negatif, 0: nötr, 1: pozitif)
    return analysis.sentiment.polarity

def process_hotels():
    """Tüm otellerin yorumlarını işler"""
    # hotels.json dosyasını oku
    with open('hotels.json', 'r', encoding='utf-8') as f:
        hotels = json.load(f)
    
    # Her otel için yorumları çek
    for hotel in hotels:
        print(f"İşleniyor: {hotel['name']}")
        reviews = get_hotel_reviews(hotel['name'], hotel['location'])
        hotel['google_reviews'] = reviews
        time.sleep(2)  # Google'ın rate limit'ini aşmamak için bekle
    
    # Sonuçları kaydet
    with open('hotels_with_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(hotels, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_hotels() 
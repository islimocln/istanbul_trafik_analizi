from flask import Flask, render_template, jsonify
from analyze_reviews import analyze_reviews
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/analysis')
def get_analysis():
    # Otel ve restoran analizlerini yap
    hotel_results = analyze_reviews('data/hotels_with_reviews_fixed.json')
    restaurant_results = analyze_reviews('data/restaurants_with_reviews_fixed.json')
    
    return jsonify({
        'hotels': hotel_results,
        'restaurants': restaurant_results
    })

@app.route('/api/eczaneler')
def get_pharmacies():
    try:
        df = pd.read_csv('data/istanbul_eczaneler.csv')
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/benzin-istasyonlari')
def get_gas_stations():
    try:
        df = pd.read_csv('data/fuel_station.csv')
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hastaneler')
def get_hospitals():
    try:
        df = pd.read_csv('data/hospitals_osm.csv')
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/avm')
def get_malls():
    try:
        df = pd.read_csv('data/istanbul_avmler.csv')
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Buraya kendi güncel API key'ini gir
client = openai.OpenAI(api_key="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")

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'Mesaj boş olamaz'}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen İstanbul Rehberi gibi davran."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({'answer': answer})
    
    except Exception as e:
        print("❌ Hata:", str(e))  # <-- HATA BURADA GÖRÜNECEK
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os  # ✅ ADDED THIS

app = Flask(__name__)
CORS(app)

# YOUR API KEY
genai.configure(api_key="AIzaSyAX008Hp4lj26WUB-FuxDfkwJ6XICJizpk")

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<body style="font-family:Arial;max-width:800px;margin:50px auto;padding:20px;">
<h1>🧠 Geopolitical AI Research</h1>
<input id="topic" placeholder="india pakistan" style="width:70%;padding:15px;font-size:16px;">
<button onclick="analyze()" style="padding:15px;font-size:16px;background:#4285f4;color:white;border:none;">🔍 RESEARCH</button>
<div id="result" style="background:#f5f5f5;padding:20px;margin-top:20px;border-radius:8px;min-height:100px;"></div>

<script>
async function analyze() {
    const topic = document.getElementById('topic').value || 'world news';
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '🔍 AI Researching (10-20s)...';
    
    try {
        const res = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({topic: topic})
        });
        const data = await res.json();
        
        resultDiv.innerHTML = `
            <h3>📊 Analysis: ${data.topic}</h3>
            <div style="white-space:pre-wrap;line-height:1.6;">${data.analysis}</div>
            <p><small>Tokens: ${data.tokens || 0}</small></p>
        `;
    } catch(e) {
        resultDiv.innerHTML = '❌ Error: ' + e.message;
    }
}
</script>
</body>
</html>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        topic = data.get('topic', 'news')
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Deep geopolitical analysis of: {topic}
        
        Include: history, current status, key players, future scenarios.
        500-700 words, professional tone.
        """
        
        response = model.generate_content(prompt)
        
        return jsonify({
            'topic': topic,
            'analysis': response.text,
            'tokens': len(response.text.split())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # ✅ Uses os
    app.run(host='0.0.0.0', port=port)
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
<body style="font-family:Arial;max-width:800px;margin:50px auto;">
<h1>🧠 AI Research Bot</h1>
<input id="input" placeholder="US-China trade war 2025" style="width:70%;padding:15px;">
<button onclick="go()" style="padding:15px;background:#4285f4;color:white;border:none;">🔍 ANALYZE</button>
<pre id="output" style="background:#f0f0f0;padding:20px;margin-top:20px;border-radius:8px;"></pre>

<script>
async function go() {
    const topic = document.getElementById('input').value;
    const out = document.getElementById('output');
    out.textContent = 'Researching...';
    
    const res = await fetch('/analyze', {
        method: 'POST',
        body: JSON.stringify({topic}),
        headers: {'Content-Type': 'application/json'}
    });
    const data = await res.json();
    
    out.textContent = `Topic: ${topic}

${data.analysis || data.result || 'No response'}`;
}
</script>
</body>
</html>
    '''
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
from flask import Flask, request, jsonify
from flask_cors import CORS
from intelligence_engine import run_perfected_analysis
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:900px;margin:50px auto;background:#f8f9fa;padding:30px;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.1);">
<h1 style="color:#2c3e50;text-align:center;">🤖 Intelligence Engine</h1>
<p style="text-align:center;color:#7f8c8d;margin-bottom:30px;">CrewAI + Gemini | Historian → Critic → Architect</p>

<div style="display:flex;gap:15px;margin-bottom:30px;flex-wrap:wrap;">
<input id="topic" placeholder="india vs pakistan" style="flex:1;min-width:300px;padding:18px;font-size:16px;border:2px solid #ddd;border-radius:10px;">
<button onclick="research()" style="padding:18px 35px;background:#3498db;color:white;border:none;border-radius:10px;font-size:16px;cursor:pointer;font-weight:bold;">🔍 RUN ANALYSIS</button>
</div>

<div id="status" style="text-align:center;padding:15px;margin-bottom:20px;border-radius:8px;font-weight:bold;"></div>
<pre id="output" style="background:#2c3e50;color:#ecf0f1;padding:25px;border-radius:12px;font-size:15px;line-height:1.6;min-height:300px;max-height:600px;overflow:auto;border-left:5px solid #3498db;"></pre>

<script>
async function research() {
    const topic = document.getElementById('topic').value.trim();
    if(!topic) {
        alert('Enter topic!');
        return;
    }
    
    const status = document.getElementById('status');
    const output = document.getElementById('output');
    
    status.style.background = '#fff3cd';
    status.style.color = '#856404';
    status.textContent = `🔍 Analyzing "${topic}"... (60-180s)`;
    output.textContent = 'Initializing Intelligence Engine...\nHistorian researching...\n';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({topic: topic})
        });
        
        const data = await response.json();
        
        status.style.background = '#d4edda';
        status.style.color = '#155724';
        status.textContent = '✅ Analysis Complete';
        
        // ✅ FIXED - Direct topic + result
        output.textContent = `Topic: ${topic}\n\n${data.result || data.analysis || 'No output'}\n\n---\nIntelligence Engine Complete`;
        
    } catch(error) {
        status.style.background = '#f8d7da';
        status.style.color = '#721c24';
        status.textContent = '❌ Error';
        output.textContent = `Error: ${error.message}`;
    }
}

// Enter key
document.getElementById('topic').addEventListener('keypress', function(e) {
    if(e.key === 'Enter') research();
});
</script>
</body>
</html>'''

@app.route('/analyze', methods=['POST'])
def analyze():
    topic = request.json.get('topic', 'news')
    
    # Run CrewAI (can take 2+ mins)
    result = run_perfected_analysis(topic)
    
    return jsonify({
        'topic': topic,
        'result': str(result),
        'status': 'complete'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
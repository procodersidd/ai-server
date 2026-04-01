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
<body style="font-family:Arial;max-width:1000px;margin:50px auto;background:#f8f9fa;padding:30px;">
<h1 style="color:#1e3a8a;">🤖 Intelligence Platform</h1>
<input id="topic" placeholder="india vs pakistan" style="width:70%;padding:20px;font-size:18px;border:2px solid #e5e7eb;border-radius:12px;">
<button onclick="analyze()" style="padding:20px 40px;background:#3b82f6;color:white;border:none;border-radius:12px;font-size:18px;cursor:pointer;">🔍 RUN ANALYSIS</button>
<div id="status" style="margin:20px 0;padding:15px;border-radius:8px;font-weight:bold;"></div>
<div id="result" style="background:#1f2937;color:#f9fafb;padding:25px;border-radius:12px;font-size:15px;line-height:1.6;min-height:400px;border-left:5px solid #3b82f6;white-space:pre-wrap;"></div>

<script>
async function analyze() {
    const topic = document.getElementById('topic').value.trim();
    if(!topic) return alert('Enter topic!');
    
    const status = document.getElementById('status');
    const result = document.getElementById('result');
    
    status.innerHTML = `<div style="background:#fef3c7;color:#92400e;padding:10px;border-radius:6px;">🔍 "${topic}" - CrewAI activated (2-3 mins)</div>`;
    result.textContent = 'Historian researching web data...\n';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({topic: topic})
        });
        
        const data = await response.json();
        
        // ✅ DIRECT DISPLAY - NO data.topic nonsense
        status.innerHTML = `<div style="background:#d1fae5;color:#065f46;padding:10px;border-radius:6px;">✅ Complete: ${topic}</div>`;
        result.textContent = data.result || 'Analysis ready';
        
    } catch(e) {
        status.innerHTML = `<div style="background:#fee2e2;color:#991b1b;padding:10px;border-radius:6px;">❌ Error</div>`;
        result.textContent = 'Error: ' + e.message;
    }
}
</script>
</body>
</html>'''

@app.route('/analyze', methods=['POST'])
def analyze():
    topic = request.json.get('topic', 'news')
    
    # 🔥 SYNCHRONOUS - Waits for CrewAI (no threading mess)
    status_msg = f'Analyzing "{topic}"...\n'
    try:
        result = run_perfected_analysis(topic)
        return jsonify({
            'topic': topic,
            'result': str(result)  # ✅ Direct string - no parsing issues
        })
    except Exception as e:
        return jsonify({
            'topic': topic,
            'result': f'ERROR: {str(e)}',
            'error': True
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
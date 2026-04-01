from flask import Flask, request, jsonify
from flask_cors import CORS
from intelligence_engine import run_perfected_analysis
import os
import threading
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto;max-width:1000px;margin:50px auto;padding:20px;background:#f8fafc;">
<h1 style="color:#1e293b;">🤖 Gemini CrewAI Intelligence Platform</h1>
<p style="color:#64748b;">3 AI agents research any topic → Historian → Critic → Final Report</p>

<input id="topic" placeholder="india pakistan war 2025" style="width:70%;padding:20px;font-size:18px;border:2px solid #e2e8f0;border-radius:12px;">
<button onclick="analyze()" style="padding:20px 40px;font-size:18px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:12px;cursor:pointer;margin-left:10px;">🚀 RUN CREW ANALYSIS</button>

<div id="status" style="color:#64748b;font-size:14px;margin:20px 0;"></div>
<pre id="result" style="background:#1e293b;color:#e2e8f0;padding:30px;border-radius:12px;font-size:15px;line-height:1.7;min-height:400px;border-left:6px solid #667eea;overflow:auto;max-height:600px;"></pre>

<script>
let isRunning = false;
async function analyze() {
    if(isRunning) return;
    
    const topic = document.getElementById('topic').value.trim();
    if(!topic) return;
    
    isRunning = true;
    const status = document.getElementById('status');
    const result = document.getElementById('result');
    
    status.textContent = `🔍 CrewAI activated: "${topic}"`;
    result.textContent = 'Historian researching...\nCritic analyzing...\nWriter compiling...\n(60-180s)';
    
    try {
        const res = await fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({topic})
        });
        const data = await res.json();
        
        status.textContent = '✅ CrewAI complete';
        result.textContent = data.result || data.analysis || data.error || 'No output';
    } catch(e) {
        status.textContent = '❌ Error';
        result.textContent = e.message;
    }
    
    isRunning = false;
}
</script>
</body>
</html>'''

@app.route('/analyze', methods=['POST'])
def analyze():
    topic = request.json.get('topic', 'global news')
    
    def run_crew():
        result = run_perfected_analysis(topic)
        return {'topic': topic, 'result': str(result)}
    
    # Run async (CrewAI can take 2-3 mins)
    thread = threading.Thread(target=lambda: setattr(app, 'crew_result', run_crew()))
    thread.start()
    
    return jsonify({'status': 'started', 'topic': topic, 'message': 'CrewAI running...'})

@app.route('/status')
def status():
    if hasattr(app, 'crew_result'):
        return jsonify(app.crew_result)
    return jsonify({'status': 'running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
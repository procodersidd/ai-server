from flask import Flask, request, jsonify
from intelligence_engine import run_perfected_analysis

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AI Server Running"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        topic = data.get("topic")

        if not topic:
            return jsonify({"error": "No topic provided"}), 400

        result = run_perfected_analysis(topic)

        return jsonify({
            "status": "success",
            "result": str(result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
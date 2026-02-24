from flask import Flask, jsonify, render_template, request

from gpt import run_analysis, DEFAULT_PROMPT

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    prompt = payload.get("prompt")
    result = run_analysis(prompt)
    return jsonify(
        {
            "prompt": prompt or DEFAULT_PROMPT,
            "result": result,
        }
    )


@app.get("/")
def landing():
    return render_template("index.html", prompt="", result="")


@app.post("/")
def landing_submit():
    prompt = (request.form.get("prompt") or "").strip()
    if not prompt:
        prompt = DEFAULT_PROMPT
    result = run_analysis(prompt)
    return render_template("index.html", prompt=prompt, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

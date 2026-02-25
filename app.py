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


@app.post("/follow-up")
def follow_up():
    prompt = (request.form.get("prompt") or "").strip() or DEFAULT_PROMPT
    prior_result = (request.form.get("result") or "").strip()
    question = (request.form.get("question") or "").strip()
    if not question:
        return render_template("index.html", prompt=prompt, result=prior_result)
    combined = (
        "You previously analyzed the following prompt and produced the result below.\n\n"
        f"PROMPT:\n{prompt}\n\nRESULT:\n{prior_result}\n\n"
        f"FOLLOW-UP QUESTION:\n{question}\n\n"
        "Answer the follow-up question concisely and only reference the analysis as needed."
    )
    followup_result = run_analysis(combined)
    return render_template("index.html", prompt=prompt, result=followup_result, question=question)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

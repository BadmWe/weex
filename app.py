from flask import Flask, jsonify, render_template, request

from gpt import run_analysis, DEFAULT_PROMPT

app = Flask(__name__)

PRESETS = [
    {
        "id": "scalp-2h",
        "name": "Scalp 2-3h",
        "prompt": DEFAULT_PROMPT,
        "hint": "Fast trade ideas with stops, leverage, and 2–3h exits.",
    },
    {
        "id": "risk-off",
        "name": "Risk-Off",
        "prompt": (
            "Provide a defensive market read: identify weak pairs, high-volatility risks, "
            "and suggest capital-preserving trades with tight stops and reduced leverage."
        ),
        "hint": "Focus on downside protection and smaller sizing.",
    },
    {
        "id": "momentum",
        "name": "Momentum",
        "prompt": (
            "Identify the strongest momentum tickers in spot and futures, "
            "outline entries, invalidation levels, and 1–2 high-conviction trades."
        ),
        "hint": "Prioritize trending pairs and breakout setups.",
    },
]

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
    return render_template("index.html", prompt="", result="", presets=PRESETS)


@app.post("/")
def landing_submit():
    prompt = (request.form.get("prompt") or "").strip()
    if not prompt:
        prompt = DEFAULT_PROMPT
    result = run_analysis(prompt)
    return render_template("index.html", prompt=prompt, result=result, presets=PRESETS)


@app.post("/follow-up")
def follow_up():
    prompt = (request.form.get("prompt") or "").strip() or DEFAULT_PROMPT
    prior_result = (request.form.get("result") or "").strip()
    question = (request.form.get("question") or "").strip()
    if not question:
        return render_template(
            "index.html", prompt=prompt, result=prior_result, presets=PRESETS
        )
    combined = (
        "You previously analyzed the following prompt and produced the result below.\n\n"
        f"PROMPT:\n{prompt}\n\nRESULT:\n{prior_result}\n\n"
        f"FOLLOW-UP QUESTION:\n{question}\n\n"
        "Answer the follow-up question concisely and only reference the analysis as needed."
    )
    followup_result = run_analysis(combined)
    return render_template(
        "index.html",
        prompt=prompt,
        result=followup_result,
        question=question,
        presets=PRESETS,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

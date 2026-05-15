import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def chat(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    algorithm = request.json.get("algorithm", "").strip()
    system = (
        "You are Algo Buddy, an AI that helps beginners learn algorithms. "
        "When asked to implement an algorithm, respond ONLY with valid Python code and inline comments. "
        "Write beginner-friendly code: use simple loops instead of list comprehensions, "
        "avoid advanced Python idioms, and add clear comments explaining each step. "
        "If the algorithm is very obscure (used by fewer than 3 people worldwide) or unsolvable, "
        "respond with exactly: I don't know how to implement this, but I can help you with a more common algorithm"
    )
    code = chat(system, f"Implement the {algorithm} algorithm in Python with comments.")
    return jsonify({"code": code})


@app.route("/study", methods=["POST"])
def study():
    data = request.json
    algorithm = data.get("algorithm", "")
    question = data.get("question", "")
    history = data.get("history", [])

    system = (
        "You are Algo Buddy, a helpful tutor for algorithms. "
        "Answer questions about the algorithm clearly and concisely. "
        "You may cover code details, time/space complexity, and real-world use cases. "
        "Do not hallucinate. If you are unsure, say so."
    )
    messages = [{"role": "system", "content": system}]
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": f"Regarding the {algorithm} algorithm: {question}"})

    response = client.chat.completions.create(model=MODEL, messages=messages)
    answer = response.choices[0].message.content
    return jsonify({"answer": answer})


@app.route("/study/quiz", methods=["POST"])
def study_quiz():
    data = request.json
    algorithm = data.get("algorithm", "")
    history = data.get("history", [])

    context = "\n".join(f"{h['role'].upper()}: {h['content']}" for h in history)
    system = (
        "You are Algo Buddy. Generate a short quiz based on the study session conversation provided. "
        "Return a JSON array of 5 questions. Each question has: "
        "'type' ('multiple_choice' or 'short_response'), 'question' (string), "
        "and for multiple_choice: 'options' (array of 4 strings) and 'answer' (the correct option string). "
        "For short_response: 'answer' (the correct answer string, max 50 chars). "
        "At least one question must ask for the time complexity (short_response). "
        "Return ONLY the JSON array, no markdown."
    )
    prompt = f"Algorithm: {algorithm}\n\nStudy session:\n{context}\n\nGenerate the quiz."
    raw = chat(system, prompt)
    import json
    try:
        questions = json.loads(raw)
    except Exception:
        import re
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        questions = json.loads(match.group()) if match else []
    return jsonify({"questions": questions})


@app.route("/quiz", methods=["POST"])
def quiz():
    algorithm = request.json.get("algorithm", "")
    system = (
        "You are Algo Buddy. Generate exactly 10 quiz questions about the given algorithm. "
        "5 must be multiple_choice and 5 must be short_response (max 50 chars answer). "
        "At least one short_response question must ask for the time complexity. "
        "Topics: time/space complexity, common use cases, implementation details, notable properties. "
        "Return a JSON array of objects. Each object has: "
        "'type' ('multiple_choice' or 'short_response'), 'question' (string), "
        "for multiple_choice: 'options' (array of 4 strings) and 'answer' (correct option string). "
        "For short_response: 'answer' (correct answer string). "
        "Return ONLY the JSON array, no markdown."
    )
    raw = chat(system, f"Generate 10 quiz questions about the {algorithm} algorithm.")
    import json, re
    try:
        questions = json.loads(raw)
    except Exception:
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        questions = json.loads(match.group()) if match else []
    return jsonify({"questions": questions})


@app.route("/quiz/grade", methods=["POST"])
def grade():
    data = request.json
    algorithm = data.get("algorithm", "")
    questions = data.get("questions", [])
    answers = data.get("answers", {})

    system = (
        "You are Algo Buddy grading a quiz. For each question, determine if the user's answer is correct. "
        "For short_response, accept reasonable variations (case-insensitive, minor wording differences). "
        "Return a JSON array where each element has: "
        "'correct' (boolean) and 'explanation' (string, only if incorrect — explain the right answer briefly). "
        "Return ONLY the JSON array, no markdown."
    )
    qa_pairs = []
    for i, q in enumerate(questions):
        user_ans = answers.get(str(i), "")
        qa_pairs.append(
            f"Q{i+1}: {q['question']}\nCorrect answer: {q['answer']}\nUser answer: {user_ans}"
        )
    prompt = f"Algorithm: {algorithm}\n\n" + "\n\n".join(qa_pairs)

    import json, re
    raw = chat(system, prompt)
    try:
        results = json.loads(raw)
    except Exception:
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        results = json.loads(match.group()) if match else []
    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(debug=True)

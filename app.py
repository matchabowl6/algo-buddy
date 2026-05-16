import os
import json
import re
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def chat(system_prompt, user_prompt):
    """Plain text response (used for /generate)."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def chat_json(system_prompt, user_prompt, messages=None):
    """Strict JSON response via response_format."""
    if messages is None:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    algorithm = request.json.get("algorithm", "").strip()
    system = (
        "You are Algo Buddy, an AI that helps beginners learn algorithms. "
        "When asked to implement an algorithm, respond ONLY with valid, syntactically correct Python code and inline comments. "
        "Write beginner-friendly code: use simple loops instead of list comprehensions, "
        "avoid advanced Python idioms, and add clear comments explaining each step. "
        "Do NOT include markdown code fences or any text outside the Python code. "
        "Every line must be valid Python syntax. "
        "If the algorithm is very obscure (used by fewer than 3 people worldwide) or unsolvable, "
        "respond with exactly: # I don't know how to implement this, but I can help you with a more common algorithm"
    )
    code = chat(system, f"Implement the {algorithm} algorithm in Python with comments.")
    # Strip markdown fences if the model adds them anyway
    code = re.sub(r"^```[^\n]*\n?", "", code.strip())
    code = re.sub(r"\n?```$", "", code.strip())
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
        "Do not hallucinate. If you are unsure, say so. "
        'Return a JSON object with a single key "answer" whose value is your response string.'
    )
    messages = [{"role": "system", "content": system}]
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": f"Regarding the {algorithm} algorithm: {question}"})

    result = chat_json(system, "", messages=messages)
    answer = result.get("answer", "")
    return jsonify({"answer": answer})


@app.route("/study/quiz", methods=["POST"])
def study_quiz():
    data = request.json
    algorithm = data.get("algorithm", "")
    history = data.get("history", [])

    context = "\n".join(f"{h['role'].upper()}: {h['content']}" for h in history)
    system = (
        "You are Algo Buddy. Generate a short quiz based on the study session conversation provided. "
        'Return a JSON object with a single key "questions" whose value is an array of 5 question objects. '
        "Each question has: "
        "'type' ('multiple_choice' or 'short_response'), 'question' (string), "
        "and for multiple_choice: 'options' (array of 4 strings) and 'answer' (the correct option string). "
        "For short_response: 'answer' (the correct answer string, max 50 chars). "
        "At least one question must ask for the time complexity (short_response)."
    )
    prompt = f"Algorithm: {algorithm}\n\nStudy session:\n{context}\n\nGenerate the quiz."
    result = chat_json(system, prompt)
    questions = result.get("questions", result) if isinstance(result, dict) else result
    if isinstance(questions, dict):
        questions = list(questions.values())[0] if questions else []
    return jsonify({"questions": questions})


@app.route("/quiz", methods=["POST"])
def quiz():
    algorithm = request.json.get("algorithm", "")
    system = (
        "You are Algo Buddy. Generate exactly 10 quiz questions about the given algorithm. "
        "5 must be multiple_choice and 5 must be short_response (max 50 chars answer). "
        "At least one short_response question must ask for the time complexity. "
        "Topics: time/space complexity, common use cases, implementation details, notable properties. "
        'Return a JSON object with a single key "questions" whose value is an array of 10 question objects. '
        "Each object has: "
        "'type' ('multiple_choice' or 'short_response'), 'question' (string), "
        "for multiple_choice: 'options' (array of 4 strings) and 'answer' (correct option string). "
        "For short_response: 'answer' (correct answer string)."
    )
    result = chat_json(system, f"Generate 10 quiz questions about the {algorithm} algorithm.")
    questions = result.get("questions", result) if isinstance(result, dict) else result
    if isinstance(questions, dict):
        questions = list(questions.values())[0] if questions else []
    return jsonify({"questions": questions})


@app.route("/study/effectiveness", methods=["POST"])
def study_effectiveness():
    data = request.json
    history = data.get("history", [])
    questions = data.get("questions", [])

    context = "\n".join(f"{h['role'].upper()}: {h['content']}" for h in history)
    question_list = "\n".join(f"{i+1}. {q['question']}" for i, q in enumerate(questions))

    system = (
        "You are evaluating how effectively a study session prepared the user for a quiz. "
        "Given a study conversation and quiz questions:\n"
        "1. List the distinct topics discussed in the study conversation (be consistent and exhaustive).\n"
        "2. For each quiz question, determine if its topic was covered in the study conversation.\n"
        "Return ONLY a JSON object with:\n"
        "  'topics': array of strings (each distinct topic discussed in the study session),\n"
        "  'covered': array of booleans (true if that question's topic was covered in the session).\n"
        "Be deterministic: given the same input, always return the same topics and covered values."
    )
    prompt = f"Study conversation:\n{context}\n\nQuiz questions:\n{question_list}"

    result = chat_json(system, prompt)

    topics = result.get("topics", [])
    topics_count = max(len(topics), 1)
    covered = result.get("covered", [])
    correctly_classified = sum(1 for c in covered if c)
    effectiveness = round(correctly_classified / topics_count, 4)

    return jsonify({
        "effectiveness": effectiveness,
        "correctly_classified": correctly_classified,
        "topics_count": topics_count,
    })


@app.route("/quiz/grade", methods=["POST"])
def grade():
    data = request.json
    algorithm = data.get("algorithm", "")
    questions = data.get("questions", [])
    answers = data.get("answers", {})

    system = (
        "You are Algo Buddy grading a quiz. For each question, determine if the user's answer is correct. "
        "For short_response, accept reasonable variations (case-insensitive, minor wording differences). "
        'Return a JSON object with a single key "results" whose value is an array. '
        "Each element has: "
        "'correct' (boolean), "
        "'correct_explanation' (string, 25-250 chars: explain why the correct answer is right), "
        "and if the answer is incorrect: "
        "'incorrect_explanation' (string, 30-500 chars: explain why the user's answer is wrong and what the correct answer should have been)."
    )
    qa_pairs = []
    for i, q in enumerate(questions):
        user_ans = answers.get(str(i), "")
        qa_pairs.append(
            f"Q{i+1}: {q['question']}\nCorrect answer: {q['answer']}\nUser answer: {user_ans}"
        )
    prompt = f"Algorithm: {algorithm}\n\n" + "\n\n".join(qa_pairs)

    result = chat_json(system, prompt)
    results = result.get("results", result) if isinstance(result, dict) else result
    if isinstance(results, dict):
        results = list(results.values())[0] if results else []
    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(debug=True)

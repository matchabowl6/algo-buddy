const $ = id => document.getElementById(id);

let currentAlgorithm = "";
let studyHistory = [];
let quizQuestions = [];

function show(sectionId) {
  ["home-section", "code-section", "study-section", "quiz-section", "results-section"]
    .forEach(id => $(`${id}`).classList.toggle("hidden", id !== sectionId));
}

function setLoading(on) {
  $("loading").classList.toggle("hidden", !on);
}

async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

// Generate code
$("algo-form").addEventListener("submit", async e => {
  e.preventDefault();
  const algorithm = $("algo-input").value.trim();
  if (!algorithm) return;
  setLoading(true);
  const data = await post("/generate", { algorithm });
  setLoading(false);
  currentAlgorithm = algorithm;
  studyHistory = [];
  $("algo-title").textContent = algorithm;
  $("code-output").textContent = data.code;
  show("code-section");
});

// Mode buttons
$("study-btn").addEventListener("click", () => {
  $("study-chat").innerHTML = "";
  $("study-input").value = "";
  studyHistory = [];
  show("study-section");
});

$("quiz-btn").addEventListener("click", async () => {
  setLoading(true);
  const data = await post("/quiz", { algorithm: currentAlgorithm });
  setLoading(false);
  quizQuestions = data.questions;
  renderQuiz(quizQuestions);
  show("quiz-section");
});

// Study: ask a question
$("study-form").addEventListener("submit", async e => {
  e.preventDefault();
  const question = $("study-input").value.trim();
  if (!question) return;
  $("study-input").value = "";

  appendChat("You", question);
  setLoading(true);
  const data = await post("/study", { algorithm: currentAlgorithm, question, history: studyHistory });
  setLoading(false);

  studyHistory.push({ role: "user", content: question });
  studyHistory.push({ role: "assistant", content: data.answer });
  appendChat("Algo Buddy", data.answer);
});

function appendChat(sender, text) {
  const div = document.createElement("div");
  div.className = `chat-msg ${sender === "You" ? "user" : "bot"}`;
  div.innerHTML = `<strong>${sender}:</strong> ${escapeHtml(text)}`;
  $("study-chat").appendChild(div);
  $("study-chat").scrollTop = $("study-chat").scrollHeight;
}

// Study quiz
$("study-quiz-btn").addEventListener("click", async () => {
  if (studyHistory.length === 0) {
    alert("Have a study session first!");
    return;
  }
  setLoading(true);
  const data = await post("/study/quiz", { algorithm: currentAlgorithm, history: studyHistory });
  setLoading(false);
  quizQuestions = data.questions;
  renderQuiz(quizQuestions);
  show("quiz-section");
});

// Render quiz questions
function renderQuiz(questions) {
  const container = $("quiz-questions");
  container.innerHTML = "";
  questions.forEach((q, i) => {
    const div = document.createElement("div");
    div.className = "quiz-question";
    div.innerHTML = `<p><strong>Q${i + 1}:</strong> ${escapeHtml(q.question)}</p>`;

    if (q.type === "multiple_choice") {
      q.options.forEach(opt => {
        const label = document.createElement("label");
        label.innerHTML = `<input type="radio" name="q${i}" value="${escapeHtml(opt)}"> ${escapeHtml(opt)}`;
        div.appendChild(label);
        div.appendChild(document.createElement("br"));
      });
    } else {
      const input = document.createElement("input");
      input.type = "text";
      input.id = `q${i}`;
      input.maxLength = 50;
      input.placeholder = "Your answer (max 50 chars)";
      div.appendChild(input);
    }
    container.appendChild(div);
  });
}

// Grade quiz
$("quiz-done-btn").addEventListener("click", async () => {
  const answers = {};
  quizQuestions.forEach((q, i) => {
    if (q.type === "multiple_choice") {
      const selected = document.querySelector(`input[name="q${i}"]:checked`);
      answers[i] = selected ? selected.value : "";
    } else {
      answers[i] = ($(`q${i}`) || {}).value || "";
    }
  });

  setLoading(true);
  const data = await post("/quiz/grade", {
    algorithm: currentAlgorithm,
    questions: quizQuestions,
    answers,
  });
  setLoading(false);
  renderResults(data.results);
  show("results-section");
});

function renderResults(results) {
  const container = $("results-output");
  container.innerHTML = "";
  let score = 0;
  results.forEach((r, i) => {
    if (r.correct) score++;
    const div = document.createElement("div");
    div.className = `result-item ${r.correct ? "correct" : "incorrect"}`;
    div.innerHTML = `<p><strong>Q${i + 1}:</strong> ${escapeHtml(quizQuestions[i].question)}</p>
      <p>${r.correct ? "✅ Correct" : `❌ Incorrect — ${escapeHtml(r.explanation || "")}`}</p>`;
    container.appendChild(div);
  });
  const summary = document.createElement("p");
  summary.className = "score";
  summary.textContent = `Score: ${score} / ${results.length}`;
  container.prepend(summary);
}

$("back-btn").addEventListener("click", () => show("code-section"));

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

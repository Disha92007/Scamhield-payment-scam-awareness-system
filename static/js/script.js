const messageBox = document.querySelector("#message");
const charCount = document.querySelector("#charCount");
const analyzeBtn = document.querySelector("#analyzeBtn");
const result = document.querySelector("#result");
const sampleList = document.querySelector("#sampleList");
let quiz = [], quizIndex = 0, score = 0, answered = false;

messageBox.addEventListener("input", () => charCount.textContent = `${messageBox.value.length} / 4000 characters`);
document.querySelector("#clearBtn").addEventListener("click", () => {
  messageBox.value = ""; charCount.textContent = "0 / 4000 characters"; messageBox.focus();
  result.innerHTML = `<div class="empty-result"><div class="shield">⬡</div><h3>Scanner Ready</h3><p>Paste a suspicious message or select a test case to inspect threat indicators and safety advice.</p></div>`;
});
analyzeBtn.addEventListener("click", analyze);
messageBox.addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") analyze(); });

async function analyze() {
  const message = messageBox.value.trim();
  if (!message) { messageBox.focus(); showError("Please paste a message first."); return; }
  analyzeBtn.disabled = true; analyzeBtn.textContent = "Analyzing message…";
  try {
    const response = await fetch("fetch("https://scamshield-backend-kbft.onrender.com/api/analyze", {", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({message})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not analyze message.");
    renderResult(data);
  } catch (e) { showError(e.message || "Unable to reach the server. Check that Flask is running."); }
  finally { analyzeBtn.disabled = false; analyzeBtn.innerHTML = "<span>⌕</span> Analyze Message"; }
}
function showError(msg) { result.innerHTML = `<div class="empty-result"><div class="shield">!</div><h3>Unable to analyze</h3><p>${escapeHtml(msg)}</p></div>`; }
function renderResult(data) {
  const indicators = data.indicators.length ? data.indicators.map(item => `<div class="indicator"><b>⚑ ${escapeHtml(item.label)}</b><p>${escapeHtml(item.explanation)}</p><p><strong>Safety tip:</strong> ${escapeHtml(item.advice)}</p></div>`).join("") : `<div class="indicator"><b>No known indicators matched</b><p>Scams can use wording that this rule set does not recognize. Verify independently.</p></div>`;
  result.innerHTML = `<div class="result-content">
    <div class="result-risk"><div><h3 class="risk-title ${data.risk}">${data.risk} RISK</h3><p>${escapeHtml(data.summary)}</p></div><span class="score">Indicator score: ${data.score}/10</span></div>
    <h4>Detected warning signs (${data.indicators.length})</h4>${indicators}
    <h4>Recommended action</h4><div class="advice-box">${escapeHtml(data.advice)}</div>
    <p class="disclaimer">${escapeHtml(data.disclaimer)}</p></div>`;
}
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }

async function loadSamples() {
  try {
    const response = await fetch("fetch("https://scamshield-backend-kbft.onrender.com/api/samples");");
    const samples = await response.json();
    sampleList.innerHTML = samples.map(s => `<button type="button" class="sample-item" data-id="${s.id}"><span>${escapeHtml(s.title)}</span><span class="risk-badge ${escapeHtml(s.expected_risk)}">${escapeHtml(s.expected_risk)} RISK</span></button>`).join("");
    sampleList.querySelectorAll("button").forEach((button, index) => button.addEventListener("click", () => {
      const sample = samples[index]; messageBox.value = sample.message;
      charCount.textContent = `${messageBox.value.length} / 4000 characters`; analyze();
    }));
  } catch { sampleList.innerHTML = `<p class="muted">Samples unavailable. Check database setup and refresh.</p>`; }
}

async function loadQuiz() {
  try {
    const response = await fetch("fetch("https://scamshield-backend-kbft.onrender.com/api/quiz");"); quiz = await response.json();
    if (!quiz.length) throw new Error("No quiz questions found.");
    quizIndex = 0; score = 0; renderQuestion();
  } catch { document.querySelector("#questionText").textContent = "Quiz unavailable. Check database setup and refresh."; }
}
function renderQuestion() {
  answered = false;
  const q = quiz[quizIndex];
  document.querySelector("#quizProgress").textContent = `Scenario ${quizIndex + 1} of ${quiz.length}`;
  document.querySelector("#quizScore").textContent = `Score: ${score}`;
  document.querySelector("#progressFill").style.width = `${quizIndex / quiz.length * 100}%`;
  document.querySelector("#questionText").textContent = q.question;
  document.querySelector("#quizFeedback").hidden = true;
  document.querySelector("#nextQuestion").hidden = true;
  const options = document.querySelector("#options"); options.innerHTML = "";
  q.options.forEach((option, index) => {
    const button = document.createElement("button"); button.className = "option"; button.textContent = `${String.fromCharCode(65 + index)}. ${option}`;
    button.addEventListener("click", () => submitAnswer(q.id, index, button)); options.appendChild(button);
  });
}
async function submitAnswer(id, answer, clicked) {
  if (answered) return; answered = true;
  try {
    const response = await fetch("fetch("https://scamshield-backend-kbft.onrender.com/api/quiz");", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question_id:id,answer})});
    const data = await response.json(); if (!response.ok) throw new Error(data.error);
    const buttons = [...document.querySelectorAll(".option")]; buttons.forEach(b => b.disabled = true);
    buttons[data.correct_answer]?.classList.add("correct");
    if (data.correct) score++; else clicked.classList.add("wrong");
    document.querySelector("#quizScore").textContent = `Score: ${score}`;
    const feedback = document.querySelector("#quizFeedback"); feedback.textContent = `${data.correct ? "Correct! " : "Not quite. "}${data.explanation}`; feedback.hidden = false;
    const next = document.querySelector("#nextQuestion"); next.hidden = false;
    next.textContent = quizIndex === quiz.length - 1 ? "See Results" : "Next Question →";
  } catch { answered = false; showQuizError(); }
}
function showQuizError() { const f=document.querySelector("#quizFeedback"); f.textContent="Could not check answer. Please try again."; f.hidden=false; }
document.querySelector("#nextQuestion").addEventListener("click", () => {
  if (quizIndex < quiz.length - 1) { quizIndex++; renderQuestion(); }
  else {
    document.querySelector("#progressFill").style.width = "100%";
    document.querySelector("#questionText").textContent = `Quiz complete! You scored ${score} out of ${quiz.length}.`;
    document.querySelector("#options").innerHTML = "";
    document.querySelector("#quizFeedback").textContent = score === quiz.length ? "Excellent work. Keep verifying payment requests." : "Review the Golden Rules above and try again.";
    document.querySelector("#quizFeedback").hidden = false;
    document.querySelector("#nextQuestion").textContent = "Try Again";
    document.querySelector("#nextQuestion").onclick = () => { document.querySelector("#nextQuestion").onclick = null; loadQuiz(); };
  }
});
loadSamples(); loadQuiz();

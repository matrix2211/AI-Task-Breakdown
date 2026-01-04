let stepsState = [];
let totalSteps = 0;

function showTab(tab) {
  document.getElementById("planTab").classList.toggle("hidden", tab !== "plan");
  document.getElementById("toolsTab").classList.toggle("hidden", tab !== "tools");

  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelector(`[onclick="showTab('${tab}')"]`).classList.add("active");
}

async function generatePlan() {
  const goal = document.getElementById("goal").value.trim();
  if (!goal) return;

  const status = document.getElementById("status");
  const resultCard = document.getElementById("resultCard");

  status.classList.remove("hidden");
  status.textContent = "Thinking…";

  const res = await fetch("/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal })
  });

  const data = await res.json();
  const result = data.result;

  stepsState = result.steps.map(() => false);
  totalSteps = stepsState.length;

  renderSteps(result.steps);
  renderTools(result.tools);
  updateProgress();

  status.classList.add("hidden");
  resultCard.classList.remove("hidden");
}

function renderSteps(steps) {
  const container = document.getElementById("steps");
  container.innerHTML = "";

  steps.forEach((step, index) => {
    const row = document.createElement("div");
    row.className = "step";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = stepsState[index];

    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        for (let i = 0; i <= index; i++) stepsState[i] = true;
      } else {
        for (let i = index; i < stepsState.length; i++) stepsState[i] = false;
      }
      renderSteps(steps);
      updateProgress();
    });

    if (checkbox.checked) row.classList.add("completed");

    const text = document.createElement("div");
    text.className = "step-text";
    text.textContent = step.text;

    row.appendChild(checkbox);
    row.appendChild(text);
    container.appendChild(row);
  });
}

function renderTools(tools) {
  const list = document.getElementById("tools");
  list.innerHTML = "";
  tools.forEach(t => {
    const li = document.createElement("li");
    li.textContent = `${t.tool} — ${t.reason}`;
    list.appendChild(li);
  });
}

function updateProgress() {
  const completed = stepsState.filter(Boolean).length;
  const percent = Math.round((completed / totalSteps) * 100);

  document.getElementById("overallProgressBar").style.width = `${percent}%`;
  document.getElementById("progressPercent").textContent = `${percent}%`;
}

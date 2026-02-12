// llm_ui.js
(() => {
  const promptEl = document.getElementById("llmPrompt");
  const btn = document.getElementById("llmSendBtn");
  const st = document.getElementById("llmStatus");

  // Si estás usando Live Server (5500), el API queda en 8000 en el mismo host.
  const apiBase = (location.port && location.port !== "8000")
    ? `${location.protocol}//${location.hostname}:8000`
    : "";

  async function send() {
    const text = (promptEl.value || "").trim();
    if (!text) return;

    st.classList.remove("offline");
    st.textContent = "LLM: enviando...";

    try {
      const res = await fetch(`${apiBase}/api/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      if (!res.ok || !data.ok) throw new Error(data.detail || "Error");

      st.textContent = `LLM: OK (${data.used_llm ? "LLM" : "fallback"}) intent=${data.cmd.intent}`;
    } catch (e) {
      st.classList.add("offline");
      st.textContent = `LLM: ERROR (${e.message})`;
    }
  }

  btn.addEventListener("click", send);

  promptEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      send();
    }
  });
})();

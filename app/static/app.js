const messagesEl = document.getElementById("messages");
const form = document.getElementById("composer");
const input = document.getElementById("input");
const send = document.getElementById("send");
const docList = document.getElementById("doc-list");

const history = [];

async function loadDocuments() {
  try {
    const res = await fetch("/api/documents");
    if (!res.ok) throw new Error("Failed to load documents");
    const docs = await res.json();
    if (!docs.length) {
      docList.innerHTML = "<li class='muted'>No documents ingested yet.</li>";
      return;
    }
    docList.innerHTML = docs
      .map(
        (doc) =>
          `<li>${escapeHtml(doc.filename)}<small>${doc.chunk_count} chunks</small></li>`
      )
      .join("");
  } catch (err) {
    docList.innerHTML = `<li class="muted">${escapeHtml(err.message)}</li>`;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  appendBubble("user", text);
  input.value = "";
  send.disabled = true;
  const pending = appendBubble("assistant", "Thinking…", { typing: true });

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(formatDetail(data.detail) || "Chat request failed");
    }
    pending.remove();
    appendBubble("assistant", data.answer, { sources: data.sources || [] });
    history.push({ role: "user", content: text });
    history.push({ role: "assistant", content: data.answer });
    if (history.length > 12) history.splice(0, history.length - 12);
  } catch (err) {
    pending.remove();
    appendBubble("assistant", err.message, { error: true });
  } finally {
    send.disabled = false;
    input.focus();
  }
});

function appendBubble(role, text, options = {}) {
  const article = document.createElement("article");
  article.className = `bubble ${role}${options.error ? " error" : ""}`;
  const sourcesHtml = (options.sources || [])
    .map(
      (source) =>
        `<span class="chip" title="${escapeHtml(source.snippet)}">${escapeHtml(
          source.filename
        )}</span>`
    )
    .join("");
  article.innerHTML = `
    <div class="avatar">${role === "user" ? "YOU" : "AI"}</div>
    <div class="body">
      <p class="${options.typing ? "typing" : ""}">${escapeHtml(text)}</p>
      ${sourcesHtml ? `<div class="sources">${sourcesHtml}</div>` : ""}
    </div>
  `;
  messagesEl.appendChild(article);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return article;
}

function formatDetail(detail) {
  if (!detail) return "";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || JSON.stringify(item)).join("; ");
  }
  return JSON.stringify(detail);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

loadDocuments();
input.focus();

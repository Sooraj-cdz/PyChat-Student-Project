const list = document.getElementById("messages");
const form = document.getElementById("message-form");
const input = document.getElementById("message-input");
const currentUser = document.getElementById("current-user").textContent;
let lastId = 0;

function addMessage(item) {
  const empty = document.getElementById("empty-state");
  if (empty) empty.remove();

  const row = document.createElement("article");
  row.className = "message" + (item.username === currentUser ? " mine" : "");
  const meta = document.createElement("div");
  meta.className = "message-meta";
  const name = document.createElement("strong");
  name.textContent = item.username;
  const time = document.createElement("time");
  time.textContent = item.created_at;
  const body = document.createElement("p");
  body.textContent = item.message;
  meta.append(name, time);
  row.append(meta, body);
  list.appendChild(row);
  list.scrollTop = list.scrollHeight;
  lastId = Math.max(lastId, item.id);
}

async function loadMessages() {
  try {
    const response = await fetch(`/api/messages?after=${lastId}`);
    if (response.status === 401) { window.location.href = "/"; return; }
    if (!response.ok) return;
    const messages = await response.json();
    messages.forEach(addMessage);
  } catch (error) {
    console.error("Could not load messages:", error);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.disabled = true;
  try {
    const response = await fetch("/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const result = await response.json();
    if (!response.ok) { alert(result.error || "Message could not be sent."); return; }
    input.value = "";
    await loadMessages();
  } catch (error) {
    alert("Connection problem. Please try again.");
  } finally {
    input.disabled = false;
    input.focus();
  }
});

loadMessages();
setInterval(loadMessages, 2000);

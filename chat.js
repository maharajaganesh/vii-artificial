const userName = localStorage.getItem("vii_user_name");
if (!userName) {
  window.location.href = "index.html";
}

document.getElementById("user-status").textContent = "Vanakkam, " + userName + "!";

const chatBody = document.getElementById("chat-body");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

function addBubble(text, from, reason) {
  const bubble = document.createElement("div");
  bubble.className = "bubble " + from;
  bubble.textContent = text;
  if (reason) {
    const r = document.createElement("span");
    r.className = "reason";
    r.textContent = "Vii oda yosanai: " + reason;
    bubble.appendChild(r);
  }
  chatBody.appendChild(bubble);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function showTyping() {
  const t = document.createElement("div");
  t.className = "typing";
  t.id = "typing-indicator";
  t.innerHTML = "<span></span><span></span><span></span>";
  chatBody.appendChild(t);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById("typing-indicator");
  if (t) t.remove();
}

async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;
  addBubble(text, "user");
  chatInput.value = "";
  showTyping();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, name: userName })
    });
    const data = await res.json();
    hideTyping();
    addBubble(data.reply, "vii", data.reason);
  } catch (err) {
    hideTyping();
    addBubble("Aiyo, server kooda connect aagala. app.py run pannirukkeengala nu check pannunga.", "vii");
  }
}

sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("vii_user_name");
  localStorage.removeItem("vii_user_email");
  window.location.href = "index.html";
});

// Opening greeting from Vii
window.addEventListener("load", () => {
  setTimeout(() => {
    addBubble("hii " + userName + ", enna venum unakku? Naan Vii — free ah kேட்குங்க, yosichu solren.", "vii");
  }, 400);
});

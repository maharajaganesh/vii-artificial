# Vii — Tanglish chatting AI

A small full-stack demo: a login page (Google Sign-In + guest mode), and a chat
home page where "Vii", an illustrated girl character, chats with you in
Tanglish (Tamil written in English letters).

## Files

- `index.html` / `style.css` / `script.js` — login/welcome screen, girl SVG
  illustration, Google Sign-In button
- `chat.html` / `chat.js` — the chat screen, greets you with
  "hii \<name\>, enna venum unakku?"
- `app.py` — Flask backend. Serves the pages and a `/api/chat` endpoint that
  runs the rule-based Tanglish reply logic
- `requirements.txt` — Python dependencies

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** in your browser.

- Click **"Guest ah try pannunga"** to skip login and go straight to chat —
  good for testing.
- Real **"Sign in with Google"** needs your own free OAuth Client ID:
  1. Go to https://console.cloud.google.com/apis/credentials
  2. Create an **OAuth client ID** → Application type: **Web application**
  3. Add `http://localhost:5000` under **Authorized JavaScript origins**
  4. Copy the Client ID and paste it into `GOOGLE_CLIENT_ID` at the top of
     `script.js`

## How the chat "AI" works

`app.py` uses simple keyword-pattern matching, the same idea as a basic
rule-based chatbot: it scans your message for known Tanglish/English
keywords (greetings, feelings, study/coding topics, thanks, bye) and returns
a matching reply. Each reply also comes with a one-line **reason** — shown
in a small italic note under Vii's chat bubble — explaining *why* Vii
answered that way. This is a simplified nod to how a more advanced AI
assistant reasons step by step before answering, rather than just spitting
out a canned line.

## Where to go from here

- **Smarter replies**: swap `get_reply()` in `app.py` for a real LLM API
  call (e.g. the Anthropic API) so Vii can understand free-form Tamil/English
  and generate original answers instead of picking from a fixed list.
- **Persistent chat history**: save messages to a database (SQLite/Postgres)
  keyed by the signed-in user's email.
- **Real Google auth on the backend**: currently the Google sign-in only
  runs in the browser (via Google Identity Services) and stores the name
  locally. For a production app, verify the Google ID token on the server
  too before trusting it.

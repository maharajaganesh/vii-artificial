"""
Vii — a Tanglish (Tamil + English) chatting AI.

This is a rule-based backend: it looks for keyword patterns in what the
user types and picks a matching Tanglish reply, the same way the very
first chatbot example was built, just themed as "Vii" and multilingual.

Every reply also comes with a short "reason" — one line explaining WHY
Vii answered that way. This mirrors how a thoughtful assistant (Claude)
walks through its reasoning step by step instead of just outputting a
canned line; here it's simplified into pattern -> reasoning -> reply.

Run:
    pip install flask
    python app.py
Then open http://localhost:5000
"""

import random
import re
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

# Each rule = (keywords to look for, reasoning shown to the user, list of possible replies)
RULES = [
    (["vanakkam", "hi", "hello", "hii", "hey"],
     "Idhu oru greeting madhiri irukku, so naan friendly ah wish pannuren.",
     ["Vanakkam nanba! Enna scene?", "Hii! Nalla irukeengala?", "Hey! Sollunga, enna venum?"]),

    (["your name", "yaru nee", "who are you", "unga peru"],
     "Peru pathi kேட்டாanga, so naan yaaru nu clear ah solren.",
     ["Naan Vii — unga Tanglish chatting AI nanba.", "En peru Vii! Just chatting mattum illa, kேட்டadhukku yosichum solven."]),

    (["how are you", "epdi irukeenga", "eppadi iruka"],
     "En nalam pathi kேட்டaanga, so short ah reply pannitu avanga kitta thirumba kேட்குren.",
     ["Naan super ah irukken! Neenga epdi irukeenga?", "Nalla irukken nanba, nீங்க sollunga?"]),

    (["thank", "nandri", "thanks"],
     "Nandri sonna udane, warm ah acknowledge pannuradhu nalladhu.",
     ["Paravala nanba, edhuku nandri!", "Yenna venumnalum kேட்குங்க, naan irukken."]),

    (["bye", "poitu varen", "poren", "see you"],
     "Sending off pannuraanga, so short ah warm ah bye solren.",
     ["Bye nanba! Thirumba pேசலாம்.", "Poitu vaanga, take care!"]),

    (["sad", "kavalai", "vருத்தம்", "feel bad", "lonely"],
     "Emotion negative ah irukku nu detect panniten, so first avanga feeling ah acknowledge pannitu, judge pannama kேட்குren.",
     ["Aiyo, adhu kேட்க vருத்தமா irukku. Enna nadandhuchu, solla vேணுமா?", "Naan kேட்குren nanba, neenga single ah illa idhula."]),

    (["happy", "santhosham", "super", "semma", "great news"],
     "Positive emotion detect panniten, so avanga oda energy oda match pannuren.",
     ["Wowww semma! Enna happy news?", "Adhu kேட்க romba santhosham nanba!"]),

    (["study", "exam", "padhipu", "college", "assignment"],
     "Padhipu related keyword paartaen, so help pannalam nu offer pannuren.",
     ["Padhipu ah? Sollunga, edho oru topic ku help pannalama?", "Exam preparation ku help venuma? Details sollunga."]),

    (["code", "program", "python", "javascript", "html", "css"],
     "Coding topic nu identify panniten, so technical ah help pannalam nu solren.",
     ["Coding doubt ah? Language enna nu sollunga, help pannuren.", "Semma! Code pathi enna venum, detail ah sollunga."]),
]

FALLBACK_REASON = "Specific keyword edhuvum match aagala, so open ended ah avanga enna solla vaanga nu kேட்குren."
FALLBACK_REPLIES = [
    "Adhu interesting ah irukku, konjam explain pannுங்களா?",
    "Puriyala nanba, konjam vேறு mathiri sollunga.",
    "Sollunga, naan kேட்கरேன்.",
]


def contains_keyword(text: str, keyword: str) -> bool:
    # Short keywords (hi, hey...) use word boundaries so they don't
    # accidentally match inside longer words like "padhipu".
    if len(keyword) <= 3 and " " not in keyword:
        return re.search(r"\b" + re.escape(keyword) + r"\b", text) is not None
    return keyword in text


def get_reply(message: str):
    text = message.lower()
    for keywords, reason, replies in RULES:
        if any(contains_keyword(text, k) for k in keywords):
            return random.choice(replies), reason
    return random.choice(FALLBACK_REPLIES), FALLBACK_REASON


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"reply": "Onnum type pannala nanba, edhavadhu sollunga.", "reason": "Empty message vandhuchu."})
    reply, reason = get_reply(message)
    return jsonify({"reply": reply, "reason": reason})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

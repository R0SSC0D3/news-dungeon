from flask import Flask, request, render_template
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    article = data.get("article", "")
    tone = data.get("tone", "High Fantasy")

    prompt = f"""
You are a Dungeon Master creating a one-shot Dungeons & Dragons campaign inspired by a real-world news article.

Article Summary:
"""
{article}
"""

Tone: {tone}

Your task is to reimagine the key figures, themes, and events from this article as a dark fantasy adventure. Be creative but stay grounded in allegory — reinterpret the article's content as if it were myth or prophecy.

Use the article’s actual people or organizations as inspiration for names and roles. For example, if the article includes public figures, transform their names into fantasy-appropriate NPCs.

Return the following in well-formatted Markdown:
1. Campaign Title
2. Setting Description
3. Central Conflict
4. Quest Hook
5. Three Major NPCs (based on real article names)
6. Two Encounters
7. One Magic Item or Lore Fragment
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=1500
    )

    result = response.choices[0].message.content
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

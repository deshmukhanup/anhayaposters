import os
import json
import datetime
from google import genai
from weasyprint import HTML
from PIL import Image, ImageDraw, ImageFont

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

today_str = datetime.date.today().strftime("%B %d, %Y")
os.makedirs("output", exist_ok=True)

# 1. Ask Gemini to generate fresh content for today
prompt = f"""
Generate unique, daily cultural/educational copy for 3 brands for today ({today_str}).
Return strictly valid JSON with this exact schema:
{{
  "spin_a_yarn": {{
    "issue": "Vol. 2026 • Issue {datetime.date.today().strftime('%j')}",
    "headline": "...",
    "quote": "...",
    "topic": "...",
    "ig_caption": "...",
    "li_caption": "..."
  }},
  "read_aloud": {{
    "issue": "Daily Insight #{datetime.date.today().strftime('%j')}",
    "stat_num": "15 MINUTES",
    "headline": "...",
    "insight": "...",
    "ig_caption": "...",
    "li_caption": "..."
  }},
  "daughters_of_india": {{
    "issue": "Movement Issue #{datetime.date.today().strftime('%j')}",
    "headline": "...",
    "quote": "...",
    "ig_caption": "...",
    "li_caption": "..."
  }}
}}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={"response_mime_type": "application/json"}
)

data = json.loads(response.text)

# Save the Social Captions to Markdown
with open("output/social_captions.md", "w") as f:
    f.write(f"# Daily Social Media Captions — {today_str}\n\n")
    f.write(f"## 1. Spin a Yarn India\n### Instagram\n{data['spin_a_yarn']['ig_caption']}\n\n### LinkedIn\n{data['spin_a_yarn']['li_caption']}\n\n")
    f.write(f"## 2. The Read Aloud Project\n### Instagram\n{data['read_aloud']['ig_caption']}\n\n### LinkedIn\n{data['read_aloud']['li_caption']}\n\n")
    f.write(f"## 3. Daughters of India\n### Instagram\n{data['daughters_of_india']['ig_caption']}\n\n### LinkedIn\n{data['daughters_of_india']['li_caption']}\n\n")

# 2. Build the multi-page A4 HTML document
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    @page {{ size: 210mm 297mm; margin: 0; }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: sans-serif; }}
    .poster-page {{ width: 210mm; height: 297mm; padding: 22mm; page-break-after: always; position: relative; display: block; }}
    .say {{ background-color: #0c061d; color: #ffffff; }}
    .trap {{ background-color: #f3fafc; color: #0b1c2d; }}
    .doi {{ background-color: #faf5f0; color: #2b1a18; }}
    .pill {{ display: inline-block; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 25px; }}
    .say .pill {{ background-color: #8c52ff; color: #f9e300; }}
    .trap .pill {{ background-color: #00c3d9; color: #0b1c2d; }}
    .doi .pill {{ background-color: #c14436; color: #ffffff; }}
    h1 {{ font-size: 38px; line-height: 1.15; margin-bottom: 30px; text-transform: uppercase; }}
    .say h1 span {{ color: #f9e300; }}
    .trap h1 span {{ color: #00c3d9; }}
    .doi h1 span {{ color: #c14436; }}
    .card {{ padding: 22px; border-radius: 12px; margin-bottom: 30px; font-size: 16px; line-height: 1.5; }}
    .say .card {{ background: rgba(255,255,255,0.08); border-left: 4px solid #f9e300; }}
    .trap .card {{ background: #ffffff; border: 1px solid #d2eff4; }}
    .doi .card {{ background: #ffffff; border: 1px solid #ebd9d2; }}
    .tagline {{ padding: 15px; text-align: center; font-weight: bold; margin-bottom: 40px; border-radius: 8px; text-transform: uppercase; }}
    .say .tagline {{ border: 1px dashed #f9e300; color: #f9e300; }}
    .trap .tagline {{ background: #0b1c2d; color: #00c3d9; }}
    .doi .tagline {{ border: 1px solid #c14436; color: #c14436; background: #faece9; }}
    .footer {{ position: absolute; bottom: 22mm; left: 22mm; right: 22mm; border-top: 1px solid rgba(128,128,128,0.3); padding-top: 15px; font-size: 12px; }}
  </style>
</head>
<body>
  <div class="poster-page say">
    <div class="pill">Spin A Yarn India • Daily Lore</div>
    <h1>{data['spin_a_yarn']['headline']}</h1>
    <div class="card">"{data['spin_a_yarn']['quote']}"</div>
    <div class="tagline">Preserve, Protect & Promote Indian Culture & Heritage</div>
    <div class="footer">#SpinAYarnIndia • SHARE ON STORIES → @SpinAYarnIndia</div>
  </div>

  <div class="poster-page trap">
    <div class="pill">The Read Aloud Project</div>
    <h1>{data['read_aloud']['headline']}</h1>
    <div class="card">{data['read_aloud']['insight']}</div>
    <div class="tagline">Your Voice, Their Imagination</div>
    <div class="footer">#ReadAloudProject • SAVE • SHARE • @ReadAloudProject</div>
  </div>

  <div class="poster-page doi">
    <div class="pill">Daughters of India</div>
    <h1>{data['daughters_of_india']['headline']}</h1>
    <div class="card">{data['daughters_of_india']['quote']}</div>
    <div class="tagline">Real Girls Support Each Other</div>
    <div class="footer">www.daughtersofindia.in • #DaughtersOfIndia • @DaughtersOfIndia</div>
  </div>
</body>
</html>"""

with open("output/index.html", "w") as f:
    f.write(html_content)

# 3. Export to PDF
HTML("output/index.html").write_pdf("output/daily_posters.pdf")
print("Generated daily posters, captions, and PDF successfully!")

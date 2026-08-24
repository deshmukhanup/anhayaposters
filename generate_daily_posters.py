import os
import json
import datetime
from google import genai
from weasyprint import HTML

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

today_str = datetime.date.today().strftime("%B %d, %Y")
day_of_year = datetime.date.today().strftime("%j")
os.makedirs("output", exist_ok=True)

# 1. Ask Gemini to generate sophisticated, thought-provoking daily content
prompt = f"""
Act as a world-class creative director, cultural essayist, cognitive scientist, and feminist philosopher.
Generate daily, high-impact cultural and educational copy for 3 distinct brands for today ({today_str}).

Brands & Strict Context:
1. Spin a Yarn India
   - Mission: Reviving oral folklore, living traditions, ancient philosophy (Shruti/Smriti), and cultural continuity.
   - Official Tagline: "Preserve, Protect & Promote Indian Culture & Heritage"
   - Tone: Majestic, profound, timeless, lyrical.

2. The Read Aloud Project
   - Mission: Early childhood cognitive neurodevelopment, literacy, emotional bonding, and speech development through reading aloud vs passive screens.
   - Official Tagline: "Your Voice, Their Imagination"
   - Tone: Empowering, neuroscience-backed, warm, urgent for modern parents.

3. Daughters of India
   - Mission: Female agency, radical sisterhood, dismantling competition among women, institutional leadership, and mutual elevation.
   - Official Tagline: "Real Girls Support Each Other"
   - Tone: Fierce, anthemic, poetic, unapologetic solidarity.

Return strictly valid JSON with this exact schema:
{{
  "spin_a_yarn": {{
    "volume_issue": "Vol. 2026 • Issue {day_of_year}",
    "sublabel": "THE SPOKEN HERITAGE SERIES",
    "headline_plain": "Provocative 8-14 word hook in ALL CAPS",
    "narrative_quote": "A 2-3 sentence deeply resonant quote or insight on the power of the spoken word and living memory.",
    "quote_attribution": "— Living Traditions & Ancestral Memory",
    "topic_meta": "The Living Epics & Oral Continuity",
    "ig_caption": "Compelling Instagram caption with storytelling hook, reflection question, and hashtags #SpinAYarnIndia #IndianCulture #OralTraditions",
    "li_caption": "Thought-leadership LinkedIn post on cultural preservation and narrative transmission."
  }},
  "read_aloud": {{
    "insight_tracker": "Daily Neuro-Insight #{day_of_year}",
    "focal_stat_number": "15 MINUTES",
    "focal_stat_statement": "of daily read-aloud exposes a child to over 1 million words before kindergarten.",
    "impact_box_title": "COGNITIVE ARCHITECTURE & EMPATHY",
    "impact_box_body": "A 2-3 sentence hard-hitting cognitive/neurodevelopment insight contrasting voice connection with passive screen time.",
    "mission_note": "1 Book. 15 Mins. 0 Screens.",
    "ig_caption": "High-engagement Instagram caption for parents with actionable tips, neuro-facts, and hashtags #ReadAloudProject #EarlyLiteracy #ParentingHacks",
    "li_caption": "Executive/parenting LinkedIn perspective on childhood literacy ROI and human voice connection."
  }},
  "daughters_of_india": {{
    "movement_issue": "Movement Issue #{day_of_year}",
    "headline_main": "When one girl rises, she lifts every sister with her.",
    "narrative_body": "A 2-3 sentence evocative discourse on collective female empowerment, replacing competition with solidarity in leadership, boardrooms, and communities.",
    "sub_footer_motto": "Educate • Elevate • Empower",
    "ig_caption": "Empowering Instagram caption celebrating sisterhood, mentorship, and community with hashtags #DaughtersOfIndia #RealGirlsSupportEachOther #WomenInLeadership",
    "li_caption": "Professional LinkedIn post on female mentorship, allyship, and creating room at the leadership table."
  }}
}}
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json"
    }
)

raw_text = response.text.strip()
if raw_text.startswith("```json"):
    raw_text = raw_text[7:]
if raw_text.startswith("```"):
    raw_text = raw_text[3:]
if raw_text.endswith("```"):
    raw_text = raw_text[:-3]

data = json.loads(raw_text.strip())

# 2. Save Social Captions to Markdown
with open("output/social_captions.md", "w", encoding="utf-8") as f:
    f.write(f"# Daily Social Media Captions — {today_str}\n\n")
    f.write(f"## 1. Spin a Yarn India\n### Instagram\n{data['spin_a_yarn']['ig_caption']}\n\n### LinkedIn\n{data['spin_a_yarn']['li_caption']}\n\n")
    f.write(f"## 2. The Read Aloud Project\n### Instagram\n{data['read_aloud']['ig_caption']}\n\n### LinkedIn\n{data['read_aloud']['li_caption']}\n\n")
    f.write(f"## 3. Daughters of India\n### Instagram\n{data['daughters_of_india']['ig_caption']}\n\n### LinkedIn\n{data['daughters_of_india']['li_caption']}\n\n")

# 3. High-Fidelity Multi-Page A4 HTML Document (WeasyPrint Compatible)
say_data = data["spin_a_yarn"]
rap_data = data["read_aloud"]
doi_data = data["daughters_of_india"]

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Daily High-Impact Social Posters ({today_str})</title>
  <style>
    @page {{
      size: 210mm 297mm;
      margin: 0;
    }}
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
      background: #000000;
      color: #111111;
      -webkit-font-smoothing: antialiased;
    }}
    .poster-page {{
      width: 210mm;
      height: 297mm;
      padding: 24mm 22mm 22mm 22mm;
      position: relative;
      page-break-after: always;
      display: block;
      overflow: hidden;
    }}

    /* -------------------------------------------------------------
       POSTER 1: SPIN A YARN INDIA
       Palette: Electric Violet #8c52ff | Vibrant Gold #f9e300 | Midnight #0c061d
       ------------------------------------------------------------- */
    .poster-say {{
      background-color: #0c061d;
      color: #ffffff;
    }}
    .say-pill {{
      display: inline-block;
      background: rgba(140, 82, 255, 0.22);
      border: 1.5px solid #8c52ff;
      color: #f9e300;
      padding: 9px 18px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .say-meta {{
      float: right;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.14em;
      color: #8c52ff;
      text-transform: uppercase;
      margin-top: 10px;
    }}
    .say-sub {{
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.22em;
      color: #8c52ff;
      text-transform: uppercase;
      margin-top: 55px;
      margin-bottom: 15px;
    }}
    .say-headline {{
      font-size: 40px;
      font-weight: 900;
      line-height: 1.08;
      letter-spacing: -0.02em;
      text-transform: uppercase;
      color: #ffffff;
      margin-bottom: 35px;
    }}
    .say-headline span {{
      color: #f9e300;
    }}
    .say-card {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(140, 82, 255, 0.35);
      border-left: 6px solid #f9e300;
      border-radius: 14px;
      padding: 24px 26px;
      margin-bottom: 35px;
    }}
    .say-quote {{
      font-size: 16px;
      line-height: 1.55;
      color: #ece8f8;
      font-style: italic;
      margin-bottom: 14px;
    }}
    .say-author {{
      font-size: 11px;
      font-weight: 800;
      color: #f9e300;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .say-tagline-box {{
      border: 2px dashed rgba(249, 227, 0, 0.7);
      background: rgba(249, 227, 0, 0.06);
      border-radius: 10px;
      padding: 16px 20px;
      text-align: center;
      margin-bottom: 30px;
    }}
    .say-tagline-text {{
      font-size: 13px;
      font-weight: 900;
      letter-spacing: 0.14em;
      color: #f9e300;
      text-transform: uppercase;
    }}
    .say-footer {{
      position: absolute;
      bottom: 22mm;
      left: 22mm;
      right: 22mm;
      border-top: 1.5px solid rgba(140, 82, 255, 0.3);
      padding-top: 16px;
    }}
    .say-footer-left {{
      float: left;
      font-size: 11px;
      color: #a497c2;
      line-height: 1.45;
    }}
    .say-footer-left strong {{
      color: #ffffff;
    }}
    .say-cta {{
      float: right;
      background: #f9e300;
      color: #0c061d;
      padding: 9px 18px;
      border-radius: 7px;
      font-size: 11px;
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    /* -------------------------------------------------------------
       POSTER 2: THE READ ALOUD PROJECT
       Palette: Luminous Cyan #00c3d9 | Slate Navy #0b1c2d | Paper #f3fafc
       ------------------------------------------------------------- */
    .poster-trap {{
      background-color: #f3fafc;
      color: #0b1c2d;
    }}
    .trap-pill {{
      display: inline-block;
      background: #00c3d9;
      color: #0b1c2d;
      padding: 9px 18px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 900;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    .trap-meta {{
      float: right;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.14em;
      color: #5c7b91;
      text-transform: uppercase;
      margin-top: 10px;
    }}
    .trap-stat-num {{
      font-size: 72px;
      font-weight: 900;
      line-height: 0.95;
      letter-spacing: -0.04em;
      color: #00c3d9;
      margin-top: 55px;
      margin-bottom: 12px;
    }}
    .trap-stat-headline {{
      font-size: 32px;
      font-weight: 900;
      line-height: 1.15;
      letter-spacing: -

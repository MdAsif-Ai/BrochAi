from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os
import json
from fastapi.responses import FileResponse

from scrape import ComprehensiveBrochureScraper  # ← Import directly
from dynamic_pdf_generator import generate_pdf
from ai_services  import generate_brochure_content






class BrochureRequest(BaseModel):
    companyName: str
    companyUrl: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi.staticfiles import StaticFiles
import os

# Serve built frontend
if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="dist")

@app.post("/generate-brochure")
async def generate_brochure(request: BrochureRequest):
    try:
        company_name = request.companyName
        company_url = request.companyUrl

        pdf_file = f"{company_name.replace(' ', '_')}_brochure.pdf"

        print("STEP 1: scraping...")

        scraper = ComprehensiveBrochureScraper(company_url)
        data = scraper.scrape(max_pages=20)
        scraped_text = str(data)

        prompt = f"""
            Create a 5-page premium corporate brochure for the following company.



BROCHURE REQUIREMENTS:

PAGE STRUCTURE:

Page 1 — Premium Cover Page
- Powerful headline
- Premium brand positioning
- Hero narrative
- Key highlights strip

Page 2 — Company Overview
- Deep company story
- Innovation philosophy
- Market presence
- Strategic vision
- Brand positioning

Page 3 — Products & Solutions
- Product ecosystem breakdown
- Flagship product families
- Technology advantages
- Use-case positioning
- Differentiation vs competitors

Page 4 — Innovation, Technology & Credibility
- R&D strengths
- Engineering excellence
- Awards and certifications
- Partnerships and ecosystem
- Trust indicators

Page 5 — Market Impact & Call to Action
- Industry impact
- Customer value narrative
- Future outlook
- Strong CTA section
- Contact section (use scraped data if available)

ENRICHMENT INSTRUCTIONS:

• Expand beyond scraped data using well-known public knowledge about the company  
• Maintain factual safety  
• Add professional marketing depth  
• Add enterprise positioning language  
• Make the brochure feel premium and complete  

TONE:

• Premium  
• Confident  
• Corporate  
• Persuasive but factual  

OUTPUT:

Return ONLY the formatted brochure content.
Do not include explanations.

You are an expert corporate brochure strategist.

Create a PREMIUM 5-page corporate brochure in STRICT JSON format.


SCHEMA:

{{
  "company": "{company_name}",
  "website": "{company_url}",
  "tagline": "short premium tagline",
  "sections": [
    {{
      "type": "cover",
      "headline": "...",
      "sub": "...",
      "tag": "..."
    }},
    {{
      "type": "text",
      "label": "Company Overview",
      "title": "...",
      "content": ["paragraph1", "paragraph2"]
    }},
    {{
      "type": "cards",
      "label": "Products & Solutions",
      "title": "...",
      "items": [
        {{"name": "...", "body": "...", "tag": "..."}}
      ]
    }},
    {{
      "type": "awards",
      "label": "Innovation & Credibility",
      "title": "...",
      "items": [
        {{"title": "...", "year": "...", "note": "..."}}
      ]
    }},
    {{
      "type": "cta",
      "heading": "...",
      "body": "...",
      "action": "..."
    }},
    {{
      "type": "contact",
      "items": {{
        "Website": "{company_url}"
      }}
    }}
  ]
}}

COMPANY DATA:

{scraped_text}

        """

        print("STEP 2: AI generating...")

        ai_data = generate_brochure_content(prompt)
        print("AI RAW OUTPUT:", ai_data[:500])

        def clean_ai_json(text: str) -> str:
          text = text.strip()

          # remove ```json ... ``` wrapper
          if text.startswith("```"):
              text = text.split("```")[1]  # remove first fence
              if text.startswith("json"):
                  text = text[4:]
              text = text.rsplit("```", 1)[0]

          return text.strip()


        cleaned = clean_ai_json(ai_data)

        try:
            brochure_json = json.loads(cleaned)
        except Exception as e:
            print("❌ JSON PARSE FAILED:", e)
            print("RAW AI OUTPUT:", ai_data[:1000])
            raise HTTPException(status_code=500, detail="Invalid AI JSON")
        print("STEP 3: generating PDF...")

        generate_pdf(
            brochure=brochure_json,
            output_path=pdf_file
        )

        if not os.path.exists(pdf_file):
            raise HTTPException(status_code=500, detail="PDF not created")

        print("STEP 4: returning file...")

        return FileResponse(
            path=pdf_file,
            media_type="application/pdf",
            filename=pdf_file,
        )

    except Exception as e:
        print("🔥 BACKEND ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

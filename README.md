🚀 BrochAI — AI-Powered Corporate Brochure Generator
BrochAI is an intelligent web application that automatically generates premium, investor-grade corporate brochures from any company website.

Simply provide a company name and URL — BrochAI will:

🔎 Scrape structured website data
🧠 Enrich content using AI
🎨 Generate a high-end multi-page brochure
📄 Export a professionally formatted PDF
Built for marketers, agencies, founders, and sales teams who want instant, high-quality marketing collateral.

✨ Features
✅ Website data scraping ✅ AI-powered content enrichment ✅ Fortune-500 style brochure copy ✅ Multi-page structured output ✅ Automated PDF generation ✅ Modern React frontend ✅ FastAPI backend ✅ Production-ready architecture

🧠 How It Works
User enters company name + website URL
Scraper extracts key business data
AI expands and structures the content
PDF engine generates a styled brochure
User downloads the final brochure
🏗️ Tech Stack
Frontend

React (Vite)
Modern JavaScript
Responsive UI
Backend

FastAPI
Python
BeautifulSoup (scraping)
ReportLab (PDF generation)
OpenAI-compatible API
📁 Project Structure
BrochAI/
│
├── main.py # FastAPI server
├── ai_services.py # AI content generation
├── scrape.py # Website scraper
├── dynamic_pdf_generator.py # PDF builder
│
├── src/ # React frontend
├── public/
├── index.html
│
├── requirements.txt
├── package.json
└── vite.config.js
⚙️ Local Setup
1️⃣ Clone the repository
git clone https://github.com/Md-Asifai/BrochAi.git
cd BrochAi
2️⃣ Backend Setup
Create virtual environment:

python -m venv venv
Activate:

Linux / Mac

source venv/bin/activate
Windows

venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Create .env file:

GOOGLE_API_KEY=your_api_key_here
Run backend:

uvicorn main:app --reload
3️⃣ Frontend Setup
Install dependencies:

npm install
Run frontend:

npm run dev
🌐 Deployment (Free)
Backend (Recommended)
Render (Free tier)
Start command

uvicorn main:app --host 0.0.0.0 --port $PORT
Frontend (Recommended)
Netlify or Vercel
Build command

npm run build
Publish directory

dist
🔐 Environment Variables
Variable Description
GOOGLE_API_KEY AI provider API key
⚠️ Never commit your .env file.

📸 Use Cases
Marketing agencies
SaaS founders
Sales teams
Startup pitch preparation
Automated lead collateral
Business analysts
🚧 Current Limitations
Works best on well-structured websites
Very heavy websites may take longer to process
AI output quality depends on available website data
🛣️ Roadmap
Advanced brochure themes
Brand color extraction
Logo auto-detection
Multi-language support
Bulk brochure generation
SaaS dashboard
🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

⭐ Support
If you find this project useful, consider giving it a star ⭐ on GitHub — it helps the project grow.

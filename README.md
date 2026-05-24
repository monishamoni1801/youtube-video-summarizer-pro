# 🎥 YouTube Video Summarizer Pro

An AI-powered YouTube video summarizer and notes generator built using Streamlit and Google Gemini AI.  
This application extracts transcripts from YouTube videos and generates:

- 📝 Easy-to-understand summaries
- 📚 Detailed study notes
- 📄 Downloadable PDF notes
- 📋 Text file exports

---

# 🚀 Features

✅ YouTube transcript extraction  
✅ AI-generated summaries using Gemini AI  
✅ Beginner-friendly bullet point summaries  
✅ Detailed structured notes  
✅ PDF download support  
✅ Text file download support  
✅ Video thumbnail preview  
✅ Transcript statistics and analytics  
✅ Clean and responsive Streamlit UI  

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- Python

## AI Model
- Google Gemini AI (`gemini-2.5-flash`)

## Libraries Used
- youtube_transcript_api
- google-generativeai
- python-dotenv
- fpdf
- streamlit

---

# 📂 Project Structure

```bash
youtube-video-summarizer-pro/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore

---

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/monishamoni1801/youtube-video-summarizer-pro.git
2️⃣ Navigate to the Project Folder
cd youtube-video-summarizer-pro
3️⃣ Install Required Packages
pip install -r requirements.txt
🔑 Setup Environment Variables

Create a .env file in the root directory.

Add your Google Gemini API key:
GOOGLE_API_KEY=your_api_key_here

Get your Gemini API key from:
https://ai.google.dev/

▶️ Run the Application
streamlit run app.py

📌 How It Works
User enters a YouTube video link
The app extracts the transcript using YouTubeTranscriptApi
Transcript is sent to Google Gemini AI
AI generates:
Easy-to-understand summary
Detailed study notes
User can download notes as:
Text file

📸 Application Features
📝 Easy to Understand Summary
Beginner-friendly bullet points
Simple explanations
Quick understanding

📚 Detailed Notes
Comprehensive study material
Organized headings and subheadings
Important concepts and examples

📄 Download Options
PDF generation
Text file export

📊 Statistics Dashboard

The application also provides:

Transcript length
Word count
Generated notes size
Video metadata

🔥 Future Enhancements
Multi-language support
Video audio transcription
Topic-wise summarization
AI chatbot for video Q&A
Dark mode UI
Notes history storage

🧠 AI Concepts Used
Natural Language Processing (NLP)
Prompt Engineering
Transcript Processing
AI-based Text Summarization

👩‍💻 Author: Monisha

📜 License
This project is licensed under the MIT License.

⭐ Support
If you like this project, give it a ⭐ on GitHub.


After creating `README.md`,
run:
git add README.md
git commit -m "Added README file"
git push

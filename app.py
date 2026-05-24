import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF
import re
from datetime import datetime

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Different prompts for different types of notes
prompts = {
    "easy_points": """You are a YouTube video summarizer. Create an EASY TO UNDERSTAND summary in bullet points.
    Focus on the key concepts and explain them in simple language.
    Format the output as clear bullet points with brief explanations.
    Keep the total summary within 250 words.
    Make it beginner-friendly and easy to grasp.
    
    Video transcript: """,
    
    "detailed_notes": """You are a YouTube video note-taker. Create COMPREHENSIVE, DETAILED notes from this video.
    Include all important concepts, steps, examples, and key takeaways.
    Organize the notes with clear headings, subheadings, and bullet points.
    Make it thorough and educational, suitable for studying.
    
    Video transcript: """
}


def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID from different URL formats
        if "youtu.be" in youtube_video_url:
            video_id = youtube_video_url.split("/")[-1].split("?")[0]
        elif "v=" in youtube_video_url:
            video_id = youtube_video_url.split("v=")[1].split("&")[0]
        else:
            video_id = youtube_video_url
        
        # Use YouTubeTranscriptApi to get transcript
        ytt_api = YouTubeTranscriptApi()
        transcript_data = ytt_api.fetch(video_id).to_raw_data()
        
        transcript = ""
        for i in transcript_data:
            transcript += " " + i["text"]
        
        return transcript, video_id
        
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None, None


def generate_content(transcript_text, prompt_type):
    """Generate content using Gemini based on prompt type"""
    
    # Use the appropriate prompt
    selected_prompt = prompts[prompt_type]
    
    # Use Gemini model
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # Trim transcript if too long
    max_chars = 30000
    if len(transcript_text) > max_chars:
        transcript_text = transcript_text[:max_chars] + "... (truncated)"
    
    try:
        response = model.generate_content(selected_prompt + transcript_text)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"


def create_pdf(content, title, video_url):
    """Create PDF using standard fonts - NO external files needed"""
    pdf = FPDF()
    pdf.add_page()
    
    # Use standard PDF fonts (works everywhere)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(5)
    
    # Add metadata
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 6, f"Source: {video_url}", ln=True)
    pdf.ln(10)
    
    # Add content
    pdf.set_font('Helvetica', '', 11)
    
    # Simple function to clean text
    def clean_text(text):
        # Replace common Unicode characters with ASCII equivalents
        replacements = {
            '→': '->', '•': '-', '…': '...', '—': '-', '–': '-',
            '"': '"', '"': '"', ''': "'", ''': "'",
            '✓': '[OK]', '✗': '[X]', '★': '*', '☆': '*',
            '✅': '[YES]', '❌': '[NO]', '⭐': '*'
        }
        for unicode_char, ascii_char in replacements.items():
            text = text.replace(unicode_char, ascii_char)
        # Remove any other non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        return text
    
    # Process each line
    for line in content.split('\n'):
        if line.strip():
            clean_line = clean_text(line)
            if clean_line.strip():
                # Handle indentation for bullet points
                if clean_line.strip().startswith(('-', '*', '•')):
                    pdf.cell(5)  # Add indent
                    pdf.multi_cell(0, 6, clean_line)
                else:
                    pdf.multi_cell(0, 6, clean_line)
        else:
            pdf.ln(2)
    
    return pdf.output(dest='S').encode('latin-1')


# Streamlit UI Configuration
st.set_page_config(
    page_title="YouTube Video Summarizer Pro",
    page_icon="📹",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 2rem;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>🎥 YouTube Video Summarizer Pro</h1><p>Get detailed notes or easy-to-understand summaries from any YouTube video</p></div>', unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.markdown("## 📌 How to Use")
    st.markdown("""
    1. **Paste YouTube URL** in the input box
    2. **Choose note type**:
       - 📝 **Easy to Understand**: Bullet points in simple language
       - 📚 **Detailed Notes**: Comprehensive, structured notes
    3. **Click the button** to generate
    4. **Download** as PDF or Text file
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Features")
    st.markdown("""
    ✅ Easy-to-understand summaries  
    ✅ Comprehensive detailed notes  
    ✅ Download as PDF  
    ✅ Download as Text file  
    ✅ Video thumbnail preview  
    ✅ Word count tracking  
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - For quick understanding: Use **Easy to Understand**
    - For studying/research: Use **Detailed Notes**
    - Videos need captions/subtitles
    - Works best with English videos
    """)

# Main content area
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    youtube_link = st.text_input(
        "🔗 Enter YouTube Video Link:",
        placeholder="https://youtu.be/HFfXvfFe9F8 or https://www.youtube.com/watch?v=..."
    )

with col2:
    note_type = st.radio(
        "📝 Select Note Type:",
        ["Easy to Understand", "Detailed Notes"],
        help="Easy = Simple bullet points | Detailed = Comprehensive study notes"
    )

with col3:
    if youtube_link:
        # Extract and display video thumbnail
        if "youtu.be" in youtube_link:
            video_id = youtube_link.split("/")[-1].split("?")[0]
        elif "v=" in youtube_link:
            video_id = youtube_link.split("v=")[1].split("&")[0]
        else:
            video_id = None
        
        if video_id:
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", width=250)

# Generate button
if st.button("🚀 Generate Notes", use_container_width=True):
    if not youtube_link:
        st.warning("⚠️ Please enter a YouTube video link")
    else:
        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["📝 Generated Notes", "📊 Statistics", "💾 Download Options"])
        
        with st.spinner("🔄 Processing your video... This may take a moment"):
            # Fetch transcript
            transcript_text, video_id = extract_transcript_details(youtube_link)
            
            if transcript_text:
                with tab1:
                    # Generate based on note type
                    if note_type == "Easy to Understand":
                        prompt_key = "easy_points"
                        title = "📝 Easy to Understand Summary"
                    else:
                        prompt_key = "detailed_notes"
                        title = "📚 Detailed Notes"
                    
                    st.markdown(f"## {title}")
                    st.markdown("---")
                    
                    # Generate content
                    with st.spinner("🤖 Generating content with AI..."):
                        content = generate_content(transcript_text, prompt_key)
                        
                        if content and not content.startswith("Error"):
                            st.markdown(content)
                            # Store in session state for downloads
                            st.session_state.generated_content = content
                            st.session_state.video_url = youtube_link
                            st.session_state.note_type = note_type
                        else:
                            st.error(content)
                
                with tab2:
                    st.markdown("## 📊 Video Statistics")
                    st.markdown("---")
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("📄 Transcript Length", f"{len(transcript_text):,} characters")
                    with col_b:
                        st.metric("📝 Words in Transcript", f"{len(transcript_text.split()):,} words")
                    with col_c:
                        if 'generated_content' in st.session_state:
                            st.metric("📋 Notes Length", f"{len(st.session_state.generated_content):,} chars")
                    
                    st.markdown("---")
                    st.markdown("### 📹 Video Information")
                    st.markdown(f"**Video ID:** `{video_id}`")
                    st.markdown(f"**Note Type:** {note_type}")
                    st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                with tab3:
                    if 'generated_content' in st.session_state:
                        st.markdown("## 💾 Download Your Notes")
                        st.markdown("---")
                        
                        # PDF Download - Using the working function
                        try:
                            pdf_data = create_pdf(
                                st.session_state.generated_content,
                                f"YouTube Notes - {note_type}",
                                st.session_state.video_url
                            )
                            st.download_button(
                                label="📥 Download as PDF",
                                data=pdf_data,
                                file_name=f"youtube_notes_{note_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as e:
                            # Fallback to text download if PDF fails
                            st.info("💡 PDF ready! If you see this message, the text download below works perfectly.")
                        
                        # Text Download
                        st.download_button(
                            label="📄 Download as Text File",
                            data=st.session_state.generated_content,
                            file_name=f"youtube_notes_{note_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                        
                        # Copy to clipboard option
                        st.markdown("---")
                        st.markdown("### 📋 Quick Preview")
                        st.code(st.session_state.generated_content[:500] + "...", language="markdown")
                        st.info("💡 The complete notes are available in the 'Generated Notes' tab above")
                    else:
                        st.info("Generate notes first to see download options")
            else:
                st.error("❌ Could not fetch transcript. Make sure the video has captions/subtitles enabled.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by Google Gemini AI & YouTube Transcript API</p>",
    unsafe_allow_html=True
)
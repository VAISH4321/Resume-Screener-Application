import streamlit as st
import docx2txt
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu 
# Set page config
st.set_page_config(page_title="Resume Screener", layout="wide")

# Custom CSS for background and text color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #A8E6CF;  /* Light mint color */
        color: black !important; /* Enforce black text */
    }
    div, span, p, label, input {
        color: black !important; /* Override white color for all text elements */
    }
    h1, h2, h3, h4, h5, h6 {
        color: black !important; /* Ensure headers are black */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation bar
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Services"],
        icons=["house", "gear"],
        menu_icon="cast",
        default_index=0,
    )

# Define functions for processing resumes
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file):
    return docx2txt.process(file)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def compute_similarity(resume_text, job_desc):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc])
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity_score

def extract_name_and_email(text):
    name_match = re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", text)
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    name = name_match.group(0) if name_match else "Unknown Name"
    email = email_match.group(0) if email_match else "No Email Found"
    return name, email

def send_email(to_email, name, match_percentage):
    from_email = "resumescreener7@gmail.com"  # Replace with your email
    from_password = "jxyruftvtpseokbf"  # Replace with your email password (use app password for Gmail)
    subject = "Job Application Status"
    body = f"""Hi {name},

    Congratulations! Your resume has been shortlisted with a match percentage of {match_percentage:.2f}%.
    Please await further communication for the next steps.

    Best regards,
    Recruitment Team
    """

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
        return "Email Sent Successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# Main app logic
if selected == "Home":
    st.title("Resume Screener")
    st.subheader("📝 Paste the Job Description Here:")
    job_desc = st.text_area("Enter the Job Description below:", height=150)
    
    st.subheader("📄 Upload Resumes (PDF/DOCX):")
    uploaded_files = st.file_uploader(
        "Select resumes to upload:",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files and job_desc:
        with st.spinner("Processing resumes..."):
            job_desc = preprocess_text(job_desc)
            results = []

            for uploaded_file in uploaded_files:
                file_type = uploaded_file.name.split(".")[-1].lower()
                if file_type == "pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif file_type == "docx":
                    resume_text = extract_text_from_docx(uploaded_file)
                else:
                    st.error(f"Unsupported file type: {uploaded_file.name}")
                    continue

                resume_text_cleaned = preprocess_text(resume_text)
                similarity = compute_similarity(resume_text_cleaned, job_desc)
                name, email = extract_name_and_email(resume_text)

                match_status = "Selected ✅" if similarity > 0.3 else "Not Selected ❌"
                email_status = send_email(email, name, similarity * 100) if match_status == "Selected ✅" and email != "No Email Found" else "Email Not Sent"

                results.append({
                    "Name": name,
                    "Email": email,
                    "Match Percentage": f"{similarity * 100:.2f}%",
                    "Status": match_status,
                    "Email Status": email_status
                })

            if results:
                st.subheader("Results")
                df_results = pd.DataFrame(results)
                st.dataframe(df_results)
            else:
                st.warning("No resumes processed.")
elif selected == "Services":
    st.title("Services")
    st.write("Explore our resume screening services.")

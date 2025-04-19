# Resume Screener Application

## Overview

The **Resume Screener** is a Streamlit-based web application that automates the process of screening resumes against job descriptions. It uses Natural Language Processing (NLP) techniques to evaluate the similarity between resumes and job descriptions, provides a match percentage, and notifies selected candidates via email. The app offers a user-friendly interface with seamless document processing for PDF and DOCX files.

## Features

- **Document Parsing**: Supports PDF and DOCX resume files.
- **Job Description Matching**: Uses TF-IDF Vectorization and Cosine Similarity to assess resume relevance to the job description.
- **Automated Email Notification**: Notifies selected candidates with a personalized email.
- **Data Presentation**: Displays results in an interactive table format for quick evaluation.
- **Streamlit UI Customization**: Includes a sidebar navigation menu for a smooth user experience.

## Technologies Used

- **Streamlit**: For building the interactive user interface.
- **Python Libraries**:
  - `docx2txt`: Extracts text from DOCX files.
  - `pdfplumber`: Extracts text from PDF files.
  - `scikit-learn`: Implements TF-IDF Vectorization and Cosine Similarity.
  - `pandas`: Handles and displays data in tabular format.
- **SMTP (Email Automation)**: Sends personalized emails to shortlisted candidates.
- **Streamlit-Option-Menu**: Enhances navigation with a sidebar menu.

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Streamlit installed (`pip install streamlit`)
- Required libraries (see below)

### Steps to Install

1. Clone this repository:
   ```bash
   git clone https://github.com/YourUsername/ResumeScreener.git
   cd ResumeScreener
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

### Environment Variables

Create an `.env` file in the root directory to store the following credentials:
```plaintext
SMTP_EMAIL=resumescreener7@gmail.com
SMTP_PASSWORD=your_email_password  # Use app-specific password for Gmail
```

## How It Works

1. **Input Job Description**:
   - Paste the job description into the provided text box.
2. **Upload Resumes**:
   - Upload multiple resumes in PDF or DOCX format.
3. **Processing**:
   - The app cleans and preprocesses the text, calculates similarity scores, and determines if a candidate is selected.
4. **Results Table**:
   - Displays the candidate’s name, email, match percentage, and selection status.
5. **Email Notification**:
   - Automatically sends a personalized email to shortlisted candidates with match percentages greater than 30%.

## File Structure

- **app.py**: The main file containing the Streamlit application logic.
- **requirements.txt**: Lists all the Python dependencies for the project.
- **assets/**: Folder for additional assets like images (if any).

## Future Enhancements

- Add support for multilingual resumes.
- Integrate cloud-based storage for processing larger datasets.
- Include advanced NLP techniques for improved matching accuracy.

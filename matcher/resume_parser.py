import PyPDF2


def extract_skills_from_resume(uploaded_file):
    text = ""

    if uploaded_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""

    

    else:
        return []

    # Split the text into simple words or phrases
    words = [w.strip().lower() for w in text.replace('\n', ' ').split() if w.strip()]
    return words

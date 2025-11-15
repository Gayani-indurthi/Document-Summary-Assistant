
# from flask import Flask, request, render_template, jsonify
# import os
# import tempfile
# from werkzeug.utils import secure_filename
# from utils import extract_text
# import google.generativeai as genai
# from dotenv import load_dotenv

# # ✅ Load environment variables (like GEMINI_API_KEY)
# load_dotenv()

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# # ✅ Configure Gemini API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'}), 400

#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)

#             try:
#                 # ✅ Extract text from file
#                 text = extract_text(file_path)

#                 # ✅ Get summary length
#                 length = request.form.get('length', 'medium')

#                 # ✅ Generate summary using Gemini
#                 summary = generate_summary(text, length)

#                 os.remove(file_path)
#                 return jsonify({'summary': summary})

#             except Exception as e:
#                 if os.path.exists(file_path):
#                     os.remove(file_path)
#                 return jsonify({'error': str(e)}), 500

#     return render_template('index.html')


# def generate_summary(text, length='medium'):
#     """Generate a summary using Gemini AI with specified length and highlighted key points."""
#     if not text.strip():
#         return "No text could be extracted from the document."

#     length_instructions = {
#         'short': "Provide a very brief summary in 1-2 sentences.",
#         'medium': "Provide a balanced summary in 3-5 sentences.",
#         'long': "Provide a detailed summary in 5-7 sentences."
#     }

#     prompt = f"{length_instructions[length]} Highlight key points using **bold** text for important keywords or phrases, and use bullet points (-) for main ideas if applicable.\n\nText to summarize:\n\n{text[:5000]}"

#     try:
#         # ✅ Use the correct Gemini model
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         response = model.generate_content(prompt)
#         return response.text.strip() if hasattr(response, 'text') and response.text else "No summary generated."
#     except Exception as e:
#         return f"Error generating summary: {str(e)}"


# if __name__ == '__main__':
#     app.run(debug=True)



import streamlit as st
import os
import tempfile
from utils import extract_text
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Document Summary Assistant")
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
length = st.selectbox("Select summary length", ["short", "medium", "long"])

def generate_summary(text, length='medium'):
    if not text.strip():
        return "No text could be extracted."

    length_instructions = {
        'short': "Provide a 1-2 sentence summary.",
        'medium': "Provide a 3-5 sentence summary.",
        'long': "Provide a detailed 5-7 sentence summary."
    }

    prompt = f"{length_instructions[length]}\n\nText:\n{text[:5000]}"

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

if uploaded_file:
    st.info("Processing file...")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    text = extract_text(tmp_path)
    summary = generate_summary(text, length)

    st.subheader("Summary")
    st.write(summary)

    os.remove(tmp_path)

from flask import Flask, request, render_template, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    html_content = request.form['html_content']
    html_file = request.files['html_file']
    if html_file:
        html_content = html_file.read().decode('utf-8')
    elif not html_content:
        return "No HTML content or file provided."

    pdf_file = 'converted_file.pdf'

    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    paragraphs = []
    for line in html_content.split('\n'):
        paragraphs.append(Paragraph(line, style))
        paragraphs.append(Spacer(1, 12))

    doc.build(paragraphs)
    
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

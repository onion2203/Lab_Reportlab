import os
from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = Flask(__name__)

stream_file = BytesIO()
content = []

def add_paragraph(text, content):
    """ Add paragraph to document content"""
    content.append(Paragraph(text))

def get_document_template(stream_file: BytesIO):
    """ Get SimpleDocTemplate """
    return SimpleDocTemplate(stream_file)

def build_document(document, content, **props):
    """ Build pdf document based on elements added in `content`"""
    document.build(content, **props)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        html_file = request.files['file']
        html_content = html_file.read().decode("utf-8")
        print(html_content)
        add_paragraph(html_content, content)
        build_document(get_document_template(stream_file), content)
        # Return the file as attachment
        stream_file.seek(0)
        open('converted.pdf', 'wb').write(stream_file.getvalue())
        # Get the path to the converted PDF file
        pdf_path = os.path.join(os.getcwd(), 'converted.pdf')
        
        return send_file(pdf_path, as_attachment=True, download_name='converted.pdf')


if __name__ == '__main__':
    app.run(debug=False)
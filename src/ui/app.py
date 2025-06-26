from flask import Flask, request, jsonify, send_file, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # TODO: Parse the DOCX file and return extracted data
        return jsonify({'success': 'File uploaded successfully'}), 200
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/analyze_job_description', methods=['POST'])
def analyze_job_description():
    data = request.json
    job_description = data.get('job_description', '')
    # TODO: Analyze the job description and generate resume sections
    return jsonify({'success': 'Job description analyzed'}), 200


@app.route('/download_resume', methods=['GET'])
def download_resume():
    # TODO: Implement resume download functionality
    return send_file('path_to_final_resume', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True) 
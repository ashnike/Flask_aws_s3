from flask import Flask, render_template, request, redirect, url_for
import os
import boto3

app = Flask(__name__)

# Create an S3 client 
s3_client = boto3.client('s3')

# Get S3 bucket name from environment variable
s3_bucket_name = os.getenv('S3_BUCKET_NAME')

@app.route('/')
def index():
    # Get list of files in S3 bucket
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return render_template('index.html', files=files)
    except Exception as e:
        return f"Error listing files: {str(e)}"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    try:
        s3_client.upload_fileobj(file, s3_bucket_name, file.filename)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error uploading file: {str(e)}"

@app.route('/delete', methods=['POST'])
def delete_file():
    file_name = request.form.get('file_name')
    if not file_name:
        return "No file name provided"

    # Delete file 
    try:
        s3_client.delete_object(Bucket=s3_bucket_name, Key=file_name)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error deleting file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


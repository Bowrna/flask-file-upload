from flask import Flask, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

# UPLOAD_FOLDER = '/Users/msd/DATALAKE'
UPLOAD_FOLDER = '/home/ubuntu'
ALLOWED_EXTENSIONS = ['zip', 'csv']
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ENV = 'earth'

@app.route('/downloads/<user>/<name>')
def download_file(user, name):
    store_path = os.path.join(app.config['UPLOAD_FOLDER'], ENV, user)
    return send_from_directory(store_path, name)


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    print(newpath)
    return newpath


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # Accept file from buffer & persist to the datalake
    # ASAD - what is the format for the data lake?

    """
    The datalake folder looks like this...

    ubuntu@ip-172-31-2-25:~/DATALAKE$ ls
    earth  mars  prod  venus
    ubuntu@ip-172-31-2-25:~/DATALAKE$ pwd
    /home/ubuntu/DATALAKE
    Store in the following format
    /home/ubuntu/DATALAKE/{env}/{user}/
    """
    if request.method == 'POST':
        user = request.form.get('user', 'guest')
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Empty upload')
            return redirect(request.url)
        if file and allowed_file_extensions(file.filename):
            filename = secure_filename(file.filename)
            store_path = os.path.join(app.config['UPLOAD_FOLDER'], ENV, user)
            create_new_folder(store_path)
            file.save(os.path.join(store_path, filename)) 
            print('File saved')          
            return redirect(url_for('download_file', user=user, name=filename))
            # return send_from_directory(app.config["UPLOAD_FOLDER"], name)
        else:
            return {'url': "Check the extension man",
                    'dataset_metdata': None}


def allowed_file_extensions(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
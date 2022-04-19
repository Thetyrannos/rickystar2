from flask import Flask, render_template, render_template_string, make_response, send_file, send_from_directory, url_for, redirect, request, session
import random
import os
import pdfkit
import io            
import pathlib
import zipfile
from urllib.parse import urlparse


app = Flask(__name__)
app.secret_key = os.urandom(16)

rick_uname = 'admin'
rick_pw = 'admin'

local_addr='127.0.0.1'

black_list=['local','spoofed','.1','.0']

url_list=['https://www.youtube.com/embed/uKxyLmbOc0Q',
          'https://www.youtube.com/embed/Oj7TMSwMLf8',
          'https://www.youtube.com/embed/pyDCubgU57g',
          'https://www.youtube.com/embed/LKP-vZvjbh8',
          'https://www.youtube.com/embed/lFsg_sDwlak',
          'https://www.youtube.com/embed/cUczfmQncXU',
          ]  

flag=open('flag.txt').read()

@app.route('/')
def index():
    return 'Due to the high severity vulnerability, I decided to move the dashboard page to another route permanently'

@app.route('/MIFM-3d23d-fdsFM')
def dashboard():    
    if 'authed' not in session:
        username=request.args.get('username')
        password=request.args.get('password')
        if username and password:
            session['authed'] = True
            if username == rick_uname and password == rick_pw and request.remote_addr == local_addr:
                session['rick']=True
            return make_response(redirect(url_for('dashboard')))
        else:
            return render_template('login.html')
        
    
    if 'rick' not in session:
        iframe_url =random.choice(url_list)
        return render_template('guest.html',iframe_url = iframe_url)
    
    return render_template('dashboard.html',flag=flag)

@app.route('/MIFM-3d23d-fdsFM',methods=['POST'])
def dashboard_post():    
    if 'authed' not in session:
        return redirect(url_for('dashboard'))
        
    url = request.form['url']

    if 'www.youtube.com' not in url:
        return "Only allow link from www.youtube.com"

    for val in black_list:
        if val in url:
            return "I don't like this link"

    file=to_pdf(url)

    return send_file(
        io.BytesIO(file),
        mimetype='application/pdf',
        as_attachment=True,
        attachment_filename='preview.pdf')
            

@app.route('/logout')
def logout():
    if 'authed' in session:
        session.pop('authed')
    return redirect(url_for('index'))

@app.route('/.git')
def send_report():
    if not os.path.exists('.git.zip'):
        zip_file('.git','.git.zip'),
    return send_file('.git.zip')
 
def to_pdf(url):
    return pdfkit.from_url(url=url)

def zip_file(path,filename):
    directory = pathlib.Path(path)

    with zipfile.ZipFile(filename, mode="w") as archive:
        for file_path in directory.rglob("*"):
            archive.write(
                file_path,
                arcname=file_path.relative_to(directory)
            )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template, send_file
mapbox_access_token = "pk.eyJ1IjoiaXNwYnMiLCJhIjoiY2poaG5tcG1qMDFqZzM5bnJwZTEwdmV3NCJ9.8v27PGqngZL_uBNrBqXL0A"

import os
import settings

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/haiti')
def about():
    return render_template('haiti.html')

# @app.route('/get-file')
# def get_file():
#     d = '../static/result.pdf'
#     return send_file(d, attachment_filename = 'result.pdf')

@app.route('/get-file')
def get_file():
    d = os.path.join(settings.STATIC_ROOT, 'result.pdf')
    return send_file(d, attachment_filename = 'result.pdf')



if __name__ == '__main__':
    app.run()


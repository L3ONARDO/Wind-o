from flask import Flask, render_template
import plotly.plotly as py
import plotly.graph_objs as graph_objs

mapbox_access_token = "pk.eyJ1IjoiaXNwYnMiLCJhIjoiY2poaG5tcG1qMDFqZzM5bnJwZTEwdmV3NCJ9.8v27PGqngZL_uBNrBqXL0A"

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/haiti')
def about():
    return render_template('haiti.html')


@app.route('/service')
def services():
    return render_template('service.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()


from flask import Flask, render_template
from flask_googlemaps import GoogleMaps


app = Flask(__name__)


GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/service')
def services():
    return render_template('service.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)


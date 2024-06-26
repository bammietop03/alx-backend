#!/usr/bin/env python3
""" A Flask Application"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """ Class that contains all language """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """ Determines the best match with our supported languages"""
    locale_param = request.args.get('locale')

    if locale_param in app.config['LANGUAGES']:
        print(locale_param)
        return locale_param
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """ Home Route"""
    return render_template("4-index.html")


if __name__ == '__main__':
    app.run(debug=True)

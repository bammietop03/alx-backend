#!/usr/bin/env python3
""" A Flask Application"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """ Class that contains all language """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


def get_user(user_id):
    """Get user information based on user ID."""
    return users.get(user_id)


@app.before_request
def before_request():
    """Execute before all other functions."""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.localeselector
def get_locale():
    """ Determines the best match with our supported languages"""
    locale_param = request.args.get('locale')

    if locale_param in app.config['LANGUAGES']:
        print(locale_param)
        return locale_param

    if g.user:
        locale = g.user.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale

    locale = request.headers.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """ Home Route"""
    return render_template("6-index.html")


if __name__ == '__main__':
    app.run(debug=True)

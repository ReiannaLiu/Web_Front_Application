
from flask import Flask, request, render_template, g, redirect, Response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return '<h1> Hello World from about page</h1>'


@app.route('/quotes')
def quotes():
    return '<h1> Life is a journey </h1>'

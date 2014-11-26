from flask import Flask, request, redirect, render_template, url_for, session, flash, abort
from www import app

@app.route("/")
def index():
    return render_template('index.html')


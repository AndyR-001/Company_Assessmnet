print("Content-Type: text/html\n")

import mysql.connector
from flask import Flask, request, redirect, render_template, url_for, session
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    #render_template('Website.html')
    return render_template('Website.html') 


    
#Start Flask application in debug mode   
if __name__ == '__main__':
    app.debug = True
    app.run()

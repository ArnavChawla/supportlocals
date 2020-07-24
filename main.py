import flask
from flask import Flask, render_template, send_file
import requests
from bs4 import BeautifulSoup as soup
import helper
from helper import casedata

app=Flask(__name__)

@app.route('/')
def home():

    data = casedata()

    return render_template('index.html',data=data)
@app.route('/testing')
def testingData():
    list=helper.testing()
    return render_template('testing.html',data={'centerData':list})
@app.route('/stats')
def stats():
    list = helper.fullState()
    return render_template('stats.html',data=list)
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

# Renu Chawla
# 4:38 PM (54 minutes ago)
# to me

# Tracking- breakdown age group if easy
# Follow second wave, as lockdown is lifted in different parts
# Testing for Covid 19, if symptomatic- where , who to contact. Could you break it statewise?
# Testing for immunity by checking antibodies (FDA approved, not sure if it available yet. Mayo is testing it internally)
# FOllow therapy- although it might not be useful for public
# Encourage people who have recovered to consider donating plasma
# Follow vaccine development.

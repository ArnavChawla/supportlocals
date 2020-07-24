import flask
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup as soup
import json
class testingCenter():
    def __init__(self,name,lat,long,phone,address):
        self.name=name
        self.lat = lat
        self.long = long
        self.phone = phone
        self.address = address
class state():
    def __init__(self,name,cases,deaths,source):
        self.name=name
        self.cases=cases
        self.deaths=deaths
        self.source=source
def graph():
    r = requests.get('https://www.cdc.gov/coronavirus/2019-ncov/json/new-cases-chart-data.json')
    data = json.loads(r.text)
    #print(data['data']['columns'])

    x = data[0]
    y = data[1]
    try:
        x.remove(''"4/26/2020"'')
        y.remove(1857238)
    except:
        pass
    del y[:41]
    del x[:41]
    return [x,y]
def ghost():

    r = requests.get('https://blog.support-locals.org/ghost/api/v3/content/posts/?key=&include=tags,authors')
    data= json.loads(r.text)
    return data['posts']
def fullState():
    r = requests.get('https://www.cdc.gov/coronavirus/2019-ncov/json/us-cases-map-data.json')
    full = json.loads(r.text)
    states=[]
    for item in full:
        states.append(state(item['Jurisdiction'],item['Cases Reported'],item['Deaths'],item['URL']))
    r = requests.get("https://www.worldometers.info/coronavirus/")
    bs = soup(r.text,"html.parser")
    #all the basic stats
    active = str(bs.find('div',{'class':"number-table-main"})).split('>')[1].replace(',','')

    cases =bs.find("div",{"class":"maincounter-number"})
    cases = soup(str(cases),"html.parser")
    deaths =bs.findAll("div",{"class":"maincounter-number"})[1]
    deaths = soup(str(deaths),"html.parser")
    recov =bs.findAll("div",{"class":"maincounter-number"})[2]
    recov = soup(str(recov),"html.parser")

    percent = soup(str(bs.find("div",{'id':'nav-tabContent'})),'html.parser')
    data = percent.findAll('td')

    total = int((cases.find("span").text).replace(',',''))
    totalDeaths = int((deaths.find("span").text).replace(',',''))
    totalR = int((recov.find("span").text).replace(',',''))

    # delta = (int((str(data[93]).split('+')[1].split('<')[0]).replace(",",'')))
    # pchange = str(round(100*(float(delta)/total),1))+("%")

    # deltaD = (int((str(data[95]).split('+')[1].split('<')[0]).replace(",",'')))
    # dchange = str(round(100*(float(deltaD)/totalDeaths),1))+("%")


    idea = graph()
    return {'cases':total,'percentChange':'1', 'deaths':totalDeaths, 'deathChange':'1', "recoveries":totalR, "active":active, "x": idea[0], "y": idea[1], 'stats':states}
def testing():
        centerData = json.load(open('testingCenters.json'))
        centerList = []
        for i in range(0,2379):
            centerList.append(testingCenter(centerData['names'][i],centerData['lat'][i],centerData['long'][i],centerData['phones'][i],centerData['address'][i]))
        return centerList
def casedata():
    session = requests.session()
    r = session.get("https://www.worldometers.info/coronavirus/")
    bs = soup(r.text,"html.parser")
    #all the basic stats
    active = str(bs.find('div',{'class':"number-table-main"})).split('>')[1].replace(',','')

    cases =bs.find("div",{"class":"maincounter-number"})
    cases = soup(str(cases),"html.parser")
    deaths =bs.findAll("div",{"class":"maincounter-number"})[1]
    deaths = soup(str(deaths),"html.parser")
    recov =bs.findAll("div",{"class":"maincounter-number"})[2]
    recov = soup(str(recov),"html.parser")

    percent = soup(str(bs.find("div",{'id':'nav-tabContent'})),'html.parser')
    data = percent.findAll('td')

    total = int((cases.find("span").text).replace(',',''))
    totalDeaths = int((deaths.find("span").text).replace(',',''))
    totalR = int((recov.find("span").text).replace(',',''))

    # delta = (int((str(data[93]).split('+')[1].split('<')[0]).replace(",",'')))
    # pchange = str(round(100*(float(delta)/total),1))+("%")
    #
    # deltaD = (int((str(data[95]).split('+')[1].split('<')[0]).replace(",",'')))
    # dchange = str(round(100*(float(deltaD)/totalDeaths),1))+("%")


    idea = graph()
    centerList = testing()
    info = ghost()
    return {'cases':total,'percentChange':'1', 'deaths':totalDeaths, 'deathChange':'1', "recoveries":totalR, "active":active, "x": idea[0], "y": idea[1], 'centerData':centerList, 'blogInfo':info}

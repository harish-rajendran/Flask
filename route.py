from flask import Flask,request
import requests
from flask_cors import CORS, cross_origin
import json

application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

@application.route('/test/signin')
@cross_origin()
def signin():
    url = 'http://localhost:5002/vendor/signin/'
    d = {'vendorid' : 3,'storename' : 'boss','storeid' : '1500','city' : 'Chennai','branch' : 'Boat Club','state' : 'Tamilnadu'}
    head = {'Content-Type' : 'application/json'}
    r=requests.post(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/details')
@cross_origin()
def info():
    url = 'http://localhost:5002/vendor/details/'
    d = {'vendorid' : 1 ,'storeid' : [200, 300] }
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/update')
@cross_origin()
def update():
    url = 'http://localhost:5002/vendor/details/update/'
    d = {'vendorid' : 7 ,'storename' : 'cozi','storeid' : '2912','city' : 'Chennai','branch' : 'Besant Nagar','state' : 'Tamilnadu'}
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/delete')
@cross_origin()
def delete():
    url = 'http://localhost:5002/vendor/details/delete/'
    d = {'vendorid' : 3 ,'storeid' : [900,1500]}
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/downloadcsv')
@cross_origin()
def downloadcsv():
    url = 'http://localhost:5002/vendor/downloadcsv/'
    d = {'vendorid' : 1  }
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text

@application.route('/test/downloadpdf')
@cross_origin()
def downloadpdf():
    url = 'http://localhost:5002/vendor/downloadpdf/'
    d = {'vendorid' : 1  }
    head = {'Content-Type' : 'application/json'}
    r=requests.get(url, data=json.dumps(d), headers=head) 
    return r.text


if __name__ == "__main__":
    application.debug = True
    application.run(host = "0.0.0.0", port = 5004)

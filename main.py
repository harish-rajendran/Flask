from flask import Flask,request
from flask_cors import CORS, cross_origin
import json
import operation


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/vendor/signin/' , methods=['POST'])
@cross_origin()
def signin():
    if request.method == 'POST':
        values = request.get_json()
        result = operation.validate(values)
        if result == True:
            results = operation.check(values)
            if results == True:
                message=operation.insert(values)
                return message
            else:
                return results
        else:
            #message = json.dumps({"status":"NOT OK","message":"Validation failed"})
            abort(400)

@app.route('/vendor/details/')
@cross_origin()
def info():
    data = request.get_json()
    if data['storeid'] == "all":
        result = operation.fetch(data)
        return result
    else:
        result = operation.fetchone(data)
        return result

@app.route('/vendor/details/update/')
@cross_origin()
def edit():
    value = request.get_json()
    result = operation.validate(value)
    if result == True:
        final = operation.update(value)
        return final
    else :
        abort(400)

@app.route('/vendor/details/delete/')
@cross_origin()
def dele():
    values = request.get_json()
    result = operation.delete(values)
    return result

@cross_origin()
@app.route('/vendor/downloadcsv/')
def downloadexcel():
    values = request.get_json()
    result = operation.excelsheet(values)
    return result

@cross_origin()
@app.route('/vendor/downloadpdf/')
def pdf():
    values = request.get_json()
    result = operation.pdf(values)
    if result == True:
        variable = operation.water()
        return variable


if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5002)


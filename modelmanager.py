from flask import Flask,request,redirect,Response
import requests
import json
import sys

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return 'Model Manager is running!'


def try_or(fn, default=None):
    try:
        return fn()
    except:
        return default

@app.route('/predict',methods=['GET','POST'])
def predict(request = request):
    global SITE_NAME
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']

    #Carrega as configurações, a cada chamada
    with open('./config/microservices.json') as json_file:
        microservices_config = json.load(json_file)

    try:
        mymodel = request.args['model']
        mymodel_url = microservices_config["models"][mymodel]['url']
    except:
        raise Exception("O modelo deve ser informado no argumento 'model' e deve ser um modelo válido nas configuracoes (config/microservices.json)")

    json_content = try_or(lambda: request.get_json(), {})

    if request.method=='GET':
        resp = requests.get(url=mymodel_url, json=json_content)
    elif request.method=='POST':
        resp = requests.post(url=mymodel_url, json=json_content)
    else:
        raise Exception("Método não suportado")

    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        args.append('8080')

    print(args)

    app.run(port=args[0], host='0.0.0.0')
    pass
from flask import Flask,request,redirect,Response
import requests
import json
import sys
import datetime
import uuid

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return 'Model Manager is running!'


def try_or(fn, default=None):
    try:
        return fn()
    except:
        return default

def logapp(jsoncontent: dict, sufix: str = None):
    try:
        logpath = f"./Log/{str( uuid.uuid1() )} EXEC {str(sufix)}.log"
        with open(logpath, 'w') as fp:
            json.dump(jsoncontent, fp, indent=2)
    except Exception as err:
        print(err)
        pass

@app.route('/predict',methods=['GET','POST'])
def predict(request = request):
    global SITE_NAME
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    reqtime = datetime.datetime.utcnow()
    logg_track = {"reqtime": str(reqtime),
                  "REMOTE_ADDR": request.environ.get('REMOTE_ADDR'),
                  "input": {"base_url": request.base_url,
                            "method": request.method,
                            "args": request.args,
                            "content": {}},
                  "output": {}}

    #Carrega as configurações, a cada chamada
    with open('./config/microservices.json') as json_file:
        microservices_config = json.load(json_file)

    try:
        mymodel = request.args['model']
        mymodel_url = microservices_config["models"][mymodel]['url']
        logg_track["model"] = mymodel
    except:
        raise Exception("O modelo deve ser informado no argumento 'model' e deve ser um modelo válido nas configuracoes (config/microservices.json)")

    json_content = try_or(lambda: request.get_json(), {})
    logg_track["input"]["content"] = json_content

    if request.method=='GET':
        resp = requests.get(url=mymodel_url, json=json_content)
    elif request.method=='POST':
        resp = requests.post(url=mymodel_url, json=json_content)
    else:
        raise Exception("Método não suportado")

    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    resp_content = json.loads(resp.content)
    logg_track["output"].update({"content": resp_content,
                                 "status_code": resp.status_code,
                                 "headers": headers})
    logapp(jsoncontent=logg_track, sufix=reqtime.strftime("%Y%m%d-%H%M%S.%f"))
    return response



if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        args.append('8080')

    print(args)

    app.run(port=args[0], host='0.0.0.0')
    pass
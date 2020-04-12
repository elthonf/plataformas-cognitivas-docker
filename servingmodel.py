import joblib
import pandas as pd
import json
import numpy as np
from flask import Flask, jsonify, request
import sys

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = NpEncoder
modelo = None

@app.route("/", methods=['GET', 'POST'])
def call_home(request = request):
    print(request.values)
    return "SERVER IS RUNNING! \n" + json.dumps({
        "args": str(sys.argv),
    })

@app.route("/predict", methods=['GET', 'POST'])
def call_predict(request = request):
    print(request.values)

    json_ = request.json
    campos = pd.DataFrame(json_)

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    for col in modelo.independentcols:
        if col not in campos.columns:
            campos[col] = 0
    x = campos[modelo.independentcols]

    prediction = modelo.predict(x)


    ret = {'prediction': list(prediction)}
    if hasattr(modelo, 'predict_proba'):
        predict_proba = modelo.predict_proba(x)
        ret['proba'] = list(predict_proba)

    return app.response_class(response=json.dumps(ret, cls=NpEncoder), mimetype='application/json')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        args.append('models/modelo01.joblib')
    if len(args) < 2:
        args.append('8080')

    print(args)

    modelo = joblib.load(args[0])
    # app.run(port=8080, host='0.0.0.0')
    app.run(port=args[1], host='0.0.0.0')
    pass


from flask import Flask, request, render_template
from keras.models import load_model
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ann = load_model('ann-general-score.h5')

    param1 = request.form['param1']
    param2 = request.form['param2']
    param3 = request.form['param3']
    param4 = request.form['param4']
    param5 = request.form['param5']

    prediction = ann.predict([[float(param1), float(param2), float(param3), float(param4), float(param5)]])

    return render_template('prediction.html', prediction=prediction)

if __name__ == '__main__':
    app.run()

from flask import session,flash
import pandas as pd
import numpy as np 
from flask import Response
import os 
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
import tempfile
import simplejson as j
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
import json
app = Flask(__name__)      

@app.route('/')
def index():
    return render_template('index.html')
    
interpreter = Interpreter.load('./models/nlu/default/restaurantnlu')
@app.route('/nlu_parsing', methods=['POST'])
def transform():
    if request.headers['Content-Type'] == 'application/json':     
        query = request.json.get("utterance")
        results=interpreter.parse(query)
        js = json.dumps(results)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

        
if __name__ == '__main__':
    app.run(debug=True)

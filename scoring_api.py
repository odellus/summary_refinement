#! /usr/bin/env python3

import json
import logging
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from urllib.parse import parse_qs
from rouge import Rouge
import nltk
from nltk.translate.meteor_score import meteor_score

from summary_db import SummaryDB

logging.basicConfig(
    filename='scoring_api.log',
    level=logging.DEBUG
)
logging.debug('This should go to the file!')

db = SummaryDB()

app = Flask(__name__)
CORS(app)
api = Api(app)

rouge = Rouge()

def check_for_wordnet():
    home = os.environ['HOME']
    if not os.path.exists(f'{home}/nltk_data/wordnet'):
        nltk.download('wordnet')

def score_hypothesis(hypothesis, reference):
    rouge_ = rouge.get_scores(hypothesis, reference)[0]['rouge-1']['f']
    meteor_ = meteor_score([hypothesis], reference)
    return rouge_, meteor_

class RougeMeteorApi(Resource):
    '''
    '''
    def post(self):
        '''
        '''
        inputs = request.get_json(force=True)
        updated_summary = parse_qs(inputs['summary'])['summary'].pop()
        article_id = parse_qs(inputs['article_id'])['article_id'].pop().rstrip()
        article_text, hypothesis = db.get_computer_summary(article_id)
        rouge_, meteor_ = score_hypothesis(hypothesis, updated_summary)
        db.update(
            article_id,
            article_text,
            updated_summary,
            rouge_,
            meteor_
        )
        return {'rouge': rouge_, 'meteor': meteor_}

api.add_resource(RougeMeteorApi, '/scoreupdate')
port=5002

if __name__ == '__main__':
    check_for_wordnet()
    app.run(debug=True, port=port)

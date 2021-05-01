#! /usr/bin/env python3

import json
import time
import logging
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from urllib.parse import parse_qs
from rouge import Rouge
from transformers import T5ForConditionalGeneration, T5Tokenizer

from summary_db import SummaryDB

logging.basicConfig(
    filename='summarize_api.log',
    level=logging.DEBUG
)

logging.debug('This should go to the file!')

db = SummaryDB()

app = Flask(__name__)
CORS(app)
api = Api(app)

def load_tokenizer_model():
    '''
    Create a transformers pipeline for question answering inference.
    '''
    msg = ' * Loading model...'
    logging.info(msg)
    model_dir = 'models'
    model_name = 't5-small'
    model_path = f'./{model_dir}/{model_name}'
    msg = f'Model loaded from {model_path}'
    logging.info(msg)
    start = time.time()
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    msg = f' * Model loaded in {time.time()-start} seconds!'
    logging.info(msg)
    return tokenizer, model

def summarize(article):
    input_str = 'summarize: ' + article
    input_ids = tokenizer(input_str, return_tensors='pt').input_ids
    output_ids = model.generate(input_ids)
    output_str = tokenizer.decode(output_ids[0])
    summary = output_str[6:] # Starts with '<pad> '
    return summary

class SummarizeArticleApi(Resource):
    '''
    '''
    def post(self):
        '''
        '''
        inputs = request.get_json(force=True)
        article = parse_qs(inputs['article'])['article'].pop()
        article_id = parse_qs(inputs['article_id'])['article_id'].pop().rstrip()
        summary = summarize(article)
        db.insert(article_id, article, summary)
        logging.info(article)
        logging.info(summary)
        return {'summary': summary}

api.add_resource(SummarizeArticleApi, '/summarizer')
port = 5001

if __name__ == '__main__':
    tokenizer, model = load_tokenizer_model()
    app.run(debug=True, port=port)

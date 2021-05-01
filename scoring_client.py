import requests
import json
from urllib.parse import quote

from summarize_client import summarizer_client

# Prime the pump. We need a computer generated summary for this to work.
summarizer_client()

summary = "Marx was a German philosopher, economist, historian, politican theorist, journalist, socialist, and all around swell guy."
print({'updated_summary': summary})
article_id = '25dgdj27d8'
url = 'http://127.0.0.1:5002/scoreupdate'

def score_update_client(summary, article_id, url=url):
    summary = 'summary=' + quote(summary)
    article_id = 'article_id=' + quote(article_id)
    data = {'summary': summary, 'article_id': article_id}
    body = json.dumps(data)
    result = requests.post(url, body)
    print(result.json())

if __name__ == '__main__':
    score_update_client(summary, article_id)

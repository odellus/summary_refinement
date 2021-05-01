# Summary Scoring API

Just playing around with a template for how one would go about creating a website to summarize text, then allow for updates to those summaries to be stored in a table along with rouge and meteor scores assessing the performance of the automated summaries.

## Install
```bash
python3 -m pip install -r requirements.txt
```
I don't know what else you might be missing.

## Usage  

In one terminal run the summarization API server with
```bash
python3 summarize_api.py
```
Then in another terminal you can run
```bash
python3 scoring_api.py
```
So that you can go to `file:///path/to/summary_scoring_api/index.html` and check out the jQuery front end I put together with these API backends that use Hugging Face, Flask, and SQLite.

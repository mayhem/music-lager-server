#!/usr/bin/env python
    
import urllib2
import json
from flask import Flask, request, render_template

# useful solr queries
# see sorted scrobbles per user: /solr/select?q=user:mayhemchaos&sort=timestamp+desc&wt=json&start=51

SOLR_SERVER = "localhost"
SOLR_PORT   = 8983

STATIC_PATH = "/static"
STATIC_FOLDER = "static"
TEMPLATE_FOLDER = "templates"

app = Flask(__name__,
            static_url_path = STATIC_PATH,
            static_folder = STATIC_FOLDER,
            template_folder = TEMPLATE_FOLDER)

@app.route("/")
def index():
    url = "/solr/select?q=*:*&sort=timestamp+desc&wt=json&rows=100"
    url = "http://%s:%d%s" % (SOLR_SERVER, SOLR_PORT, url)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    docs = data['response']['docs']
    print "before: " , docs
    for doc in docs:
        for k in doc.keys():
            if type(doc[k]) == list:
                doc[k] = doc[k][0]
    print "after: " , docs
    print
    return render_template("index", docs=docs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

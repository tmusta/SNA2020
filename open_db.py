"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import os
import requests
    
## Load configuration
## You should visit https://dev.elsevier.com/ and create your API key that you insert into config.json
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
#client.inst_token = config['insttoken']

if not os.path.exists("db.json"):
    doc_srch = ElsSearch('issn(1944-7973)', 'scopus') ## Downloads all the articles of Water Resource Research
    doc_srch.execute(client, get_all = True)
    print ("doc_srch has", len(doc_srch.results), "results.")

    print(doc_srch.results[0:5])
    with open("db.json", "w") as f:
    
        json.dump(doc_srch.results, f)

        
with open("db.json") as f:
    data = json.load(f)
if not os.path.exists("db_past_5_years.json"):
    odb = []
    for i in data:

        #print(i['prism:volume'])
        if int(i['prism:coverDate'].split("-")[0]) >= 2015:
            odb.append(i)

    with open("db_past_5_years.json", "w") as f:
    
        json.dump(odb, f)
with open("db_past_5_years.json") as f:
    data = json.load(f)
    
print("The database has ",  len(data), "entries")
print()
if not os.path.exists("articles.json"):
    final = {}
    for i in data:
        final[i["prism:doi"]] = {}
        if "dc:title" in i:
            final[i["prism:doi"]]["title"] = i["dc:title"]
        if "prism:volume" in i:
            final[i["prism:doi"]]["volume"] = i["prism:volume"]
        if "citedby-count" in i:
            final[i["prism:doi"]]["citedby"] =  i["citedby-count"]
        if "prism:coverDate" in i:
            final[i["prism:doi"]]["date"] =  i["prism:coverDate"]
    with open("articles.json", "w") as f:
        
        json.dump(final, f)

#print("First entry :",  data[0]) 

with open("articles.json") as f:
    data = json.load(f)
n = 0
for i, j in data.items():
    n += 1
    if n > 5:
        break
    print(i,j)

"""
closed_url = data[0]['prism:url']
open_url = odb[0]['prism:url']
print(closed_url)
print(open_url)

headers = dict()
headers['X-ELS-APIKey'] = config['apikey']
headers['X-ELS-ResourceVersion'] = 'XOCS'
headers['Accept'] = 'application/json'

try:
    article_request = requests.get(closed_url + "?field=authkeywords", headers=headers)
    article_keywords = json.loads(article_request.content.decode("utf-8"))
    closed_keywords = [keyword['$'] for keyword in article_keywords['abstracts-retrieval-response']['authkeywords']['author-keyword']]
except:
    print(article_keywords)
try:
    article_request = requests.get(open_url + "?field=authkeywords", headers=headers)
    article_keywords = json.loads(article_request.content.decode("utf-8"))
    open_keywords = [keyword['$'] for keyword in article_keywords['abstracts-retrieval-response']['authkeywords']['author-keyword']]
except:
    print(article_keywords)
print(closed_keywords)
print(open_keywords)
"""

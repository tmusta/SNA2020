"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import os
    
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
print("The database has ",  len(data), "entries")
print()
print("First entry :",  data[0])

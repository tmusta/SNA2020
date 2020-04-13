from crossref.restful import Works
import json

works = Works()

with open('articles.json') as f:
    data = json.load(f)
authors = {}
n = 0
try:
    for i, j in data.items():
            n += 1
            if "refs" in j:
                continue
            try:
                work = works.doi(i)
            except Exception as e:
                print(e)
                continue

            if not work:
                continue
            print(n, "/", len(data))
            refs = []
            auths = []
            if "reference" in work:
                for r in work["reference"]:
                    if "DOI" in r and r["DOI"] in data:
                        refs.append(r["DOI"])
            if "author" in work:
                for a in work["author"]:
                    insert = {}
                    name = ""
                    if "family" in a:
                        name += a["family"]
                    if "given" in a:    
                        name += "," + a["given"]
                    insert["name"] = name
                    if "affiliation" in a and len(a["affiliation"]):
                        insert["affiliation"] = a["affiliation"][0]["name"]
                    #auths.append({"name":name, "affiliation": a["affiliation"][0]["name"]})
                    auths.append(insert)
                    j["refs"] = refs
                    j["auths"] = auths
                    
except Exception as e:
    print(e)
    pass
with open('articles.json', 'w') as f:
    json.dump(data, f)

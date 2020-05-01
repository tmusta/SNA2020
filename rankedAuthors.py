import json
import os
import matplotlib.pyplot as plt
import numpy as np

with open("db.json") as f:
    data = json.load(f)
print("The database has ",  len(data), "entries")
print()

keylist = list(data.keys())
d = {"author": "name", "publications": 0, "colabs": 0}

authorsList = []
numberPublications = []
colabs = []
institution = []
repeated = 0
for k in keylist:
    if data[k].get('auths'):
        for authors in data[k]['auths']:
            repeated += 1

usaAuthors = 0
chinaAuthors = 0
for k in keylist:
        if data[k].get('auths'):
            for authors in data[k]['auths']:
                if authors['name'] not in authorsList:
                    authorsList.append(authors['name'])
                    institution.append(authors['affiliation'])
                    numberPublications.append(1)
                    colabs.append(len(data[k]['auths']))
                    if authors['affiliation'][-5:] == "China":
                        chinaAuthors += 1
                    elif authors['affiliation'][-3:] == "USA":
                        usaAuthors += 1
                else:
                    index = authorsList.index(authors['name'])
                    numberPublications[index] = numberPublications[index] + 1
                    colabs[index] = len(data[k]['auths']) + colabs[index]

print("Total authors without repetition: ", len(authorsList))
print()

print("China has a total of " + str(chinaAuthors) + " authors")
print("USA has a total of " + str(usaAuthors) + " authors")


rankingAuthors = []
for i in range(len(authorsList)):
    d = {'author': authorsList[i], 'publications': numberPublications[i], 'colabs': colabs[i]/numberPublications[i], 'institution': institution[i]}
    rankingAuthors.append(d)

rankingAuthors = sorted(rankingAuthors, key = lambda i: i['publications'], reverse=True)


histogramAuthors = []
publications = []
colabs = []


for i in range(len(rankingAuthors)):
    histogramAuthors.append(rankingAuthors[i]['author'])
    publications.append(rankingAuthors[i]['publications'])
    colabs.append(rankingAuthors[i]['colabs'])
    i += 1

avgColabs = 0
for c in colabs:
    avgColabs += c

avgColabs = avgColabs / len(colabs)
print ("Average colaborations: " + str(avgColabs))


histogramAuthors = []
publications = []
colabs = []
i = 0
while i < 10:
    histogramAuthors.append(rankingAuthors[i]['author'])
    publications.append(rankingAuthors[i]['publications'])
    colabs.append(rankingAuthors[i]['colabs'])
    i += 1





r1 = np.arange(len(histogramAuthors))

plt.bar(r1, publications, color='#7f6d5f', width=0.25, edgecolor='white', label='publications')
plt.bar(r1, colabs, color='#557f2d', width=0.25, edgecolor='white', label='colabs')


plt.xticks(r1, histogramAuthors, color='orange', rotation=25, fontweight='bold', fontsize='6', horizontalalignment='right')

plt.xlabel('Authors´names', fontweight='bold', color = 'orange', fontsize='7', horizontalalignment='center')
plt.legend()
plt.show()



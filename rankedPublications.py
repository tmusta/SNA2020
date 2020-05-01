import json
import os
import matplotlib.pyplot as plt
import numpy as np


with open("db.json") as f:
    data = json.load(f)

keylist = list(data.keys())
institutions = []
published_articles = []



for k in keylist:
        if data[k].get('auths'):
            for authors in data[k]['auths']:
                if authors['affiliation'] not in institutions:
                    institutions.append(authors['affiliation'])
                    published_articles.append(1)

                else:
                    index = institutions.index(authors['affiliation'])
                    published_articles[index] += 1

print("Institutions without repetition: " + str(len(institutions)))


countries = ['China', 'USA', 'Japan', 'Italy']
countAux = [0, 0, 0, 0]

for i in range(len(institutions)):
    if institutions[i][-5:] == 'China':
        countAux[0] += published_articles[i]
    elif institutions [i][-3:] == 'USA':
        countAux[1] += published_articles[i]
    elif institutions[i][-5:] == 'Japan':
        countAux[2] += published_articles[i]
    elif institutions[i][-5:] == 'Italy':
        countAux[3] += published_articles[i]

for c in range(len(countries)):
    print(countries[c] + " has a total of " + str(countAux[c]) + " articles.")


tuple_institutions = []
for i in range(len(institutions)):
    d = {'name': institutions[i], 'value': published_articles[i]}
    tuple_institutions.append(d)

tuple_institutions = sorted(tuple_institutions, key = lambda i: i['value'], reverse=True)

ranked_institutions = []
num_publications = []
i = 0


while i < 10:
    ranked_institutions.append(tuple_institutions[i]['name'])
    num_publications.append(tuple_institutions[i]['value'])
    i+= 1

avgPublic = 0
for c in published_articles:
    avgPublic += c

avgPublic = avgPublic / len(published_articles)
print ("Average publications: " + str(avgPublic))

r1 = np.arange(len(ranked_institutions))

plt.bar(r1, num_publications, color='#7f6d5f', width=0.25, edgecolor='white', label='publications')



plt.xticks(r1, ranked_institutions, color='orange', rotation=19, fontweight='bold', fontsize='6', horizontalalignment='right')

plt.xlabel('Institutions', fontweight='bold', color = 'orange', fontsize='15', horizontalalignment='center')
plt.legend()
plt.show()
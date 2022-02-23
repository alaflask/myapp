import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_title_from_index(index):
	return dd[dd.index == index]["title"].values[0]

def get_index_from_title(title):
	return dd[dd.title == title]["index"].values[0]
dd = pd.read_csv('companies-17-12-2021.xls')
dd['title']=dd['Organization Name']
dd['index']=dd.index
features=['Industries','Headquarters Location','Full Description']
def combined_features(row):
    try:
        return row['Industries']+" "+ row['Headquarters Location']+" "+row['Full Description']
    except:
        return "Error:", row

for feature in features:
    dd[feature]=dd[feature].fillna('')

dd['combined_features']=dd.apply(combined_features, axis=1)
cv=CountVectorizer()
count_matrix=cv.fit_transform(dd["combined_features"])
cosine_sim=cosine_similarity(count_matrix)



from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Bienvenue à notre nouveau systeme de recommendation basé sur CRUNCHBASE"}


class Companies_similaires(BaseModel):
    content: List = []

@app.post("/companies_similaires/{companyName}")
async def create_item(companyName: str ,companies_similaires: Companies_similaires):
    company_index = get_index_from_title(companyName)
    similar_company = list(enumerate(cosine_sim[company_index]))
    sorted_similar_company = sorted(similar_company, key=lambda x: x[1], reverse=True)
    i = 0
    for x in sorted_similar_company:
        companies_similaires.content.append(get_title_from_index(x[0]))
        i = i + 1
        if i > 15:
             break

    return {"companies_similaires":companies_similaires}


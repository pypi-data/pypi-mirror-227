import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from pydantic import BaseModel
from faker import Faker
import os
import pandas as pd
import json
import random

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')


class textAnonyms(BaseModel):
    originalText: str
    textFormat: str


stop_words = set(stopwords.words('french'))
liste_pays = ["afghanistan", "afrique du sud", "albanie", "algérie", "allemagne", "andorre", "angola", "antigua-et-barbuda", "arabie saoudite", "argentine", "arménie", "aruba", "australie", "autriche", "azerbaïdjan", "bahamas", "bahreïn", "bangladesh", "barbade", "belgique", "belize", "bélarus", "bénin", "bhoutan", "birmanie", "bolivie", "bosnie-herzégovine", "botswana", "brésil", "brunéi", "bulgarie", "burkina faso", "burundi", "cambodge", "cameroun", "canada", "cap-vert", "chili", "chine", "chypre", "colombie", "comores", "corée du nord", "corée du sud", "costa rica", "côte d'ivoire", "croatie", "cuba", "curaçao", "danemark", "djibouti", "dominique", "egypte", "el salvador", "émirats arabes unis", "équateur", "érythrée", "espagne", "estonie", "éthiopie", "fidji", "finlande", "france", "gabon", "gambie", "géorgie", "ghana", "grèce", "grenade", "guatemala", "guinée", "guinée équatoriale", "guinée-bissau", "guyana", "haïti", "honduras", "hongrie", "inde", "indonésie", "irak", "iran", "irlande", "islande", "israël", "italie", "jamaïque", "japon", "jordanie", "kazakhstan", "kenya", "kirghizistan", "kiribati", "kosovo", "koweït", "laos", "lesotho", "lettonie", "liban", "libéria", "libye", "liechtenstein", "lituanie", "luxembourg", "macédoine du nord", "madagascar", "malaisie", "malawi", "maldives", "mali", "malte", "maroc", "marshall", "maurice", "mauritanie", "mexique", "micronésie", "moldavie", "monaco", "mongolie", "monténégro", "mozambique", "namibie", "nauru", "nepal", "nicaragua", "niger", "nigeria", "niue", "norvège", "nouvelle-zélande", "oman", "ouganda", "ouzbékistan", "pakistan", "palaos", "panama", "papouasie nouvelle-guinée", "paraguay", "pays-bas", "pérou", "philippines", "pologne", "portugal", "qatar", "république centrafricaine", "république démocratique du congo", "république dominicaine", "république du congo", "république tchèque", "roumanie", "royaume-uni", "russie", "rwanda", "saint-christophe-et-niévès", "saint-marin", "saint-martin", "saint-vincent-et-les-grenadines", "sainte-lucie", "salomon", "salvador", "samoa", "são tomé-et-principe", "sénégal", "serbie", "seychelles", "sierra leone", "singapour", "slovaquie", "slovénie", "somalie", "soudan", "soudan du sud", "sri lanka", "suède", "suisse", "surinam", "swaziland", "syrie", "tadjikistan", "tanzanie", "tchad", "thaïlande", "timor oriental", "togo", "tonga", "trinité-et-tobago", "tunisie", "turkménistan", "turquie", "tuvalu", "ukraine", "uruguay", "vanuatu", "vatican", "venezuela", "vietnam", "yémen", "zambie", "zimbabwe"]
faker = Faker(["fr_FR"])




def anonymiser_mot(text: textAnonyms ):
    try:
        anonymisedData = pd.read_csv("words.csv", dtype={"original": str, "anonymous": str})

        if(text.originalText == "FM"):
            fakeData = "DAB+"
        elif(text.originalText == "DAB+"):
            fakeData = "FM"
        elif(text.originalText.lower() == "iqoya"):
            fakeData = "codec audio"
        elif(text.textFormat == "PERSON"):

            if(cherche_ville(text.originalText.upper())):
                fakeData = random.choice(["TOULON", "NANTES", "MONTPELLIER", "CHAMBOURCY", "NANTERRE",  "GRENOBLE", "LYON" ])
            elif(cherche_chaine(text.originalText.upper())):
                fakeData = random.choice(["TF1", "M6", "BFMTV"  "FRANCE5", "FRANCE2" ])
            else:
                fakeData = random.choice(["PAUL", "JEAN", "PHILIPPE", "PIERRE", "MARC",  "DAVID", "GUILLAUME" ])
        elif(text.textFormat == "DATE"):
            fakeData = faker.date()
        elif(text.textFormat == "LOCATION"):
            fakeData = faker.address()
        elif(text.textFormat == "NUMBER"):
                if(int(text.originalText) <24):
                    fakeData = faker.numerify(text='#')
                else:
                    fakeData = str(faker.random_int(min=0, max=(int(text.originalText) - 1)))
        elif(text.textFormat == "COUNTRY"):
            fakeData = faker.country()
        elif(text.textFormat == "ORGANIZATION"):
            fakeData = random.choice([ "ORANGE", "SAFRAN", "BOUYGUES", "FREE" ])



        while any(anonymisedData["anonymous"] == fakeData):
            fakeData = faker.first_name()

        anonymisedData = pd.concat([anonymisedData, pd.DataFrame([[text.originalText, fakeData]], columns=["original", "anonymous"])])
        anonymisedData.to_csv("words.csv", index=False)

        return fakeData
    except Exception as e:
        return text.originalText


def cherche_chaine(chaine):
    chaine = chaine.upper()

    data  = ["C8","CNEWS","TF1","M6","CSTAR","BFM","F5"]
    for item in data:
        if    item in chaine  :
            return True
            break

    return False


def cherche_ville(ville):
    ville = ville.upper()

    with open('villes.json', 'r') as json_file:
        data = json.load(json_file)
    for item in data:
        if  ville in item["Nom_commune"]  :
            return True
            break

    return False

def desanonymiser_mot(anonymised_name):
    anonymisedData = pd.read_csv("words.csv", dtype={"original": str, "anonymous": str})
    if not anonymisedData.empty:
        originalData = anonymisedData[anonymisedData["anonymous"] == anonymised_name]["original"]
        if not originalData.empty:
            return originalData.iloc[0]
    return None

def initialiser():
    csv_file_path = "words.csv"

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    empty_dataframe = pd.DataFrame(columns=["original", "anonymous"])

    empty_dataframe.to_csv(csv_file_path, index=False)




def anonymiser_paragraphe(paragraphe):

    phrase = paragraphe
    phrase = phrase.replace(".", ". ")
    phrase = phrase.replace(",", ", ")
    phrase = phrase.replace("0H", "0 H")
    phrase = phrase.replace("1H", "1 H")
    phrase = phrase.replace("2H", "2 H")
    phrase = phrase.replace("3H", "3 H")
    phrase = phrase.replace("4H", "4 H")
    phrase = phrase.replace("5H", "5 H")
    phrase = phrase.replace("6H", "6 H")
    phrase = phrase.replace("7H", "7 H")
    phrase = phrase.replace("8H", "8 H")
    phrase = phrase.replace("9H", "9 H")
    phrase = phrase.replace("0F", "0 F ")
    phrase = phrase.replace("1F", "1 F ")
    phrase = phrase.replace("2F", "2 F ")
    phrase = phrase.replace("3F", "3 F ")
    phrase = phrase.replace("4F", "4 F ")
    phrase = phrase.replace("5F", "5 F ")
    phrase = phrase.replace("6F", "6 F ")
    phrase = phrase.replace("7F", "7 F ")
    phrase = phrase.replace("8F", "8 F ")
    phrase = phrase.replace("9F", "9 F ")

    tokens = word_tokenize(phrase, language="french")
    tags = pos_tag(tokens )
    entites_nommees = []

    stop_words = set(stopwords.words('french'))
    pronoms_possessifs = ["h","mon", "ma","HF", "mes", "ton", "ta", "tes", "son", "sa", "ses", "notre", "votre", "leur", "leurs","merci","alors","fh", "hf", "intervention","j'ai", "télégéstion", "télégestion","absence","énergie","radio"]
    stop_words.update(pronoms_possessifs)
    index = 0
    for word, tag in tags:
        index=index+1
        if word.lower() in liste_pays:
            entites_nommees.append(("COUNTRY", word))
        elif tag == "NNP" and "DS" in word or "LA" in word :
            entites_nommees.append(("NUMBER", word))
        elif tag == "NNP" and word.isupper() and word.lower() not in stop_words and len(word)>1:
            entites_nommees.append(("ORGANIZATION", word))
        elif tag == "NNP" and word.lower() not in stop_words and index>1 and len(word)>1:
            entites_nommees.append(("PERSON", word))
        elif tag == "CD" and "/" in word  :
            entites_nommees.append(("DATE", word))
        elif tag == "CD" and ":" not in word:
            entites_nommees.append(("NUMBER", word))
        elif tag == "NNP" and word.lower() not in stop_words  and index>1 and len(word)>1:
            entites_nommees.append(("LOCATION", word))



    for entity_type, entity_value in entites_nommees:
        text = textAnonyms(originalText=entity_value, textFormat=entity_type)
        paragraphe = paragraphe.replace(entity_value, anonymiser_mot(text))

    paragraphe = paragraphe.replace("-", "/")
    paragraphe = paragraphe.replace(" / ", " - ")
    return paragraphe

def desanonymiser_paragraphe(anonymous_paragraphe):


    anonymisedData = pd.read_csv("words.csv", dtype={"original": str, "anonymous": str})
    for index, row in anonymisedData.iterrows():

        anonymous_paragraphe = anonymous_paragraphe.replace(row["anonymous"],row["original"])
    return anonymous_paragraphe


initialiser()
#text_anonyms = anonymiser_paragraphe("Coupure de la fibre Nouvelle Calédonie - Culver impactant Malakoff via Interxion")
text_anonyms =  anonymiser_paragraphe("J'habite à Chambourcy")
print(text_anonyms)
print(desanonymiser_paragraphe(text_anonyms))



# URL de l'API de l'INSEE pour obtenir la liste des communes


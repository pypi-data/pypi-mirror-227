import nltk #line:1
from nltk .corpus import stopwords #line:2
from nltk .tokenize import word_tokenize #line:3
from nltk .tag import pos_tag #line:4
from pydantic import BaseModel #line:5
from faker import Faker #line:6
import os #line:7
import pandas as pd #line:8
import json #line:9
import random #line:10
nltk .download ('averaged_perceptron_tagger')#line:12
nltk .download ('punkt')#line:13
nltk .download ('stopwords')#line:14
class textAnonyms (BaseModel ):#line:17
    originalText :str #line:18
    textFormat :str #line:19
stop_words =set (stopwords .words ('french'))#line:22
liste_pays =["afghanistan","afrique du sud","albanie","algérie","allemagne","andorre","angola","antigua-et-barbuda","arabie saoudite","argentine","arménie","aruba","australie","autriche","azerbaïdjan","bahamas","bahreïn","bangladesh","barbade","belgique","belize","bélarus","bénin","bhoutan","birmanie","bolivie","bosnie-herzégovine","botswana","brésil","brunéi","bulgarie","burkina faso","burundi","cambodge","cameroun","canada","cap-vert","chili","chine","chypre","colombie","comores","corée du nord","corée du sud","costa rica","côte d'ivoire","croatie","cuba","curaçao","danemark","djibouti","dominique","egypte","el salvador","émirats arabes unis","équateur","érythrée","espagne","estonie","éthiopie","fidji","finlande","france","gabon","gambie","géorgie","ghana","grèce","grenade","guatemala","guinée","guinée équatoriale","guinée-bissau","guyana","haïti","honduras","hongrie","inde","indonésie","irak","iran","irlande","islande","israël","italie","jamaïque","japon","jordanie","kazakhstan","kenya","kirghizistan","kiribati","kosovo","koweït","laos","lesotho","lettonie","liban","libéria","libye","liechtenstein","lituanie","luxembourg","macédoine du nord","madagascar","malaisie","malawi","maldives","mali","malte","maroc","marshall","maurice","mauritanie","mexique","micronésie","moldavie","monaco","mongolie","monténégro","mozambique","namibie","nauru","nepal","nicaragua","niger","nigeria","niue","norvège","nouvelle-zélande","oman","ouganda","ouzbékistan","pakistan","palaos","panama","papouasie nouvelle-guinée","paraguay","pays-bas","pérou","philippines","pologne","portugal","qatar","république centrafricaine","république démocratique du congo","république dominicaine","république du congo","république tchèque","roumanie","royaume-uni","russie","rwanda","saint-christophe-et-niévès","saint-marin","saint-martin","saint-vincent-et-les-grenadines","sainte-lucie","salomon","salvador","samoa","são tomé-et-principe","sénégal","serbie","seychelles","sierra leone","singapour","slovaquie","slovénie","somalie","soudan","soudan du sud","sri lanka","suède","suisse","surinam","swaziland","syrie","tadjikistan","tanzanie","tchad","thaïlande","timor oriental","togo","tonga","trinité-et-tobago","tunisie","turkménistan","turquie","tuvalu","ukraine","uruguay","vanuatu","vatican","venezuela","vietnam","yémen","zambie","zimbabwe"]#line:48
faker =Faker (["fr_FR"])#line:49
def anonymiser_mot (O00O0O00O00O0OO0O :textAnonyms ):#line:52
    try :#line:53
        OO00O000OOO0OO00O =pd .read_csv ("words.csv",dtype ={"original":str ,"anonymous":str })#line:54
        if (O00O0O00O00O0OO0O .originalText =="FM"):#line:56
            O00000O00O0O00OOO ="DAB+"#line:57
        elif (O00O0O00O00O0OO0O .originalText =="DAB+"):#line:58
            O00000O00O0O00OOO ="FM"#line:59
        elif (O00O0O00O00O0OO0O .originalText .lower ()=="iqoya"):#line:60
            O00000O00O0O00OOO ="codec audio"#line:61
        elif (O00O0O00O00O0OO0O .textFormat =="PERSON"):#line:62
            if (cherche_ville (O00O0O00O00O0OO0O .originalText .upper ())):#line:64
                O00000O00O0O00OOO =random .choice (["TOULON","NANTES","MONTPELLIER","CHAMBOURCY","NANTERRE","GRENOBLE","LYON"])#line:66
            elif (cherche_chaine (O00O0O00O00O0OO0O .originalText .upper ())):#line:67
                O00000O00O0O00OOO =random .choice (["TF1","M6","BFMTV" "FRANCE5","FRANCE2"])#line:68
            else :#line:69
                O00000O00O0O00OOO =random .choice (["PAUL","JEAN","PHILIPPE","PIERRE","MARC","DAVID","GUILLAUME"])#line:70
        elif (O00O0O00O00O0OO0O .textFormat =="DATE"):#line:71
            O00000O00O0O00OOO =faker .date ()#line:72
        elif (O00O0O00O00O0OO0O .textFormat =="LOCATION"):#line:73
            O00000O00O0O00OOO =faker .address ()#line:74
        elif (O00O0O00O00O0OO0O .textFormat =="NUMBER"):#line:75
            if (int (O00O0O00O00O0OO0O .originalText )<24 ):#line:76
                O00000O00O0O00OOO =faker .numerify (text ='#')#line:77
            else :#line:78
                O00000O00O0O00OOO =str (faker .random_int (min =0 ,max =(int (O00O0O00O00O0OO0O .originalText )-1 )))#line:79
        elif (O00O0O00O00O0OO0O .textFormat =="COUNTRY"):#line:80
            O00000O00O0O00OOO =faker .country ()#line:81
        elif (O00O0O00O00O0OO0O .textFormat =="ORGANIZATION"):#line:82
            O00000O00O0O00OOO =random .choice (["ORANGE","SAFRAN","BOUYGUES","FREE"])#line:83
        while any (OO00O000OOO0OO00O ["anonymous"]==O00000O00O0O00OOO ):#line:85
            O00000O00O0O00OOO =faker .first_name ()#line:86
        OO00O000OOO0OO00O =pd .concat ([OO00O000OOO0OO00O ,pd .DataFrame ([[O00O0O00O00O0OO0O .originalText ,O00000O00O0O00OOO ]],columns =["original","anonymous"])])#line:89
        OO00O000OOO0OO00O .to_csv ("words.csv",index =False )#line:90
        return O00000O00O0O00OOO #line:92
    except Exception as OO000O0O000O00000 :#line:93
        return O00O0O00O00O0OO0O .originalText #line:94
def cherche_chaine (OOO0OO000O0O000O0 ):#line:97
    OOO0OO000O0O000O0 =OOO0OO000O0O000O0 .upper ()#line:98
    OOO00O0O00OOO0OO0 =["C8","CNEWS","TF1","M6","CSTAR","BFM","F5"]#line:100
    for OO0000OO0O000O000 in OOO00O0O00OOO0OO0 :#line:101
        if OO0000OO0O000O000 in OOO0OO000O0O000O0 :#line:102
            return True #line:103
            break #line:104
    return False #line:106
def cherche_ville (O0OOO0O0O000O000O ):#line:109
    O0OOO0O0O000O000O =O0OOO0O0O000O000O .upper ()#line:110
    with open ('villes.json','r')as OOOOO00OO0O0O0O00 :#line:112
        O000O000OO0000O00 =json .load (OOOOO00OO0O0O0O00 )#line:113
    for O000OO0000OOO0O00 in O000O000OO0000O00 :#line:114
        if O0OOO0O0O000O000O in O000OO0000OOO0O00 ["Nom_commune"]:#line:115
            return True #line:116
            break #line:117
    return False #line:119
def desanonymiser_mot (OO0O0O0O0OOOOOOOO ):#line:122
    OOO000O00O000O0O0 =pd .read_csv ("words.csv",dtype ={"original":str ,"anonymous":str })#line:123
    if not OOO000O00O000O0O0 .empty :#line:124
        OO0000O0000O00O00 =OOO000O00O000O0O0 [OOO000O00O000O0O0 ["anonymous"]==OO0O0O0O0OOOOOOOO ]["original"]#line:125
        if not OO0000O0000O00O00 .empty :#line:126
            return OO0000O0000O00O00 .iloc [0 ]#line:127
    return None #line:128
def initialiser ():#line:131
    O0O0OO0O00OO00O00 ="words.csv"#line:132
    if os .path .exists (O0O0OO0O00OO00O00 ):#line:134
        os .remove (O0O0OO0O00OO00O00 )#line:135
    O0OO00O00O00000O0 =pd .DataFrame (columns =["original","anonymous"])#line:137
    O0OO00O00O00000O0 .to_csv (O0O0OO0O00OO00O00 ,index =False )#line:139
def anonymiser_paragraphe (OOO0O0OO0OO000O0O ):#line:142
    O0OOO00O000OOO0OO =OOO0O0OO0OO000O0O #line:143
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace (".",". ")#line:144
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace (",",", ")#line:145
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("0H","0 H")#line:146
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("1H","1 H")#line:147
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("2H","2 H")#line:148
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("3H","3 H")#line:149
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("4H","4 H")#line:150
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("5H","5 H")#line:151
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("6H","6 H")#line:152
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("7H","7 H")#line:153
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("8H","8 H")#line:154
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("9H","9 H")#line:155
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("0F","0 F ")#line:156
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("1F","1 F ")#line:157
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("2F","2 F ")#line:158
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("3F","3 F ")#line:159
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("4F","4 F ")#line:160
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("5F","5 F ")#line:161
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("6F","6 F ")#line:162
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("7F","7 F ")#line:163
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("8F","8 F ")#line:164
    O0OOO00O000OOO0OO =O0OOO00O000OOO0OO .replace ("9F","9 F ")#line:165
    O00O000000OO0OO0O =word_tokenize (O0OOO00O000OOO0OO ,language ="french")#line:167
    OO000O0OO00O00O0O =pos_tag (O00O000000OO0OO0O )#line:168
    O0O0O000OOO000OO0 =[]#line:169
    OO0OOOOO0O00OO0O0 =set (stopwords .words ('french'))#line:171
    OOOO0OO000O0OO0O0 =["h","mon","ma","HF","mes","ton","ta","tes","son","sa","ses","notre","votre","leur","leurs","merci","alors","fh","hf","intervention","j'ai","télégéstion","télégestion","absence","énergie","radio"]#line:174
    OO0OOOOO0O00OO0O0 .update (OOOO0OO000O0OO0O0 )#line:175
    O0O000O0O000OO0OO =0 #line:176
    for OOOO000O000OOOO00 ,OOO0OO00O0OOO00O0 in OO000O0OO00O00O0O :#line:177
        O0O000O0O000OO0OO =O0O000O0O000OO0OO +1 #line:178
        if OOOO000O000OOOO00 .lower ()in liste_pays :#line:179
            O0O0O000OOO000OO0 .append (("COUNTRY",OOOO000O000OOOO00 ))#line:180
        elif OOO0OO00O0OOO00O0 =="NNP"and "DS"in OOOO000O000OOOO00 or "LA"in OOOO000O000OOOO00 :#line:181
            O0O0O000OOO000OO0 .append (("NUMBER",OOOO000O000OOOO00 ))#line:182
        elif OOO0OO00O0OOO00O0 =="NNP"and OOOO000O000OOOO00 .isupper ()and OOOO000O000OOOO00 .lower ()not in OO0OOOOO0O00OO0O0 and len (OOOO000O000OOOO00 )>1 :#line:183
            O0O0O000OOO000OO0 .append (("ORGANIZATION",OOOO000O000OOOO00 ))#line:184
        elif OOO0OO00O0OOO00O0 =="NNP"and OOOO000O000OOOO00 .lower ()not in OO0OOOOO0O00OO0O0 and O0O000O0O000OO0OO >1 and len (OOOO000O000OOOO00 )>1 :#line:185
            O0O0O000OOO000OO0 .append (("PERSON",OOOO000O000OOOO00 ))#line:186
        elif OOO0OO00O0OOO00O0 =="CD"and "/"in OOOO000O000OOOO00 :#line:187
            O0O0O000OOO000OO0 .append (("DATE",OOOO000O000OOOO00 ))#line:188
        elif OOO0OO00O0OOO00O0 =="CD"and ":"not in OOOO000O000OOOO00 :#line:189
            O0O0O000OOO000OO0 .append (("NUMBER",OOOO000O000OOOO00 ))#line:190
        elif OOO0OO00O0OOO00O0 =="NNP"and OOOO000O000OOOO00 .lower ()not in OO0OOOOO0O00OO0O0 and O0O000O0O000OO0OO >1 and len (OOOO000O000OOOO00 )>1 :#line:191
            O0O0O000OOO000OO0 .append (("LOCATION",OOOO000O000OOOO00 ))#line:192
    for O000OOOO000O00OO0 ,O0OOOOO0O00O00O0O in O0O0O000OOO000OO0 :#line:194
        OO0000OOO00OOO0O0 =textAnonyms (originalText =O0OOOOO0O00O00O0O ,textFormat =O000OOOO000O00OO0 )#line:195
        OOO0O0OO0OO000O0O =OOO0O0OO0OO000O0O .replace (O0OOOOO0O00O00O0O ,anonymiser_mot (OO0000OOO00OOO0O0 ))#line:196
    OOO0O0OO0OO000O0O =OOO0O0OO0OO000O0O .replace ("-","/")#line:198
    OOO0O0OO0OO000O0O =OOO0O0OO0OO000O0O .replace (" / "," - ")#line:199
    return OOO0O0OO0OO000O0O #line:200
def desanonymiser_paragraphe (OO0000O00O000OOO0 ):#line:203
    O0O00O000OOO0OO00 =pd .read_csv ("words.csv",dtype ={"original":str ,"anonymous":str })#line:204
    for OOO000OO0000O00OO ,O000000000OOOO0OO in O0O00O000OOO0OO00 .iterrows ():#line:205
        OO0000O00O000OOO0 =OO0000O00O000OOO0 .replace (O000000000OOOO0OO ["anonymous"],O000000000OOOO0OO ["original"])#line:206
    return OO0000O00O000OOO0 #line:207

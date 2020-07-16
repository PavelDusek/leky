import glob
import pdftotext
import pandas as pd
import re

getName = re.compile("název přípravku(.+)kvalitativní a kvantitativní složení", re.IGNORECASE | re.DOTALL | re.UNICODE )
getForm = re.compile("léková forma(.+)klinické údaje", re.IGNORECASE | re.DOTALL | re.UNICODE )
garbage = re.compile(" {2,}|2\.$|4\.$")

names, forms = [], []

def extractData( pdf ):
    try:
        text = pdf[0] #first page
        name = getName.findall(text)[0]
        form = getForm.findall(text)[0]
        name = name.strip()
        form = form.strip()
        name = garbage.sub("", name.strip())
        form = garbage.sub("", form.strip())
        name = name.strip()
        form = form.strip()
        return name, form
    except Exception:
        text = pdf[1] #second page
        name = getName.findall(text)[0]
        form = getForm.findall(text)[0]
        name = name.strip()
        form = form.strip()
        name = garbage.sub("", name.strip())
        form = garbage.sub("", form.strip())
        name = name.strip()
        form = form.strip()
        return name, form

for file in glob.glob("spc/*.pdf"):
    try:
        with open(file, "rb") as f:
            pdf = pdftotext.PDF(f)
        name, form = extractData(pdf)
        names.append(name)
        forms.append(form)
    except Exception: pass

df = pd.DataFrame( {'names': names, 'forms': forms} )

puliciRyha = re.compile( "půl[ií]cí\s+rýh", re.UNICODE )
def isPuliciRyha( popis ):
    if puliciRyha.findall(popis):
        return True
    else:
        return False
df['pulici_ryha'] = df['forms'].apply(isPuliciRyha)


def getLekovaForma(popis):
    forma = popis.splitlines()[0].replace(".","")
    return forma.strip().lower()
df['lekova_forma'] = df['forms'].apply(getLekovaForma)

    
barvy = re.compile( "(červen|oranž|žlut|nažloutl|zelen|modr|růžov|lososov|broskvov|krémov|slonov|fialov|bíl|béžov|hněd|čern|bezbarv)\w*\W", re.UNICODE | re.IGNORECASE )
def getBarvy(popis):
    f = barvy.finditer(popis)
    if f:
        b = [ m.group().replace(",","").strip().lower() for m in f ]
        return ", ".join(b)
    else:
        print(popis)
        print()
        return None
df['barva'] = df['forms'].apply(getBarvy)

tvary = re.compile( "(kulat|ploch|podlouhl|tobol|okrouh|srdčitého tvaru|ováln|cylindrick|eliptick|protáhlého tvar|čtyřlíst|osmiúhel|gel|roztok|číp[ek]|krém|zkosen|torpédovit|vypukl)\w*\W", re.UNICODE | re.IGNORECASE )
def getTvar(popis):
    s = tvary.search( popis )
    if s:
        return s.group().replace(",", "").strip().lower()
    else:
        print(popis)
        print()
        return None
df['tvar'] = df['forms'].apply(getTvar)



konvexita = re.compile( "(\Wkonvexn|bikonvex|gel|tobol[ek]|roztok|mast)\w*\W", re.UNICODE | re.IGNORECASE )
def getKonvexita(popis):
    s = konvexita.search( popis )
    if s:
        return s.group().replace(",", "").lower().strip()
    else:
        print(popis)
        print()
        return None
df['konvexita'] = df['forms'].apply(getKonvexita)


velikost = re.compile("\d+[\.,]\d+\Wmm|\d+\Wmm")
def getVelikost( popis ):
    f = velikost.findall( popis )
    if f:
        return f
    else:
        print( popis )
        print()
        return None
df['velikost'] = df['forms'].apply(getVelikost)

imprint = re.compile("„(.*?)“|\"(.*?)\"", re.UNICODE | re.DOTALL)
#TODO bez uvozovek
def getImprint( popis ):
    f = imprint.finditer( popis )
    if f:
        i = [ m.group() for m in f ]
        return ", ".join( i )
    else:
        print(popis)
        print()
        return None
df['imprint'] = df['forms'].apply(getImprint)

df.to_csv('forms.csv')
df.to_excel('forms.xlsx')

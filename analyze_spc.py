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
df.to_csv('forms.csv')
df.to_excel('forms.xlsx')

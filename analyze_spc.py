import glob
import pdftotext
import pandas as pd
import re

for file in glob.glob("spc/*.pdf"):
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f)
    text = pdf[0] #first page
    print(text)

# leky
Webscraper that extracts information about drugs from the Czech State Institute for Drug Control website.

## download_spc.py
Downloads PDFs with SPC.

## analyze_spc.py
Extracts text information from the downloaded SPCs.

## windows 10 installation instructions:
Building pdftotext dependency through pip requires visual c++ 14.0 (obtainable at https://visualstudio.microsoft.com/visual-cpp-build-tools/).
Or consider obtaining Windows Subsystem for Linux (Debian, Ubuntu) and install python3 and python3-pip. Afterwards install all pdftotext build dependencies (build-essential libpoppler-cpp-dev pkg-config python-dev) and get all required python libraries listed in requirements.txt through pip3.

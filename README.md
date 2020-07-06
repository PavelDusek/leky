# leky
webscraper that extracts information about drugs from the Czech State Institute for Drug Control website

## download_spc.py
Downloads PDFs with SPC.

## analyze_spc.py
Extracts text information from the downloaded SPCs.

##windows 10 installation instructions:
Building pdftotext dependency through pip requires visual c++ 14.0 (obtainable at https://visualstudio.microsoft.com/visual-cpp-build-tools/). Or consider using Windows Subsystem for Linux (Debian, Ubuntu) with python3 and python3-pip and installing all pdftotext build dependencies (build-essential libpoppler-cpp-dev pkg-config python-dev).

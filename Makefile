DATA_DIR=data


all: download-data
.PHONY: download-data

download-data:
	@rm -rf $(DATA_DIR)
	@mkdir -p $(DATA_DIR)
	@wget -P $(DATA_DIR)/ http://catalogue.datalocale.fr//fr/storage/f/2014-06-20T151409/communes.csv.gz
	@wget -P $(DATA_DIR)/ http://catalogue.datalocale.fr//fr/storage/f/2014-06-20T145640/elections.csv.gz

install:
	pip install -r requirements.txt

webserver:
	python -m SimpleHTTPServer


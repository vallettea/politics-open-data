DATA_DIR=data


all: download-data
.PHONY: download-data

download-data:
	@rm -rf $(DATA_DIR)
	@mkdir -p $(DATA_DIR)
	@wget -P $(DATA_DIR)/ http://catalogue.datalocale.fr//fr/storage/f/2014-06-20T151409/communes.csv.gz
	@wget -P $(DATA_DIR)/ http://catalogue.datalocale.fr//fr/storage/f/2014-06-20T145640/elections.csv.gz

<<<<<<< HEAD
=======
install: getdata
	pip install -r requirements.txt

syncdata:
	s3cmd sync --recursive data s3://public-shared-everybody/politics-open-data/
	
getdata:
	mkdir -p data
	s3cmd get --recursive s3://public-shared-everybody/politics-open-data/data/ data/

webserver:
	python -m SimpleHTTPServer
>>>>>>> a4c34494a2b0ffa3d816e1b9718f9f1aa8e50278

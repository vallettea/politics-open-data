.PHONY: get

install: getdata
	pip install -r requirements.txt

syncdata:
	s3cmd sync --recursive data s3://public-shared-everybody/politics-open-data/
	
getdata:
	mkdir -p data
	s3cmd get --recursive s3://public-shared-everybody/politics-open-data/data/ data/

webserver:
	python -m SimpleHTTPServer

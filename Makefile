.PHONY: syncdata

syncdata:
	s3cmd sync --recursive data s3://public-shared-everybody/politics-open-data/
	
getdata:
	s3cmd get --recursive s3://public-shared-everybody/politics-open-data/data/ data/
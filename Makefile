all: chiba tokyo hokkaido

chiba:
	python src/chiba.py

tokyo:
	python src/tokyo.py

hokkaido:
	DOWNLOAD_DELAY=1 scrapy runspider src/hokkaido.py -O data/hokkaido/$(shell date +%Y-%m-%d).csv

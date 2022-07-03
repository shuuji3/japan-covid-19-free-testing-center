all: chiba fukushima hokkaido iwate miyagi tokyo

chiba:
	python src/chiba.py

fukushima:
	python src/iwate.py

hokkaido:
	DOWNLOAD_DELAY=1 scrapy runspider src/hokkaido.py -O data/hokkaido/$(shell date +%Y-%m-%d).csv

iwate:
	python src/iwate.py

miyagi:
	python src/miyagi.py

tokyo:
	python src/tokyo.py

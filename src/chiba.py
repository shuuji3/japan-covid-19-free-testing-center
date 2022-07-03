# Chiba: fetch latest kml data and save as CSV file

import fastkml
import requests
from zipfile import ZipFile

def main():
    google_my_maps_url = 'https://www.google.com/maps/d/u/0/kml?mid=1phRqjG-gfPxjqClWrZIpkh23QECRZu_t'
    r = requests.get(google_my_maps_url)
    kml_text = gzip.decompress(r.content)
    kml = fastkml.kml.KML()
    kml.from_string(kml_text)
    print(kml)


if __name__ == '__main__':
    main()

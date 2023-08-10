# Get data from Scopus
# A 0.2 second delay for each search is added to comply with agreements.
# The whole repository takes about 45 minutes to access (as of Dec 2022).
import pandas as pd
import numpy as np
from pybliometrics.scopus import AbstractRetrieval
from tqdm import tqdm
import time
import requests
import xml.etree.ElementTree as ET
import os 

def fetch_and_save_full_text(doils, api_key, output_folder='output'):
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	base_url = 'https://api.elsevier.com/content/article/doi/'

	for doi in doils:
		url = f'{base_url}{doi}?apiKey={api_key}'
		response = requests.get(url)
		if response.status_code == 200:

			full_text = response.content
			root = ET.Element('article')
			root.text = full_text.decode('utf-8')

			tree = ET.ElementTree(root)
			xml_filename = f'{output_folder}/{doi.replace("/", "-")}_full_text.xml'
			with open(xml_filename, 'wb') as xml_file:
				tree.write(xml_file, encoding='utf-8', xml_declaration=True)
			print(f"Full-text content for {doi} written to {xml_filename}")
		else:
			print(f"Failed to retrieve the article {doi}. Status code: {response.status_code}")


#apikey = '5a1dd9dc03af1a475c71361d4933f453'
#scopus_doi = pd.read_csv('/Users/muthuku/Downloads/scopus.csv', encoding = "utf-8")

# list_doi = scopus_doi['DOI'].values.tolist()
# print(list_doi)

# fetch_and_save_full_text(list_doi, apikey, output_folder='output_folder_scopus_test')

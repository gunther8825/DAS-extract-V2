import os
import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree
from io import StringIO, BytesIO
import nltk
from nltk.tokenize import sent_tokenize
import re

def parse_xml_directory_NLP(directory):

	xml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.nxml')]
	print(xml_files)
	data = []
	urls = []


	for xml_file in xml_files:
		parser = etree.XMLParser(remove_comments=True)
		tree = etree.parse(xml_file)
		root = tree.getroot()

		#NLP extract data availability
		article_text = ''
		for element in root.iter():
			if element.text is not None:
				article_text += element.text

		cleaned_text = re.sub('<.*?>', '', article_text)
		sentences = sent_tokenize(cleaned_text)
		data_availability_statements = []

		keywords = ["data availability", "data deposition", "availability statement", "availability of data", "data and materials availability"]

		for sentence in sentences:
			for keyword in keywords:
				if keyword in sentence.lower():
					data_availability_statements.append(sentence)
					break
		data_availability = data_availability_statements


		for article in root.xpath('//article'):
			title = article.xpath('//article-title/text()')[0]
			pmid = article.xpath('//article-id/text()')[0]
			DOI = article.xpath('//article-id[@pub-id-type = "doi"]/text()')
			abstract = article.xpath('//abstract/p/text()')

		data.append({'Title': title, 'PubMed ID': pmid, 'DOI': DOI, 'Abstract':abstract, 'Data Availability':data_availability})
	df = pd.DataFrame(data)
	return df



# xml_directory = '/Users/muthuku/Desktop/final_xmls'
# df_2 = parse_xml_directory(xml_directory)
# print(df_2)
# df_2.to_csv("NLP_test.csv")
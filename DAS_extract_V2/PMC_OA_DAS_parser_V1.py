import os
import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree
from io import StringIO, BytesIO
import re

def parse_xml_directory(directory):

	xml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.nxml')]
	print(xml_files)
	data = []



	for xml_file in xml_files:

		parser = etree.XMLParser(remove_comments=True)
		tree = etree.parse(xml_file)
		root = tree.getroot()

		data_availability_notes = []
		url1 = []
		element_notes = tree.find('.//notes[@notes-type="data-availability"]/p')
		if element_notes is not None:
			element_string_notes = etree.tostring(element_notes, encoding='unicode')
			root1 = etree.fromstring(element_string_notes)
			ext_link_elements = root1.xpath('.//ext-link')
			url = [element.get('{http://www.w3.org/1999/xlink}href') for element in ext_link_elements]
			url1.append(url)

			clean_text = element_string_notes.replace('\xa0', ' ')
			clean_text = re.sub('<[^>]*>', '', clean_text)
			data_availability_notes.append(clean_text)
		else:
			data_availability_notes.append('')
			url1.append('')


		# #data_availability_sec = []
		# element_sec = tree.find('.//sec[@sec-type = "data-availability"]')
		# if element_sec is not None:
		# 	element_string_sec = etree.tostring(element_sec, encoding='unicode')
		# 	#data_availability_sec.append(element_string_sec)
		# else:
		# 	#data_availability_sec.append("")

		# #data_availability_meta= []
		# element_meta = tree.find('.//custom-meta[meta-name="Data Availability"]/meta-value')
		# if element_meta is not None:
		# 	element_string_meta = etree.tostring(element_meta, encoding='unicode')
		# 	#data_availability_meta.append(element_string_meta)
		# else:
		# #data_availability_meta.append("")



		# data_availability_sec_elems = root.xpath(".//*[local-name()='sec'][@sec-type='data-availability']")
		# for data_availability_elem in data_availability_sec_elems:
		# 	links = data_availability_elem.xpath(".//*[local-name()='ext-link'][@xlink:type='uri']/@xlink:href")
		# 	for link in links:
		# 		print(link)

		for article in root.xpath('//article'):


			title = article.xpath('//article-title/text()')[0]
			pmid = article.xpath('//article-id/text()')[0]
			DOI = article.xpath('//article-id[@pub-id-type = "doi"]/text()')
			PMC = article.xpath('//article-id[@pub-id-type = "pmc"]/text()')
			abstract = article.xpath('//abstract/p/text()')

			#THE BELOW CODE IS MY FIRST ITERATION AND IT ONLY GRABS TEXT OF DATA AVAILABILITY WITHOUT LINKS
			#data_availability_notes = article.xpath('.//notes[@notes-type="data-availability"]/p/text()')
			data_availability_sec = article.xpath('.//sec[@sec-type = "data-availability"]/p/text()')
			data_availability_meta = article.xpath('//custom-meta-group/custom-meta[meta-name[contains(text(), "Data Availability")]]/meta-value/text()')


		data.append({'Title': title, 'PubMed ID': pmid, 'PMC': PMC, "Abstract":abstract, 'Data Availability 1': data_availability_notes, 'Data Availability 2': data_availability_sec, "Data Availability 3" : data_availability_meta, 'URL1': url1})

	
	df = pd.DataFrame(data)
	return df



xml_directory = '/Users/muthuku/Desktop/final_xmls'
df1 = parse_xml_directory(xml_directory)

print(df1)
df1['combined'] = df1['Data Availability 1'] + df1['Data Availability 2'] + df1['Data Availability 3']
df1.to_csv("string_test.csv")

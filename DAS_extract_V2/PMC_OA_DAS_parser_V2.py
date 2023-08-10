import os
import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree
from io import StringIO, BytesIO
import re

def parse_xml_directory(directory):
	'''Function that can be used to parse through a directory of xmls and outputs a csv/excel 
	of Title, PMID, PMC, DOI, abstract, data availability statements and urls linking to data

	directory: folder of .xml files specifically from Pubmed OpenAccess'''

	#creates a list of xml files within the directory to be looped through
	xml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.nxml')]

	#initialize empty dataframe to be filled with final output dataframe 
	data = []


	#loop through directory of xml files
	for xml_file in xml_files:
		#eTree parser to parse XML file into xml elements 
		parser = etree.XMLParser(remove_comments=True)
		tree = etree.parse(xml_file)
		#get root of article- this root node differs for each XML
		root = tree.getroot()

		#grab DAS/if it is in the notes section -NOTES ID
		url_notes = []
		data_availability_notes = []
		#use findall to find all of the sections that may have this tag 
		element_notes = tree.findall('.//notes[@notes-type="data-availability"]/p')
		if element_notes is not None:
			#convert each ,<p> DAS section from xml element to string, in order to maintain the url links
			for note in element_notes:
				element_string_note = etree.tostring(note, encoding='unicode')
				#clean the text and strip down to only the paragraph section
				clean_text = element_string_note.replace('\xa0', ' ')
				clean_text = re.sub('<[^>]*>', '', clean_text)
				#append to DAS statement for that xml file 
				data_availability_notes.append(clean_text)

				'''for the links , convert the XML DAS string back into an XML element and 
				then use xpath to grab all the links that have the ".//ext-link, and append to list of urls''' 
				root1 = etree.fromstring(element_string_note)
				ext_link_elements = root1.xpath('.//ext-link')
				for element in ext_link_elements:
					url1 = element.get('{http://www.w3.org/1999/xlink}href')
					url_notes.append(url1)

		#same description as above for a different XML structure-SECTION ID
		url_sec = []
		data_availability_sec = []

		element_sec = tree.findall('.//sec[@sec-type = "data-availability"]/p')
		if element_sec is not None:
			for elem in element_sec:
				element_string_sec = etree.tostring(elem, encoding='unicode')
				clean_text1 = re.sub('<[^>]*>', '', element_string_sec)
				data_availability_sec.append(clean_text1)

				root2 = etree.fromstring(element_string_sec)
				ext_link_elements = root2.xpath('.//ext-link')
				for elem in ext_link_elements:
					url2 = elem.get('{http://www.w3.org/1999/xlink}href')
					url_sec.append(url2)

		#same description as above for a different XML structure-CUSTOM META-ID- only found in PLOS 
		url_meta = []
		data_availability_meta= []

		element_meta = tree.findall('.//custom-meta[meta-name="Data Availability"]/meta-value/p')
		if element_meta is not None:
			for elem in element_meta:
				element_string_meta = etree.tostring(elem, encoding='unicode')
				clean_text2 = re.sub('<[^>]*>', '', element_string_meta)
				data_availability_sec.append(clean_text2)

				root3 = etree.fromstring(element_string_sec)
				ext_link_elements = root3.xpath('.//ext-link')
				for elem in ext_link_elements:
					url3 = elem.get('{http://www.w3.org/1999/xlink}href')
					url_meta.append(url3)

		#code to extract other key data from XML
		for article in root.xpath('//article'):
			#use xPATH identifiers to get title,PMID, DOI and PMC, abstract 
			title = article.xpath('//article-title/text()')[0]
			pmid = article.xpath('//article-id/text()')[0]
			DOIs = article.xpath('//article-id[@pub-id-type = "doi"]/text()')
			if DOIs == []:
				DOI = "None"
			else:
				DOI = article.xpath('//article-id[@pub-id-type = "doi"]/text()')[0]
				print(DOI)
			PMC = article.xpath('//article-id[@pub-id-type = "pmc"]/text()')
			abstract = article.xpath('//abstract/p/text()')
			#for orid ID and author names, since there are many , we need to fina all elements, parse through each individually and output a list 
			orcid = []
			orcid_elem = article.findall('.//contrib-id[@contrib-id-type="orcid"]')
			for elem in orcid_elem:
				orcid.append(elem.text)

			author_names = []
			author_elem =  article.findall('.//contrib[@contrib-type="author"]/name')
			for elem in author_elem:
				surname = elem.findtext("surname")
				given_names = elem.findtext("given-names")
				author_name = f"{given_names} {surname}"
				author_names.append(author_name)


			#THE BELOW CODE IS MY FIRST ITERATION AND IT ONLY GRABS TEXT OF DATA AVAILABILITY WITHOUT LINKS-or_test.csv file output
			#data_availability_notes = article.xpath('.//notes[@notes-type="data-availability"]/p/text()')
			#data_availability_sec = article.xpath('.//sec[@sec-type = "data-availability"]/p/text()')
			#data_availability_meta = article.xpath('//custom-meta-group/custom-meta[meta-name[contains(text(), "Data Availability")]]/meta-value/text()')

		#finally we populate the data frame with each attribute of interest, and some clean up

		data.append({'Title': title,"Author names": author_names, "ORCID":orcid, 'PubMed ID': pmid, 'PMC': PMC, 'DOI':DOI, "Abstract":abstract, 'Data Availability 1': data_availability_notes, 'Data Availability 2': data_availability_sec, "Data Availability 3" : data_availability_meta, 'URL1': url_notes, 'URL2': url_sec, 'URL3':url_meta})

	
	df = pd.DataFrame(data)
	return df
#this should be the path to the folder containing all xml files of full text articles 
#xml_directory = '/Users/muthuku/Desktop/final_xml_07_22'
#use the function to parse through each file in directory and extract key info +DAS
#df1 = parse_xml_directory(xml_directory)

#DATAFRAME CLEAN UP STEPS

# create a combined DAS column to include results from 3 methods of DAS collection 
# df1['combined_DAS'] = df1['Data Availability 1'] + df1['Data Availability 2'] + df1['Data Availability 3']

# count = 0
# for n in df1['combined_DAS']:
# 	count += 1
# 	if n == []:
# 		n.append("Not applicable " + str(count))


#combine URLs as well 
# df1['all_urls'] = df1['URL1'] +df1['URL2'] + df1['URL3']
#drop individual columns 
# column_list = ['Data Availability 1','Data Availability 2','Data Availability 3','URL1', 'URL2','URL3']
# df2= df1.drop(columns = column_list)
# df2.to_csv("findall3.csv")

#convert the list of seperate strings into a single string
# df2['combined_string_DAS'] = df2['combined_DAS'].apply(lambda x: ' '.join(x))
# df2['combined_string_DAS'] = df2['combined_string_DAS'].str.replace(',', '')
#df2.to_csv("cleaned_DAS.csv", encoding = "utf-8", header = False, index = False)
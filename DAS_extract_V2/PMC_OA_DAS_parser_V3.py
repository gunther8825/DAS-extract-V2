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
		print(xml_file)
		#eTree parser to parse XML file into xml elements 
		parser = etree.XMLParser(remove_comments=True)
		tree = etree.parse(xml_file)
		#get root of article- this root node differs for each XML
		root = tree.getroot()

		#grab DAS/if it is in the notes element- element title contains keywords for Data availability statements 
		url_notes = []
		data_availability_notes = []
		#use findall to find all of the sections that may have this tag 
		potential_titles = ['Data availability','Accession Codes','Oncomine microarry datasets','Datasets','Availability of data and materials', 'Code availability','Data Availability Statement']
		for title in potential_titles:
			lower_title = title.lower()
			element_notes = tree.xpath(f".//notes[translate(title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = '{lower_title}']/p")
			if element_notes:
			#convert each ,<p> DAS section from xml element to string, in order to maintain the url links
				for note in element_notes:
					title_elem = note.find("./title")
					if title_elem is not None:
						note.remove(title_elem)
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

		#same description as above for a different XML element-SEC- title contains keyword
		url_sec = []
		data_availability_sec = []

		potential_titles = ['Data availability','MATLAB Code and Data','Network visualization','Data files','Data Deposition and Access','Data Availability and Accession Code Availability Statements','System requirements and software availability','Accession Codes','Data sharing statement','Accession nos.','Availability','DATA AND SOFTWARE AVAILABILITY','Data and Software Availability:','ACCESSION NUMBER','Availability of data','Availability of Supporting Data and Materials','Data and code','Additional data files','Major datasets','Major dataset','URLs','Accession codes','Data deposits','Source code and datasets','Datasets','Availability and requirements','Availability and implementation','Accessions', 'Program availability.', 'European Nucleotide Archive', 'Sequence Read Archive','Data availability and visualisation', 'Software availability', 'Software license', 'Data and materials availability:', 'Data availability.', 'Code availability', 'DATA DEPOSITION','Software and data availability', 'Data and code availability', 'Accession numbers', 'Code and data availability', 'Data Availability Statement','Data sharing','Data accessibility', 'Data, Materials, and Software Availability', 'Data access', 'Availability of supporting data','Availability of data and materials', 'Availability of data and material']
		for title in potential_titles:
			lower_title = title.lower()
			#element_sec = tree.findall(f".//sec[title = '{title}']/p")
			#element_sec = tree.xpath(f".//sec[translate(title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = '{lower_title}']/p")
			#element_sec = tree.xpath(f".//sec[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{lower_title}')]")
			element_sec = tree.xpath(f".//sec[normalize-space(translate(title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')) = '{lower_title}']")
			#data_availability_sec.append(element_sec)
			if element_sec:
				for elem in element_sec:
					title_elem = elem.find("./title")
					if title_elem is not None:
						elem.remove(title_elem)

					element_string_sec = etree.tostring(elem, encoding='unicode')
					clean_text1 = re.sub('<[^>]*>', '', element_string_sec)
					data_availability_sec.append(clean_text1)

					root2 = etree.fromstring(element_string_sec)
					ext_link_elements = root2.xpath('.//ext-link')
					for elem in ext_link_elements:
						url2 = elem.get('{http://www.w3.org/1999/xlink}href')
						url_sec.append(url2)


		#same description as above for a different XML element-CUSTOM META-ID 
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

		#ADD URLS nto this code 
		urls_bold = []
		das_bold = []
		potential_bolds = ["Database URL:","Data deposition:","Author Information","Data and materials availability:","DATA AVAILABILITY STATEMENT","UCSC genome browser tracks and data availability","Data accession", "Database URL","Accession codes.", "Data Availability","Code Availability", "ACCESSION NUMBERS","Accession numbers","Availability and Implementation:", "Availability:", "Accession Codes:","Accession codes"]
		for title in potential_bolds:
			p_element = root.xpath(f'.//bold[contains(., "{title}")]')
			for elem in p_element:
				p_element = elem.getparent()
				if p_element is not None:
					p_element_string = etree.tostring(p_element,  encoding = "unicode",method = "xml")
					clean_text3 = re.sub('<[^>]*>', '', p_element_string)
					clean_text3 = re.sub(fr'^\s*{re.escape(title)}\s*', '', clean_text3)
					das_bold.append(clean_text3)
					
					root4 = etree.fromstring(p_element_string)
					ext_link_elements = root4.xpath('.//ext-link')
					for elem in ext_link_elements:
						url4 = elem.get('{http://www.w3.org/1999/xlink}href')
						urls_bold.append(url4)
		urls_fn = []
		das_fn = []
		potential_fn = ["Data availability","Data Deposition Statement","Data access","Data deposition:","Availability","ACCESSION NUMBER.","Accession Numbers","Database accession numbers","Links to data tracks","Accession Codes,","Endnotes","DATA AND SOFTWARE AVAILABILITY", "Code Availability", "Data Availability", "Accession numbers", "Accession codes","Supplementary Materials","SEQUENCING DATA","Accession code:","URLs"]
		#ADD URLS
		for title in potential_fn:
			fn_element = root.xpath(f".//fn/p[contains(., '{title}')]")
			for elem in fn_element:
			#string_test = etree.tostring(elem, encoding = "unicode")
			#print(string_test)
				#index = elem.getparent().index(elem)
				#next_p_element = elem.getparent()[index + 1]
				index = elem.getparent()
				fn_element_string = etree.tostring(index, encoding='unicode')
				clean_text4 = re.sub('<[^>]*>', '', fn_element_string)
				clean_text4 = re.sub(fr'^\s*{re.escape(title)}\s*', '', clean_text4)
				das_fn.append(clean_text4)

				root5 = etree.fromstring(fn_element_string)
				ext_link_elements = root5.xpath('.//ext-link')
				for elem in ext_link_elements:
					url5 = elem.get('{http://www.w3.org/1999/xlink}href')
					urls_fn.append(url5)




		#code to extract other key data from XML
		for article in root.xpath('//article'):
			#use xPATH identifiers to get title,PMID, DOI and PMC, abstract 
			title_elem = article.xpath('//title-group')
			title_string = etree.tostring(title_elem[0], encoding = "unicode")
			title = re.sub('<[^>]*>', '', title_string)
			journal_title = article.xpath('//journal-title/text()')

			pmid = article.xpath('//article-id/text()')[0]
			DOIs = article.xpath('//article-id[@pub-id-type = "doi"]/text()')
			if DOIs == []:
				DOI = "None"
			else:
				DOI = article.xpath('//article-id[@pub-id-type = "doi"]/text()')[0]
				#print(DOI)
			year_element = article.xpath("//pub-date[@pub-type='pmc-release']/year/text()")
			if year_element == []:
				year = article.xpath("//pub-date[@pub-type='ppub']/year/text()")
				if year == []:
					year = article.xpath("//pub-date[@pub-type='epub']/year/text()")
					if year == []:
						year = article.xpath("//pub-date[@pub-type='collection']/year/text()")
			else:
				year = article.xpath("//pub-date[@pub-type='pmc-release']/year/text()")[0]
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

		data.append({'Title': title,"Year": year, "Author names": author_names,"Journal": journal_title, "ORCID":orcid, 'PMID': pmid, 'PMC': PMC, 'DOI':DOI, "Abstract":abstract, 'Data Availability 1': data_availability_notes, 'Data Availability 2': data_availability_sec, "Data Availability 3" : data_availability_meta,"Data Availability 4" : das_bold,"Data Availability 5":das_fn, 'URL1': url_notes, 'URL2': url_sec, 'URL3':url_meta, 'URL4':urls_bold, 'URL5': urls_fn })

	
	df = pd.DataFrame(data)
	return df
#this should be the path to the folder containing all xml files of full text articles 
#xml_directory = '/Users/muthuku/Desktop/final_xml_07_22'
#use the function to parse through each file in directory and extract key info +DAS
#df1 = parse_xml_directory(xml_directory)
#df1.to_csv("new_code_check.csv", encoding = "utf-8")

#DATAFRAME CLEAN UP STEPS

# create a combined DAS column to include results from 3 methods of DAS collection 
# df1['combined_DAS'] = df1['Data Availability 1'] + df1['Data Availability 2'] + df1['Data Availability 3'] + df1['Data Availability 4'] + df1['Data Availability 5'] 
# df1['unique_combined_das'] = df1['combined_DAS'].apply(lambda x: list(set(x)))
# count = 0
# for n in df1['unique_combined_das']:
# 	count += 1
# 	if n == []:
# 		n.append("Not applicable " + str(count))


#combine URLs as well 
# df1['all_urls'] = df1['URL1'] +df1['URL2'] + df1['URL3'] +df1['URL4'] + df1['URL5']
# #drop individual columns 
# column_list = ['Data Availability 1','Data Availability 2','Data Availability 3','Data Availability 4','Data Availability 5','URL1', 'URL2','URL3','URL4','URL5', 'combined_DAS']
# df2= df1.drop(columns = column_list)
# df2.to_csv("findall_5.csv", encoding = "utf-8")

#convert the list of seperate strings into a single string
# df2['combined_string_DAS'] = df2['unique_combined_das'].apply(lambda x: ' '.join(x))
# df2['combined_string_DAS'] = df2['combined_string_DAS'].str.replace(',', '')
# df2 = df2.drop(['unique_combined_das'], axis = 1)
# df2.to_csv("all_statements.csv", encoding = "utf-8")

#journal_counts = df2['Journal'].value_counts().reset_index()
#journal_counts.columns = ['Journal', 'Count']

#print(journal_counts)

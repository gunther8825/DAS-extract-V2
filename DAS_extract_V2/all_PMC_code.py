import itertools
import pandas as pd 
import numpy as np
import scipy
import urllib.request
import os
import shutil
import tarfile
import zipfile

def grab_PMIDs_from_csv(source_file, target_file):
	'''
	Function to extract PMIDs from a DataFrame column and save them to a target file.
    
    Parameters:
        - source_file (str): Path to the source file (CSV) containing the PMID.
        - target_file (str): Path to the target file (TXT) where the extracted URLs will be saved.
       '''
	# Read the source file
	df1 = pd.read_csv(source_file)
	# Extract the URLs from the DataFrame
	extracted_PMID = df1["official_url"].str[-8:]

	# Remove empty strings and drop NaN values
	extracted_PMID.replace('', np.nan, inplace=True)
	extracted_PMID.dropna(inplace=True)
	filtered_PMIDs = [pmid for pmid in extracted_PMID if pmid.isdigit()]
	filtered_df = pd.DataFrame(filtered_PMIDs, columns=["PMIDs"])
	# Save the extracted URLs to the target file
	filtered_df.to_csv(target_file, header=True, index=None)

def isolate_rows_by_PMID(source_file, database, output_file):
	'''
    Function to isolate rows from a DataFrame based on PMIDs and save the result to a CSV file.
    
    Parameters:
        - source_file (str): Path to the source file containing the PMIDs.
        - target_file (str): Path to the target file to save the isolated rows.
        - data_file (str): Path to the data file (CSV) containing the rows to be isolated.
	'''
	# Read the source file containing the PMIDs
	df_pmids = pd.read_csv(source_file)
	# Read the data file
	df_database = pd.read_csv(database)
	# Convert the PMIDs to a list and convert type to integers

	pmid_list = df_pmids['PMIDs'].astype(int).tolist()
	# Isolate the rows based on PMIDs

	isolated_rows = df_database[df_database['PMID'].isin(pmid_list)]
	# Save the isolated rows to a new CSV file

	isolated_rows.to_csv(output_file, index=False)

def download_PMC(source_file, output_folder):

	'''
	Function to download files from a list of URLs and save them to a destination folder.
    
    Parameters:
        - source_file (str): Path to the file containing the URLs.
        - output_folder (str): Path to the folder where the downloaded files will be saved.
    '''

	# Read the file containing the URLs
	df1 = pd.read_csv(source_file)
	# Extract the URLs from the DataFrame
	urls = df1["File"]
	# Create the destination folder if it doesn't exist
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	
	# Loop through each URL and download the file

	for url in urls:
		link = "https://ftp.ncbi.nlm.nih.gov/pub/pmc/" + str(url)
		file_name = os.path.basename(link)
		destination_path = os.path.join(output_folder, file_name)
		urllib.request.urlretrieve(link, destination_path)

def extract_files(folder_path):
	# folder_path : path where all zipped PMC.tar.gz files exist 
	#loop through tar.gz files within folder
	for file_name in os.listdir(folder_path):
		#generate a file path with folder path and file name
		file_path = os.path.join(folder_path, file_name)
		#check if file ends with tar.gz and extract file contents 
		if file_name.endswith('.tar.gz'):
			with tarfile.open(file_path, 'r') as tar_ref:
				tar_ref.extractall(file_path)
			os.remove(file_path)


def get_nxml(source_folder, target_folder, file_extension):
	#make target folder if it doesn't already exist 
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)
	# loop through each PMC folder and make path to folder 
	for folder_name in os.listdir(source_folder):
		folder_path = os.path.join(source_folder, folder_name)
		if os.path.isdir(folder_path):
			#loop through each file and if file ends with .nxml, move to output folder
			for file_name in os.listdir(folder_path):
				file_path = os.path.join(folder_path, file_name)
				# Check if the file already exists in the target folder
				if file_name.endswith(file_extension):
					target_file_path = os.path.join(target_folder, file_name)
					counter = 1
					while os.path.exists(target_file_path):
						# If the file already exists, modify the filename with a suffix
						base_name, extension = os.path.splitext(file_name)
						new_file_name = f"{base_name}_{counter}{extension}"
						target_file_path = os.path.join(target_folder, new_file_name)
						counter += 1
					shutil.move(file_path, target_file_path)





## GET FULL TEXT ARTICLES-limited to ones accessible through PubMed OA database 

# STEP 0 - from the initial CSV downloaded from the CSHL repository, extract the PMIDs into a text file 

#grab_PMIDs_from_csv('/Users/muthuku/Downloads/2023_07_06_CSHL_articles_2007-2022_from_IR.csv',"pmids_07_22.txt")

'''STEP 1 - search the full Pubmed OA database for the articles, use oa_file_list.csv, 
outputs a filtered csv of database containing only our articles of interest'''

#isolate_rows_by_PMID('/Users/muthuku/Desktop/Pragati2023/first10000_results_canceronly.txt', '/Users/muthuku/Desktop/Pragati2023/oa_file_list.csv', 'output1_largerPMC.csv')

#STEP 2 - using the links in the output file and download zipped PMC folders containing .nxml, .pdf, figures and data into a directory (download_PMC fxn)
#STEP 2A- Each downladed file will look like PMC{ID Number}.tar.gz, using extract_files function to unzip them 

#download_PMC('/Users/muthuku/Desktop/output1_largerPMC.csv', "PMC_folder_LARGEDB1")

#folder = '/Users/muthuku/Desktop/PMC_folder_LARGE_DB2'
#extract_files(folder)

#STEP 3 - grab the full text XML from each PMC folder and create a folder with all articles

# source_folder = '/Users/muthuku/Desktop/PMC_folder_LARGE_DB2'
# target_folder = '/Users/muthuku/Desktop/final'
# file_extension = '.nxml'

# get_nxml(source_folder,target_folder,file_extension)

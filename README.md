# DAS-extract-V2
Python based workflow to get full texts, article metadata, DAS and citation counts. Install all required packages with the code below. 

	pip install -r requirements.txt
# STEP 0 - Dataset 
In order to run this computational workflow, you will need a list of PubMed IDs or PubMedCentral IDs. This can be done:

1. Go to the CSHL Digital Repository, filter by year, author and journal article, export your search results as a EP3 XML and then import the data into an Excel .csv (UTF-8) that contains a list of PMIDs
2. Go to PubMed and search for papers by your specific criteria, and download a textfile of PMIDs.
   
Ulimately you want to end up with a textfile (.txt) of PMIDs to be able to grab the full text XMLs from the PubMed Open Access Database.
__________________________________________________________________________________________________________________________________________
# STEP 1- Grabbing full text XMLs from the PubMed OA data base (all python functions are in the file all_PMC_code.py)
If you have a .csv from the CSHL digital repository, you must first use and you use function grab_PMIDs_from_csv(source_file=(CSHL Repo).csv, target_file = PMIDS.txt)

   	CHECK example_files folder for example input files:
   	CSHL digital repo file = 2023_07_06_CSHL_articles_2007-2022_from_IR
   	PMIDS_textfile = pmids_07_22.txt
    PubMed_OpenAccess_Database = oa_file_list.csv
    Files_to_Download = output1_07_22_PMC.csv

3. With the .txt of PMIDs, you then use function isolate_rows_by_PMIDs(source_file = "PMIDs.txt", database = oa_file_list.csv, output_file = output1_07_22_PMC.csv), this will search through the entire oa database and return an output CSV containing downloadable links. Download this file into the example_files in your local directory using this link https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_file_list.csv

   		To download the oa_file_list.csv go to the Base FTP URL https://ftp.ncbi.nlm.nih.gov/pub/pmc/ and download the file. Update this file once every 3 weeks

5. Using the output file from Step 2 (output_files_downloadable.csv), we now download folders containing figures, supplemental and full text articles. This is done using download_PMC(source_file = output1_07_22_PMC.csv, folder=full_texts. This leads to an output of a directory/folder containing the zipped (.tar.gz) versions of the PMC files. 
	
		A. Each downladed file will look like PMC{ID Number}.tar.gz, USE extract_files function to unzip them

6. use function extract_files(input = folder of zipped files) to unzip and untar the zipped files

7. Use function get_nxml(source_folder = folder of unzipped files,target_folder = file where full text xmls are,file_extension = .nxml/.pdf/.xml)
__________________________________________________________________________________________________________________________________________________

# STEP 2- Parsing through xmls and populate table with article metadata and DAS
Using the PMC_OA_DAS_parser.py Python file, you can input the entire folder of full text XMLs and get an output CSV with article metadata such as - article title, Journal, Year published, Abstract, DOI, PMID, PMCID, Data availability statement and URL links to Data

1. PMC_OA_DAS_parser_V1.py- utilized NLP to grab full DAS, but has issues with specificity. It will call any sentence that contains the word "Data availability", however you as a user can get to know your dataset and update the keywords it searches. 

2. PMC_OA_DAS_parser_V2.py= searched through specific XML elements such as sec, notes, fn and attributes that contain "data-availability". This works for more recent articles (post 2016) because older articles don't have this specific section.
ex. <sec sec-type="data-availability" id="s1"> 

3. PMC_OA_DAS_parser_V3.py= similar to V2 but also includes more code to be able to extract DAS from older articles, by examining the full text of the XML element (sec, notes, bold, fn etc) that contains a DAS keyword - MOST ROBUST and MORE SPECIFIC THAN V1 and V2

   		Check PMC_parser_output.csv in the example_files folder to see an example of the output of this code.
__________________________________________________________________________________________________________________________________________________
# STEP 3 - ML + NLP classifier Colviazza et al, 2020 - This code can be used on any list of DAS, even the ones extracted using different methods
Download large file glove.6B.50d.txt into your local directory version of ML_input in order to be able to run this section. You can download it from https://github.com/alan-turing-institute/das-public/blob/v1.2/dataset/das_classifier/input/glove.6B.50d.txt.zip where you will see the file name.

	To run this code, you must go into the classify_das2.py file and modify the inputs as described below. 
# Input descriptions
dir_out = "example_files/ML_output" #this can be named as anything

dir_in = "example_files/ML_input" #this is the directory where your input files are located - file of statements, and annotated data for training and testing of the ML model 

	Within you ML_input file, you will need large file glove.6B.50d.txt, which is necessary for the vectorizing of words in the DAS, needed for ML tool

annotated_file_name = "ML_input_test_annotations.csv"  # Annotated data- this will not change, but user can modify it to contain more annotated entries, currently only has 200 

input_file_name = "ML_input_das_statements.csv" # file containing DAS to be classified, follow the format of the example file included in Github repo "ML_input_das_statements.csv"

output_summary_file_all = "overview_models_parameters.csv" #this can be named as anything, or leave as is

Then you can input this code into the jupyter notebook to finally get the classified DAS statements, found within the ML_output folder 

	!python3 ./DAS_extract_V2/classify_das2.py --istest no --user_input yes --combine_labels no --coding 1 --stopwords no --uniform_prior yes --stemming yes --skip_model1 yes --skip_model2 yes --skip_model3 no --skip_model4 yes --skip_model5 yes
__________________________________________________________________________________________________________________________________________________

# STEP 4- grabbing citation counts from the SCOPUS database (accessible via CSHL library access) and merge all dfs into final output 
Using the output CSV for the parser, create a dataframe containing the all data. Then create a smaller dataframe containing the full list of DOIs, when you input a list of DOIs, the SCOPUS ID can return the citation counts for each article. You can then add a new column to the original dataframe and add any other modifications before returning the output. 

	file1 = "example_files/PMC_parser_output.csv"

	file2 = "example_files/ML_output/Classified_SVM_combined_labels_no-coding-approach1-stopwords-no-uniformprior_yes-stemming_yes-test_no.csv"

	df3 = merge_og_classify_dfs(file1, file2)

	df4 = df3["DOI"]

	df3['citation_count'] = citation_count(df4)

 	df3.to_csv("example_files/final_output_test_JN.csv", encoding = "utf-8", index = False)

Check final_output_test_JN.csv in example_files folder to see an example of the output.

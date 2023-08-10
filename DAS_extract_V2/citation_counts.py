
# Get data from Scopus
# A 0.2 second delay for each search is added to comply with agreements.
# The whole repository takes about 45 minutes to access (as of Dec 2022).
import pandas as pd
import numpy as np
from pybliometrics.scopus import AbstractRetrieval
from tqdm import tqdm
import time


def citation_count(dataframe):
    '''
    Input: dataframe - a dataframe containing a column of DOIs corresponding to the article title 
    '''
    citation_count = np.zeros(len(dataframe))
#    pub_date = np.zeros(len(pub_list_format))
    #length of dataframe, and then loop through each DOI using for loop 
    LENGTH = len(dataframe) # Number of iterations required to fill pbar
    ii =0
    ab = ''
    for doi in tqdm(dataframe, total = LENGTH):
        try:
            #retrieve the abstract using the retrieval function and grab the cited by value
            ab = AbstractRetrieval(doi)
            citation_count[ii] = ab.citedby_count
            time.sleep(.2)
            ii = ii+1
        except Exception:
            citation_count[ii] = np.nan
            ii = ii+1
            pass
    return citation_count

def merge_og_classify_dfs(file1, file2):
    #read file 1 which contains all article metadata, including the column 'combined_string_DAS'
    df1 = pd.read_csv(file1)
    #set the row index to the combined strings
    df1.set_index('combined_string_DAS', inplace=True)
    #read file 2 which is the output file of the ML DAS classifier, contains no headers

    df2 = pd.read_csv(file2, header=None)
    #generate headers for the two columns and make sure the indexes match to 'combined_string_DAS'
    df2.columns = ['combined_string_DAS', 'classifying_number']
    df2.set_index('combined_string_DAS', inplace=True)
    #merge the two based on the indexes and output a final DF 
    merged_df = pd.merge(df1, df2, left_index=True, right_index=True, how='left')
    merged_df.reset_index(inplace=True)

    return merged_df

#merge DFs code 

# file1 = '/Users/muthuku/Desktop/all_statements1.csv'
# file2 = '/Users/muthuku/Downloads/alan-turing-institute-das-public-5581446_modify/output_LARGE_DB/Classified_SVM_combined_labels_no-coding-approach1-stopwords-no-uniformprior_yes-stemming_yes-test_no.csv'
# df3 = merge_og_classify_dfs(file1, file2)
# df3.to_csv("final_output_LARGE_DB.csv", encoding = "utf-8")

# CITATION COUNT code 

# df1 = pd.read_csv('/Users/muthuku/Desktop/final_output_LARGE_DB.csv')
# df2 = df1['DOI']
# df1['citation_count'] = citation_count(df2)
# # citations = citation_count(df1['citation_count'])

#code to get average citation counts and class count number by year 

# result = df1.groupby(['Year', 'classifying_number']).size().reset_index(name='counts')
# average_citation_by_class_year = df1.groupby(['Year', 'classifying_number'])['citation_count'].mean().reset_index()

# df1.to_csv('og_df_with_citations1.csv', encoding = "utf-8", index = False)
          
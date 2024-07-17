# Keyword Search for Research Papers

# Script searches a .csv file of citations (such as obtained from Dimensions) for specified keywords. 

import pandas as pd
import re

# Load the list of citing papers as a dataframe
papers_1 = pd.read_csv('/home/annajellema/rothman/dimensions_early.csv', header=0)
papers_2 = pd.read_csv('/home/annajellema/rothman/dimensions2009.csv', header=0)

papers_df = pd.concat([papers_1,papers_2], ignore_index = True)

# Define keywords
animal_keywords = [
    'c. elegans', 'mice', 'mouse', 'rat', 'animal', 'mammal', 'zebrafish', 
    'fruit fly', 'Drosophila', 'Caenorhabditis elegans', 'chicken', 'frog', 
    'Xenopus', 'nematode'
]
aging_keywords = [
    'age', 'aging', 'longevity', 'gerontology', 'life span', 'age-related', 
    'age-associated', 'ageing', 'senior', 'senile', 'elderly'
]

# Function to check for exact word ignoring case
def word_match(text, keyword):
    pattern = r'\b{}\b'.format(re.escape(keyword.lower()))
    return re.search(pattern, text.lower()) is not None if isinstance(text, str) else False

# Function to search for keywords in the dataframe
def search_keywords(dataframe, keywords):
    results = 0
    for index, row in dataframe.iterrows():
        title = row.get('Title', '')
        abstract = row.get('Abstract', '')
        source_title = row.get('Source title', '')

        match_found = False
        matched_keyword = None
        matched_section = None

        # Check if any exact keyword match is found in title, abstract, or source title
        for keyword in keywords:
            if word_match(title, keyword):
                match_found = True
                matched_keyword = keyword
                matched_section = 'Title'
                break
            if word_match(abstract, keyword):
                match_found = True
                matched_keyword = keyword
                matched_section = 'Abstract'
                break
            if word_match(source_title, keyword):
                match_found = True
                matched_keyword = keyword
                matched_section = 'Source'
                break

        if match_found:
            results += 1
            print(f"Matched keyword '{matched_keyword}' in {matched_section} of row {index}.")
    
    return results

# Example usage: search for animal keywords
results = search_keywords(papers_df, animal_keywords)
print(f"\n TOTAL COUNT: {results} entries match keywords")

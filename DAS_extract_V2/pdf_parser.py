import PyPDF2
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data (if not already downloaded)
nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
	with open(pdf_path, 'rb') as pdf_file:
		pdf_reader = PyPDF2.PdfReader(pdf_file)
		text = ''
		for page in pdf_reader.pages:
			text += page.extract_text()
	return text

def tokenize_text(text):
	tokens = word_tokenize(text)
	return tokens


# pdf_directory = 'path_to_your_directory'  # Replace with the actual path to your directory

# for pdf_filename in os.listdir(pdf_directory):
# 	if pdf_filename.endswith('.pdf'):
# 		pdf_path = os.path.join(pdf_directory, pdf_filename)
# 		pdf_text = extract_text_from_pdf(pdf_path)
# 		tokenized_text = tokenize_text(pdf_text)
		# output_filename = os.path.splitext(pdf_filename)[0] + '_tokens.txt'
		# output_path = os.path.join(pdf_directory, output_filename)

		# with open(output_path, 'w', encoding='utf-8') as output_file:
		# 	output_file.write(' '.join(tokenized_text))

#pdf_path = '/Users/muthuku/Downloads/pdfs/1936-Young-SQB.pdf'  # Replace with the actual path to your PDF file
#Extract all text from PDF
#pdf_text = extract_text_from_pdf(pdf_path)
#tokenize
#tokenized_text = tokenize_text(pdf_text)
#clean up this text as tokenized text may have entries such as '.' which may not be important to us
#cleaned_tokens = [token for token in tokenized_text if token not in ['.', ',']]
#print(cleaned_tokens)
#print(tokenized_text)
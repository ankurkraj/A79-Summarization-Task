# A79-Summarization-Task

## Project Structure and Source ode Files

### The repository is formatted as :-
| -- dummpy_Papers - Consists the results of 5 sample files.  
| -- summarize_pdf.py - Implements functions to perform the summarization task given the contents of a PDF file.  
| -- extract_table.py - Implements functions to extract table from a given PDF file.  
| -- download_papers.py - Imports functions from the other files to finally perform all the tasks. The primary file of the project (This needs to be run to get all the tasks done).  

### The Result direcotry is formatted as follows (dummy_Papers) :-
<pre>
| -- 38612630 -- | -- paper_38612630.pdf                             
                 | -- table_38612630.csv                              
                 | -- summary_38612630.txt          
| -- ..
| -- ..
</pre>

**38612630** - Represents the **PMID number** that is associated with every **PubMED** Paper.

## Approach and Assumptions

### Extracting Full papers and parsing it as PDF
<pre>
(1) Python module **metapub**'s  FindIt function was used to locate the Paper after obtianing the PMID from the link, the full text for all Papers were not found using this precisely 162/294 were downloaded.
(2) The paper was saved as pdf by chunking into bytes and appending into a file.
</pre>
### Summarization

OpenAI's model gpt-4o-mini was used to summarize the paper. The PDF Paper was parsed using PyPDF2 module. The following prompts were provided to the model to get in a standard format, the precise format was also created using an AI model from some vague descriptions.
        
        Please provide a concise summary of the following research paper. The summary should be around 250 words and should include the following key points:

        Research Question: What is the main question or problem the paper aims to address?
        Methodology: How did the authors conduct the research?
        Key Findings: What are the most important results or discoveries?
        Implications: What are the implications of the findings?
        Limitations: What are the limitations of the research?
        Conclusion: What is the overall conclusion of the paper?
        Below is the research paper\n

### Table Extraction and selection

AryanAI's python module aryn-sdk was used to detect the tables from the PDF files, it returns all the tables present with a confidence score. The header file of each table along with the summary of the PDF file is sent to  gpt-4o-mini model to recognize the most appropriate table. It grades the table according to its header's relevance to the summairzed text, the max graded table is chosen if grade > 50.

### Performance Optimization 

Multiprocessing is used to optimize the time taken to generate the files. Also chunking is used to parse and create PDF files to optimize RAM usage. Also an exponentially increasing backoff timer is used to access OpenAI's API since there are restrictions in the number of calls/tokens per minute. This turned out to be the bottleneck in performance (time wise) .

## How to Run 

### Setup
<pre>
Beside the system provided modules you would require the following third-party libraries 

metapub - To obtain the PubMED paper using PMID
openai - For Summarization and Grading Tables
aryn_sdk - For extracting Tables
PyPDF2 - For Parsing PDFs

API's required 

OpenAI API - To be used in line 6  in extract_table.py and line 4 and 5 in summarize_pdf.py 
ArynAI API - To be used in line 7  in extract_table.py

Change the direcories where you want the Results file 'Papers' to be stored. By changing the parent direcotry at line 10 in download_papers.py and line 6 in summarize_pdf.py.

</pre>
### Running

Run the primary file download_papers.py to obtain the results in the parent_direcory.








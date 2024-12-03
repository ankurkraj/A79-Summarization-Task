import multiprocessing
from threading import Lock
from metapub import FindIt
import os
import requests
import time
from summarize_pdf import extract_text_from_pdf, summarize_text
from extract_table import extract_table

parent_directory = "C:/Users/Ankur Kumar Raj/Downloads/Papers"

success_overall = multiprocessing.Value('i',0)
pmid_error = multiprocessing.Value('i',0)
link_format_error = multiprocessing.Value('i',0)
link_inaccessible = multiprocessing.Value('i',0)
link_absent = multiprocessing.Value('i',0)
total = multiprocessing.Value('i',0)

def save_pdf(pmid, response):
    global parent_directory
    pmid_directory = parent_directory + '/' + str(pmid)
    if not os.path.exists(pmid_directory):
        os.mkdir(pmid_directory)
    pdf_directory = pmid_directory + '/paper_' + str(pmid) + '.pdf'
    with open(pdf_directory, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
        print(f"Saved PDF file for {pmid} at address {pdf_directory}\n")
    return pdf_directory

def save_summary(pmid, pdf_directory):
    global parent_directory
    text = extract_text_from_pdf(pdf_directory)
    backoff_factor = 2
    max_backoff = 60
    lock = Lock()
    while True:
        try:
            summary = summarize_text(text)
            summary_directory = parent_directory + '/' + str(pmid) + '/summary_' + str(pmid) + '.txt'
            with open(summary_directory, 'w') as f:
                f.write(summary)
            print("Summary created")
            break
        except Exception as e:
            with lock:
                backoff_time = min(max_backoff, backoff_factor)
                backoff_factor *= 2
                print(f"API rate limit reached. Retrying in {backoff_time:.2f} seconds...")
                time.sleep(backoff_time)



def process_link(link):
    global parent_directory, success_overall , pmid_error ,link_format_error ,link_inaccessible ,link_absent ,total
    strings = link.split('/')

    with total.get_lock():
        total.value += 1
    try:
        pmid = strings[3]
    except Exception as E:
        print(f"The string is {link} not in the expected form to extract the PMID\n")
        with link_format_error.get_lock():
            link_format_error.value += 1
        return

    try:
        src = FindIt(pmid)
    except Exception as E:
        print(f"The PMID {link} is no associated with any papers\n")
        with pmid_error.get_lock():
            pmid_error.value += 1
        return

    if src.url:
        try:
            response = requests.get(src.url, stream=True)
        except Exception as E:
            print("No response received from the link obtained\n")
        if response.status_code == 200:
            pdf_directory = save_pdf(pmid, response)
            save_summary(pmid, pdf_directory)
            extract_table(pmid, parent_directory)
        else:
            print(f"The PMID {link} is not accessible\n")
    else:
        print(f"The PMID {link} is not available\n")

def main():
    global parent_directory
    path_to_papers = "C:/Users/Ankur Kumar Raj/Downloads/PubMed.txt"
    with open(path_to_papers, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    if not os.path.exists(parent_directory):
        os.mkdir(parent_directory)

    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        pool.map(process_link, lines)

if __name__ == '__main__':
    t = time.time()
    main()
    print(f"Total time taken for the analysis {time.time() - t} second\n")
from aryn_sdk.partition import partition_file, table_elem_to_dataframe
import os
import openai
import re

client = openai.OpenAI(api_key="OPENAI_API_KEY")
os.environ["ARYN_API_KEY"] = 'ARYN_API_KEY'
def extract_number(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    else:
        return 0
def ai_judge(summary, header):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are relevance grader"},
            {
                "role": "user",
                "content": ''' You are given a 'summary' and a table 'header', you have the give a relevance score
                            to the 'header' such that, if the header was a head of a table in the research paper
                            how relevant would be according to the summary. Here is the summary\n''' + summary +
                            '''\n Here is the header \n. ''' + header + '''\n. The score must lie between 0 and 100.
                            Output nothing but a single number'''
            }
        ],
        max_tokens=5,
        n=1,
        stop=None,
        temperature=0.2
    )
    grade = extract_number(response.choices[0].message.content)
    print(f"The response {response.choices[0].message.content} the grade {grade}\n")
    return grade

def extract_table(pmid, parent_directory):
    pdf_directory = parent_directory +'/' + str(pmid) + '/paper_' + str(pmid) + '.pdf'
    summary_directory = parent_directory +'/' + str(pmid) + '/summary_' + str(pmid) + '.txt'
    table_directory = parent_directory + '/' + str(pmid) + '/table_' + str(pmid) + '.csv'
    with open(pdf_directory, "rb") as f:
        data = partition_file(
            f,
            use_ocr=True,
            extract_table_structure=True,
            extract_images=True
        )

    list_tables = []
    for element in data['elements']:
        if element['type'] == 'table':
            df = table_elem_to_dataframe(element)
            list_tables = list_tables + [df]

    summary = ""
    with open(summary_directory, 'r') as f:
        summary = f.read()

    grade = 0
    my_table = 0
    for table in list_tables:
        first_row = table.head(1).to_string(index=False)
        print(first_row)
        grade_text = ai_judge(summary, first_row)
        grade_curr = extract_number(grade_text)
        if grade_curr>grade:
            grade = grade_curr
            my_table = table

    print(my_table)
    if grade>50:
        my_table.to_csv(table_directory)
    print(grade)
import openai
import PyPDF2

client = openai.OpenAI(api_key="OPENAI_API_KEY")
openai.api_key = "OPENAI_API_KEY"
parent_directory = "C:/Users/Ankur Kumar Raj/Downloads/Papers"

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

def save_summary(pmid, pdf_directory):
    global parent_directory
    text = extract_text_from_pdf(pdf_directory)
    summary = summarize_text(text) # Handle successful API call
    summary_directory = parent_directory + '/' + str(pmid) + '/summary_' + str(pmid) + '.txt'
    with open(summary_directory, 'w') as f:
        f.write(summary)
        print("Summary created")

def summarize_text(text, max_tokens=350):
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": "You are a scientific research paper summarizer."},
      {
        "role": "user",
        "content": ''' Please provide a concise summary of the following research paper. The summary should be around 250 words and should include the following key points:

        Research Question: What is the main question or problem the paper aims to address?
        Methodology: How did the authors conduct the research?
        Key Findings: What are the most important results or discoveries?
        Implications: What are the implications of the findings?
        Limitations: What are the limitations of the research?
        Conclusion: What is the overall conclusion of the paper?
        Below is the research paper\n''' + text
      }
    ],
    max_tokens=max_tokens,
    n=1,
    stop=None,
    temperature=0.2
  )

  summary = response.choices[0].message.content
  return summary


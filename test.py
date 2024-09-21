import json
import fitz
from glob import glob
from tqdm import tqdm
from ollama import Client

client = Client(host='http://localhost:11434')

def read_pdf(file_path: str) -> str:
    text = ""
    pdf_document = fitz.open(file_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def generate_questions_and_answers(paragraph: str):
    prompt = (
        "Create a list of general questions and answers based on the following text. "
        "Each question should be specific and clearly related to the key concepts or important details in the text. "
        "The questions should be designed to be standalone, meaning that each question and answer pair should contain enough information to be understood without needing to refer back to the original text. "
        "The answers should be detailed and provide comprehensive information that fully addresses the question. Each answer should be written in a complete paragraph, ensuring that it offers a thorough explanation relevant to the question. "
        "Format your response strictly in JSON. The JSON should be an array of objects, with each object containing two properties: "
        "\"question\": a string that clearly states the question. "
        "\"answer\": a string that provides a detailed paragraph answering the question. "
        "Ensure that there is no additional text or formatting outside of the JSON structure.\n\n"
        f"Text:\n{paragraph}"
    )

    response = client.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}])

    generated_text = response['message']['content']

    # Load the response as JSON to ensure it's valid
    try:
        qa_pairs = json.loads(generated_text)
        return qa_pairs
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {generated_text}")
        return []

# Process the PDF and chunk it into pieces
all_qa_pairs = []
max_chunk_size = 1024
pdf_text = read_pdf("a_5.pdf")

for i in tqdm(range(0, len(pdf_text), max_chunk_size)):
    chunk = pdf_text[i:i + max_chunk_size]
    try:
        qa_pairs = generate_questions_and_answers(chunk)
        if qa_pairs:  # Only append valid responses
            all_qa_pairs.extend(qa_pairs)
    except Exception as e:
        print(f"An error occurred: {e}")

# Save all Q&A pairs into a JSON file
with open('raw_data.json', 'w') as json_file:
    json.dump(all_qa_pairs, json_file, indent=4)

print("Questions and answers have been saved to raw_data.json.")

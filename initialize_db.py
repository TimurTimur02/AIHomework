import json
import psycopg2
from transformers import BertTokenizer, BertModel

file_path = r'dev-v2..json'

with open(file_path, 'r') as file:
    data = json.load(file)

qas_data = []

for section in data['data']:
    for paragraph in section['paragraphs']:
        context = paragraph['context']
        for qa in paragraph['qas']:
            question = qa['question']
            answers = qa['answers'] if qa['answers'] else (qa['plausible_answers'] if 'plausible_answers' in qa else [])
            answer_texts = [answer['text'] for answer in answers]
            qas_data.append({'question': question, 'answers': answer_texts, 'context': context})

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def encode_question(question):
    inputs = tokenizer(question, return_tensors='pt', max_length=512, truncation=True)
    outputs = model(**inputs)
    features = outputs.last_hidden_state[:, 0, :].detach().numpy()
    return features

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345678",
    host="localhost"
)
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS qa_pairs;
    CREATE TABLE qa_pairs (
        id SERIAL PRIMARY KEY,
        question TEXT,
        question_vector FLOAT[],
        answer TEXT
    )
""")

print("Таблица создана.")
print("Вставка данных...")

for item in qas_data:
    encoded_question = encode_question(item['question'])
    answer = item['answers'][0] if item['answers'] else 'Ответ не найден'
    cur.execute("INSERT INTO qa_pairs (question, question_vector, answer) VALUES (%s, %s, %s)",
                (item['question'], encoded_question.tolist(), answer))

print("Данные вставлены.")

conn.commit()
cur.close()
conn.close()
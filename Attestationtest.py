import psycopg2
import torch
from torch import cosine_similarity
from transformers import BertTokenizer, BertModel

def encode_question(question):
    inputs = tokenizer(question, return_tensors='pt', max_length=512, truncation=True)
    outputs = model(**inputs)
    features = outputs.last_hidden_state[:, 0, :].squeeze()
    return features

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def find_most_similar_question(user_question, threshold=0.8):
    encoded_user_question = encode_question(user_question)

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="12345678",
        host="localhost"
    )
    cur = conn.cursor()

    cur.execute("SELECT question, question_vector, answer FROM qa_pairs")

    max_similarity = 0
    most_similar_question = None
    most_similar_answer = None

    for record in cur.fetchall():
        db_question, db_vector, answer = record
        db_vector_tensor = torch.tensor(db_vector).squeeze()
        similarity = cosine_similarity(encoded_user_question.unsqueeze(0), db_vector_tensor.unsqueeze(0), dim=1)
        similarity_value = similarity.item()

        if similarity_value > max_similarity and similarity_value > threshold:
            max_similarity = similarity.item()
            most_similar_question = db_question
            most_similar_answer = answer

    cur.close()
    conn.close()

    return most_similar_question, most_similar_answer

while True:
    user_input = input("Введите ваш вопрос (или 'exit' для выхода): ")
    if user_input.lower() == 'exit':
        break

    similar_question, answer = find_most_similar_question(user_input)
    if similar_question:
        print(f"Найденный вопрос: {similar_question}\nОтвет: {answer}\n")
    else:
        print("Похожий вопрос не найден.")
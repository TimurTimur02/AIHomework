from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

model = joblib.load("model.pkl")

# Маршрут для предсказания качества молока
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Получаем данные от клиента в формате JSON
        data = request.get_json()

        # Проверяем, что все необходимые признаки присутствуют в данных
        required_features = ["pH", "Temprature", "Taste", "Odor", "Fat", "Turbidity", "Colour"]
        for feature in required_features:
            if feature not in data:
                return jsonify({"error": f"Missing feature: {feature}"})

        # Преобразуем данные в формат, подходящий для модели
        features = [data[feature] for feature in required_features]

        # Вызываем модель для предсказания
        prediction = model.predict([features])

        # Возвращаем результат в формате JSON
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})

# Маршрут для отображения HTML-формы
@app.route('/')
def home_page():
    return render_template('input_form.html')

    # Запускаем приложение на порту 5000
if __name__ == "__main__":
    app.run(port=5000)

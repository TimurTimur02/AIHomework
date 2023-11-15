from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv('milknew.csv')

milk_data = data

# Создаем гистограммы для каждого признака
for feature in data.columns:
    plt.figure(figsize=(8, 6))
    sns.histplot(data=data, x=feature, kde=True)
    plt.title(f"Distribution of {feature}")
    plt.xlabel(feature)
    plt.ylabel("Frequency")
    plt.show()

label_encoder = LabelEncoder()
milk_data['Grade'] = label_encoder.fit_transform(milk_data['Grade'])

# Создаем матрицу корреляции
correlation_matrix = data.corr()

# Создаем тепловую карту для матрицы корреляции
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix")
plt.show()

# Отобразить закодированные метки
grade_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
print("Label Encoding for 'Grade':", grade_mapping)

numeric_columns = ["pH", "Temprature", "Taste", "Odor", "Fat ", "Turbidity", "Colour"]

scaler = StandardScaler()
scaled_numeric_data = scaler.fit_transform(milk_data[numeric_columns])

milk_data[numeric_columns] = scaled_numeric_data

# Определение функций и целевой переменной
X = milk_data.drop('Grade', axis=1)
y = milk_data['Grade']

# Разделение набора данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Отображение размера каждого набора
(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

"Модель логистической регрессии"
# Создание модели логистической регрессии
logistic_model = LogisticRegression(max_iter=1000, random_state=42)

# Обучение модели
logistic_model.fit(X_train, y_train)

# Составление прогнозов по тестовому набору
y_pred = logistic_model.predict(X_test)

# Оценка модели
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

'Модель Рандомный Лес и Градиентный бустинг(сравнение результатов)'
# Создание и обучение модели случайного леса
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Составление прогнозов и оценка модели случайного леса
rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
rf_classification_rep = classification_report(y_test, rf_pred)

# Создание и обучение модели градиентного бустинга
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X_train, y_train)

# Составление прогнозов и оценка модели повышения градиента
gb_pred = gb_model.predict(X_test)
gb_accuracy = accuracy_score(y_test, gb_pred)
gb_classification_rep = classification_report(y_test, gb_pred)

"""Random Forest
Точность: 99.53%
Отчёт по классификации:
Высокая точность, полнота и F1-оценка по всем классам.
Gradient Boosting
Точность: 99.06%
Отчёт по классификации:
Аналогично высокие показатели точности, полноты и F1-оценки по всем классам.
Эти результаты значительно лучше, чем у модели логистической регрессии. Модели случайного леса и 
градиентного бустинга демонстрируют высокую точность и могут быть очень эффективными 
для этой задачи классификации качества молока."""

# Определите параметры, которые вы хотите настроить и их значения
param_grid = {
    "n_estimators": [10, 50, 100, 200],
    "max_depth": [None, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "bootstrap": [True, False]
}

# Создайте модель случайного леса
rf_model = RandomForestClassifier()

# Создайте объект случайного поиска
random_search = RandomizedSearchCV(rf_model, param_distributions=param_grid, n_iter=100, cv=5, verbose=2,
                                   random_state=42, n_jobs=-1)

# Запустите случайный поиск на вашем датасете
random_search.fit(X_train, y_train)

# Получите лучшую модель
best_rf_model = random_search.best_estimator_

# Сохраните лучшую модель в файл
joblib.dump(best_rf_model, 'model.pkl')

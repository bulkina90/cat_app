from flask import Flask, render_template, url_for, jsonify
import requests
import json
from random import randint

cat_json_url = 'https://cats-paradise-f994f218e0ee.herokuapp.com/api/v1/cats'

def fetch_data (url):
    response = requests.get(url)
    return response.json()

def fetch_data_new():
    try:
        with open('cats.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print("Error reading cats.json:", e)
        return None


def collect_stat(url):
    #data = fetch_data(url)
    #print(url)
    data = fetch_data_new()
    total_num_of_cats = len(data)
    
    weights = [cat['weight'] for cat in data]
    min_weight = min(weights)
    max_weight = max(weights)
    avg_weight = sum(weights) / len(weights)
    
    life_spans = [cat['life_span'] for cat in data]
    min_life_span = min(life_spans)
    max_life_span = max(life_spans)
    avg_life_span = sum(life_spans) / len(life_spans)
    
    # Собираем статистику в формате JSON
    statistics = {
        "total_num_of_cats": total_num_of_cats,
        "weight": {
            "min": min_weight,
            "max": max_weight,
            "average": avg_weight
        },
        "life_span": {
            "min": min_life_span,
            "max": max_life_span,
            "average": avg_life_span
        }
        # Дополнительные статистические данные могут быть добавлены здесь
    }
    
    return statistics

app = Flask(__name__)

@app.route('/')
def home():
    data = fetch_data(cat_json_url)
    #cat_name = data[0]['name'] 
   # print("DEBUG", cat_name, data[0])
    # random_index = randint(0, len(data) - 1)  # Выбираем случайный индекс
    # cat_name = data[random_index]['name']  # Получаем имя кота по выбранному индексу
    return render_template('index.html', cats=data)


@app.route('/cat')
def cat():
    #data = fetch_data(cat_json_url)
    data = fetch_data_new()
    random_index = randint(0, len(data) - 1)  # Выбираем случайный индекс
    cat = data[random_index]  # Получаем имя кота по выбранному индексу
    print(cat)
    return render_template('cat.html', cat=cat)

@app.route('/statistic')
def stat():
    data = collect_stat(cat_json_url)
    print(data)
    return render_template('statistic.html', data=data)


@app.route('/info')
def info():
    data = ""
    return render_template('info.html', data=data)

@app.route('/api/v1/cats')
def get_cats():
    data = fetch_data_new()
    return jsonify(data)


@app.route('/generate_json', methods=['GET'])
def generate_json():
    # Генерация JSON-данных (замените этот код на вашу логику генерации JSON)
    json_data = fetch_data_new()

    # Преобразование JSON в текстовый формат
    json_text = json.dumps(json_data, indent=2)

    # Определение имени файла
    filename = 'cats.json'

    # Отправка JSON в виде файла для загрузки
    response = jsonify(json_data)
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename
    response.headers['Content-Type'] = 'application/json'
    return response
 

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5000)
 
# upload application tto github, push it


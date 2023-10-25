import requests
from bs4 import BeautifulSoup
import json

# Функция для получения комментариев на странице
def get_comments_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = []

    for comment in soup.find_all('span', class_='text'):
        comments.append(comment.get_text())

    return comments

# Функция для получения всех комментариев на нескольких страницах
def get_all_comments(base_url, num_pages):
    all_comments = []
    
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}/page/{page_num}/"
        comments = get_comments_on_page(url)
        all_comments.extend(comments)
    
    return all_comments

# Функция для подсчета комментариев по категориям
def count_comments_by_category(comments):
    category_count = {}

    for comment in comments:
        # Используем первое слово в комментарии как категорию
        words = comment.split()
        if words:
            category = words[0]
            if category in category_count:
                category_count[category].append(comment)
            else:
                category_count[category] = [comment]

    return category_count

if __name__ == "__main__":
    base_url = "http://quotes.toscrape.com"
    num_pages = int(input("Введите количество страниц: "))
    
    comments = get_all_comments(base_url, num_pages)
    
    # Подсчет комментариев по категориям
    category_count = count_comments_by_category(comments)
    
    # Запись результата в JSON файл
    with open('comments_by_category.json', 'w', encoding='utf-8') as file:
        json.dump(category_count, file, ensure_ascii=False, indent=4)

    # Открываем JSON-файл и загружаем данные
    with open('comments_by_category.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Выводим данные
    print(json.dumps(data, indent=4, ensure_ascii=False))


from django.shortcuts import render
import json
import os

def home(request):
    return render(request, 'shop/home.html')

def about(request):
    return render(request, 'shop/about.html')

def store(request):
    return render(request, 'shop/store.html')

def load_qualifications():
    try:
        # Попробуем сначала загрузить файл из корня проекта Django
        json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dump.json')
        if not os.path.exists(json_path):
            # Если не найден, попробуем загрузить из корня всего проекта
            json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'dump.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            print(f"Загружен файл: {json_path}")
            return json.load(f)
    except FileNotFoundError:
        print("Файл dump.json не найден")
        return []
    except json.JSONDecodeError:
        print("Некорректный формат JSON в файле dump.json")
        return []
    
def qualification_list(request):
    qualifications = load_qualifications()
    return render(request, 'shop/qualification_list.html', {'qualifications': qualifications})

def qualification_detail(request, id):
    qualifications = load_qualifications()
    
    qualification = next((q for q in qualifications if q.get('id') == id), None)
    
    if qualification:
        return render(request, 'shop/qualification_detail.html', {'qualification': qualification})
    else:
        return render(request, 'shop/error.html', {'message': f"Квалификация с ID '{id}' не найдена"})
# Subtracker

Навчальний проєкт на Django (відстежувач платних підписок).

## Інструкція з запуску:

1. Клонувати репозиторій:
   git clone https://github.com/Xirobrat/subtracker.git
   cd subtracker

2. Створити та активувати віртуальне оточення:
   python -m venv venv
   # На Windows:
   venv\Scripts\activate

3. Встановити залежності:
   pip install -r requirements.txt

4. Застосувати міграції та запустити сервер:
   python manage.py migrate
   python manage.py runserver

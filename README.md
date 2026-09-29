Subtracker
Навчальний проєкт на Django (відстежувач платних підписок).

Інструкція з запуску:
Клонувати репозиторій:
git clone https://github.com/Xirobrat/subtracker.git
cd subtracker

Створити та активувати віртуальне оточення:
python -m venv venv

На Windows:
venv\Scripts\activate

На Linux / macOS:
source venv/bin/activate

Встановити залежності:
pip install -r requirements.txt

Застосувати міграції:
python manage.py migrate

Запустити сервер:
python manage.py runserver

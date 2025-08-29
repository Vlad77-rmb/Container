# Создаем docker-compose.yml и запускаем контейнер с MySQL командой ниже (должен быть установлен и запущен Docker)
docker-compose up -d mysql

# Создаем файл .env с настройками подключения к базе данных
Устанавливаем зависимости Python командой:
pip install -r requirements.txt

# Так же запускаем скрипт инициализации базы данных
python scripts/init_db.py

# После запускаем наше приложение командой ниже и переходим на http://localhost:8000 , после чего на http://localhost:8000/docs
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Для остановки контейнера вводим команду 
docker-compose down

Для входа используем логин: user1 и пароль: password1

1. Поиск контейнеров
GET /api/containers - все контейнеры (первые 50)

GET /api/containers?q=ABC - поиск по части номера

2. Поиск по стоимости
GET /api/containers/by-cost?cost=1000.50 - по точной стоимости

GET /api/containers/by-cost?min_cost=1000&max_cost=2000 - по диапазону

3. Добавление контейнера
POST /api/containers - добавление нового контейнера

Тело запроса:

json
{
  "container_number": "ABCU1234567",
  "cost": 1000.50
}

# Формат номера контейнера:
Номер контейнера должен соответствовать формату: Три заглавные латинские буквы, Буква "U", Семь цифр

Пример: WEQU8764678

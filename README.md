# GuardianWayBE

GuardianWayBE — це бекендна частина проекту GuardianWay, яка відповідає за обробку та збереження інформації про дорожні вибоїни та світлофори.

## Зміст

- [Про проект](#про-проект)
- [Особливості](#особливості)
- [Технології](#технології)
- [Встановлення](#встановлення)
- [Запуск](#запуск)
- [Структура проекту](#структура-проекту)
- [Автори](#автори)
- [Ліцензія](#ліцензія)

## Про проект

GuardianWayBE забезпечує серверну логіку для GuardianWay. Вона включає в себе обробку даних, авторизацію користувачів та аналітику. Ця частина проекту реалізована на Python Flask та використовує PostgreSQL для збереження даних.

## Особливості

- Обробка даних про дорожні вибоїни та світлофори
- Авторизація та аутентифікація користувачів
- Підтримка WebSocket для реального часу

## Технології

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/)

## Встановлення

Для встановлення проекту виконайте наступні кроки:

1. Клонуйте репозиторій:
    ```bash
    git clone https://github.com/yourusername/GuardianWayBE.git
    ```

2. Перейдіть в директорію проекту:
    ```bash
    cd GuardianWayBE
    ```

3. Створіть віртуальне середовище та активуйте його:
    ```bash
    python -m venv venv
    source venv/bin/activate  # для Windows використовуйте venv\Scripts\activate
    ```

4. Встановіть необхідні залежності:
    ```bash
    pip install flask flask-sqlalchemy flask-socketio
    ```

5. Створіть локальну базу даних PostgreSQL та налаштуйте файл `app.py`:
    - Створіть нову базу даних в PostgreSQL.
    - Внесіть конфігурацію підключення до бази даних в файл `app.py`:
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/yourdatabase'
    ```

## Запуск

Для запуску проекту виконайте команду:
```bash
python app.py
```
Сервер буде доступний за адресою http://localhost:5000/.

## Структура проекту
  app - основні файли додатку
    analytics - модуль аналітики
    auth - модуль авторизації
    data_processing - модуль обробки даних
    __init__.py - файл ініціалізації модуля
  resources - додаткові ресурси
  .gitignore - файл ігнорування Git
  app.py - головний файл додатку

## Автори
  Заневич Юлія


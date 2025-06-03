import os
import csv
import time
import uuid
import random
import logging

from logging.handlers import RotatingFileHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        RotatingFileHandler("logs/app.log", maxBytes=1, backupCount=0),
        logging.StreamHandler()
    ]
)

# Возможные значения
event_types = ['login', 'logout', 'search', 'add_to_cart', 'purchase']
levels = ['INFO', 'WARNING', 'ERROR']
traffic_sources = ['MOBILE', 'WEB', 'DESKTOP']
countries = ['RU', 'BY', 'KZ', 'UZ', 'AR']

# Файл для хранения session_id
SESSION_ID_FILE = "session_id.csv"


# Создание файла с session_id при первом запуске
def initialize_session_ids():
    if not os.path.exists(SESSION_ID_FILE):
        print("Creating new session_id.csv file with 1000 unique session IDs")
        session_ids = [str(uuid.uuid4()) for _ in range(1000)]
        with open(SESSION_ID_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['session_id'])  # Заголовок
            writer.writerows([[sid] for sid in session_ids])

# Чтение session_id из файла
def read_session_ids():
    with open(SESSION_ID_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропускаем заголовок
        return [row[0] for row in reader]


# Генератор события
def generate_event(session_ids):
    # session_id = str(uuid.uuid4())
    session_id = random.choice(session_ids)
    event_type = random.choice(event_types)
    traffic_source = random.choice(traffic_sources)
    country = random.choice(countries)
    
    # metadata = f"user_action={event_type};product_id={random.randint(1000, 9999)}"
    metadata_parts = [""]
    
    if event_type == 'add_to_cart':
        metadata_parts.append(f"product_id={random.randint(1000, 9999)}")
    elif event_type == 'purchase':
        metadata_parts.append(f"order_id={random.randint(10000, 99999)}")
    elif event_type == 'search':
        metadata_parts.append(f"search_query={random.choice(['пылесос', 'телефон', 'ноутбук', 'часы', 'камера'])}")
    
    metadata_parts.append(f"country={country}")

    level = random.choices(levels, weights=[0.7, 0.2, 0.1])[0]
    log_message = (
        f"session_id={session_id} | "
        f"traffic_source={traffic_source} | "
        f"event_type={event_type}"
        
        f"{' | '.join(metadata_parts)}"
    )

    return level, log_message


if __name__ == "__main__":
    # Количество создаваемых записей в секунду
    depth_of_creation = 1
    if depth_of_creation <= 0: depth_of_creation = 1
    creation_interval = 1.0 / float(depth_of_creation)
    
    # Инициализация session_id
    initialize_session_ids()
    session_ids = read_session_ids()

    try:
        while True:
            level, message = generate_event(session_ids)
            if level == 'INFO':
                logging.info(message)
            elif level == 'WARNING':
                logging.warning(message)
            else:
                logging.error(message)
            time.sleep(creation_interval)  # генерировать событие каждую секунду
    except KeyboardInterrupt:
        print("Application stopped manually.")
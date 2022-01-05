import logging
import os
import sys

log = logging.getLogger("client")
log.setLevel(logging.INFO)

sys.path.append('../')

_format = logging.Formatter("%(asctime)-25s %(levelname)-10s %(module)s %(message)s")

log_file_name = os.path.dirname(os.path.abspath(__file__))
log_file_name = os.path.join(log_file_name, f'{log.name}.log')

# Добавить несколько обработчиков в регистратор
file_handler = logging.FileHandler(log_file_name, encoding='utf-8')
file_handler.setFormatter(_format)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(_format)

log.addHandler(file_handler)
log.addHandler(stream_handler)
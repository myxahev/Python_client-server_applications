import json
import logging
import sys
import socket
import time

from utils import load_configs, send_message, get_message
import log.client_log_config

CONFIGS = dict()
log_client = logging.getLogger("client")


class PrintLog:
    def __init__(self):
        pass

    def __call__(self, func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            log_client.info(f'{func.__name__} - {res}')
            return res

        return decorated


@PrintLog()
def create_presence_message(account_name):
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    return message


@PrintLog()
def handle_response(message):
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            return '200 : OK'
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except IndexError:
        server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_PORT')
    except ValueError:
        log_client.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        transport.connect((server_address, server_port))
        presence_message = create_presence_message('Guest')
        send_message(transport, presence_message, CONFIGS)

        response = get_message(transport, CONFIGS)
        hanlded_response = handle_response(response)
        log_client.info(f'Ответ от сервера: {response}')
        log_client.info(hanlded_response)
    except (ValueError, json.JSONDecodeError):
        log_client.error('Ошибка декодирования сообщения')
    except ConnectionRefusedError as e:
        log_client.error(e.strerror)


if __name__ == '__main__':
    main()
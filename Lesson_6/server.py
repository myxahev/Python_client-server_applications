import json
import logging
import sys
import socket

from utils import load_configs, get_message, send_message
import log.server_log_config


CONFIGS = dict()
log_server = logging.getLogger("server")


def print_log(func):
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        log_server.info(f'{func.__name__} {r}')
        return r
    return wrapper


@print_log
def handle_message(message):
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        return {CONFIGS.get('RESPONSE'): 200}
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


def main():
    global CONFIGS
    CONFIGS = load_configs()
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = CONFIGS.get('DEFAULT_PORT')
        if not 65535 >= listen_port >= 1024:
            raise ValueError
    except IndexError:
        log_server.critical('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        log_server.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        log_server.critical('После \'a\'- необходимо указать адрес для ')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        client, client_address = transport.accept()
        try:
            message = get_message(client, CONFIGS)
            response = handle_message(message)
            log_server.info(message)
            send_message(client, response, CONFIGS)
            log_server.info(response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            log_server.error('Принято некорректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()

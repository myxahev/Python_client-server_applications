import logging
import select
import chat.chat as chat
import chat.jim as jim
import log.client_log_config

logger = logging.getLogger('chat.client')


def main():
    logger.debug('App started')

    parser = chat.create_parser()
    namespace = parser.parse_args()

    client_name = input('Введите имя: ')

    sock = chat.get_client_socket(namespace.addr, namespace.port)
    serv_addr = sock.getpeername()
    start_info = f'Connected to server: {serv_addr[0]}:{serv_addr[1]}'
    print(start_info)
    logger.info(start_info)

    jim.PRESENCE['user']['account_name'] = client_name
    try:
        chat.send_data(sock, jim.PRESENCE)
    except ConnectionResetError as e:
        logger.error(e)
        sock.close()
        exit(1)

    while True:
        r = []

        try:
            r, w, e = select.select([sock], [], [], 1)
        except Exception as e:
            pass

        if sock in r:
            try:
                data = chat.get_data(sock)
            except ConnectionResetError as e:
                logger.error(e)
                break

            if data['response'] != '200':
                logger.debug('App ending')
                break

            if 'messages' in data:
                for message in data['messages']:
                    print(f'{message["time"]} - {message["from"]}: {message["message"]}')

        else:
            msg = input('Введите сообщение ("exit" для выхода): ')
            if msg:
                jim.MESSAGE['message'] = msg

                try:
                    chat.send_data(sock, jim.MESSAGE)
                except ConnectionResetError as e:
                    logger.error(e)
                    break

    sock.close()


if __name__ == '__main__':
    main()
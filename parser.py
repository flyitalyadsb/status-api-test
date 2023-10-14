import argparse


def host_and_ports(string):
    try:
        parts = string.split(':')
        if len(parts) != 2:
            raise ValueError()
        return parts[0], int(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{string} should be in this formats: 'host:tcp_port'")


def server_main(parser):
    parser.add_argument('--server-listen',
                        help="Specify the address and port for the server to listen on (format: 'host:port').",
                        type=host_and_ports,
                        default="0.0.0.0:83")


def readsb_input(parser):
    parser.add_argument('--receivers-json',
                        help="Path to the receivers JSON data file.",
                        default="/json/ingest/receivers.json")


def mlat_server_input(parser):
    parser.add_argument('--clients-mlat-json',
                        help="Path to the mlat clients JSON data file.",
                        default="/mlat/clients.json")


def get_parser():
    parser = argparse.ArgumentParser(description="MyFlyitalyadsb")
    server_main(parser.add_argument_group("Main options"))
    readsb_input(parser.add_argument_group('Readsb options'))
    mlat_server_input(parser.add_argument_group('Mlat server options'))
    return parser


def get_args():
    parser = get_parser()
    args = parser.parse_args()
    return args

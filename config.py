from argparse import Namespace
from parser import get_args


class Config:
    def __init__(self, args: Namespace) -> None:
        # server_main
        self.host: str = args.server_listen[0]
        if args.server_listen[1]:
            self.port: int = int(args.server_listen[1])

        self.clients_json: str = args.clients_json

        # mlat_server_input
        self.clients_mlat_json: str = args.clients_mlat_json


args_gotten = get_args()
config: Config = Config(args_gotten)

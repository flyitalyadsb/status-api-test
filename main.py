import asyncio
import re
import socket

import aiofiles
import uvicorn
from fastapi import FastAPI, Request, Query
from orjson import orjson
from typing import Optional

from config import config

amIFeeding_bp = FastAPI()


async def read_file(filename):
    async with aiofiles.open(filename, "r") as file:
        data = await file.read()

        parsed_data = orjson.loads(data)
        if filename == config.clients_json:
            return parsed_data["clients"]
        else:
            return parsed_data


def convert_to_ip(input_string):
    ip = "0.0.0.0"
    if input_string in ["mlat-server"]:
        return ip
    ip_match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', input_string)
    hostname_match = re.search(r'\b\w+\.\w+\b', input_string)
    if ip_match:
        ip = ip_match.group(0)
        #print(f"IP found: {ip}")
    elif hostname_match:
        hostname = hostname_match.group(0)
        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            print(f"No ip found for hostname: {hostname}")
    else:
        print("No IP address or hostname found")

    return ip


def proxy_ip(request: Request):
    forwarded_ip = request.headers.get("X-Forwarded-For")
    client_ip = forwarded_ip if forwarded_ip else request.client.host
    return client_ip


async def am_i_feeding_debug(request_ip):
    beast = False
    mlat = False

    clients_readsb, clients_mlat = await asyncio.gather(read_file(config.clients_json),
                                                        read_file(config.clients_mlat_json))
    for client in clients_readsb:
        if convert_to_ip(client[1]) == request_ip:
            beast = True
            client_mlat_data = next(
                (c for c in clients_mlat.values() if c["uuid"] and (c["uuid"] == client[0] or client[0] in c["uuid"])),
                None)
            if client_mlat_data:
                mlat = True

    return beast, mlat


@amIFeeding_bp.api_route('/am_i_feeding', methods=["GET"])
async def am_i_feeding(request: Request, ip: Optional[str] = Query(None)):
    if ip:
        request_ip = ip
    else:
        request_ip = proxy_ip(request)
    beast, mlat = await am_i_feeding_debug(request_ip)
    result = {"feeding": {"beast": beast, "mlat": mlat}}
    print(f"ip: {request_ip}, result: {result['feeding']}")
    return result

async def fastapi_start():
    configuration = uvicorn.Config(amIFeeding_bp, host=config.host, port=config.port, loop="auto")
    server = uvicorn.Server(configuration)
    await server.serve()


asyncio.run(fastapi_start())

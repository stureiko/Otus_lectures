from fastapi import FastAPI
from contextlib import asynccontextmanager
from netifaces import interfaces, ifaddresses, AF_INET
import socket

app = FastAPI()

# create a route
@app.get("/")
def index():
    return {"message": "FastAPI Hello World"}

@app.get("/info")
def info():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

@app.get("/ip")
def get_ip():
    ip_addr = {}
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        if addresses != ['No IP addr']:
            ip_addr[ifaceName] = addresses
    return ip_addr
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 22:54:28 2023

@author: floasp
"""

import socket
import random

# TODO: edit for your use
HOST = '<enter ip address or domain>' # The remote host
PORT = 00000                          # The same port as used by the server
sock = None
    

def random_req_id():
    return random.randint(0, 2**16-1)

def create_rcon_message(reqID: int, mtype: int, payload: str):
    bin_reqID = int(reqID).to_bytes(4, "little")
    bin_mtype = int(mtype).to_bytes(4, "little")
    bin_payload = bytearray(payload, "ascii")
    bin_pad = int(0).to_bytes(1, "little")
    
    bin_length = (4 + 4 + len(bin_payload) + 1).to_bytes(4, "little")
    
    message = bin_length + bin_reqID + bin_mtype + bin_payload + bin_pad
    
    return message

def create_login(password):
    message = create_rcon_message(random_req_id(), 3, password)
    return message

def create_command(comm):
    message = create_rcon_message(random_req_id(), 2, comm)
    return message

def send_message(message):
    check = sock.sendall(message)
    data = sock.recv(1024)
    return data

def get_type(bin_message):
    bin_type = bin_message[8:12]
    int_type = int.from_bytes(bin_type, "little")
    return int_type

def get_length(bin_message):
    bin_len = bin_message[0:4]
    int_len = int.from_bytes(bin_len, "little")
    return int_len

def get_string(bin_message):
    msg_len = get_length(bin_message)
    bin_payload = bin_message[12:12+msg_len-4-4-1]
    message = bin_payload.decode("ascii")
    return message
    
def print_response(bin_message):
    print(get_string(bin_message))
    
    
def auth(password):
    message = create_login("minecraft")
    res =  send_message(message)
    
    int_type = get_type(res)
    if int_type != -1:
        return True
    return False

def command(comm):
    message = create_command(comm)
    res =  send_message(message)
    
    int_type = get_type(res)
    if int_type == 0:
        print_response(res)
    elif int_type == -1:
        print("error sending command")
    
    
if __name__ == "__main__":

    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # connect to server
        sock.connect((HOST, PORT))

        # authenticate with rcon password
        if auth("<enter password here>"):
            # send commands to the server
            command("list")
            command("say hello from RCON!")
            
    finally:
        sock.close()
        
        

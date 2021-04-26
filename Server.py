#server

import socket
import os
import time

IP = input("Enter IP address:")

port = int(input("Enter port number:"))

buffer_size = 4096 #size to be sent
addr = (IP, port)
SEPARATOR = "<SEPARATOR>"


#Create a UDP socket to know if the client want UDP or TCP for file transfer
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(addr)
UDPorTCP = s.recvfrom(buffer_size)
choice = UDPorTCP[0].decode("utf-8")
print(choice)
s.close()

if choice == "UDP": #UDP server: Lynn Fanous
    
    print ("...server UDP...")
    my_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creating UDP socket
    my_socket.bind(addr) #binding step
     
    T1 = time.time() #initial time
    
    file, address = my_socket.recvfrom(buffer_size) 
    filesize, address = my_socket.recvfrom(buffer_size)
    
    size = int(filesize.decode("utf-8")) #transforming the received file size to integer
    
    filename = os.path.basename(file)
    
    f = open(filename, 'wb')
    
    i = 0
    j = 0
    
    while i < size: #while in the file
        j = j+1
        data = my_socket.recvfrom(buffer_size) #syntax to receive the data
        if not data:
            break
        f.write(data[0]) 
        i+=len(data[0])
        
            
    T2 = time.time() # T2 is when we receive the data from the server in seconds
    RTT = T2 - T1 #RTT is the difference between initial time and final time
    
    print("File received successfully!")
    
    my_socket.close()
    f.close()
    
    
    bitrate = (size*8)/RTT #bitrate formula
    print("bitrate =",bitrate,"bps")


else: #TCP server: Hasan Ramadan

    print("...Server TCP...")
    tcp_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creating TCP socket
    tcp_socket.bind(addr) #binding step

    tcp_socket.listen(5) #listening 
    print("…Listening…")

    client_socket, address = tcp_socket.accept() #accept connection request

    print("Client is connected.") #confirmation message
    T1 = time.time()
    receivedFile = client_socket.recv(buffer_size).decode()
    fileName, fileSize = receivedFile.split(SEPARATOR) #storing the received filename and size in variables

    fileName = os.path.basename(fileName) 
    fileSize = int(fileSize) #transforming the fileSize to integer

    
    with open(fileName, "wb") as f: #open the file in write mode
        while 1: #while true
            read_bytes = client_socket.recv(buffer_size)
            if not read_bytes:
                break
            f.write(read_bytes) #write the content of the file
             
    T2 = time.time() # T2 is when we receive the data from the server in milliseconds
    RTT = T2 - T1 #RTT is the difference
    
    client_socket.close() 
    tcp_socket.close()
    
    print("File received successfully!")
    bitrate = (fileSize*8)/RTT # bitrate (bps)
    print("the bitrate is: ", bitrate)

"""
Links used:
https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
https://github.com/nikhilroxtomar/Multithreaded-File-Transfer-using-TCP-Socket-in-Python/blob/main/server.py
https://www.youtube.com/watch?v=MEcL0-3k-2c


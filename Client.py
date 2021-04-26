#client

import socket
import os
import time


# Choose host IP and port number to send and receive data
IP = input("Enter IP address: ") 

port = int(input("Enter port: "))

addr= (IP, port)
SEPARATOR = "<SEPARATOR>"
buffer_size = 4096 #size to be sent


UDPorTCP = 0

#Choose UDP or TCP
while (UDPorTCP != "UDP" and UDPorTCP != "TCP"):
    UDPorTCP = input("Choose UDP or TCP: ") #allows the client to choose 
    if (UDPorTCP != "UDP" and UDPorTCP != "TCP"): #if client enters an unkown protocol
        print("Error!")
        print("Please enter 'UDP' or 'TCP':")
#Send your choice to the server using UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(UDPorTCP.encode("utf-8"), addr)
sock.close()


if UDPorTCP == "UDP": #UDP client: Elie Mina
    print("...Client UDP...")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP socket
    
    filename = input("Enter file name with extension:") #Enter the file to send to the server
    filesize = os.path.getsize (filename) # this function gives us the size of the file in bytes
    size = int(filesize)
    
    T1 = time.time() # T1 is when we send the file to the server
    print("Started at: ",T1)
    s.sendto(filename.encode("utf-8"), addr)
    s.sendto(str(filesize).encode("utf-8"),addr)
    
    print("...Sending to server...")
    
    f = open(filename, 'rb') #read content of file
    
    i = 0
    
    while i <= filesize: #while in the file
    
        data = f.read(buffer_size) #read the content of the file and store it in variable
        if not (data):
            break
        s.sendto(data,addr) #send the data to the server
        i += len(data)
          
    T2 = time.time()
    print("Finished at:",T2)
    RTT = T2 - T1 #RTT is the difference
    print("RTT = ",RTT)
    s.close()
    f.close()
    print("File sent successfully!")
    
    bandwidth = (size*8) / RTT
    print ("Bandwith = ", bandwidth, " bps")

else: #TCP client: Karim Safar
    print("...Client TCP...")
    filename = input("Enter the file name with extension: ") #input file name
    
    filesize = int(os.path.getsize(filename)) # size of file in bytes
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #client socket
   
    
    print("...Connecting to server…") #connecting client to server
    client.connect(addr)
    
    print("Connected.")
    
    client.send(f"{filename}{SEPARATOR}{filesize}".encode("utf-8")) #sending file name and size
    
    T1 = time.time() # T1 is when we send the file to the server
    
    print("...Sending to server...")
    
    with open(filename, 'rb') as f:
        while 1:
            read_bytes = f.read(buffer_size)
            if not read_bytes:
                break
            client.sendall(read_bytes)
          
    print ("File sent successfully!")         
    T2 = time.time()  # T2 is when we receive the data from the server
    RTT = T2 - T1 #RTT is the difference
    client.close()
    
    bandwidth = (filesize*8) / RTT  
    print ("Bandwith = ", bandwidth, " bps")

"""
Links used:
https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
https://github.com/nikhilroxtomar/Multithreaded-File-Transfer-using-TCP-Socket-in-Python/blob/main/server.py
https://www.youtube.com/watch?v=MEcL0-3k-2c


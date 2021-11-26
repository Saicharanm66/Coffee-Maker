import struct
import sys
from socket import *
# create UDP socket
udp_soc = socket(AF_INET, SOCK_DGRAM)
server_port = 16000
try:
     udp_soc.bind(('', server_port))
except OSError as message:
     print('Data is not being recieved')
     sys.exit()
udp_soc.settimeout(5)

print('Data is receiving')

def pkt():
     # list to check missed message
     pct_list=[]
     for i in range(10001, 10047):
          pct_list.append(i)
     return pct_list
# creating empty list to append received message sequence numbers
pack_list = []
total_data = 0
def to_print(seq,siz,add):
     # printing required messages
     print(f" Sequence number of data = { seq_num };")
     print(f" Data size = { data_size }")
     print(f" Client's IP address and port = { clientAddress }")
def update_list(msg):
     # updating sequence number
     pack_list.append(msg)
     return pack_list

pkt_list=pkt()

while True:
     try:
          inform, clientAddress = udp_soc.recvfrom(2048)
          # unpacking the recieved message
          message = inform[0:8]
          message_2 = struct.unpack('ii', message)
          # size of data
          data_size = message_2[1] - 8
          total_data += data_size
          # Sequence number of present message
          seq=int(message_2 [0])
          print(seq)
          seq_num = f"{ message_2 [0]} "
          print(pack_list)
          print(pack_list[-1])
          #update sequence
          #pack_list = update_list(message_2[0])
          if pack_list[-1] > seq:
               error_data.append(pack_list[-1]+1)
               error_data.append(seq)
          pack_list = update_list(seq)
          #printing received packets
          trans_mess = f" Packet '{message_2 [0]} ' has been received at receiver side "

          #printing information
          to_print(seq_num,data_size,clientAddress)
          udp_soc.sendto(trans_mess.encode(), clientAddress)

     except timeout and OSError:
          udp_soc.close()
          print("timed out")
          break
     
print("Total data recieved succesfully")

# print received data
print(f"data received : {total_data}")

# packets lost
total_pck_loss = list(set(pkt_list) - set(pack_list))
print(f"packets lost : {total_pck_loss}")


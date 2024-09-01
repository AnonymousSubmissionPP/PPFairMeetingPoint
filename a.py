import socket
import pickle
import base64
from MPC import shares
import pandas as pd


import time



nbrparticipants = int(input("Enter the number of participants: "))




options=[{'number': '1',
  'name': 'Helsinki Cathedral',
  'location': [60170928, 24952069]},
 {'number': '2',
  'name': 'Uspenski Cathedral',
  'location': [60168652, 24959949]},
 {'number': '3',
  'name': 'Temppeliaukio Church',
  'location': [60173107, 24925212]},
 {'number': '4', 'name': 'Kamppi', 'location': [60169432, 24933301]},
 {'number': '5', 'name': 'Market Square', 'location': [60167824, 24953774]},
 {'number': '6',
  'name': 'Sibelius Monument',
  'location': [60182257, 24913411]},
 {'number': '7',
  'name': 'Helsinki Central Railway Station',
  'location': [60171974, 24941357]},
 {'number': '8',
  'name': 'Ateneum Art Museum',
  'location': [60170293, 24944244]},
 {'number': '9',
  'name': 'Kiasma Museum of Contemporary Art',
  'location': [60171798, 24936990]},
 {'number': '10',
  'name': 'National Museum of Finland',
  'location': [60174985, 24931964]},
 {'number': '11',
  'name': 'Helsinki Central Park',
  'location': [660225652, 24917903]},
 {'number': '12',
  'name': 'Linnanmäki Amusement Park',
  'location': [60192846, 24939907]},
 {'number': '13',
  'name': 'Helsinki Olympic Stadium',
  'location': [60188326, 24926557]},
 {'number': '14',
  'name': 'Töölönlahti Park',
  'location': [60177671, 24936545]},
 {'number': '15', 'name': 'Circus Helsinki', 'location': [60187351, 24970442]},
 {'number': '16', 'name': 'Esplanade Park', 'location': [60167596, 24947697]},
 {'number': '17',
  'name': 'Helsinki Ice Hall',
  'location': [60189381, 24922522]},
 {'number': '18',
  'name': 'Roihuvuori Cherry Tree Park',
  'location': [60197344, 25048467]},
 {'number': '19',
  'name': 'Mannerheim Museum',
  'location': [60159043, 24960597]},
 {'number': '20',
  'name': 'Kumpula Campus Helsinki',
  'location': [60205139, 24962347]},
 {'number': '21', 'name': 'Löyly', 'location': [60152188, 24930316]}]

for i, option in enumerate(options):
    op=option["name"]
    print(f"{i+1}. {op}")
choice = int(input("Enter your location: "))
selected = options[choice-1]
loc=selected["name"]
print(f"You selected {loc}.")
cor=selected["location"]
convcorx=cor[0]/(10**(6))
convcory=cor[1]/(10**(6))
print(f"With coordinates{[convcorx,convcory]}.")
mylocation=[convcorx,convcory]
x=cor[0]
y=cor[1]



#Compute coordinates shares 





Xshares=shares(nbrparticipants,x)
Yshares=shares(nbrparticipants,y)

Bxshare=Xshares[0]
Cxshare=Xshares[1]

Byshare=Yshares[0]
Cyshare=Yshares[1]


Axshare=Xshares[2]
Ayshare=Yshares[2]


## Socket communication



# Define the IP address and port numbers
IP_ADDRESS = '127.0.0.1'
PORT1 = 8081
PORT2 = 8082
# Create the server sockets
server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.bind((IP_ADDRESS, PORT1))
server_socket1.listen()
server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2.bind((IP_ADDRESS, PORT2))
server_socket2.listen()


# Accept the connection with Charlie
client_socket1, address1 = server_socket1.accept()
print(f"Connection established with Charlie with address {address1}")

# Send coordinates share to Charlie
StoC=[Cxshare,Cyshare]
Cmessage = pickle.dumps(StoC)

client_socket1.send(Cmessage)
print(f"Alice sent her coordinates share to Charlie ({len(Cmessage)} bytes)")



# Accept the connection with Bob
client_socket2, address2 = server_socket2.accept()
print(f"Connection established with Bob with address {address2}")

# Send coordinates share to Bob
StoB=[Bxshare,Byshare]
Bmessage = pickle.dumps(StoB)
client_socket2.send(Bmessage)
print(f"Alice sent her coordinates share to Bob ({len(Cmessage)} bytes)")


# Receive response from Bob
rBmessage = client_socket2.recv(6048)
Bobmsg1=pickle.loads(rBmessage)
print(f"Received coordinates share from Bob: {Bobmsg1}")

# Receive response from Charlie
rCmessage = client_socket1.recv(6048)
Charmsg1=pickle.loads(rCmessage)
print(f"Received coordinates share from Charlie: {Charmsg1}")




#Sum shares 

Xa=Axshare+Bobmsg1[0]+Charmsg1[0]
Ya=Ayshare+Bobmsg1[1]+Charmsg1[1]


# Send sum of shares to Bob
StoB2=[Xa,Ya]
Bmessage2 = pickle.dumps(StoB2)

client_socket2.send(Bmessage2)
print(f"Alice sent her sum of shares to Bob: {StoB2}" )

# Receive centroid from Bob
Cmessage = client_socket2.recv(6048)
center_sp=pickle.loads(Cmessage)
center=center_sp[0]
selected_places_df=center_sp[1]
print(f"Received centroid from Bob: {center}")
SP=pd.DataFrame(selected_places_df)
NN=SP["name"]
print(f"Received selected places from Bob: {NN}")



#Compute distances

from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Compute the differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula for distance calculation
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers (along the surface of the sphere)
    distance = R * c

    return distance

#Compute distances to center
list_distances=[]
for i in selected_places_df:
    list_distances.append({"name":i['name'],"Distance (Km)": haversine(mylocation[0], mylocation[1], i['lat'], i['lon'])})
    
#Sort distances    




df = pd.DataFrame(list_distances)

# Sorting wrt distance
df_sorted_by_dist = df.sort_values(by='Distance (Km)')
df_with_index = df_sorted_by_dist.copy()
df_with_index['Index'] = df_sorted_by_dist.index
df_with_index['Score'] = range(len(df_with_index), 0,-1)
df_Score=df_with_index.sort_values(by='Index')
df_Score=df_Score.drop('Index', axis=1)
print(f"Distances from location and score")
print(df_Score)


#Compute scores shares

Bshares_scores=[]
Cshares_scores=[]
Ashares_scores=[]

for i in df_Score["Score"]:
    T=shares(nbrparticipants,i)
    Ashares_scores.append(T[0])
    Bshares_scores.append(T[1])
    Cshares_scores.append(T[2])
    
# Send scores share to Charlie

Csharescore = pickle.dumps(Cshares_scores)
client_socket1.send(Csharescore)
print(f"Alice sent her scores share to Charlie")
# Send scores share to Bob
Bsharescore = pickle.dumps(Bshares_scores)
client_socket2.send(Bsharescore)
print(f"Alice sent her scores share to Bob")

# Receive response from Charlie
ScorfromC = client_socket1.recv(6048)
Cscors=pickle.loads(ScorfromC)

print(f"Alice received scores share from Charlie")
# Receive response from Bob
ScorfromB = client_socket2.recv(6048)
Bscors=pickle.loads(ScorfromB)
print(f"Alice received scores share from Bob")
#Sum of scors shares

A_Sc_sum=[x + y + z for x, y, z in zip(Ashares_scores, Bscors,Cscors)]

#Send scors sum to Bob

SumScorsForBob = pickle.dumps(A_Sc_sum)
client_socket2.send(SumScorsForBob )
print(f"Alice sent the sum of shares to Bob")


# Receive sum of score shares from Bob
sumScorfromB = client_socket2.recv(6048)
sumBscors=pickle.loads(sumScorfromB)


# Close the sockets
client_socket1.close()
client_socket2.close()
server_socket1.close()
server_socket2.close()
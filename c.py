import socket
import pickle
import base64
import datetime


from MPC import shares
import pandas as pd

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
Axshare=Xshares[1]

Byshare=Yshares[0]
Ayshare=Yshares[1]

Cxshare=Xshares[2]
Cyshare=Yshares[2]








#Socket communication

# Define the IP address and port number
IP_ADDRESS = '127.0.0.1'
PORT = 8081

# Create the client socket (with Alice)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))

"""
# Create the client socket (with Bob)
PORT3 = 8083
client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket3.connect((IP_ADDRESS, PORT3))

"""

PORT3 = 8083
# Create the server sockets
server_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket3.bind((IP_ADDRESS, PORT3))
server_socket3.listen()
# Accept the connection with Charlie
client_socket3, address1 = server_socket3.accept()
print(f"Connection established with Charlie with address {address1}")





# Send coordinates share to Alice
StoA=[Axshare,Ayshare]
Amessage = pickle.dumps(StoA)
print(f"Charlie sent coordinate share to Alice  ({len(Amessage)} bytes)")
client_socket.send(Amessage)

# Send coordinates share to Bob
StoB=[Bxshare,Byshare]
Bmessage = pickle.dumps(StoB)
print(f"Charlie coordinate share to Bob is {len(Bmessage)} bytes")
client_socket3.send(Bmessage)
print(f"Charlie sent his coordinatesshare to Bob")



# Receive message from Alice
Amessage = client_socket.recv(6048)
Alicemsg1=pickle.loads(Amessage)
print(f"Received coordinates share from Alice: {Alicemsg1}")




# Receive message from Bob
rBmessage = client_socket3.recv(6048)
rBobmsg1=pickle.loads(rBmessage)
print(f"Received coordinates share from Bob: {rBobmsg1}")




#Compute the sum of shares 

Xc=Cxshare+rBobmsg1[0]+Alicemsg1[0]
Yc=Cyshare+rBobmsg1[1]+Alicemsg1[1]


StoB2=[Xc,Yc]
Bmessage2 = pickle.dumps(StoB2)

client_socket3.send(Bmessage2)
print(f"Charlie sent his sum of shares to Bob: {StoB2}")

# Receive centroid from Bob
Cmessage = client_socket3.recv(6048)
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
    
# Send scores share to Bob

Bsharescore = pickle.dumps(Bshares_scores)
client_socket3.send(Bsharescore)
print(f"Charlie sent scores shares to Bob")
# Send cscores share to Alice
Asharescore = pickle.dumps(Ashares_scores)
client_socket.send(Asharescore)

print(f"Charlie sent scores shares to Alices")
# Receive scores from Alice
ScorfromA = client_socket.recv(6048)
Ascors=pickle.loads(ScorfromA)

print(f"Charlie revceived scores shares from Alices")
# Receive scores from Bob
ScorfromB = client_socket3.recv(6048)
Bscors=pickle.loads(ScorfromB)
print(f"Charlie revceived scores shares from Bob")
#Sum of scors shares

C_Sc_sum=[x + y + z for x, y, z in zip(Ascors, Bscors,Cshares_scores)]

#Send scores sum to Bob

SumScorsForBob = pickle.dumps(C_Sc_sum)
client_socket3.send(SumScorsForBob )
print(f"Charlie sent sum of scores shares to Bob")

# Receive scores from Bob
sumScorfromB = client_socket3.recv(6048)
sumBscors=pickle.loads(sumScorfromB)
# Close the socket
client_socket.close()
client_socket3.close()
server_socket3.close()
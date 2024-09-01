import socket
import pickle
import base64
from MPC import shares
import folium
import requests
import random
import numpy as np
import pandas as pd

import json
import math


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

start_timeA=time.time()
start_time1=time.time()

Xshares=shares(nbrparticipants,x)
Yshares=shares(nbrparticipants,y)

Axshare=Xshares[0]
Cxshare=Xshares[1]

Ayshare=Yshares[0]
Cyshare=Yshares[1]


Bxshare=Xshares[2]
Byshare=Yshares[2]

end_time1=time.time()
total_time1 = end_time1 - start_time1
#total_timef=round(total_time, 6)
mstime1=total_time1*1000
print("Total time taken to compute the other \n participants shares is :", mstime1, "ms")



#Socket communication
# Define the IP address and port number
IP_ADDRESS = '127.0.0.1'
PORT = 8082

# Create the client socket (with Alice)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))
# Set a timeout of 5 seconds


#Create channel with Charlie

"""
PORT3 = 8083
# Create the server sockets
server_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket3.bind((IP_ADDRESS, PORT3))
server_socket3.listen()
# Accept the connection with Charlie
client_socket3, address1 = server_socket3.accept()
print(f"Connection established with Charlie with address {address1}")

"""
PORT3 = 8083
client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket3.connect((IP_ADDRESS, PORT3))





# Receive coordinates share from Alice
Amessage = client_socket.recv(6048)
Alicemsg1=pickle.loads(Amessage)
print(f"Received coordinates share from Alice: {Alicemsg1}")

# Receive coordinates from Charlie
rCmessage = client_socket3.recv(6048)
Charmsg1=pickle.loads(rCmessage)
print(f"Received coordinates share from Charlie: {Charmsg1}")



# Send coordinates share to Alice
StoA=[Axshare,Ayshare]
Amessage = pickle.dumps(StoA)
client_socket.send(Amessage)
print(f"Bob sent his coordinatesshare to Alice ({len(Amessage)} bytes)")

# Send coordinates share to Charlie
StoC=[Cxshare,Cyshare]
Cmessage = pickle.dumps(StoC)
client_socket3.send(Cmessage)
print(f"Bob sent his coordinatesshare to Charlie ({len(Cmessage)} bytes)")


#Compute the sum of shares

start_time2=time.time()
Xb=Bxshare+Alicemsg1[0]+Charmsg1[0]
Yb=Byshare+Alicemsg1[1]+Charmsg1[1]

end_time2=time.time()
total_time2 = end_time2 - start_time2
#total_timef=round(total_time, 6)
mstime2=total_time2*1000
print("Total time taken to compute the other \n sume of shares is :", mstime2, "ms")

# Receive shares from Charlie
rCmessage2 = client_socket3.recv(6048)
Charmsg2=pickle.loads(rCmessage2)
print(f"Received sum of shares from Charlie: {Charmsg2}")


# Receive shares from Alice
Amessage2 = client_socket.recv(6048)
Alicemsg2=pickle.loads(Amessage2)
print(f"Received sum of shares from Alice: {Alicemsg2}")

start_time3=time.time()
sumX=Alicemsg2[0]+Charmsg2[0]+Xb

sumY=Alicemsg2[1]+Charmsg2[1]+Yb




print(f"SUM OF X COORDINATES IS: {sumX}")
print(f"SUM OF Y COORDINATES IS: {sumY}")


Cx=sumX/(nbrparticipants*(10**6))
Cy=sumY/(nbrparticipants*(10**6))
Cxr=round(Cx, 6)
Cyr=round(Cy, 6)


center=[Cxr,Cyr]
end_time3=time.time()
total_time3 = end_time3 - start_time3
#total_timef=round(total_time, 6)
mstime3=total_time3*1000
print("Total time taken to compute the final result centroid is :", mstime3, "ms")
mcenter=mstime1+mstime2+mstime3


print("Total time taken to compute the centroid (including all operations) is :", mcenter, "ms")
print(f"Centroid coordinates are: {center}")





start_timeLBS=time.time()

# Define the Overpass API query (OpenStreetMap)
query = f"""
    [out:json];
    (
        node["amenity"="restaurant"](around:1000, {center[0]}, {center[1]});
        node["amenity"="cafe"](around:1000, {center[0]}, {center[1]});
        node["tourism"="hotel"](around:1000, {center[0]}, {center[1]});
    );
    out center;
"""

# Make API request to the Overpass API and retrieve data
overpass_url = "https://lz4.overpass-api.de/api/interpreter"  # Example Overpass API endpoint
response = requests.get(overpass_url, params={"data": query})
data = response.json()   

# Pick random places and add markers to the map
places = data["elements"]
random.shuffle(places)
num_places = min(len(places), 4)  # Limit to 8 places (or the available number of places)
place_names = []
selected_places_df = []
selected_places = []

for place in places[:num_places]:
    location = [place["lat"], place["lon"]]
    place_name = place.get("tags", {}).get("name", "Unnamed Place")
    place_names.append(place_name)
    selected_places.append(place)
    selected_places_df.append({"name":place_name, "lat":place["lat"], "lon": place["lon"]})


# Print place names
print(f"Names of the places: {place_names}")

number_places=len(place_names)
print(f"Number of places: {number_places}")


end_timeLBS=time.time()
total_timeLBS = end_timeLBS - start_timeLBS
#total_timef=round(total_time, 6)
mstimeLBS=total_timeLBS*1000
print("Total time taken for requesting meeting points (LBS) :", mstimeLBS, "ms")


#Send Centroid to Alice and Charlie

# Send centroid and selected places to Alice

AmessageCenter = pickle.dumps([center,selected_places_df])
client_socket.send(AmessageCenter)
print(f"Bob sent centroid to Alice")


# Send centroid and selected places to Charlie

CmessageCenter = pickle.dumps([center,selected_places_df])
client_socket3.send(CmessageCenter)
print(f"Bob sent centroid to Charlie")



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
start_time4=time.time()
list_distances=[]
for i in selected_places_df:
    list_distances.append({"name":i['name'],"Distance (Km)": haversine(mylocation[0], mylocation[1], i['lat'], i['lon'])})
    

end_time4=time.time()
total_time4 = end_time4 - start_time4
#total_timef=round(total_time, 6)
mstime4=total_time4*1000
print("Total time taken to compute \n the distances to centroid from candidate locations is:", mstime4, "ms")    
    
    
#Sort distances   

start_timeS=time.time()

df = pd.DataFrame(list_distances)

# Sorting wrt distance
df_sorted_by_dist = df.sort_values(by='Distance (Km)')

df_with_index = df_sorted_by_dist.copy()
df_with_index['Index'] = df_sorted_by_dist.index
df_with_index['Score'] = range(len(df_with_index), 0,-1)
df_Score=df_with_index.sort_values(by='Index')
df_Score=df_Score.drop('Index', axis=1)
print(df_Score)
    


end_timeS=time.time()
total_timeS = end_timeS - start_timeS
#total_timef=round(total_time, 6)
mstimeS=total_timeS*1000
print("Total time taken to score locations :", mstimeS, "ms")


#Compute scores shares
start_timeS2=time.time()
Bshares_scores=[]
Cshares_scores=[]
Ashares_scores=[]

for i in df_Score["Score"]:
    T=shares(nbrparticipants,i)
    Ashares_scores.append(T[0])
    Bshares_scores.append(T[1])
    Cshares_scores.append(T[2])
    


end_timeS2=time.time()
total_timeS2 = end_timeS2 - start_timeS2
#total_timef=round(total_time, 6)
mstimeS2=total_timeS2*1000
print("Total time taken to \n compute scores shares :", mstimeS2, "ms")
    
# Send scores share to Charlie

Csharescore = pickle.dumps(Cshares_scores)
client_socket3.send(Csharescore)
print(f"Bob sent his scores share to Charlie")

# Receive scores share from Charlie
ScorfromC = client_socket3.recv(6048)
Cscors=pickle.loads(ScorfromC)
print(f"Bob received scores shares from Charlie")


# Send score share to Alice
Asharescore = pickle.dumps(Ashares_scores)
client_socket.send(Asharescore)
print(f"Bob sent his scores share to Alice")

# Receive scores from Alice
ScorfromA = client_socket.recv(6048)
Ascors=pickle.loads(ScorfromA)
print(f"Bob received scores shares from Alice")



#Sum of scors shares

B_Sc_sum=[x + y + z for x, y, z in zip(Ascors,  Bshares_scores,Cscors)]

# Send sum of scors shares to Charlie
SumforC = pickle.dumps(B_Sc_sum)
client_socket3.send(SumforC)
print(f"Bob sent his sum of scores shares to Charlie")

# Receive scores from Charlie
sumScorfromC = client_socket3.recv(6048)
sumCscors=pickle.loads(sumScorfromC)
print(f"Bob received sum of scores shares from Charlie")

# Send sum score share to Alice
SumforA = pickle.dumps(B_Sc_sum)
client_socket.send(SumforA)
print(f"Bob sent his sum of scores shares to Alice")

# Receive sum of scores from Alice
sumScorfromA = client_socket.recv(6048)
sumAscors=pickle.loads(sumScorfromA)
print(f"Bob received sum of scores shares from Alice")




#Final Scores

start_time5=time.time()
Final_scores=[x + y + z for x, y, z in zip(sumAscors,  B_Sc_sum,sumCscors)]

m=max(Final_scores)
winnerInd=Final_scores.index(m)
end_time5=time.time()
total_time5 = end_time5 - start_time5
#total_timef=round(total_time, 6)
mstime5=total_time5*1000
print("Total time taken to get the final score is :", mstime5, "ms")

timetaken= mstime1+mstime2+mstime3+mstime4+mstime5+mstimeS2


print("Total time taken by the protocol operations (without sorting) is :", timetaken, "ms")


# Creating a DataFrame
dfScore = pd.DataFrame(list(zip(place_names,Final_scores)), columns=['Place', 'Score'])




winner=selected_places_df[winnerInd]["name"]
print(f"The final scores are: {dfScore}")
print(f"The meeting point is: {winner}")



end_timeA=time.time()
total_timeA = end_timeA - start_timeA
#total_timef=round(total_time, 6)

print("Total time taken from start to end :", total_timeA, "s")


winner_coor=[selected_places_df[winnerInd]["lat"],selected_places_df[winnerInd]["lon"]]





#Get MAP




# Coordinates for Helsinki, Finland
helsinki_coords = [60.1695, 24.9354]

# Create a Folium map centered in Helsinki
m = folium.Map(location=helsinki_coords, zoom_start=13)

# Define the locations and labels for the two icons
selectedloc = [convcorx,convcory]
label1 = "Selected Location"


label2 = "Meeting Point"

# Add markers with labels to the map
folium.Marker(location=selectedloc, popup=label1, icon=folium.Icon(color='green', icon='info-sign')).add_to(m)
folium.Marker(location=center, popup=label2, icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)


# Save the map to an HTML file or display it
m.save('MeetingPoint.html')
# Uncomment the line below if you want to display the map in a Jupyter notebook
# helsinki_map


# Close the socket
client_socket.close()
client_socket3.close()
#server_socket3.close()

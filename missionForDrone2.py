
import time

from dronekit import connect, LocationGlobalRelative, Command
from pymavlink import mavutil
from algorithm import algorithm1

#konum bilgileri giriliyor.

drone1 = connect('127.0.0.1:14560', wait_ready= True)
cmd = drone1.commands
print("baglandi")
while drone1.is_armable is not True:
    time.sleep(1)
drone1.mode = "GUIDED"
drone1.armed = True
print("motorlar armlandı...")
drone1.home_location=drone1.location.global_frame

drone1.simple_takeoff(11)

while True:
    altitude = drone1.location.global_relative_frame.alt
    if altitude >= 11 * 0.95:  # Trigger just below target alt.
        print("Reached target altitude")
        break
    time.sleep(1)

#x1'den başlayan drone için...
lat1=drone1.location.global_relative_frame.lat
lon1=drone1.location.global_relative_frame.lon
# we are assuming drone is on a point
a_location = drone1.location.global_relative_frame
# a noktasi : lat = -35.361815 , lon = 149.162960
# b noktasi : lat = -35.363331 , lon = 149.162973
# c noktasi : lat = -35.361164 , lon = 149.165163
# d noktasi : lat = -35.3632622 , lon = 149.1652375

print("koordinatlar giriliyor...")
lat2 = -35.363331
lon2 = 149.162973
b_location = LocationGlobalRelative(lat2,lon2,11.0)
lat3=-35.361164
lon3=149.165163
c_location=LocationGlobalRelative(lat3,lon3,11.0)
lat4=-35.3632622
lon4=149.1652375
d_location = LocationGlobalRelative(lat4,lon4,11.0)

print(a_location)
print(b_location)
print(c_location)
print(d_location)

#we are assuming the vehicle is already on a_location
listOfRotation = algorithm1(a_location,b_location,c_location,d_location)
y_location = listOfRotation[0]

cmd.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,1,0,0,0,y_location.lat,y_location.lon,11))
for i in range(len(listOfRotation)):
    y_location = listOfRotation[i]
    cmd.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,1,0,0,0,y_location.lat,y_location.lon,11))
cmd.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,1,0,0,0,0,0,0))
drone1.parameters['RTL_ALT'] = 11

cmd.upload()

# Komutların drone tarafından otomatik olarak gerçekleştirilmesini sağlamak için AUTO modunu etkinleştirin.
drone1.mode = "AUTO"
print("Görev başlatıldı.")

komutSayisi = cmd.count

# Görevlerin tamamlanmasını bekle.
while True:
    next_waypoint = drone1.commands.next
    print(f"Gidilecek sonraki waypoint: {next_waypoint}")

    if next_waypoint == komutSayisi:
        print("Tüm görevler tamamlandı.")
        break
    time.sleep(3)

print("RTL komutu gönderildi. Başlangıç noktasına dönülüyor.")

while drone1.armed:
    print("Dönüş yapılıyor...")
    time.sleep(1)

print("Görev tamamlandı ve drone güvenli şekilde iniş yaptı.")
cmd.clear()
drone1.close()



import time

from dronekit import connect, LocationGlobalRelative, Command
from pymavlink import mavutil
from algorithm import algorithm1

drone1 = connect('127.0.0.1:14550', wait_ready= True)
cmd = drone1.commands
print("baglandi")
while drone1.is_armable is not True:
    time.sleep(1)
drone1.mode = "GUIDED"
drone1.armed = True
print("motorlar armlandı...")
drone1.home_location=drone1.location.global_frame

drone1.simple_takeoff(7)

while True:
    altitude = drone1.location.global_relative_frame.alt
    if altitude >= 7 * 0.95:  # Trigger just below target alt.
        print("Reached target altitude")
        break
    time.sleep(1)

# a noktasi : lat = -35.36355044, lon = 149.16398570
# b noktasi : lat = -35.36355044, lon = 149.16178626
# c noktasi : lat = -35.36175679 , lon = 149.16398570
# d noktasi : lat = -35.36176165 , lon = 149.16178626

print("koordinatlar giriliyor...")
lat1 = -35.36355044
lon1 = 149.16398570
a_location = LocationGlobalRelative(lat1,lon1,7.0)
lat2 = -35.36355044
lon2 = 149.16178626
b_location = LocationGlobalRelative(lat2,lon2,7.0)
lat3=-35.36175679
lon3=149.16398570
c_location=LocationGlobalRelative(lat3,lon3,7.0)
lat4=-35.36176165
lon4=149.16178626
d_location = LocationGlobalRelative(lat4,lon4,7.0)

print(a_location)
print(b_location)
print(c_location)
print(d_location)
#we are assuming the vehicle is on a_location

cmd.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,1,0,0,0,a_location.lat,a_location.lon,7))
cmd.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,1,0,0,0,a_location.lat,a_location.lon,7))
listOfRotation = algorithm1(a_location,b_location,c_location,d_location)
for i in range(len(listOfRotation)):
    y_location = listOfRotation[i]
    cmd.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,1,0,0,0,y_location.lat,y_location.lon,7))
cmd.add(Command(0,0,0,mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,0,0,1,0,0,0,0,0,0))
drone1.parameters['RTL_ALT'] = 7

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


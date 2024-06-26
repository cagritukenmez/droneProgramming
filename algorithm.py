
import math

from functions import haversine
from dronekit import LocationGlobalRelative

# return a list of rotation information kind of LocationGlobalRelative.
# a noktası drone'un başlangıç noktasıdır.
# b noktası ise kesinlikle a noktasına en uzak olan nokta olamaz.
# c noktası ya da d noktasının ikisinden birisi  
def algorithm1(a_location,b_location,c_location,d_location):
    rotasyonBilgisi=[]#rotasyonun koordinatlarının listesi
    #x1'den başlayan drone için...
    lat5=(b_location.lat+d_location.lat)/2
    lon5=(b_location.lon+d_location.lon)/2
    e_location=LocationGlobalRelative(lat5,lon5,7.0)
    #c noktası ve d noktası arasında olan e noktasını hesaplar.
    lat6=(a_location.lat+c_location.lat)/2
    lon6=(a_location.lon+c_location.lon)/2
    #a noktası ve b noktası arasında olan f noktasını hesaplar.
    f_location=LocationGlobalRelative(lat6,lon6,7.0)

    x_location = a_location
    y_location = b_location

    #k ve m noktaları olarak düşünülsün
    k_location = b_location
    m_location = e_location
    counter=0
    aralarindakiUzaklik = aralarindakiUzaklik = haversine(k_location.lat,k_location.lon,m_location.lat,m_location.lon)
    #0.001 sayısı KM cinsinden gezilecek en yakın 2 nokta arasındaki uzaklığı temsil etmektedir ve değiştirilebilir
    while aralarindakiUzaklik > 0.01:
        aralarindakiUzaklik = haversine(k_location.lat,k_location.lon,m_location.lat,m_location.lon)
        counter+=1
        m_location=LocationGlobalRelative((k_location.lat+m_location.lat)/2,(k_location.lon+m_location.lon)/2,7.0)
        #k noktası ve temsil edilecek olan yeni m noktası arasındaki mesafe 0.001 km olasıya kadar 2ye böl ve sayacı bir arttır. 
    tekrarSayisi = float(math.pow(2,counter))
    #Yatay dönüş sayısını hesaplar

    #her bir en kısa yatay ya da dikey dönüş için hesaplanılan koordinatın değişikliği 
    kooordinatDegisikligi = LocationGlobalRelative(((e_location.lat-b_location.lat)/tekrarSayisi),((e_location.lon-b_location.lon)/tekrarSayisi),7.0)
    for i in range(int(tekrarSayisi)):
        rotasyonBilgisi.append(y_location)
        y_location=LocationGlobalRelative(y_location.lat+kooordinatDegisikligi.lat,y_location.lon+kooordinatDegisikligi.lon,7.0)
        rotasyonBilgisi.append(y_location)
        simdikiLocation = y_location
        y_location = LocationGlobalRelative(x_location.lat+kooordinatDegisikligi.lat,x_location.lon+kooordinatDegisikligi.lon,7.0)
        x_location = simdikiLocation
    
    y_location = LocationGlobalRelative((e_location.lat+f_location.lat)/2,(e_location.lon+f_location.lon)/2,7.0)
    rotasyonBilgisi.append(y_location)
    return rotasyonBilgisi

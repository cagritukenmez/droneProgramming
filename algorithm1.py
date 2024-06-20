
import math

from functions import haversine
from dronekit import LocationGlobalRelative

#return a list of rotation information kind of LocationGlobalRelative.
def algorithm1(a_location,b_location,c_location,d_location):
    rotasyonBilgisi=[]

#x1'den başlayan drone için...
    lat5=(c_location.lat+d_location.lat)/2
    lon5=(c_location.lon+d_location.lon)/2
    e_location=LocationGlobalRelative(lat5,lon5,7.0)
    lat6=(a_location.lat+b_location.lat)/2
    lon6=(a_location.lon+b_location.lon)/2
    f_location=LocationGlobalRelative(lat6,lon6,7.0)
    x_location = a_location
    y_location = b_location

#k ve m noktaları olarak düşünülsün
    k_location = c_location
    m_location = e_location
    counter=0
    aralarindakiUzaklik = aralarindakiUzaklik = haversine(k_location.lat,k_location.lon,m_location.lat,m_location.lon)
    while aralarindakiUzaklik > 0.001:
        aralarindakiUzaklik = haversine(k_location.lat,k_location.lon,m_location.lat,m_location.lon)
        print("Aralarindaki uzaklik",aralarindakiUzaklik)
        counter+=1
        m_location=LocationGlobalRelative((k_location.lat+m_location.lat)/2,(k_location.lon+m_location.lon)/2,7.0)
        print(aralarindakiUzaklik)
    tekrarSayisi = float(math.pow(2,counter))
    print ("tekrar sayisi:",tekrarSayisi)
#koordinat değişikliği için değişken hesaplaması
#new_location = c_location +(tekrarSayisi-1)*
    kooordinatDegisikligi = LocationGlobalRelative(((e_location.lat-c_location.lat)/tekrarSayisi),((e_location.lon-c_location.lon)/tekrarSayisi),7.0)
    print(kooordinatDegisikligi)
    for i in range(int(tekrarSayisi)):
        #push here
        rotasyonBilgisi.append(y_location)
        print("diziye ekleniyor ",y_location)
        y_location=LocationGlobalRelative(y_location.lat+kooordinatDegisikligi.lat,y_location.lon+kooordinatDegisikligi.lon,7.0)
        #push here
        rotasyonBilgisi.append(y_location)
        print("diziye ekleniyor ",y_location)
        simdikiLocation = y_location
        #simdikiLocation = LocationGlobalRelative(y_location.lat+kooordinatDegisikligi.lat,y_location.lon+kooordinatDegisikligi.lon,7.0)
        y_location = LocationGlobalRelative(x_location.lat+kooordinatDegisikligi.lat,x_location.lon+kooordinatDegisikligi.lon,7.0)
        x_location = simdikiLocation
    
    y_location = LocationGlobalRelative((e_location.lat+f_location.lat)/2,(e_location.lon+f_location.lon)/2,7.0)
    rotasyonBilgisi.append(y_location)
    return rotasyonBilgisi

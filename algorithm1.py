
import math

from functions import haversine
from dronekit import LocationGlobalRelative

#return a list of rotation information kind of LocationGlobalRelative.
def algorithm1(a_location,b_location,c_location,d_location):
    rotasyonBilgisi=[]

#x1'den başlayan drone için...
    lat5=(c_location.lat+d_location.lat)/2
    lon5=(c_location.lon+d_location.lon)/2
    e_location=LocationGlobalRelative(lat5,lon5,7)
    lat6=(a_location.alt+b_location.lat)/2
    lon6=(d_location.alt+d_location.alt)/2
    f_location=LocationGlobalRelative(lat = lat6,lon = lon6,alt = 7)
    x_location = a_location
    y_location = b_location

#k ve m noktaları olarak düşünülsün
    k_location = c_location
    m_location = e_location
    counter=0
    aralarindakiUzaklik = haversine(k_location.lat,k_location.lon,m_location.lat,m_location.lon)
    while aralarindakiUzaklik < 0.001:
        aralarindakiUzaklik = haversine(k_location.lat,k_location.lon,m_location.lat,m_location.lon)
        counter+=1
        m_location=((k_location.alt+m_location.alt)/2,(k_location.lon+m_location.lon)/2,7)
        print(aralarindakiUzaklik)
    tekrarSayisi = int(math.pow(2,counter))

#koordinat değişikliği için değişken hesaplaması
    kooordinatDegisikligi = LocationGlobalRelative((((c_location.alt+d_location.alt)*(tekrarSayisi+1))/tekrarSayisi),(((c_location.lon+d_location.lon)*(tekrarSayisi+1))/tekrarSayisi),7)
    for i in range(tekrarSayisi):
        #push here
        rotasyonBilgisi.append(y_location)
        y_location=LocationGlobalRelative(y_location.alt+kooordinatDegisikligi.alt,y_location.lon+kooordinatDegisikligi.lon,7)
        #push here
        rotasyonBilgisi.append(y_location)
        simdikiLocation=LocationGlobalRelative(y_location.alt+kooordinatDegisikligi.alt,y_location.lon+kooordinatDegisikligi.lon,7)
        y_location = LocationGlobalRelative(x_location.alt+kooordinatDegisikligi.alt,x_location.lon+kooordinatDegisikligi.lon,7)
        x_location = simdikiLocation
    
    y_location = LocationGlobalRelative((e_location.alt+f_location.alt)/2,(e_location.lon+f_location.lon)/2,7)
    rotasyonBilgisi.append(y_location)
    return rotasyonBilgisi

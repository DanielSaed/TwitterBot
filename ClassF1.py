from calendar import c
from importlib.resources import path
import re
from unicodedata import decimal, name
import fastf1 as ff1
from fastf1 import plotting
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd
from datetime import date 
from fastf1 import utils
from fastf1 import plotting 
from matplotlib import pyplot as plt


ff1.Cache.enable_cache('C:/Users/admin/Desktop/Programas/Python/Algoritmo/__pycache__') 
pd.options.mode.chained_assignment = None 

#Get seconds from laptime
def get_secFromLap(string):
        if(len(string) == 6):
            string+='0'
        if(len(string) == 7):
            string+='0'
        if(len(string) == 8):
            m, s = string.split(':')
            res = "{:.3f}".format((int(m) * 60) + float(s))
        else:
            res = 200
        return  res

#Transform sec to Laptime
def get_lapFromSec(flo):
    flo = float(flo)
    if flo - 60.0 < 1:
        string = str(flo)
    elif flo - 60 < 60:
        flo = float("{:.3f}".format(flo - 60))
        if flo < 10:
            string = '1:0'
        else: 
            string = '1:'
        string = string + str(flo)  
    elif flo - 60 > 60:
        flo = float("{:.3f}".format(flo - 120))
        if flo < 10:
            string = '2:0'
        else: 
            string = '2:'
        string = string + str(flo)  
    return string

#input sector object and output sector time as string
def get_sectorFromObject(sector,indice):
    l = []
    l = sector.split()
    sector = l[indice][6:].replace("000","")
    return sector

#Object to string laptime
def get_lapFromObject(laptime):
    l = []
    characters = "days "
    for i in range(len(characters)):
        laptime = laptime.replace(characters[i],"")
    laptime = re.sub(r'.', '', laptime, count = 5)
    laptime = laptime.replace("000","")
    l = laptime.split()
    lap = l[0]
    while True:
        if(len(lap) <= 8):
            break
        else:
            lap= lap[1:]
    return lap

#input the tyre ouput a short name of it
def get_typeOfTyre(tyre):
    if tyre == 'SOFT':
        tyre = 'S🔴'
    elif tyre == 'MEDIUM':
        tyre = 'M🟡'
    elif tyre == 'HARD':
        tyre = 'H⚪'
    elif tyre == 'INTERMEDIATE':
        tyre = 'I🟢'
    return tyre


class Data:

    DicDrivers = {'PER':'🇲🇽PER','LEC':'🇲🇨LEC','VER':'🇳🇱VER','SAI':'🇪🇸SAI','ALO':'🇪🇸ALO','HAM':'🇬🇧HAM','RUS':'🇬🇧RUS','OCO':'🇫🇷OCO','NOR':'🇬🇧NOR','RIC':'🇦🇺RIC','GAS':'🇫🇷GAS','TSU':'🇯🇵TSU','MSC':'🇩🇪MSC','MAG':'🇩🇰MAG','STR':'🇨🇦STR','VET':'🇩🇪VET','ALB':'🇹🇭ALB','LAT':'🇨🇦LAT','BOT':'🇫🇮BOT','ZOU':'🇨🇳ZOU'}
    DicSesion = {'FP1':'░F░P░1░🏁','FP2':'F P 2 🏁','FP3':'FP3🏁','Q':'Qualy Session🏁','R':'Race🏁','S':'Sprint Race🏁'}

    def __init__(self, name,year,weekend,sesion):
        self.name = name
        self.sesion = sesion
        self.session= ff1.get_session(year,weekend,sesion)
        self.driverDataLaps = self.session.load_laps(with_telemetry=True).pick_driver(self.name)
        self.driverDataFastestLap = self.driverDataLaps.pick_fastest()
        self.driverTelFastestLap  = self.driverDataFastestLap.get_car_data()

    def get_lapsInStint(self):  
        #print(driverSesionLaps)
        dic = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
        for a in self.driverDataLaps.LapNumber:
            ls =[]
            #selecciona la vuelta
            self.currentDriverLap =  self.driverDataLaps[self.driverDataLaps.LapNumber==a]
            self.currentDriverLapTime  = get_lapFromObject(str(self.currentDriverLap.LapTime))

            #Obtener stint de la vuelta
            listStint = []
            listStint = re.sub(r'.', '', str(self.currentDriverLap ['Stint']), count = 2)[3:].split()
            stint = float(listStint[0])

            #Checa si existe el laptime de la vuelta
            if self.currentDriverLapTime != ':LpTime,tpe:timeelt64[n]' and self.currentDriverLapTime != 'e:LpTime,tpe:timeelt64[n]' and self.currentDriverLapTime != 'elt64[n]':
                
                ls.append(get_sectorFromObject(str(self.currentDriverLap['Sector1Time']),3))
                ls.append(get_sectorFromObject(str(self.currentDriverLap['Sector2Time']),3))
                ls.append(get_sectorFromObject(str(self.currentDriverLap['Sector3Time']),3))
                listDic, listComp = [],[]
                listComp = str(self.currentDriverLap['Compound'])[4:].split()
                listDic.append(self.currentDriverLapTime)
                listDic.append(listComp[0])
                listDic.append(a)
                listDic.append(ls)
                dic[stint].append(listDic)
        return dic

    def get_avgStint(self):
        self.fastestLap = float(get_secFromLap(get_lapFromObject(str(self.driverDataFastestLap['LapTime']))))
        dic = self.get_lapsInStint()
        dicNew = {}
        for i in dic:
            cont = 0
            fastest = 200
            avg = 0
            avgs1 = 0
            avgs2 = 0
            avgs3 = 0
            for a in dic[i]:
                if fastest > float(get_secFromLap(a[0])):
                    fastest = float(get_secFromLap(a[0])) 
                    s1 = float(a[3][0])
                    s2 = float(a[3][1])
                    s3 = float(a[3][2])
                    tyre = a[1]
            fastest += 1.5
            ls =[]
            for x in dic[i]:
                actual = float(get_secFromLap(x[0]))
                
                if fastest >= actual and fastest < 200:
                    
                    avgs1 += float(x[3][0])
                    avgs2 += float(x[3][1])
                    avgs3 += float(x[3][2])
                    avg += actual
                    
                    ls.append(get_secFromLap(actual))
                    cont +=1
            if cont !=0:
                avg = "{:.3f}".format(avg/cont)
                avgs1 = float("{:.3f}".format(avgs1/cont))
                avgs2 = float("{:.3f}".format(avgs2/cont))
                avgs3 = float("{:.3f}".format(avgs3/cont))
                if fastest - 1.5 < self.fastestLap + 1.0:
                    tipo = 'Sim. Qualy'
                elif fastest - 1.5 < self.fastestLap + 2.0:
                    tipo = 'Vueltas Rapidas'
                elif fastest - 1.5 < self.fastestLap + 10 and len(ls) > 1:
                    tipo = 'Sim. Carrera'
                elif fastest - 1.5 > self.fastestLap + 10:
                    tipo = 'Vueltas practica'
                else:
                    tipo = 'Vueltas de instalacion'
                dic1 = {'Average': get_secFromLap(avg),'Tyre':get_secFromLap(tyre),'LapNumber':cont,'Tipo':tipo,'Laps':ls,'Fastest':get_secFromLap(fastest-1.5),'AvgS1':avgs1,'AvgS2':avgs2,'AvgS3':avgs3,'S1':s1,'S2':s2,'S3':s3}
                
                dicNew[i] = dic1
        return dicNew

    def get_lapsSession(self):
        
        cont = 1
        vueltas = 0
        for i in self.driverDataLaps:
            cont +=1  
        dic = self.get_avgStint()
        for i in dic:
            if dic[i]['Tipo'] == 'Sim. Qualy' or dic[i]['Tipo'] == 'Vueltas Rapidas' or dic[i]['Tipo'] == 'Sim. Carrera':
                vueltas += int(dic[i]['LapNumber'])
        text = 'Total de vueltas dadas en '+ str(self.DicSesion[self.sesion]) + ' por ' + self.DicDrivers[self.name] +'\n\n' + str(cont) + "\n\nVueltas efectivas: \n\n" + str(vueltas)

        return text
    
    def get_velMax(self):
        
        vel = 0
        for i in self.driverTelFastestLap['Speed']:
            if(int(i) > vel):
                vel = int(i)
        return vel

    def set_par(self, par):
        """Asigna paralaje en segundos de arco"""
        self.par = par

    def get_mag(self):
        print("La magnitud de {} de {}".format(self.name, self.mag))

    def get_dist(self):
        """Calcula la distancia en parsec a partir de la paralaje"""
        print("La distacia de {} es  {:.2f} pc".format(self.name, 1/self.par))

    def get_stars_number(self):
        print("Numero total de estrellas: {}")

    def fastlap(self,driver):  
        fastlap = self.session.load_laps(with_telemetry=True).pick_driver(driver).pick_fastest()
        dic = {1:[]}
        ls = []
        #selecciona la vuelta
        #convertir vuelta a string
        driverLapLaptime = get_lapFromObject(str(fastlap.LapTime))
        print(fastlap['Sector1Time'])
        print(fastlap['Sector2Time'])
        print(fastlap['Sector3Time'])
        ls.append(get_sectorFromObject(str(fastlap['Sector1Time']),2))
        ls.append(get_sectorFromObject(str(fastlap['Sector2Time']),2))
        ls.append(get_sectorFromObject(str(fastlap['Sector3Time']),2))

        #Checa si existe el laptime de la vuelta
        if driverLapLaptime != ':LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'e:LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'elt64[n]':
            listDic, listComp = [],[]
            listComp = str(fastlap['Compound'])[0:].split()
            dic[1].append(driverLapLaptime)
            dic[1].append(listComp[0])
            dic[1].append(ls)
        return dic

    def tweetFastLapPV(self,d1,d2):
        dic = {}
        dicDriver1 = self.fastlap(d1)
        dicDriver2 = self.fastlap(d2)
        secdriver1 = float(get_secFromLap(dicDriver1[1][0]))
        secdriver2 = float(get_secFromLap(dicDriver2[1][0]))
        tDriver1 = dicDriver1[1][0]
        tDriver2 = dicDriver2[1][0]
        tyreDriver1 = get_typeOfTyre(dicDriver1[1][1])
        tyreDriver2 = get_typeOfTyre(dicDriver2[1][1])
        
        d1ls = [d1,d1,self.DicDrivers[d1]]
        d2ls = [d2,d2,self.DicDrivers[d2]]
        if (secdriver1 < secdriver2): 
            tDiff = "{:.3f}".format(secdriver2 - secdriver1)
            dic['Fastest'] = d1ls
            dic['Slowest'] = d2ls
            dic['Diferencia'] = tDiff
            dic['LaptimeF'] = dicDriver1[1][0]
            dic['LaptimeS'] = dicDriver2[1][0]
            dic['Fsectors'] = dicDriver1[1][2]
            dic['Ssectors'] = dicDriver2[1][2]
            dic['TyreF'] = tyreDriver1
            dic['TyreS'] = tyreDriver2
        else:
            tDiff = "{:.3f}".format(secdriver1 - secdriver2)
            dic['Fastest'] = d2ls
            dic['Slowest'] = d1ls
            dic['Diferencia'] = tDiff
            dic['LaptimeF'] = dicDriver2[1][0]
            dic['LaptimeS'] = dicDriver1[1][0]
            dic['Fsectors'] = dicDriver2[1][2]
            dic['Ssectors'] = dicDriver1[1][2]
            dic['TyreF'] = tyreDriver2
            dic['TyreS'] = tyreDriver1
        
        diffS1 = float("{:.3f}".format(float(dic['Ssectors'][0]) - float(dic['Fsectors'][0])))
        if diffS1 >= 0: diffS1 = "+"+str(diffS1)
        diffS2 = float("{:.3f}".format(float(dic['Ssectors'][1]) - float(dic['Fsectors'][1])))
        if diffS2 >= 0: diffS2 = "+"+str(diffS2)
        diffS3 = float("{:.3f}".format(float(dic['Ssectors'][2]) - float(dic['Fsectors'][2])))
        if diffS3 >= 0: diffS3 = "+"+str(diffS3)
        
        text = self.DicSesion[self.sesion]+"\nMas rapido " + dic['Fastest'][2] + " a una vuelta que "+ dic['Slowest'][2] +"\n\n"+ dic['Fastest'][2] + ": " + dic['LaptimeF'] +" "+dic['TyreF']+ "\n S1: " +dic['Fsectors'][0]+"   S2: "+dic['Fsectors'][1]+"   S3: "+dic['Fsectors'][2]+"\n\n"+ dic['Slowest'][2] + ": " + dic['LaptimeS']+ " "+dic['TyreS']+"\n S1: " +dic['Ssectors'][0]+"   S2: "+dic['Ssectors'][1]+"    S3: "+dic['Ssectors'][2]+ "\n\nGap +" +dic['Diferencia'] +" ( S1: "+str(diffS1)+", S2: "+str(diffS2)+", S3: "+str(diffS3)+")\n"+str((self.session.event['EventName'])).replace(" ", "")
        return text
per = Data('PER', 2022, 14, 'FP3')
print(per.tweetFastLapPV('PER','VER'))
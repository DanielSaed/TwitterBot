from calendar import c
from importlib.resources import path
from lib2to3.pgen2 import driver
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
   
    
    
    if (lap[0] == '0'):
        lap = '2:00.000'
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

class Sesion:

    DicDrivers = {'PER':'🇲🇽PER','LEC':'🇲🇨LEC','VER':'🇳🇱VER','SAI':'🇪🇸SAI','ALO':'🇪🇸ALO','HAM':'🇬🇧HAM','RUS':'🇬🇧RUS','OCO':'🇫🇷OCO','NOR':'🇬🇧NOR','RIC':'🇦🇺RIC','GAS':'🇫🇷GAS','TSU':'🇯🇵TSU','MSC':'🇩🇪MSC','MAG':'🇩🇰MAG','STR':'🇨🇦STR','VET':'🇩🇪VET','ALB':'🇹🇭ALB','LAT':'🇨🇦LAT','BOT':'🇫🇮BOT','ZOU':'🇨🇳ZOU'}
    DicSesion = {'FP1':'░F░P░1░🏁','FP2':'F P 2 🏁','FP3':'FP3🏁','Q':'Qualy Session🏁','R':'Race🏁','S':'Sprint Race🏁'}
    listDrivers = ['PER','LEC','VER','SAI','ALO','HAM','RUS','OCO','NOR','RIC','GAS','TSU','MSC','MAG','STR','VET','DEV','LAT','BOT','ZHO']
   
    def __init__(self,year,weekend,sesion):
        
        self.sesion = sesion
        self.session= ff1.get_session(year,weekend,sesion)
        self.driverDataLapsLoad = self.session.load_laps(with_telemetry=True)

    def get_lapsInStint(self,driver):  
        #print(driverSesionLaps)
        dic = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
        driverDataLaps = self.session.load_laps(with_telemetry=True).pick_driver(driver)
        for a in driverDataLaps.LapNumber:
            ls =[]
            #selecciona la vuelta
            currentDriverLap =  driverDataLaps[driverDataLaps.LapNumber==a]
            currentDriverLapTime  = get_lapFromObject(str(currentDriverLap.LapTime))

            #Obtener stint de la vuelta
            listStint = []
            listStint = re.sub(r'.', '', str(currentDriverLap['Stint']), count = 2)[3:].split()
            stint = float(listStint[0])

            #Checa si existe el laptime de la vuelta
            if currentDriverLapTime != ':LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'e:LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'elt64[n]':
                
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector1Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector2Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector3Time']),3))
                listDic, listComp = [],[]
                listComp = str(currentDriverLap['Compound'])[4:].split()
                listDic.append(currentDriverLapTime)
                listDic.append(listComp[0])
                listDic.append(a)
                listDic.append(ls)
                dic[stint].append(listDic)
        return dic

    def get_avgStint(self,driver):
        data=self.session.load_laps(with_telemetry=True)
        datafastest=data.pick_fastest()
        fastestLap = float(get_secFromLap(get_lapFromObject(str(datafastest['LapTime']))))
        print(fastestLap)

        dic = self.get_lapsInStint(driver)
        
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
                    
                    ls.append(get_lapFromSec(actual))
                    cont +=1
            if cont !=0:
                avg = "{:.3f}".format(avg/cont)
                avgs1 = float("{:.3f}".format(avgs1/cont))
                avgs2 = float("{:.3f}".format(avgs2/cont))
                avgs3 = float("{:.3f}".format(avgs3/cont))
                if fastest - 1.5 < fastestLap + 1.0:
                    tipo = 'Sim. Qualy'
                
                elif fastest - 1.5 < fastestLap + 2.0:
                    tipo = 'Vueltas Rapidas'
                elif fastest - 1.5 < fastestLap + 10 and len(ls) > 1:
                    tipo = 'Sim. Carrera'
                elif fastest - 1.5 > fastestLap + 10:
                    tipo = 'Vueltas practica'
                else:
                    tipo = 'Vueltas de instalacion'
                dic1 = {'Average': get_lapFromSec(avg),'Tyre':get_typeOfTyre(tyre),'LapNumber':cont,'Tipo':tipo,'Laps':ls,'Fastest':get_lapFromSec(fastest-1.5),'AvgS1':avgs1,'AvgS2':avgs2,'AvgS3':avgs3,'S1':s1,'S2':s2,'S3':s3}
                
                dicNew[i] = dic1
       
        return dicNew

    def get_SessionVelMax(self):
        vel = []
        
        lenlist =len(self.listDrivers)
        for i in self.listDrivers:
            driverDataLaps = self.driverDataLapsLoad.pick_driver(i)
            driverDataFastestLap = driverDataLaps.pick_fastest()
           
            driverTelFastestLap  = driverDataFastestLap.get_car_data()
            velmax = 0
            for x in driverTelFastestLap['Speed']:
                if(int(x) > velmax):
                    velmax = int(x) 
            vel.append((velmax,i))
            
        final = []
        
        for i in range(1,lenlist):
            mayor = 200
            cont = -1
            for a in range(0,(len(vel))):
                if mayor < int(vel[a][0]):
                    mayor = int(vel[a][0])
                    tupl = vel[a]
                    cont = a
            final.append(tupl)
            vel.pop(cont)
        final.append(vel[0])
        print(final)
        cont  = 0  
        text = 'Results\n'  
        for i in final:
            cont+=1    
            text += str(cont) + '- ' + str(i[1]) + ' ' +(str(i[0])) + ' km/h\n' 
        return text

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

    def get_CompFastLap2(self,d1,d2):
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
 
    def get_SessionFastest(self):
        laps = []
        cont = 0
        for i in self.listDrivers:
            self.dl = self.driverDataLapsLoad.pick_driver(i)
            driverFastest = self.dl.pick_fastest()
            listComp = str(driverFastest['Compound'])[0:].split()
            laps.append((get_secFromLap(get_lapFromObject(str(driverFastest['LapTime']))),i,get_typeOfTyre(listComp[0])))  
        final = []
        lenlist =len(self.listDrivers)
        for i in range(1,lenlist):
            mayor = 200
            cont = -1
            for a in range(0,(len(laps)-1)):
                if mayor > float(laps[a][0]):
                    mayor = float(laps[a][0])
                    tupl = laps[a]
                    cont = a
            final.append(tupl)
            laps.pop(cont)
        final.append(laps[0])
        cont  = 0  
        text = 'Results\n'  
        for i in final:
            cont+=1    
            text += str(cont) + '- ' + str(i[1]) + ' ' + get_lapFromSec(str(i[0])) + ' ' + i[2] +'\n'
        return text

    def get_StringCarreraRF(self):
        dicNew = {}
        dicPER = self.get_avgStint('PER')
        dicVER = self.get_avgStint('VER')
        dicLEC = self.get_avgStint('LEC')
        dicSAI = self.get_avgStint('SAI')
        print(dicLEC)
        i = 1
        for a in dicPER:
            if dicPER[a]['Tipo']=='Sim. Carrera':
                dic1 = {'Average': get_secFromLap(dicPER[a]['Average']),'Tyre':str(dicPER[a]['Tyre']),'LapNumber':str(dicPER[a]['LapNumber']),'Driver':'🇲🇽PER','AvgS1':dicPER[a]['AvgS1'],'AvgS2':dicPER[a]['AvgS2'],'AvgS3':dicPER[a]['AvgS3']}
                dicNew[i]=dic1
                i += 1
        for b in dicVER:
            if dicVER[b]['Tipo']=='Sim. Carrera':
                dic1 = {'Average': get_secFromLap(dicVER[b]['Average']),'Tyre':str(dicVER[b]['Tyre']),'LapNumber':str(dicVER[b]['LapNumber']),'Driver':'🇳🇱VER','AvgS1':dicVER[b]['AvgS1'],'AvgS2':dicVER[b]['AvgS2'],'AvgS3':dicVER[b]['AvgS3']}
                dicNew[i]=dic1
                i += 1
        for c in dicLEC:
            if dicLEC[c]['Tipo']=='Sim. Carrera':
                print(dicLEC[c]['Average'])
                dic1 = {'Average': get_secFromLap(dicLEC[c]['Average']),'Tyre':str(dicLEC[c]['Tyre']),'LapNumber':str(dicLEC[c]['LapNumber']),'Driver':'🇲🇨LEC','AvgS1':dicLEC[c]['AvgS1'],'AvgS2':dicLEC[c]['AvgS2'],'AvgS3':dicLEC[c]['AvgS3']}
                dicNew[i]=dic1
                i += 1
        #print(dicNew)
        for d in dicSAI:
            if dicSAI[d]['Tipo']=='Sim. Carrera':
                dic1 = {'Average': get_secFromLap(dicSAI[d]['Average']),'Tyre':str(dicSAI[d]['Tyre']),'LapNumber':str(dicSAI[d]['LapNumber']),'Driver':'🇪🇸SAI','AvgS1':dicSAI[d]['AvgS1'],'AvgS2':dicSAI[d]['AvgS2'],'AvgS3':dicSAI[d]['AvgS3']}
                dicNew[i]=dic1
                i += 1
        
        fastest = 0
        dicFinal = {}
        longitud = len(dicNew)

        for f in range(1,i):
            fast = 201
            for e in dicNew:
                if float(dicNew[e]['Average']) < fast:
                    fast = float(dicNew[e]['Average'])
                    fastest = e
                    #print(e)
            dicFinal[f]=dicNew[fastest].copy()
            dicNew.pop(fastest)
        text1 =''
        text = []
        cont = 0
        lsNumber = [0,'1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣',8,9,10]
        text1 = self.DicSesion[self.sesion]+'\n𝗦𝗶𝗺𝘂𝗹𝗮𝗰𝗶𝗼𝗻 𝗱𝗲 𝗰𝗮𝗿𝗿𝗲𝗿𝗮\n🇦🇹 𝐑𝐞𝐝 𝐁𝐮𝐥𝐥 𝐯𝐬 𝐅𝐞𝐫𝐫𝐚𝐫𝐢 🇮🇹\n\n'
    
        for g in dicFinal:
            if len(text1) > 190:
                text1 += '1 \ 2 ⤵'
                text.append(text1)
                text1 = ''
                cont+=1
            text1 += str(lsNumber[g]) + " " + str(dicFinal[g]['Driver'])+"  Ritmo: "+ str(get_lapFromSec(dicFinal[g]['Average']))+ "  v:"+str(dicFinal[g]['LapNumber'])+ "  " +str(dicFinal[g]['Tyre'])+ "\n \n"
        text.append(text1)
        return text

    def get_StringStintQualyRF(self):
        dicNew = {}
        dicPER = self.get_avgStint('PER')
        dicVER = self.get_avgStint('VER')
        dicLEC = self.get_avgStint('LEC')
        dicSAI = self.get_avgStint('SAI')
        cont = 0
        i = 1

        #New Dictionaries with the data of the 4 drivers
        for a in dicPER:
            if dicPER[a]['Tipo']=='Sim. Qualy':
                    dic1 = {'Fastest': get_secFromLap(dicPER[a]['Fastest']),'Tyre':str(dicPER[a]['Tyre']),'LapNumber':str(dicPER[a]['LapNumber']),'Driver':'🇲🇽PER','S1':dicPER[a]['S1'],'S2':dicPER[a]['S2'],'S3':dicPER[a]['S3']}
                    dicNew[i]=dic1  
                    i += 1
        for b in dicVER:
            if dicVER[b]['Tipo']=='Sim. Qualy':
                    dic1 = {'Fastest': get_secFromLap(dicVER[b]['Fastest']),'Tyre':str(dicVER[b]['Tyre']),'LapNumber':str(dicVER[b]['LapNumber']),'Driver':'🇳🇱VER','S1':dicVER[b]['S1'],'S2':dicVER[b]['S2'],'S3':dicVER[b]['S3']}
                    dicNew[i]=dic1    
                    i += 1
        for c in dicLEC:
            if dicLEC[c]['Tipo']=='Sim. Qualy':
                    dic1 = {'Fastest': get_secFromLap(dicLEC[c]['Fastest']),'Tyre':str(dicLEC[c]['Tyre']),'LapNumber':str(dicLEC[c]['LapNumber']),'Driver':'🇲🇨LEC','S1':dicLEC[c]['S1'],'S2':dicLEC[c]['S2'],'S3':dicLEC[c]['S3']}
                    dicNew[i]=dic1
                    i += 1 
        for d in dicSAI:
            if dicSAI[d]['Tipo']=='Sim. Qualy':
                if cont < 2:
                    dic1 = {'Fastest': get_secFromLap(dicSAI[d]['Fastest']),'Tyre':str(dicSAI[d]['Tyre']),'LapNumber':str(dicSAI[d]['LapNumber']),'Driver':'🇪🇸SAI','S1':dicSAI[d]['S1'],'S2':dicSAI[d]['S2'],'S3':dicSAI[d]['S3']}
                    dicNew[i]=dic1
                    i += 1
                
        fastest = 0
        dicFinal = {}
        lsname = []

        #order fastest to slowest
        for f in range(1,i):
            fast = 201
            for e in dicNew:
                if float(dicNew[e]['Fastest']) < fast:
                    fast = float(dicNew[e]['Fastest']) 
                    fastest = e
                    #print(e)
            dicFinal[f]=dicNew[fastest].copy()
            dicNew.pop(fastest)
        
        #select the 2 fastest stints per driver
        for m in range(1,len(dicFinal)+1):
            valido = 0
            lsname1 = list(lsname)
            print(lsname)
            print(lsname1)
            for z in lsname:
                if z == dicFinal[m]['Driver']:
                    lsname1.remove(z)
                    for w in lsname1:
                        if w == dicFinal[m]['Driver']:
                            valido = 1
            lsname.append(dicFinal[m]['Driver']) 
            if valido == 1:
                print('borrado')
                dicFinal.pop(m)

        #put it all in a final string
        text1,text2 ='',''
        cont,i = 0, 0
        text = []
        text1 = self.DicSesion[self.sesion]+'\n𝗦𝗶𝗺𝘂𝗹𝗮𝗰𝗶𝗼𝗻 𝗱𝗲 Qualy\n🇦🇹 𝐑𝐞𝐝 𝐁𝐮𝐥𝐥 𝐯𝐬 𝐅𝐞𝐫𝐫𝐚𝐫𝐢 🇮🇹\nMejores 2 intentos\n\n'
        lsNumber = [0,'1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣',8,9,10]
        for g in dicFinal:
            i+=1
            
            if len(text) > 198:
                if len(text1) >198:
                    text1 += 'continua ⤵'
                    cont+=1
                    text.append(text1)
                    text1 = '' 
            text1 += str(lsNumber[i]) + ".-"+str(dicFinal[g]['Driver'])+"  Lap: "+str(get_lapFromSec(dicFinal[g]['Fastest']))+"  "+str(dicFinal[g]['Tyre'])+ "\n\n" 
           
        text.append(text1)
        return text
   

class Driver(Sesion):
    def __init__(self, name,year,weekend,sesion):

        super().__init__(year,weekend,sesion)
        self.name = name
        self.driverDataLaps = self.session.load_laps(with_telemetry=True).pick_driver(self.name)
        self.driverDataFastestLap = self.driverDataLaps.pick_fastest()
        self.driverTelFastestLap  = self.driverDataFastestLap.get_car_data()

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
        return str(vel) + " km\h"

    def get_StringVueltasDadas(self):
        cont = 1
        vueltas = 0
        for i in self.driverDataLaps:
            cont +=1
        
        dic = self.get_avgStint(self.name)
        for i in dic:
            if dic[i]['Tipo'] == 'Sim. Qualy' or dic[i]['Tipo'] == 'Vueltas Rapidas' or dic[i]['Tipo'] == 'Sim. Carrera':
                vueltas += int(dic[i]['LapNumber'])
        text = 'Total de vueltas dadas en '+str(self.DicSesion[self.sesion])+ ' por '+self.DicDrivers[self.name]+'\n\n' +str(cont)+"\n\nVueltas efectivas: \n\n"+str(vueltas)
        return text

    def get_StringStintQualy(self):
        dic = self.get_avgStint(self.name)
        
        cont = 0
        text = []
        text1 = self.DicDrivers[self.name]+ ' 𝙑𝙪𝙚𝙡𝙩𝙖𝙨 𝙋𝙤𝙘𝙖 𝙂𝙖𝙨𝙤𝙡𝙞𝙣𝙖 '+self.DicSesion[self.sesion]+'\n\n'
        for a in dic:
            if dic[a]['Tipo']=='Sim. Qualy':
                if len(text1) > 190:
                    cont+=1
                    text.append(text1)
                    text1 = ''
                text1 += " 𝙎𝙩𝙞𝙣𝙩 "+str(a)+"  V. Rapida: "+str(dic[a]['Fastest'])+" - "+ str(dic[a]['LapNumber'])+"L - "+ str(dic[a]['Tyre'])+" " +str(dic[a]['Tipo'])+"\n\n"
                for x in dic[a]['Laps']:
                    text1 += " "+x + "\n"
                text1 += "\n\n"
        if (text == []):
            text.append(text1)
        #text += '\n#F1 #SP11'
        return text

    def get_StringStintCarrera(self):
        dic = self.get_avgStint(self.name)
        text = []
        text1 = self.DicDrivers[self.name]+ ' 𝙎𝙞𝙢𝙪𝙡𝙖𝙘𝙞𝙤𝙣 𝘾𝙖𝙧𝙧𝙚𝙧𝙖 '+self.DicSesion[self.sesion]+'\n\n'
        cont = 0
        for a in dic:
            if dic[a]['Tipo']=='Sim. Carrera':
                text1 += "Ritmo: "+str(dic[a]['Average'])+" - "+ str(dic[a]['LapNumber'])+"L - "+ str(dic[a]['Tyre'])+" " +str(dic[a]['Tipo'])+"\n"
                text1 += "Avg sectors  S1: "+str(dic[a]['AvgS1'])+"  S2: "+ str(dic[a]['AvgS2'])+"  S3: "+ str(dic[a]['AvgS3'])+"\n\nLaps:\n"
                
                for x in dic[a]['Laps']:
                    text1 += " "+x + "\n"
                cont+=1
                text.append(text1)
                text1 = ''
        return text

    
sesion = Sesion(2022, 15, 'FP2')
per = Driver('PER', 2022, 16, 'FP3')
print(sesion.tweetStintQualyRF())
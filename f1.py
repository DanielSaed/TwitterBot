import fastf1 as ff1
from fastf1 import plotting
from matplotlib.collections import LineCollection
import pandas as pd
from datetime import date 
from fastf1 import plotting 
from matplotlib import pyplot as plt
import re

#datetime
today = date.today()
d1 = today.strftime("%d/%m/%Y")
ans = 'false'
DicSesion = {'FP1':'░F░P░1░🏁','FP2':'F P 2 🏁','FP3':'FP3🏁','Q':'Qualy Session🏁','R':'Race🏁','S':'Sprint Race🏁'}
'''while not ans == 'true':
    print("Numero de carrera")
    carrera = input()
    print("Sesion")
    sesion = input()
    if sesion == 'FP1' or sesion == 'FP2' or sesion == 'FP3' or sesion == 'Q' or sesion == 'R' or sesion == 'S':
        ans = 'true' '''
carrera = 1
sesion = 'Q'
dicDrivers = {'PER':'🇲🇽PER','LEC':'🇲🇨LEC','VER':'🇳🇱VER','SAI':'🇪🇸SAI','ALO':'🇪🇸ALO','HAM':'🇬🇧HAM','RUS':'🇬🇧RUS','OCO':'🇫🇷OCO','NOR':'🇬🇧NOR','RIC':'🇦🇺RIC','GAS':'🇫🇷GAS','TSU':'🇯🇵TSU','MSC':'🇩🇪MSC','MAG':'🇩🇰MAG','STR':'🇨🇦STR','VET':'🇩🇪VET','ALB':'🇹🇭ALB','LAT':'🇨🇦LAT','BOT':'🇫🇮BOT','ZOU':'🇨🇳ZOU'}
listDrivers = ['PER','LEC','VER','SAI','ALO','HAM','RUS','OCO','NOR','RIC','GAS','TSU','MSC','MAG','STR','VET','ALB','LAT','BOT','ZHO']
plotting.setup_mpl()

#Get seconds from laptime
def get_sec(string):
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

#input sector object and output sector time as string
def sectorToString(sector,indice):
    l = []
    l = sector.split()
    sector = l[indice][6:].replace("000","")
    return sector

#Transform sec to Laptime
def secToLap(flo):
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

#input the tyre ouput a short name of it
def typeOfTyre(tyre):
    if tyre == 'SOFT':
        tyre = 'S🔴'
    elif tyre == 'MEDIUM':
        tyre = 'M🟡'
    elif tyre == 'HARD':
        tyre = 'H⚪'
    elif tyre == 'INTERMEDIATE':
        tyre = 'I🟢'
    return tyre

#Object to string laptime
def lapToStringR(laptime):
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


def lapToStringP(laptime):
    l = []
    characters = "days "
    for i in range(len(characters)):
        laptime = laptime.replace(characters[i],"")
    laptime = re.sub(r'.', '', laptime, count = 6)
    laptime = laptime.replace("000","")

    l = laptime.split()
    lap = l[0]
    return lap

#Obtiene la vuelta rapida de un piloto
def fastlap(piloto):  
    fastlap = laps_r.pick_driver(piloto).pick_fastest()
    dic = {1:[]}
    ls = []
    #selecciona la vuelta
    #convertir vuelta a string
    driverLapLaptime = lapToStringR(str(fastlap.LapTime))
    print(fastlap['Sector1Time'])
    print(fastlap['Sector2Time'])
    print(fastlap['Sector3Time'])
    ls.append(sectorToString(str(fastlap['Sector1Time']),2))
    ls.append(sectorToString(str(fastlap['Sector2Time']),2))
    ls.append(sectorToString(str(fastlap['Sector3Time']),2))

    #Checa si existe el laptime de la vuelta
    if driverLapLaptime != ':LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'e:LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'elt64[n]':
        listDic, listComp = [],[]
        listComp = str(fastlap['Compound'])[0:].split()
        dic[1].append(driverLapLaptime)
        dic[1].append(listComp[0])
        dic[1].append(ls)
    return dic

#compare the fastest lap betwenn Sergio and Max
def compFastLapsRB():
    dic = {}
    dicVer = fastlap('VER')
    dicPer = fastlap('PER')
    secVer = float(get_sec(dicVer[1][0]))
    secPer = float(get_sec(dicPer[1][0]))
    tVer = dicVer[1][0]
    tPer = dicPer[1][0]
    tyreVer = typeOfTyre(dicVer[1][1])
    tyrePer = typeOfTyre(dicPer[1][1])
    
    checols = ['Perez','Checo','🇲🇽PER']
    verls = ['Verstappen','Max','🇳🇱VER']
    if (secVer < secPer): 
        tDiff = "{:.3f}".format(secPer - secVer)
        dic['Fastest'] = verls
        dic['Slowest'] = checols
        dic['Diferencia'] = tDiff
        dic['LaptimeF'] = dicVer[1][0]
        dic['LaptimeS'] = dicPer[1][0]
        dic['Fsectors'] = dicVer[1][2]
        dic['Ssectors'] = dicPer[1][2]
        dic['TyreF'] = tyreVer
        dic['TyreS'] = tyrePer
    else:
        tDiff = "{:.3f}".format(secVer - secPer)
        dic['Fastest'] = checols
        dic['Slowest'] = verls
        dic['Diferencia'] = tDiff
        dic['LaptimeF'] = dicPer[1][0]
        dic['LaptimeS'] = dicVer[1][0]
        dic['Fsectors'] = dicPer[1][2]
        dic['Ssectors'] = dicVer[1][2]
        dic['TyreF'] = tyrePer
        dic['TyreS'] = tyreVer
    return dic

#Average of the laps in the stints
def avgStint(piloto):
    driverSesionLaps = laps_r.pick_driver(piloto)
    driverSesionLaps = driverSesionLaps.pick_fastest()
    fastestLap = float(get_sec(lapToStringR(str(driverSesionLaps['LapTime']))))
    dic = lapsInStint(piloto)
    dicNew = {}
    for i in dic:
        cont = 0
        fastest = 200
        avg = 0
        avgs1 = 0
        avgs2 = 0
        avgs3 = 0
        for a in dic[i]:
            if fastest > float(get_sec(a[0])):
                fastest = float(get_sec(a[0])) 
                s1 = float(a[3][0])
                s2 = float(a[3][1])
                s3 = float(a[3][2])
                tyre = a[1]
        fastest += 1.5
        ls =[]
        for x in dic[i]:
            actual = float(get_sec(x[0]))
            
            if fastest >= actual and fastest < 200:
                
                avgs1 += float(x[3][0])
                avgs2 += float(x[3][1])
                avgs3 += float(x[3][2])
                avg += actual
                 
                ls.append(secToLap(actual))
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
            dic1 = {'Average': secToLap(avg),'Tyre':typeOfTyre(tyre),'LapNumber':cont,'Tipo':tipo,'Laps':ls,'Fastest':secToLap(fastest-1.5),'AvgS1':avgs1,'AvgS2':avgs2,'AvgS3':avgs3,'S1':s1,'S2':s2,'S3':s3}
            
            dicNew[i] = dic1
    return dicNew

#Carga las vueltas por stint en un diccionario de una sesion
def lapsInStint(piloto):
    #carga las vueltas de verstappen
    driverSesionLaps = laps_r.pick_driver(piloto)
    #print(driverSesionLaps)
    dic = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    for a in driverSesionLaps.LapNumber:
        ls =[]
        #selecciona la vuelta
        driverLap =  driverSesionLaps[driverSesionLaps.LapNumber==a]
        
        
        #convertir vuelta a string
        driverLapLaptime = lapToStringR(str(driverLap.LapTime))

        #Obtener stint de la vuelta
        listStint = []
        listStint = re.sub(r'.', '', str(driverLap['Stint']), count = 2)[3:].split()
        stint = float(listStint[0])

        #Checa si existe el laptime de la vuelta
        if driverLapLaptime != ':LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'e:LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'elt64[n]':
            
            ls.append(sectorToString(str(driverLap['Sector1Time']),3))
            ls.append(sectorToString(str(driverLap['Sector2Time']),3))
            ls.append(sectorToString(str(driverLap['Sector3Time']),3))
            listDic, listComp = [],[]
            listComp = str(driverLap['Compound'])[4:].split()
            listDic.append(driverLapLaptime)
            listDic.append(listComp[0])
            listDic.append(a)
            listDic.append(ls)
            dic[stint].append(listDic)
    return dic


def velMax(piloto):
    driverLaps = laps_r.pick_driver(piloto)
    driverFastest = driverLaps.pick_fastest()

    vel = 0
    driverTel = driverFastest.get_car_data()
    for i in driverTel['Speed']:
        if(int(i) > vel):
            vel = int(i) 
    return vel


def SessionFastest():
    laps = []
    cont = 0
    for i in listDrivers:
        driverLaps = laps_r.pick_driver(i)
        driverFastest = driverLaps.pick_fastest()
        laps.append((get_sec(lapToStringR(str(driverFastest['LapTime']))),i))  
    final = []
    lenlist =len(listDrivers)
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
    return final

#String para tweet comparacion de la vuelta rapida en la sesion de checo y verstappen
def tweetFastLapPV():
    dic = {}
    dic = compFastLapsRB()
    diffS1 = float("{:.3f}".format(float(dic['Ssectors'][0]) - float(dic['Fsectors'][0])))
    if diffS1 >= 0: diffS1 = "+"+str(diffS1)
    diffS2 = float("{:.3f}".format(float(dic['Ssectors'][1]) - float(dic['Fsectors'][1])))
    if diffS2 >= 0: diffS2 = "+"+str(diffS2)
    diffS3 = float("{:.3f}".format(float(dic['Ssectors'][2]) - float(dic['Fsectors'][2])))
    if diffS3 >= 0: diffS3 = "+"+str(diffS3)
    
    text = DicSesion[sesion]+"\nMas rapido " + dic['Fastest'][2] + " a una vuelta que "+ dic['Slowest'][2] +"\n\n"+ dic['Fastest'][2] + ": " + dic['LaptimeF'] +" "+dic['TyreF']+ "\n S1: " +dic['Fsectors'][0]+"   S2: "+dic['Fsectors'][1]+"   S3: "+dic['Fsectors'][2]+"\n\n"+ dic['Slowest'][2] + ": " + dic['LaptimeS']+ " "+dic['TyreS']+"\n S1: " +dic['Ssectors'][0]+"   S2: "+dic['Ssectors'][1]+"    S3: "+dic['Ssectors'][2]+ "\n\nGap +" +dic['Diferencia'] +" ( S1: "+str(diffS1)+", S2: "+str(diffS2)+", S3: "+str(diffS3)+")\n#"+str((race.event['EventName'])).replace(" ", "")+ " #NeverGiveUP"
    return text


def tweetStintCarrera(piloto):
    dic = avgStint(piloto)
    text = []
    text1 = dicDrivers[piloto]+ ' 𝙎𝙞𝙢𝙪𝙡𝙖𝙘𝙞𝙤𝙣 𝘾𝙖𝙧𝙧𝙚𝙧𝙖 '+DicSesion[sesion]+'\n\n'
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
    #text += '\n#F1 #SP11'
    return text


def tweetStintQualy(piloto):
    dic = avgStint(piloto)
    cont = 0
    text = []
    text1 = dicDrivers[piloto]+ ' 𝙑𝙪𝙚𝙡𝙩𝙖𝙨 𝙋𝙤𝙘𝙖 𝙂𝙖𝙨𝙤𝙡𝙞𝙣𝙖 '+DicSesion[sesion]+'\n\n'
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
    #text += '\n#F1 #SP11'
    return text


def tweetStintQualyRF():
    dicNew = {}
    dicPER = avgStint('PER')
    dicVER = avgStint('VER')
    dicLEC = avgStint('LEC')
    dicSAI = avgStint('SAI')
    cont = 0
    i = 1

    #New Dictionaries with the data of the 4 drivers
    for a in dicPER:
        if dicPER[a]['Tipo']=='Sim. Qualy':
                dic1 = {'Fastest': get_sec(dicPER[a]['Fastest']),'Tyre':str(dicPER[a]['Tyre']),'LapNumber':str(dicPER[a]['LapNumber']),'Driver':'🇲🇽PER','S1':dicPER[a]['S1'],'S2':dicPER[a]['S2'],'S3':dicPER[a]['S3']}
                dicNew[i]=dic1  
                i += 1
    for b in dicVER:
        if dicVER[b]['Tipo']=='Sim. Qualy':
                dic1 = {'Fastest': get_sec(dicVER[b]['Fastest']),'Tyre':str(dicVER[b]['Tyre']),'LapNumber':str(dicVER[b]['LapNumber']),'Driver':'🇳🇱VER','S1':dicVER[b]['S1'],'S2':dicVER[b]['S2'],'S3':dicVER[b]['S3']}
                dicNew[i]=dic1    
                i += 1
    for c in dicLEC:
        if dicLEC[c]['Tipo']=='Sim. Qualy':
                dic1 = {'Fastest': get_sec(dicLEC[c]['Fastest']),'Tyre':str(dicLEC[c]['Tyre']),'LapNumber':str(dicLEC[c]['LapNumber']),'Driver':'🇲🇨LEC','S1':dicLEC[c]['S1'],'S2':dicLEC[c]['S2'],'S3':dicLEC[c]['S3']}
                dicNew[i]=dic1
                i += 1 
    for d in dicSAI:
        if dicSAI[d]['Tipo']=='Sim. Qualy':
            if cont < 2:
                dic1 = {'Fastest': get_sec(dicSAI[d]['Fastest']),'Tyre':str(dicSAI[d]['Tyre']),'LapNumber':str(dicSAI[d]['LapNumber']),'Driver':'🇪🇸SAI','S1':dicSAI[d]['S1'],'S2':dicSAI[d]['S2'],'S3':dicSAI[d]['S3']}
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
    
    text = DicSesion[sesion]+'\n𝗦𝗶𝗺𝘂𝗹𝗮𝗰𝗶𝗼𝗻 𝗱𝗲 Qualy\n🇦🇹 𝐑𝐞𝐝 𝐁𝐮𝐥𝐥 𝐯𝐬 𝐅𝐞𝐫𝐫𝐚𝐫𝐢 🇮🇹\nMejores 2 intentos\n\n'
    lsNumber = [0,'1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣',8,9,10]
    for g in dicFinal:
        i+=1
        
        if len(text) > 198:
            if len(text1) >198:
                if cont == 1:
                    text1 += '2 \ 3 ⤵'
                    cont+=1
                text2 += str(lsNumber[i]) + ".-"+str(dicFinal[g]['Driver'])+"  Lap: "+str(secToLap(dicFinal[g]['Fastest']))+"  "+str(dicFinal[g]['Tyre'])+ "\n\n"   
            else:
                if cont == 0:
                    text += '1 \ 2 ⤵'
                    cont+=1
                text1 += str(lsNumber[i]) + ".-"+str(dicFinal[g]['Driver'])+"  Lap: "+str(secToLap(dicFinal[g]['Fastest']))+"  "+str(dicFinal[g]['Tyre'])+ "\n\n" 
        else:
            text += str(lsNumber[i]) + ".-"+str(dicFinal[g]['Driver'])+"  Lap: "+str(secToLap(dicFinal[g]['Fastest']))+"  "+str(dicFinal[g]['Tyre'])+ "\n\n"

    return text,text1,text2
   

def tweetStintCarreraRF():
    dicNew = {}
    dicPER = avgStint('PER')
    dicVER = avgStint('VER')
    dicLEC = avgStint('LEC')
    dicSAI = avgStint('SAI')
    print(dicPER)

    i = 1
    for a in dicPER:
        if dicPER[a]['Tipo']=='Sim. Carrera':
            dic1 = {'Average': get_sec(dicPER[a]['Average']),'Tyre':str(dicPER[a]['Tyre']),'LapNumber':str(dicPER[a]['LapNumber']),'Driver':'🇲🇽PER','AvgS1':dicPER[a]['AvgS1'],'AvgS2':dicPER[a]['AvgS2'],'AvgS3':dicPER[a]['AvgS3']}
            dicNew[i]=dic1
            i += 1
    for b in dicVER:
        if dicVER[b]['Tipo']=='Sim. Carrera':
            dic1 = {'Average': get_sec(dicVER[b]['Average']),'Tyre':str(dicVER[b]['Tyre']),'LapNumber':str(dicVER[b]['LapNumber']),'Driver':'🇳🇱VER','AvgS1':dicVER[b]['AvgS1'],'AvgS2':dicVER[b]['AvgS2'],'AvgS3':dicVER[b]['AvgS3']}
            dicNew[i]=dic1
            i += 1
    for c in dicLEC:
        if dicLEC[c]['Tipo']=='Sim. Carrera':
            print(dicLEC[c]['Average'])
            dic1 = {'Average': get_sec(dicLEC[c]['Average']),'Tyre':str(dicLEC[c]['Tyre']),'LapNumber':str(dicLEC[c]['LapNumber']),'Driver':'🇲🇨LEC','AvgS1':dicLEC[c]['AvgS1'],'AvgS2':dicLEC[c]['AvgS2'],'AvgS3':dicLEC[c]['AvgS3']}
            dicNew[i]=dic1
            i += 1
    #print(dicNew)
    for d in dicSAI:
        if dicSAI[d]['Tipo']=='Sim. Carrera':
            dic1 = {'Average': get_sec(dicSAI[d]['Average']),'Tyre':str(dicSAI[d]['Tyre']),'LapNumber':str(dicSAI[d]['LapNumber']),'Driver':'🇪🇸SAI','AvgS1':dicSAI[d]['AvgS1'],'AvgS2':dicSAI[d]['AvgS2'],'AvgS3':dicSAI[d]['AvgS3']}
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
        print(dicFinal)
        dicNew.pop(fastest)
    text1 =''
    cont = 0
    lsNumber = [0,'1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣',8,9,10]
    text = DicSesion[sesion]+'\n𝗦𝗶𝗺𝘂𝗹𝗮𝗰𝗶𝗼𝗻 𝗱𝗲 𝗰𝗮𝗿𝗿𝗲𝗿𝗮\n🇦🇹 𝐑𝐞𝐝 𝐁𝐮𝐥𝐥 𝐯𝐬 𝐅𝐞𝐫𝐫𝐚𝐫𝐢 🇮🇹\n\n'
   
    for g in dicFinal:
        if len(text) > 190:
            if cont == 0:
                text += '1 \ 2 ⤵'
                cont+=1
            text1 += str(lsNumber[g]) + " " + str(dicFinal[g]['Driver'])+"  Ritmo: "+ str(secToLap(dicFinal[g]['Average']))+ "  v:"+str(dicFinal[g]['LapNumber'])+ "  " +str(dicFinal[g]['Tyre'])+ "\n \n"
        else:
            text += str(lsNumber[g])  + " " + str(dicFinal[g]['Driver'])+"  Ritmo: "+ str(secToLap(dicFinal[g]['Average']))+ "  v:"+str(dicFinal[g]['LapNumber'])+ "  " +str(dicFinal[g]['Tyre'])+ "\n \n"

    return text,text1


def tweetPromedioStint(piloto):
    dic = avgStint(piloto)
    text = '🇲🇽Checo Tiempos FP1 🏁\n\n'
    for a in dic:
        text += "Ritmo: "+str(a)+" 𝐀𝐯𝐠: "+str(dic[a]['Average'])+" - "+ str(dic[a]['LapNumber'])+"L - "+ str(dic[a]['Tyre'])+" " +str(dic[a]['Tipo'])+"\n"
    #text += '\n#F1 #SP11'
    return text


def tweetVueltasDadas(piloto):
    driverLaps = laps_r.pick_driver('PER')
    cont = 1
    vueltas = 0
    for i in driverLaps:
        cont +=1
        print(cont)
    
    dic = avgStint(piloto)
    for i in dic:
        if dic[i]['Tipo'] == 'Sim. Qualy' or dic[i]['Tipo'] == 'Vueltas Rapidas' or dic[i]['Tipo'] == 'Sim. Carrera':
            vueltas += int(dic[i]['LapNumber'])
    text = 'Total de vueltas dadas en '+str(DicSesion[sesion])+ ' por '+dicDrivers[piloto]+'\n\n' +str(cont)+"\n\nVueltas efectivas: \n\n"+str(vueltas)

    return text
        


# Configurar gráficos
ff1.plotting.setup_mpl()

# Habilitamos el cache en nuestro equipo
ff1.Cache.enable_cache('C:/Users/admin/Desktop/Programas/Python/Algoritmo/__pycache__') 

# Ignoramos los Warning
pd.options.mode.chained_assignment = None 

# Cargar la carrera y clasificación
race = ff1.get_session(2022, int(carrera), sesion)
pathApi = ff1.api.make_path('Hungarian Grand Prix', '2022-07-31','Race','2022-07-31')
sss = ff1.api.session_status_data(pathApi)

quali = ff1.get_session(2021, 'Yas Marina', 'Q')
res = ''
live,live1 = ff1.api.timing_data(pathApi)
car = ff1.api.car_data(pathApi)
# Get the laps

laps_r = race.load_laps(with_telemetry=True)
#ppp = sss.load(laps =True)
live11 = live1[live1.Driver == '11']

live12 = live = live[live.Driver == '11']

best = live12[live12.IsPersonalBest == True]



laps_r.head()
race.load()
fastest_lap = laps_r

#print(f'Vuelta más rápida: ',fastest_lap['LapTime'])
#print(f'Tipo de neumático: ',fastest_lap['Compound'])
#print(f'Piloto: ',fastest_lap['Driver'])

PER_lap = laps_r.pick_driver('PER')


VER_lap = laps_r.pick_driver('VER')
PER_Fastest = PER_lap.pick_fastest()
VER_Fastest = VER_lap.pick_fastest()
#print(PER_lap)
print(PER_lap)
#PER_actual = PER_lap[PER_lap.LapNumber==10]
#VER_actual = VER_lap[VER_lap.LapNumber==10]

'''
delta_time, ref_tel, compare_tel = utils.delta_time(PER_Fastest, VER_Fastest)


fig, ax = plt.subplots()
# use telemetry returned by .delta_time for best accuracy,
# this ensure the same applied interpolation and resampling
ax.plot(ref_tel['Distance'], ref_tel['Speed'],
        color='blue')
ax.plot(compare_tel['Distance'], compare_tel['Speed'],
        color='red')

twin = ax.twinx()
twin.plot(ref_tel['Distance'], delta_time, '--', color='white')
twin.set_ylabel("<-- Lec ahead | Ham ahead -->")
plt.show()
'''
#print(ver_lap)
#di = lapsInStint('PER')
#print(di)

#print(tweetPromedioStint('PER'))
#lapsStint()
#print(avgStint('SAI'))
#print(tweetStintQualy('PER')



from calendar import c
import re
import fastf1 as ff1
import pandas as pd
from datetime import date 
from fastf1 import utils
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import boto3
import io

#dddasd
s3 = boto3.resource("s3")
s3_client = boto3.client('s3')
bucket = s3.Bucket("checobot")
#bucket.upload_file(Key="",Filename="")

ff1.Cache.enable_cache('C:/Users/admin/Documents/Github/BotTwitter/__pycache__') 
pd.options.mode.chained_assignment = None 

#test
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
    elif flo - 60 >=60:
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
    if "000" in laptime:
        laptime = laptime.replace("000","")
    l = laptime.split()
    lap = l[0]
   

    while True:
        if(len(lap) <= 8):
            if lap[0] == ":" or lap[0] == "0" :
                if len(lap) == 1:
                    lap = '2:00.000'
                else:
                    lap= lap[1:]
            else:
                break
        else:
            lap= lap[1:]
    diferencia = 8- len(lap)
    arraDif = ".000"
    if len(lap) < 8:
        lap = lap + arraDif[-abs(diferencia):]
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
    elif tyre =='WET':
        tyre = 'W🔵'
    return tyre

class Sesion:
    DicDrivers = {'PER':'🇲🇽PER','LEC':'🇲🇨LEC','VER':'🇳🇱VER','SAI':'🇪🇸SAI','ALO':'🇪🇸ALO','HAM':'🇬🇧HAM','RUS':'🇬🇧RUS','OCO':'🇫🇷OCO','NOR':'🇬🇧NOR','RIC':'🇦🇺RIC','GAS':'🇫🇷GAS','TSU':'🇯🇵TSU','MSC':'🇩🇪MSC','MAG':'🇩🇰MAG','STR':'🇨🇦STR','VET':'🇩🇪VET','ALB':'🇹🇭ALB','LAT':'🇨🇦LAT','BOT':'🇫🇮BOT','ZOU':'🇨🇳ZOU','HUL':'🇩🇪HUL','DEV':'🇳🇱DEV','FIT':'🇧🇷FIT','PAL':'🇪🇸PAL','OWA':'🇲🇽OWA','GIO':'🇮🇹GIO','POU':'🇫🇷POU','SAR':'🇺🇸SAR','SHW':'SHW','PIA':'PIA🇦🇺'}
    DicSesion = {'FP1':'F P 1 🏁','FP2':'F P 2 🏁','FP3':'F P 3 🏁','Q':'Qualy 🏁','R':'Race 🏁','S':'Sprint Race 🏁'}
    DicCalendar = {1:"BAHRAIN",2:"ARABIA SAUDITA",3:"AUSTRALIA",4:"AZERBAIJAN",5:"MIAMI",6:"MONACO",7:"ESPAÑA",8:"CANADA",9:"AUSTRIA",10:"GRAN BRETAÑA",11:"HUNGRIA",12:"BELGICA",13:"PAISES BAJOS",14:"ITALIA",15:"SINGAPURE",16:"JAPON",17:"QATAR",18:"USA",19:"MEXICO",20:"BRAZIL",21:"LAS VEGAS",22:"ABU DHABI"}
    DicCalendarFlag = {1:"🇧🇭",2:"🇸🇦",3:"🇦🇺",4:"🇦🇿",5:"🇺🇸",6:"🇮🇹",7:"🇲🇨",8:"🇪🇸",9:"🇨🇦",10:"🇦🇹",11:"🇬🇧",12:"🇭🇺",13:"🇧🇪",14:"🇳🇱",15:"🇮🇹",16:"🇸🇬",17:"🇯🇵",18:"🇶🇦",19:"🇺🇸",20:"🇲🇽",21:"🇧🇷",22:"🇺🇸",23:"🇦🇪"}
    DicTeams = {'RedBull':('PER','VER'),'Ferrari':('SAI','LEC'),'Mercedes':('HAM','RUS'),'Alphine':('GAS','OCO'),'Mclaren':('PIA','NOR'),'AlfaRomeo':('BOT','ZHO'),'AlphaTauri':('RIC','TSU'),'Hass':('HUL','MAG'),'AstonMartin':('ALO','STR'),'Williams':('SAR','ALB')}
    DicTeamsVel = {'RedBull':0,'Ferrari':0,'Mercedes':0,'Alphine':0,'Mclaren':0,'AlfaRomeo':0,'AlphaTauri':0,'Hass':0,'AstonMartin':0,'Williams':0}
    DicTeamsColor = {'RedBull':'#011E3D','Ferrari':'#ED1C24','Mercedes':'#00A19B','Alphine':'#2173B8','Mclaren':'#FF8000','AlfaRomeo':'#981E32','AlphaTauri':'#2B4562','Hass':'White','AstonMartin':'#00594F','Williams':'#00A3E0'}
    listTeams = ['RedBull','Ferrari','Mercedes','Alphine','Mclaren','AlfaRomeo','AlphaTauri','Hass','AstonMartin','Williams']
    
    def __init__(self,year,weekend,sesion):  
        self.sesion = sesion
        self.weekend = weekend
        self.session= ff1.get_session(year,weekend,sesion)
        self.driverDataLapsLoad = self.session.load_laps(with_telemetry=True)
        self.listDrivers = []
        cont = 0
        for i in self.driverDataLapsLoad['Driver']:
            cont +=1
            if i not in self.listDrivers:
                self.listDrivers.append(i)

    def test(self):

        #print(self.session.__dict__)
        print(self.session.event)
    
    def dic_stints1(self,driver):  
            #driver---name of the driver

            dic = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
            driverDataLaps = self.session.load_laps(with_telemetry=True).pick_driver(driver)
            cont = 0
            avg = 0
            for a in driverDataLaps.LapNumber:
                ls =[]
                #selecciona la vuelta
                if a > 23 and a < 43:
                    cont +=1
                    currentDriverLap =  driverDataLaps[driverDataLaps.LapNumber==a] 
                    currentDriverLapTime  = get_lapFromObject(str(currentDriverLap.LapTime))
                    #print(str(currentDriverLap.LapTime))
                    #Obtener stint de la vuelta
                    listStint = []
                    listStint = re.sub(r'.', '', str(currentDriverLap['Stint']), count = 2)[3:].split()
                    stint = float(listStint[0])
                    freshTyre = str(currentDriverLap.FreshTyre).split()
                    
                    #Checa si existe el laptime de la vuelta
                    if currentDriverLapTime != ':LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'e:LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'elt64[n]':
                        if freshTyre[1] == 'True':
                            Tyrelife = 'New'
                        else:
                            Tyrelife = 'Used'
                        ls.append(get_sectorFromObject(str(currentDriverLap['Sector1Time']),3))
                        ls.append(get_sectorFromObject(str(currentDriverLap['Sector2Time']),3))
                        ls.append(get_sectorFromObject(str(currentDriverLap['Sector3Time']),3))
                        listDic, listComp = [],[]
                        listComp = str(currentDriverLap['Compound'])[4:].split()   
                        listDic.append(currentDriverLapTime)
                        avg+=float(get_secFromLap(currentDriverLapTime))
                        listDic.append(listComp[0])
                        listDic.append(a)
                        listDic.append(ls)
                        listDic.append(Tyrelife)
                        dic[stint].append(listDic)
            avg = "{:.3f}".format(avg/cont)
            avg = get_lapFromSec(avg)
            print(avg)

            return dic
    
    def dic_stints(self,driver):  
        #driver---name of the driver

        dic = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
        driverDataLaps = self.session.load_laps(with_telemetry=True).pick_driver(driver)
        
        for a in driverDataLaps.LapNumber:
            ls =[]
            #selecciona la vuelta
            currentDriverLap =  driverDataLaps[driverDataLaps.LapNumber==a] 
            currentDriverLapTime  = get_lapFromObject(str(currentDriverLap.LapTime))
            #print(str(currentDriverLap.LapTime))
            #Obtener stint de la vuelta
            listStint = []
            listStint = re.sub(r'.', '', str(currentDriverLap['Stint']), count = 2)[3:].split()
            stint = float(listStint[0])
            freshTyre = str(currentDriverLap.FreshTyre).split()
            
            #Checa si existe el laptime de la vuelta
            if currentDriverLapTime != ':LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'e:LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'elt64[n]':
                if freshTyre[1] == 'True':
                    Tyrelife = 'New'
                else:
                    Tyrelife = 'Used'
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector1Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector2Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector3Time']),3))
                listDic, listComp = [],[]
                listComp = str(currentDriverLap['Compound'])[4:].split()   
                listDic.append(currentDriverLapTime)
                listDic.append(listComp[0])
                listDic.append(a)
                listDic.append(ls)
                listDic.append(Tyrelife)
                dic[stint].append(listDic)
        return dic
    
    def dic_stintstest(self,driver):  
        #driver---name of the driver
        Session=ff1.get_testing_session ( 2023 , 1 , 3 )

        Session.load(laps=True, telemetry=True, weather=True, messages=True, livedata=None)
        driverDataLaps=Session.laps.pick_driver(driver)
       
        dic = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
        
        
        for a in driverDataLaps.LapNumber:
            ls =[]
            #selecciona la vuelta
            currentDriverLap =  driverDataLaps[driverDataLaps.LapNumber==a] 
            currentDriverLapTime  = get_lapFromObject(str(currentDriverLap.LapTime))
            #print(str(currentDriverLap.LapTime))
            #Obtener stint de la vuelta
            listStint = []
            listStint = re.sub(r'.', '', str(currentDriverLap['Stint']), count = 2)[3:].split()
            stint = float(listStint[0])
            freshTyre = str(currentDriverLap.FreshTyre).split()
            
            #Checa si existe el laptime de la vuelta
            if currentDriverLapTime != ':LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'e:LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'elt64[n]':
                if freshTyre[1] == 'True':
                    Tyrelife = 'New'
                else:
                    Tyrelife = 'Used'
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector1Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector2Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector3Time']),3))
                listDic, listComp = [],[]
                listComp = str(currentDriverLap['Compound'])[4:].split()   
                listDic.append(currentDriverLapTime)
                listDic.append(listComp[0])
                listDic.append(a)
                listDic.append(ls)
                listDic.append(Tyrelife)
                dic[stint + 1] = []
                dic[stint + 2] = []
                dic[stint + 3] = []
                dic[stint + 4] = []
                dic[stint].append(listDic)
        return dic

    def dic_avg_stintstest(self,driver):
        #driver---name of the driver
        Session=ff1.get_testing_session ( 2023 , 1 , 3 )
        Session.load(laps=True, telemetry=True, weather=True, messages=True, livedata=None)
        driverDataLaps=Session.laps.pick_fastest()
        #obtiene la vuelta mas rapida de la sesion del piloto
        fastestLap = float(get_secFromLap(get_lapFromObject(str(driverDataLaps['LapTime']))))

        #obtiene los stints del piloto en la sesion 
        dic = self.dic_stintstest(driver)
        dicNew = {}
        for i in dic:
            cont = 0
            fastest = 200
            avg = 0
            avgs1 = 0
            avgs2 = 0
            avgs3 = 0
            error = 0
            for a in dic[i]:#find fastest lap of the stint 
                if fastest > float(get_secFromLap(a[0])):
                    fastest = float(get_secFromLap(a[0]))
                    try:
                        s1 = float(a[3][0])
                        s2 = float(a[3][1])
                        s3 = float(a[3][2])
                    except:
                        s1 = 0.0
                        s2 = 0.0
                        s3 = 0.0
                        error+=1
                    tyre = a[1]
            fastest += 2.8
            ls =[]
            for x in dic[i]:
                actual = float(get_secFromLap(x[0]))
                if fastest >= actual and fastest < 200:
                    try:
                        avgs1 += float(x[3][0])
                        avgs2 += float(x[3][1])
                        avgs3 += float(x[3][2])
                        avg += actual
                        ls.append(get_lapFromSec(actual))
                        cont +=1   
                    except ValueError:
                        print ("Not a float")
            if cont !=0:     
                avg = "{:.3f}".format(avg/cont)
                avgs1 = float("{:.3f}".format(avgs1/(cont-error)))
                avgs2 = float("{:.3f}".format(avgs2/(cont-error)))
                avgs3 = float("{:.3f}".format(avgs3/(cont-error)))
                tipo = "test"

                dic1 = {'Average': get_lapFromSec(avg),'Tyre':get_typeOfTyre(tyre),'LapNumber':cont,'Tipo':tipo,'Fastest':get_lapFromSec(fastest-2.8),'AvgS1':avgs1,'AvgS2':avgs2,'AvgS3':avgs3,'S1':s1,'S2':s2,'S3':s3}
                if int(dic1['LapNumber']) > 3:
                    dicNew[i] = dic1
        return dicNew

    def dic_avg_stints(self,driver):
        #driver---name of the driver

        #obtiene la vuelta mas rapida de la sesion del piloto
        data=self.session.load_laps(with_telemetry=True)
        datafastest=data.pick_fastest()
        fastestLap = float(get_secFromLap(get_lapFromObject(str(datafastest['LapTime']))))

        #obtiene los stints del piloto en la sesion 
        dic = self.dic_stints(driver)
        dicNew = {}
        for i in dic:
            cont = 0
            fastest = 200
            avg = 0
            avgs1 = 0
            avgs2 = 0
            avgs3 = 0
            error = 0
            for a in dic[i]:#find fastest lap of the stint 
                if fastest > float(get_secFromLap(a[0])):
                    fastest = float(get_secFromLap(a[0]))
                    try:
                        s1 = float(a[3][0])
                        s2 = float(a[3][1])
                        s3 = float(a[3][2])
                    except:
                        s1 = 0.0
                        s2 = 0.0
                        s3 = 0.0
                        error+=1
                    tyre = a[1]
            fastest += 2.8
            ls =[]
            for x in dic[i]:
                actual = float(get_secFromLap(x[0]))
                if fastest >= actual and fastest < 200:
                    try:
                        avgs1 += float(x[3][0])
                        avgs2 += float(x[3][1])
                        avgs3 += float(x[3][2])
                        avg += actual
                        ls.append(get_lapFromSec(actual))
                        cont +=1   
                    except ValueError:
                        print ("Not a float")
            if cont !=0:     
                avg = "{:.3f}".format(avg/cont)
                avgs1 = float("{:.3f}".format(avgs1/(cont-error)))
                avgs2 = float("{:.3f}".format(avgs2/(cont-error)))
                avgs3 = float("{:.3f}".format(avgs3/(cont-error)))
                if fastest - 2.8 < fastestLap + 1.5 and len(ls) < 3:
                    tipo = 'Sim. Qualy'
                    """elif fastest - 2.8 < fastestLap + 2.0:
                        tipo = 'Vueltas Rapidas'"""
                elif (fastest - 2.8 < fastestLap + 10 and len(ls) > 4 and float(avg) > fastestLap + 3) or len(ls) > 5:
                    tipo = 'Sim. Carrera'
                elif fastest - 2.8 > fastestLap + 10:
                    tipo = 'Vueltas practica'
                else:
                    tipo = 'Vueltas de instalacion'
                dic1 = {'Average': get_lapFromSec(avg),'Tyre':get_typeOfTyre(tyre),'LapNumber':cont,'Tipo':tipo,'Laps':ls,'Fastest':get_lapFromSec(fastest-2.8),'AvgS1':avgs1,'AvgS2':avgs2,'AvgS3':avgs3,'S1':s1,'S2':s2,'S3':s3}
                dicNew[i] = dic1
        return dicNew

    def dic_sim_racepace_stints(self,*driver):
        #*driver--- name of the driver or drivers

        dicNew = {}
        dic1,dic2 = {},{}
        ls = []
        
        for i,d in enumerate(driver,1):
            if d in self.listDrivers:
                dic1 = self.dic_avg_stints(d)
                for a in dic1:
                    if dic1[a]['Tipo']=='Sim. Carrera':
                         dic2 = {'Average': get_secFromLap(dic1[a]['Average']),'Tyre':str(dic1[a]['Tyre']),'LapNumber':str(dic1[a]['LapNumber']),'Driver':d,'AvgS1':dic1[a]['AvgS1'],'AvgS2':dic1[a]['AvgS2'],'AvgS3':dic1[a]['AvgS3']}
                         dicNew[i] = dic2
        return dicNew

    def graph_vel_max_teams(self):
        dicteams = {}
        text = '𝐕𝐞𝐥𝐨𝐜𝐢𝐝𝐚𝐝 𝐦á𝐱𝐢𝐦𝐚 𝐩𝐨𝐫 𝐞𝐪𝐮𝐢𝐩𝐨𝐬\n'+ self.DicSesion[self.sesion]+" "+str((self.session.event['EventName'])).replace(" ", "")+ " "+self.DicCalendarFlag[self.weekend]+'\n'
        teamVel,final = self.get_session_vel_max()
        print(teamVel)
        for (key, value) in teamVel:
            dicteams.setdefault(key, value)
        colors = []
        x = list(dicteams.keys())
        y = list(dicteams.values())
        for i in x:
            colors.append(self.DicTeamsColor[i]) 
        fig,ax1 = plt.subplots(figsize =(14,8),facecolor='#1f1f23',edgecolor='#85929E')
        axes = ax1.bar(x, y,width=.6,color = colors,align='center',edgecolor='#85929E')
        ax1.set_title('Velocidad maxima por equipos \ Top speed\n' +self.sesion + " " +str((self.session.event['EventName'])).replace(" ", ""),color = "white",weight='bold')
        ax1.set_ylabel('km\h\n',color = "white",weight='bold')
        ax1.set_ylim(ymin=int(y[-1] - 3),ymax=(int(y[0])+3))
        fig.tight_layout()
        ax1.set_xticklabels(x,color = "white",weight='bold')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.grid(color = 'grey', linestyle = '--', linewidth = 0.4)
        ax1.set_facecolor("#0e0e10")
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.bar_label(axes, padding=3,color = 'white',weight='bold')
        ax1.text(0.85, 0.85, '@ChecoData', transform=ax1.transAxes,
        fontsize=15, color='gray', alpha=0.3,
        ha='center', va='center', rotation=20)
        for axis in ['top', 'bottom', 'left', 'right']:
                ax1.spines[axis].set_linewidth(2)  # change width
                ax1.spines[axis].set_color('#566573')    # change color

        #name of the file
        foto = self.sesion + str(self.DicCalendar[self.weekend]) + "velmax.png"
        #save image in bucket s3 
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        print(img_data)
        img_data.seek(0)
        bucket.put_object(Body=img_data, ContentType='image/png', Key="img/"+foto)

        return text,foto

    def graph_racepace_simulation(self):
        dicNew = {}
        i = 1
        dicNew = self.dic_sim_racepace_stints('PER','VER','LEC','SAI','HAM','RUS','ALO','STR','PIA','NOR')
        
        fastest = 0
        dicFinal = {}

        for f in range(1,len(dicNew)+1):
            fast = 201
            for e in dicNew:
                if float(dicNew[e]['Average']) < fast:
                    fast = float(dicNew[e]['Average'])
                    fastest = e
                    #print(e)
            dicFinal[f]=dicNew[fastest].copy()
            dicNew.pop(fastest)
        cont = 0
        textIntro = '𝐒𝐢𝐦𝐮𝐥𝐚𝐜𝐢𝐨𝐧 𝐫𝐢𝐭𝐦𝐨 𝐝𝐞 𝐜𝐚𝐫𝐫𝐞𝐫𝐚\n'+ self.DicSesion[self.sesion]+" "+str((self.session.event['EventName'])).replace(" ", "")+ " "+self.DicCalendarFlag[self.weekend]+'\n𝑹𝒆𝒅𝑩𝒖𝒍𝒍🇦🇹 - 𝑭𝒆𝒓𝒓𝒂𝒓𝒊🇮🇹 - 𝑴𝒆𝒓𝒄𝒆𝒅𝒆𝒔🇩🇪 - 𝑨𝒔𝒕𝒐𝒏 𝑴𝒂𝒓𝒕𝒊𝒏🇬🇧 - Mclaren🇬🇧\n'

        plotDic = {}
        colors = []
        
        for g in dicFinal:
            if(str(dicFinal[g]['Driver']) == 'PER' or str(dicFinal[g]['Driver']) == 'VER' ):
                colors.append("#001A57")
            elif(str(dicFinal[g]['Driver']) == 'LEC' or str(dicFinal[g]['Driver']) == 'SAI' ):
                colors.append("#CC0000")
            elif(str(dicFinal[g]['Driver']) == 'ALO' or str(dicFinal[g]['Driver']) == 'STR' ):
                colors.append("#00594F")
            elif(str(dicFinal[g]['Driver']) == 'NOR' or str(dicFinal[g]['Driver']) == 'PIA' ):
                colors.append("#FF8000")
            else:
                colors.append("#48C9B0")
            plotDic[str(g)+"- "+str(dicFinal[g]['Driver'])] = float(dicFinal[g]['Average']) - float(dicFinal[1]['Average'])

        def get_flag(name):
            path = "C:/Users/admin/Documents/png/{}.png".format(name.title())
            im = plt.imread(path)
            return im

        def offset_image(coord, name, ax):
            img = get_flag(name)
            im = OffsetImage(img, zoom=.05)
            im.image.axes = ax
            ab = AnnotationBbox(im, (0, coord),  xybox=(-15, -21), frameon=False,
                                xycoords='data',  boxcoords="offset points", pad=0)
            ax.add_artist(ab)
        
        print(plotDic)
        if len(plotDic) > 0:
            countries = list(plotDic.keys())
            valuesA = list(plotDic.values())
            xx = ['0','1','2','3']
        
            fig, ax = plt.subplots(figsize=(len(plotDic)+4,len(plotDic)+2),facecolor='#1f1f23')
            hbars =  ax.barh(range(len(countries)), valuesA, height=.5,color = colors,align='edge',edgecolor='#85929E')
            ax.set_yticks(range(len(countries)),color = "white")
            ax.set_xticks(range(4),color = "white")
            ax.set_xticklabels(xx,color = "white",weight='bold')
            ax.set_yticklabels(countries,color = "white",weight='bold')
            ax.tick_params(axis='x', which='major', pad=6,color = "white")
            ax.tick_params(axis='y', which='major', pad=6,color = "white")
            ax.invert_yaxis()
            for axis in ['top', 'bottom', 'left', 'right']:
                ax.spines[axis].set_linewidth(2)  # change width
                ax.spines[axis].set_color('#566573')    # change color
            ax.set_xlabel('Gap (seg)',color = "white",weight='bold')
            ax.set_title('Simulacion ritmo de carrera \ Race pace simulation \n' +self.sesion + " " +str((self.session.event['EventName'])).replace(" ", "")+'\n Gap to fastest '+ str(get_lapFromSec(dicFinal[1]['Average'])),color = "white",weight='bold')
            ax.set_facecolor("#0e0e10")
            ax.text(0.85, 0.85, '@ChecoData', transform=ax.transAxes,
            fontsize=12, color='gray', alpha=0.3,
            ha='center', va='center', rotation=20)
            fig.tight_layout()
            ax.set_xlim(right=valuesA[-1]+.3)
            for i, v in enumerate(valuesA):
                ax.text(v, i+.4, str(str(" +{:.2f}".format(v)) + "\n v:"+ str(dicFinal[i+1]['LapNumber'])), color='white', fontweight='bold')
            for i, c in enumerate(countries):
                offset_image(i, get_typeOfTyre(dicFinal[i+1]['Tyre']), ax)

            #name of the file
            foto = self.sesion + str(self.DicCalendar[self.weekend]) + "racepace.png"
            #save image in bucket s3 
            img_data = io.BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            bucket.put_object(Body=img_data, ContentType='image/png', Key="img/"+foto)
        else:
            textIntro = "No"
            foto = "No"
        return textIntro, foto

    def graph_telemetry_fastlap_of_two(self,driver1,driver2,sector):
        #driver1--- name of the driver 1
        #driver2--- name of the driver 2
        #sector--- 1 for sector 1, 2 for sector 2, 3 for sector 3, 4 for full lap
        
        sector = sector -1
        dicDriver1 = self.get_fastlap(driver1)
        dicDriver2 = self.get_fastlap(driver2)
        dicDriver1 = dicDriver1[1]
        dicDriver2 = dicDriver2[1]
        
        #fastlap1 = self.session.load_laps(with_telemetry=True).pick_driver(driver1).pick_fastest()
        #fastlap2 = self.session.load_laps(with_telemetry=True).pick_driver(driver2).pick_fastest()
        fastlap1 = self.session.load_laps(with_telemetry=True).pick_driver(driver1)
        fastlap2 = self.session.load_laps(with_telemetry=True).pick_driver(driver2)
        currentDriverLap1 =  fastlap1[fastlap1.LapNumber==2]
        currentDriverLap2 =  fastlap2[fastlap2.LapNumber==2]
        fl1_tel = currentDriverLap1.get_car_data().add_distance()
        fl2_tel = currentDriverLap2.get_car_data().add_distance()

        lst = fl2_tel['nGear']
        lst1 = []
        for i in lst:
            print(lst[i])
            if lst[i] < 9:
                lst1.append(lst[i])
            else:
                lst1.append(0)
        print(lst1)
        #fig, ax = plt.subplots()
        fig,(ax3,ax1,ax2) = plt.subplots(3,figsize =(18,12),sharex=True,gridspec_kw={'height_ratios': [4,2,1]})
        ax3.plot(fl2_tel['Distance'], fl2_tel['RPM'], color='Red', label='PER',ls='-')
        ax3.plot(fl1_tel['Distance'], fl1_tel['RPM'], color='Blue', label='VER',ls='--')
        ax2.plot(fl2_tel['Distance'], lst1 , color='Red', label='PER',ls='-')
        ax2.plot(fl1_tel['Distance'], fl1_tel['nGear'], color='Blue', label='VER',ls='--')
        ax1.plot(fl2_tel['Distance'], fl2_tel['DRS'], color='Red', label='PER',ls='-')
        ax1.plot(fl1_tel['Distance'], fl1_tel['DRS'], color='Blue', label='VER',ls='--')
        ax3.text(0.85, 0.9, '@SaedIbarra', transform=ax3.transAxes,
            fontsize=15, color='gray', alpha=0.3,
            ha='center', va='center', rotation=20)
        

        ax3.set_xlabel('Distance in m')
        ax3.set_ylabel('RPM')
        ax1.set_ylabel('DRS')
        ax2.set_ylabel('Gear')

        ax3.legend()
        plt.suptitle(f"Q1 Perez vs Verstappen\n ")

        plt.show()
        #fl1_tel = fastlap1.get_telemetry()
        #fl2_tel = fastlap2.get_telemetry()
        #fl1_tel = fastlap1.get_car_data().add_distance()
        #fl2_tel = fastlap2.get_car_data().add_distance()
        print(pd.DataFrame(fl1_tel['Time']).values.tolist())
        sectors1 = [float(dicDriver1['Sectors'][0]),float(dicDriver1['Sectors'][0])+float(dicDriver1['Sectors'][1]),float(dicDriver1['Sectors'][0])+float(dicDriver1['Sectors'][1])+float(dicDriver1['Sectors'][2])]
        sectors2 = [float(dicDriver2['Sectors'][0]),float(dicDriver2['Sectors'][0])+float(dicDriver2['Sectors'][1]),float(dicDriver2['Sectors'][0])+float(dicDriver2['Sectors'][1])+float(dicDriver2['Sectors'][2])]
        IndexDistanciaSectores = [[],[]]
        DistanciaSectores = []
        i = 0
        for cont in range(3):
            
            for l in fl1_tel['Time']:
                i+=1
                lap = str(l).split()
                times = lap[2]
                times = times[4:].replace("000","")
                print(l)
                print(i)
                
                if(float(get_secFromLap(times)) > sectors1[cont]):
                    IndexDistanciaSectores[0].append(i)
                    break
           
            for a,s in enumerate(fl2_tel['Time']):
                lap = str(s).split()
                times = lap[2]
                times = times[4:].replace("000","")
                if(float(get_secFromLap(times)) > sectors2[cont]):
                    IndexDistanciaSectores[1].append(a)
                    break
            
        IndexDistanciaSectores[0].append(len(fl1_tel['Time'])-1)
        IndexDistanciaSectores[1].append(len(fl2_tel['Time'])-1)
        DistanciaSectores = IndexDistanciaSectores[0].copy()
        for cont in range(3):
            for i,l in enumerate(fl1_tel['Distance']):
                if i == IndexDistanciaSectores[0][cont]:
                    DistanciaSectores[cont]=l
                    break

        arra = list(fl1_tel['Distance'])
        arra2 = list(fl2_tel['Distance'])
        
        
        x1 = [[],[],[]]
        x2 = [[],[],[]]
        x3 = [[],[],[]]
        y1 = [[[],[],[]],[[],[],[]],[[],[],[]]]
        y2 = [[[],[],[]],[[],[],[]],[[],[],[]]]
        y3 = [[[],[],[]],[[],[],[]],[[],[],[]]]
        
        for i,l in enumerate(arra):
            if i < IndexDistanciaSectores[0][0]:
                x1[0].append(l)
            elif i < IndexDistanciaSectores[0][1]:
                x1[1].append(l)
            elif i < IndexDistanciaSectores[0][2]:
                x1[2].append(l)
        for a,s in enumerate(arra2):
            if a < IndexDistanciaSectores[1][0]:
                x2[0].append(s)
            elif a < IndexDistanciaSectores[1][1]:
                x2[1].append(s)
            elif a < IndexDistanciaSectores[1][2]:
                x2[2].append(s)
        
        for i,data in enumerate(fl1_tel['Throttle']):
            if i < len(x1[0]):
                y1[0][0].append(data)
            elif i < (len(x1[0])+len(x1[1])):
                y1[0][1].append(data)
            elif i < (len(x1[0])+len(x1[1])+len(x1[2])):
                y1[0][2].append(data)
        for j,data in enumerate(fl2_tel['Throttle']):
            if j < len(x2[0]):
                y2[0][0].append(data)
            elif j < (len(x2[0])+len(x2[1])):
                y2[0][1].append(data)
            elif j < (len(x2[0])+len(x2[1])+len(x2[2])):
                y2[0][2].append(data)

        for k,data in enumerate(fl1_tel['Brake']):
            if k < len(x1[0]):
                y1[1][0].append(data)
            elif k < (len(x1[0])+len(x1[1])):
                y1[1][1].append(data)
            elif k < (len(x1[0])+len(x1[1])+len(x1[2])):
                y1[1][2].append(data)
        for l,data in enumerate(fl2_tel['Brake']):
            if l < len(x2[0]):
                y2[1][0].append(data)
            elif l < (len(x2[0])+len(x2[1])):
                y2[1][1].append(data)
            elif l < (len(x2[0])+len(x2[1])+len(x2[2])):
                y2[1][2].append(data)

        for k,data in enumerate(fl1_tel['Speed']):
            if k < len(x1[0]):
                y1[2][0].append(data)
            elif k < (len(x1[0])+len(x1[1])):
                y1[2][1].append(data)
            elif k < (len(x1[0])+len(x1[1])+len(x1[2])):
                y1[2][2].append(data)
        for l,data in enumerate(fl2_tel['Speed']):
            if l < len(x2[0]):
                y2[2][0].append(data)
            elif l < (len(x2[0])+len(x2[1])):
                y2[2][1].append(data)
            elif l < (len(x2[0])+len(x2[1])+len(x2[2])):
                y2[2][2].append(data)

                
       
        fig,(ax3,ax1,ax2) = plt.subplots(3,figsize =(18,12),facecolor='#000000',edgecolor='#85929E',sharex=True,gridspec_kw={'height_ratios': [4,2,1]})
        if sector == 3:
            text = '𝐓𝐞𝐥𝐞𝐦𝐞𝐭𝐫í𝐚 𝐯𝐮𝐞𝐥𝐭𝐚 𝐜𝐨𝐦𝐩𝐥𝐞𝐭𝐚 \n'+ self.DicSesion[self.sesion]+" "+str((self.session.event['EventName'])).replace(" ", "")+ " \n"+self.DicDrivers[str(driver1)]+' vs '+self.DicDrivers[str(driver2)]
            ax3.plot(fl1_tel['Distance'], fl1_tel['Speed'], color='#FFD300', label=driver1,ls='-')
            ax3.plot(fl2_tel['Distance'], fl2_tel['Speed'], color='#1D19AC', label=driver2,ls='-')
            ax1.plot(fl1_tel['Distance'], fl1_tel['Throttle'], color='#FFD300', label=driver1,ls='-')
            ax1.plot(fl2_tel['Distance'], fl2_tel['Throttle'], color='#1D19AC', label=driver2,ls='-')
            ax2.plot(fl1_tel['Distance'], fl1_tel['Brake'], color='#FFD300', label=driver1,ls='-')
            ax2.plot(fl2_tel['Distance'], fl2_tel['Brake'], color='#1D19AC', label=driver2,ls='-')
            ax3.set_title("Telemetria Vuelta Rapida " +str((self.session.event['EventName'])).replace(" ", "")+ "  \n" + driver1 + ": " + get_lapFromSec(dicDriver1['Lap']) + "\n" + driver2 + ": " + get_lapFromSec(dicDriver2['Lap']),color = "white",weight='bold')
        else:
            text = '𝐓𝐞𝐥𝐞𝐦𝐞𝐭𝐫í𝐚 𝐬𝐞𝐜𝐭𝐨𝐫 '+str(int(sector) +1)+'\n'+ self.DicSesion[self.sesion]+" "+str((self.session.event['EventName'])).replace(" ", "")+ " "+self.DicCalendarFlag[self.weekend]+'\n'+self.DicDrivers[driver1]+' vs '+self.DicDrivers[driver2]
            ax1.plot(x1[sector], y1[0][sector], color='#FFD300', label=driver1,ls='-')
            ax1.plot(x2[sector], y2[0][sector], color='#1D19AC', label=driver2,ls='-')
            ax2.plot(x1[sector], y1[1][sector], color='#FFD300', label=driver1,ls='-')
            ax2.plot(x2[sector], y2[1][sector], color='#1D19AC', label=driver2,ls='-')
            ax3.plot(x1[sector], y1[2][sector], color='#FFD300', label=driver1,ls='-')
            ax3.plot(x2[sector], y2[2][sector], color='#1D19AC', label=driver2,ls='-')
            ax3.set_title("Sector " + str(int(sector) +1)+ " Telemetria Vuelta Rapida \n" +str((self.session.event['EventName'])).replace(" ", "")+ " \n" + driver1 + ": " + str(dicDriver1['Sectors'][sector]) + "\n" + driver2 + ": "+ str(dicDriver2['Sectors'][sector]) ,color = "white",weight='bold')
            print(sector)
        ax3.text(0.85, 0.9, '@ChecoData', transform=ax3.transAxes,
            fontsize=15, color='gray', alpha=0.3,
            ha='center', va='center', rotation=20)
        ax3.set_ylabel('Velocidad KM\H',color = "white",weight='bold')
        ax2.set_xlabel('Distancia en metros',color = "white",weight='bold')
        ax1.set_ylabel('Acelerador/Throttle',color = "white",weight='bold')
        ax2.set_ylabel('Freno/Brake',color = "white",weight='bold')
        fig.tight_layout()
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')
        ax3.tick_params(axis='x', colors='white')
        ax3.tick_params(axis='y', colors='white')
        ax3.legend(loc ="upper right",fancybox=True)
        #ax2.legend(loc ="upper right",fancybox=True)
        #ax1.grid(color = 'grey', linestyle = '--', linewidth = 0.4)
        #ax2.grid(color = 'grey', linestyle = '--', linewidth = 0.4)
        ax1.set_facecolor("#000000")
        ax2.set_facecolor("#000000")
        ax3.set_facecolor("#000000")
        for axis in ['top', 'bottom', 'left', 'right']:
                ax1.spines[axis].set_linewidth(.5)  # change width
                ax1.spines[axis].set_color('#FFFFFF')    # change color
                ax2.spines[axis].set_linewidth(.5)  # change width
                ax2.spines[axis].set_color('#FFFFFF')    # change color
                ax3.spines[axis].set_linewidth(.5)  # change width
                ax3.spines[axis].set_color('#FFFFFF')    # change color
        #name of the file
        foto = self.sesion + str(self.DicCalendar[self.weekend]) + "telemetry.png"
        #save image in bucket s3 
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        print(img_data)
        img_data.seek(0)
        bucket.put_object(Body=img_data, ContentType='image/png', Key="img/"+foto)
        return text, foto

    def graph_qualy_simulation(self):
        cont = 0
        i = 1
        dicNew = self.get_fastlap('PER','VER','LEC','SAI','HAM','RUS','ALO','STR','PIA','NOR')      
        fastest = 0
        dicFinal = {}
        lsname = []

        #order fastest to slowest
        for f in range(1,len(dicNew)+1):
            fast = 201
            for e in dicNew:
                if float(dicNew[e]['Lap']) < fast:
                    fast = float(dicNew[e]['Lap']) 
                    fastest = e
                    #print(e)
            dicFinal[f]=dicNew[fastest].copy()
            dicNew.pop(fastest)
       
        #put it all in a final string

        cont,i = 0, 0
        textIntro = '𝐒𝐢𝐦𝐮𝐥𝐚𝐜𝐢𝐨𝐧 𝐝𝐞 𝐜𝐚𝐥𝐢𝐟𝐢𝐜𝐚𝐜𝐢𝐨𝐧\n'+ self.DicSesion[self.sesion]+" "+str((self.session.event['EventName'])).replace(" ", "")+ " "+self.DicCalendarFlag[self.weekend]+'\n𝑹𝒆𝒅𝑩𝒖𝒍𝒍🇦🇹 - 𝑭𝒆𝒓𝒓𝒂𝒓𝒊🇮🇹 - 𝑴𝒆𝒓𝒄𝒆𝒅𝒆𝒔🇩🇪 - 𝑨𝒔𝒕𝒐𝒏 𝑴𝒂𝒓𝒕𝒊𝒏🇬🇧 - Mclaren🇬🇧\n'

        plotDic = {}
        colors = []
        
        for g in dicFinal:
            if(str(dicFinal[g]['Driver']) == 'PER' or str(dicFinal[g]['Driver']) == 'VER' ):
                colors.append("#001A57")
            elif(str(dicFinal[g]['Driver']) == 'LEC' or str(dicFinal[g]['Driver']) == 'SAI' ):
                colors.append("#CC0000")
            elif(str(dicFinal[g]['Driver']) == 'ALO' or str(dicFinal[g]['Driver']) == 'STR' ):
                colors.append("#00594F")
            elif(str(dicFinal[g]['Driver']) == 'NOR' or str(dicFinal[g]['Driver']) == 'PIA' ):
                colors.append("#FF8000")
            else:
                colors.append("#48C9B0")
            plotDic[str(g)+"- "+str(dicFinal[g]['Driver'])] = float(dicFinal[g]['Lap']) - float(dicFinal[1]['Lap'])

        #pathimage = "C:/Users/admin/Desktop/png/rb.png"
        #logo = image.imread(pathimage)
        #imagebox = OffsetImage(logo, zoom = .2)
        #Annotation box for solar pv logo
        #Container for the imagebox referring to a specific position *xy*.
        #ab = AnnotationBbox(imagebox, (len(plotDic)+1,0), frameon = False)
        #ax.add_artist(ab)
        def get_flag(name):
            path = "C:/Users/admin/Documents/png/{}.png".format(name.title())
            im = plt.imread(path)
            return im

        def offset_image(coord, name, ax):
            img = get_flag(name)
            im = OffsetImage(img, zoom=.05)
            im.image.axes = ax
            ab = AnnotationBbox(im, (0, coord),  xybox=(-15, -21), frameon=False,
                                xycoords='data',  boxcoords="offset points", pad=0)
            ax.add_artist(ab)
        
        if len(plotDic) > 0:
            countries = list(plotDic.keys())
            valuesA = list(plotDic.values())
            xx = ['0','1','2','3']
        
            fig, ax = plt.subplots(figsize=(len(plotDic)+2,len(plotDic)+1),facecolor='#1f1f23')
            hbars =  ax.barh(range(len(countries)), valuesA, height=.5,color = colors,align='edge',edgecolor='#85929E')
            ax.set_yticks(range(len(countries)),color = "white")
            ax.set_xticks(range(4),color = "white")
            ax.set_xticklabels(xx,color = "white",weight='bold')
            ax.set_yticklabels(countries,color = "white",weight='bold')
            ax.tick_params(axis='x', which='major', pad=6,color = "white")
            ax.tick_params(axis='y', which='major', pad=6,color = "white")
            ax.invert_yaxis()
            for axis in ['top', 'bottom', 'left', 'right']:
                ax.spines[axis].set_linewidth(2)  # change width
                ax.spines[axis].set_color('#566573')    # change color
            ax.set_xlabel('Gap (seg)',color = "white",weight='bold')
            ax.set_title('Simulacion de calificacion \ Qualy simulation \n' +self.sesion + " " +str((self.session.event['EventName'])).replace(" ", "")+'\n Gap to fastest '+ str(get_lapFromSec(dicFinal[1]['Lap'])),color = "white",weight='bold')
            ax.set_facecolor("#0e0e10")
            fig.tight_layout()
            ax.text(0.85, 0.85, '@ChecoData', transform=ax.transAxes,
            fontsize=15, color='gray', alpha=0.1,
            ha='center', va='center', rotation=20)
            ax.set_xlim(right=valuesA[-1]+.5)
            for i, v in enumerate(valuesA):
                ax.text(v, i+.3, str(str(" +{:.2f}".format(v))), color='white', fontweight='bold')
            for i, c in enumerate(countries):
                offset_image(i, get_typeOfTyre(dicFinal[i+1]['Tyre']), ax)
            foto = self.sesion + str(self.DicCalendar[self.weekend]) + "qualysim.png"
            #save image in bucket s3 
            img_data = io.BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            bucket.put_object(Body=img_data, ContentType='image/png', Key="img/"+foto)
            #plt.savefig("C:/Users/admin/Desktop/Programas/Python/Algoritmo/"+ foto +".jpg")
        else:
            textIntro = "No"
            foto = "No"
        return textIntro, foto

    def get_session_vel_max(self):
        vel = []
        teamVel = []
        lenlist =len(self.listDrivers)
        for i in self.listDrivers:
            driverDataLaps = self.driverDataLapsLoad.pick_driver(i)
            driverDataFastestLap = driverDataLaps.pick_fastest()
            if ((str(driverDataFastestLap['Time']) != 'nan')):
                try:
                    driverTelFastestLap  = driverDataFastestLap.get_car_data()
                    velmax = 0
                    for x in driverTelFastestLap['Speed']:
                        
                        if(int(x) > velmax):
                            velmax = int(x) 
                    vel.append((velmax,i))
                    print(i)
                    print(velmax)
                except:
                    print('error')
        final = []
        for i in range(1,len(vel)):
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

        for i in final:
            for j in self.DicTeams:
                if i[1] == self.DicTeams[j][0] or i[1] == self.DicTeams[j][1]:
                    
                    if i[0] > self.DicTeamsVel[j]:
                        print([j])
                        self.DicTeamsVel[j]= i[0]
                        
                    break
        print(self.DicTeamsVel)
        for i in range(1,11):
            mayor = 200
            cont = -1
            for j in self.DicTeamsVel:
                if mayor < int(self.DicTeamsVel[j]):
                    mayor = int(self.DicTeamsVel[j])
                    tupl = (j,self.DicTeamsVel[j])
                    index = j
            teamVel.append(tupl)
            self.DicTeamsVel.pop(index)

        cont  = 0  
        text = 'Results\n'  
        for i in final:
            cont+=1    
            text += str(cont) + '- ' + str(i[1]) + ' ' +(str(i[0])) + ' km/h\n' 
        return teamVel,final

    def laps_in_session(self,driver):
            
            cont = 1
            vueltas = 0
            for i in self.driverDataLapsLoad.pick_driver(driver):
                cont +=1  
            dic = self.dic_avg_stints(driver)
            for i in dic:
                if dic[i]['Tipo'] == 'Sim. Qualy' or dic[i]['Tipo'] == 'Vueltas Rapidas' or dic[i]['Tipo'] == 'Sim. Carrera':
                    vueltas += int(dic[i]['LapNumber'])
            text = 'Total de vueltas dadas en '+ str(self.DicSesion[self.sesion]) + ' por ' + self.DicDrivers[self.name] +'\n\n' + str(cont) + "\n\nVueltas efectivas: \n\n" + str(vueltas)

            return text

    def get_fastlap(self,*driver):
        #*driver--- name of the driver or drivers

        dicNew = {}
        for i,d in enumerate(driver,1):
            if d in self.listDrivers:
                fastlap = self.session.load_laps(with_telemetry=True).pick_driver(d).pick_fastest()
                
                #abs', 'add', 'add_differential_distance', 'add_distance', 'add_driver_ahead', 'add_prefix', 'add_relative_distance', 'add_suffix', 'agg', 'aggregate', 'align', 'all', 'any', 'append', 'apply', 'applymap', 'asfreq', 'asof', 'assign', 'astype', 'at', 'at_time', 'attrs', 'axes', 'backfill', 'base_class_view', 'between_time', 'bfill', 'bool', 'boxplot',
                 #'calculate_differential_distance', 'calculate_driver_ahead', 'clip', 'columns', 'combine', 'combine_first', 'compare', 'convert_dtypes', 'copy', 'corr', 'corrwith', 'count', 'cov', 'cummax', 'cummin', 'cumprod', 'cumsum', 'describe', 'diff', 'div', 'divide', 'dot', 'driver', 'drop', 'drop_duplicates', 'droplevel', 'dropna', 'dtypes', 'duplicated', 'empty', 
                 #'eq', 'equals', 'eval', 'ewm', 'expanding', 'explode', 'ffill', 'fill_missing', 'fillna', 'filter', 'first', 'first_valid_index', 'flags', 'floordiv', 'from_dict', 'from_records', 'ge', 'get', 'get_first_non_zero_time_index', 'groupby', 'gt', 'head', 'hist', 'iat', 'idxmax', 'idxmin', 'iloc', 'index', 'infer_objects', 'info', 'insert', 'integrate_distance', 'interpolate', 'isin', 'isna', 'isnull', 'items', 'iteritems', 'iterrows', 'itertuples', 'join', 'keys', 'kurt', 'kurtosis', 'last', 'last_valid_index', 'le', 'loc', 'lookup', 'lt', 'mad', 'mask', 'max', 'mean', 'median', 'melt', 'memory_usage', 'merge', 'merge_channels', 'min', 'mod', 'mode', 'mul', 'multiply', 'nGear', 'ndim', 'ne', 'nlargest', 'notna', 'notnull', 'nsmallest', 'nunique', 'pad', 'pct_change', 'pipe', 'pivot', 'pivot_table', 'plot', 'pop', 'pow', 'prod', 'product', 'quantile', 'query', 'radd', 'rank', 'rdiv', 'register_new_channel', 'reindex', 'reindex_like', 'rename', 'rename_axis', 'reorder_levels', 'replace', 'resample', 'resample_channels', 'reset_index', 'rfloordiv''''
                dic = {}
                ls = []
                #selecciona la vuelta
                #convertir vuelta a string
                driverLapLaptime = get_lapFromObject(str(fastlap.LapTime))
                ls.append(get_sectorFromObject(str(fastlap['Sector1Time']),2))
                ls.append(get_sectorFromObject(str(fastlap['Sector2Time']),2))
                ls.append(get_sectorFromObject(str(fastlap['Sector3Time']),2))
                #Checa si existe el laptime de la vuelta
                if driverLapLaptime != ':LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'e:LpTime,tpe:timeelt64[n]' and driverLapLaptime != 'elt64[n]':
                    listComp = [],[]
                    listComp = str(fastlap['Compound'])[0:].split()
                    dic = {'Driver':d,'Lap':get_secFromLap(driverLapLaptime),'Tyre':get_typeOfTyre(listComp[0]),'Sectors':ls}
                    dicNew[i] = dic
        return dicNew

    def comparation_fast_lap_of_two(self,d1,d2):
        #d1--- name of the driver 1
        #d2--- name of the driver 2

        dic = {}
        dicDriver1 = self.get_fastlap(d1)
        dicDriver2 = self.get_fastlap(d2)
        dicDriver1 = dicDriver1[1]
        dicDriver2 = dicDriver2[1]
        secdriver1 = float((dicDriver1['Lap']))
        secdriver2 = float((dicDriver2['Lap']))

        tyreDriver1 = get_typeOfTyre(dicDriver1['Tyre'])
        tyreDriver2 = get_typeOfTyre(dicDriver2['Tyre'])
        
        d1ls = [d1,d1,self.DicDrivers[d1]]
        d2ls = [d2,d2,self.DicDrivers[d2]]
        if (secdriver1 < secdriver2): 
            tDiff = "{:.3f}".format(secdriver2 - secdriver1)
            dic['Fastest'] = d1ls
            dic['Slowest'] = d2ls
            dic['Diferencia'] = tDiff
            dic['LaptimeF'] = dicDriver1['Lap']
            dic['LaptimeS'] = dicDriver2['Lap']
            dic['Fsectors'] = dicDriver1['Sectors']
            dic['Ssectors'] = dicDriver2['Sectors']
            dic['TyreF'] = tyreDriver1
            dic['TyreS'] = tyreDriver2
        else:
            tDiff = "{:.3f}".format(secdriver1 - secdriver2)
            dic['Fastest'] = d2ls
            dic['Slowest'] = d1ls
            dic['Diferencia'] = tDiff
            dic['LaptimeF'] = dicDriver2['Lap']
            dic['LaptimeS'] = dicDriver1['Lap']
            dic['Fsectors'] = dicDriver2['Sectors']
            dic['Ssectors'] = dicDriver1['Sectors']
            dic['TyreF'] = tyreDriver2
            dic['TyreS'] = tyreDriver1
        
        diffS1 = float("{:.3f}".format(float(dic['Ssectors'][0]) - float(dic['Fsectors'][0])))
        if diffS1 >= 0: diffS1 = "+"+str(diffS1)
        diffS2 = float("{:.3f}".format(float(dic['Ssectors'][1]) - float(dic['Fsectors'][1])))
        if diffS2 >= 0: diffS2 = "+"+str(diffS2)
        diffS3 = float("{:.3f}".format(float(dic['Ssectors'][2]) - float(dic['Fsectors'][2])))
        if diffS3 >= 0: diffS3 = "+"+str(diffS3)
        
        text = self.DicSesion[self.sesion]+" "+str((self.session.event['EventName'])).replace(" ", "")+ " "+self.DicCalendarFlag[self.weekend]+"\nMas rapido  " + dic['Fastest'][2] + " a una vuelta que  "+ dic['Slowest'][2] +"\n\n"+ dic['Fastest'][2] + ": " + get_lapFromSec(dic['LaptimeF']) +" "+dic['TyreF']+ "\n S1: " +dic['Fsectors'][0]+"   S2: "+dic['Fsectors'][1]+"   S3: "+dic['Fsectors'][2]+"\n\n"+ dic['Slowest'][2] + ": " + get_lapFromSec(dic['LaptimeS'])+ " "+dic['TyreS']+"\n S1: " +dic['Ssectors'][0]+"   S2: "+dic['Ssectors'][1]+"    S3: "+dic['Ssectors'][2]+ "\n\nGap +" +dic['Diferencia'] +" ( S1: "+str(diffS1)+", S2: "+str(diffS2)+", S3: "+str(diffS3)+")\n"
        return text

    def get_session_fastest(self):
        laps = []
        cont = 0
        for i in self.listDrivers:
            print(i)
            self.dl = self.driverDataLapsLoad.pick_driver(i)
            driverFastest = self.dl.pick_fastest()
            #if ((str(driverFastest['Time']) != 'nan')):
            listComp = str(driverFastest['Compound'])[0:].split()
            try:
                laps.append((get_secFromLap(get_lapFromObject(str(driverFastest['LapTime']))),i,get_typeOfTyre(listComp[0])))  
            except:
                print('non')
        final = []
        lenlist =len(laps)

        for i in range(1,lenlist):
            mayor = 200
            cont = -1
            for a in range(0,(len(laps))):
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

    def get_RacePace(self,driver):
        dic = self.dic_stints(driver)
        data=self.session.load_laps(with_telemetry=True).pick_driver(driver)
        datafastest=data.pick_fastest()
        fastestLap = float(get_secFromLap(get_lapFromObject(str(datafastest['LapTime']))))

        cont,lap = 0,0
        for item in dic:
            for i in dic[item]:
                if fastestLap + 6 > float(get_secFromLap(str(i[0]))):
                    cont += 1
                    lap += float(get_secFromLap(str(i[0])))
        avg = get_lapFromSec((lap/cont))
        
        text = '🏁 Race Pace \n\n' +  self.DicDrivers[driver] + ' ' +avg
        
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
        dic = self.get_avgStint(self.name)
        for i in dic:
            if dic[i]['Tipo'] == 'Sim. Qualy' or dic[i]['Tipo'] == 'Vueltas Rapidas' or dic[i]['Tipo'] == 'Sim. Carrera':
                vueltas += int(dic[i]['LapNumber'])
        text = 'Total de vueltas dadas en '+ str(self.DicSesion[self.sesion]) + ' por ' + self.DicDrivers[self.name] +'\n\n' + str(cont) + "\n\nVueltas efectivas: \n\n" + str(vueltas)

        return text
    
    def get_lapsInStintRace(self,driver):  
    #print(driverSesionLaps)
        dic = {1:[]}
        driverDataLaps = self.session.load_laps(with_telemetry=True).pick_driver(driver)
        for a in driverDataLaps.LapNumber:
            ls =[]
            pit = []
            #selecciona la vuelta
            currentDriverLap =  driverDataLaps[driverDataLaps.LapNumber==a]
            currentDriverLapTime  = get_lapFromObject(str(currentDriverLap.LapTime))
            pit = str(currentDriverLap.PitOutTime).split()
            
            #Obtener stint de la vuelta
            listStint = []
            listStint = re.sub(r'.', '', str(currentDriverLap['Stint']), count = 2)[3:].split()
            stint = float(listStint[0])
            lStatus = str(currentDriverLap.TrackStatus).split()
            
            
            #Checa si existe el laptime de la vuelta
            if currentDriverLapTime != ':LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'e:LpTime,tpe:timeelt64[n]' and currentDriverLapTime != 'elt64[n]' and pit[1] == 'NaT' and lStatus[1].find("3") ==-1 and lStatus[1].find("4") ==-1 and lStatus[1].find("5") ==-1 and lStatus[1].find("6") ==-1 and lStatus[1].find("7") ==-1:
                
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector1Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector2Time']),3))
                ls.append(get_sectorFromObject(str(currentDriverLap['Sector3Time']),3))
                listDic, listComp = [],[]
                listComp = str(currentDriverLap['Compound'])[4:].split()
                listDic.append(currentDriverLapTime)
                listDic.append(listComp[0])
                listDic.append(a)
                listDic.append(ls)
                if stint in dic:
                    dic[stint].append(listDic)
                else:
                    dic[stint] = []
                    dic[stint].append(listDic)

        return dic

    def get_RacePace(self):
        dic = self.get_lapsInStintRace(self.name)
        data=self.session.load_laps(with_telemetry=True)
        datafastest=data.pick_fastest()
        cont,lap = 0
        text = []
        for item in dic:
            for i in dic[item]:
                cont += 1
                lap += float(get_secFromLap(str(i[0])))
        avg = get_lapFromSec((lap/cont))
        
        text1 = '🏁 Race Pace \n\n' +  self.DicDrivers[self.name] + ' ' +avg
        text.append(text1)
        return text

    def get_manyRacePace(self):
        dicPER = self.get_lapsInStintRace('PER')
        dicVER = self.get_lapsInStintRace('VER')
        dicLEC = self.get_lapsInStintRace('LEC')
        dicSAI = self.get_lapsInStintRace('SAI')
        lap,cont = 0,0
        text,dic = [],{}
        text1 = '🏁 Race Pace \n\n'

        for item in dicPER:
            for i in dicPER[item]:
                cont += 1
                lap += float(get_secFromLap(str(i[0])))
        avg = (lap/cont)
        dic['PER'] = [avg,'PER']
        lap,cont = 0,0
        
        for item in dicVER:
            for i in dicVER[item]:
                cont += 1
                lap += float(get_secFromLap(str(i[0])))
        avg = (lap/cont)
        dic['VER'] = [avg,'VER']
        lap,cont = 0,0

        for item in dicLEC:
            for i in dicLEC[item]:
                cont += 1
                lap += float(get_secFromLap(str(i[0])))
        avg = (lap/cont)
        dic['LEC'] = [avg,'LEC']
        lap,cont = 0,0
        
        for item in dicSAI:
            for i in dicSAI[item]:
                cont += 1
                lap += float(get_secFromLap(str(i[0])))
        if cont != 0:
            avg = (lap/cont)
            dic['SAI'] = [avg,'SAI']
        
        
        print(dic)

        dicFinal = {}
        for f in range(1,(len(dic)+1)):
            fast = 201
            for e in dic:
                if float(dic[e][0]) < fast:
                    fast = float(dic[e][0])
                    fastest = e
                    #print(e)
            dicFinal[f]=dic[fastest].copy()
            dic.pop(fastest)

        for i in dicFinal:
            text1 +=  self.DicDrivers[dicFinal[i][1]] + '  '  + get_lapFromSec(dicFinal[i][0]) +  '\n'

        text.append(text1)
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

#sesion = Sesion(2023, 11, 'FP2')

#print(sesion.graph_racepace_simulation())
#get_lapFromObject(":01:34.632")
#per = Driver('PER', 2022, 18, 'R')
#print(sesion.get_CompFastLap2('VER','LEC'))
#print(sesion.get_telemetryGraph('VER','PER',1))
#print(sesion.dic_stints1('ALO'))





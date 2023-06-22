import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:/Users/admin/Desktop/Programas/Python/TwitterApi/')
import time
import config
import tweepy
import ClassF1
import boto3
import io
from PIL import Image
import os
from pymongo import MongoClient
import datetime
from traceback import print_exc

now = datetime.datetime.now()
print(now.year, now.month, now.day, now.hour, now.minute, now.second)
# 2015 5 6 8 53 40

CONNECTION_STRING = config.CONNECTION_STRING
client = MongoClient(CONNECTION_STRING)
dbname = client['checobot']
collection_actualdata = dbname["actualdata"]
collection_fechas = dbname["fechas"]

s3 = boto3.resource('s3')
bucket = s3.Bucket("checobot")
name_sesion_normal = ['','FP1','FP2','FP3','Q','R']
name_sesion_sprint = ['','FP1','Q','FP2','S','R']
sprint = [4,10,13,18,19,21]
practicas = ['FP1','FP2','FP3']
carreras = ['R','S']
qualy = ['Q']

def image_from_s3(key):
    image = bucket.Object(key)
    img_data = image.get().get('Body').read()
    return Image.open(io.BytesIO(img_data))

def tweet(result):
    
    if(len(result) == 2):
        if(result[0]!= "No"):
            photo_name = result[1]
            img = image_from_s3("img/"+ photo_name)
            img.save(photo_name,format="PNG")
            media = api.media_upload(filename= photo_name)
            response = client.create_tweet(text=result[0],media_ids=[media.media_id])
            idAnterior = response.data['id']
            client.like(idAnterior)
            os.remove(photo_name)
            print(response)
        else:
            print("No se puede")
    else:
        if(result != "No"):
            response = client.create_tweet(text=result)
            idAnterior = response.data['id']
            client.like(idAnterior)
            print(response)
        else:
            print("No se puede")

client = tweepy.Client(consumer_key=config.API_KEY,
                    consumer_secret=config.API_KEY_SECRET,
                    access_token=config.ACCES_TOKEN,
                    access_token_secret=config.ACCES_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(consumer_key=config.API_KEY,
                    consumer_secret=config.API_KEY_SECRET,
                    access_token=config.ACCES_TOKEN,
                    access_token_secret=config.ACCES_TOKEN_SECRET)
api = tweepy.API(auth)


while True:
    now = datetime.datetime.now()
    
    db_next_sesion = collection_actualdata.find_one({"id": "1"})
    namesesion =str(db_next_sesion['sesion'])
    weekend=int(db_next_sesion['fin_de_semana']) 
    numero_sesion =int(db_next_sesion['numero_sesion']) 
    dict = collection_fechas.find_one({"id": str(weekend)})

    if(int(now.month) >= int(dict[namesesion]['mes'])):
        print('mes')
        if(int(now.day) >=int(dict[namesesion]['dia'])):
            print('dia')
            if(int(now.hour) >= int(dict[namesesion]['hora'])):
                print('hora')
                if(int(now.minute) >= int(dict[namesesion]['minuto'])):

                    print('hora')
                    print('minuto')
                    
                    sesion = ClassF1.Sesion(2022,weekend, namesesion)
                    #per = ClassF1.Driver('PER', 2022, 18, 'FP3')

                    if namesesion in practicas:
                        try:
                            results = sesion.graph_racepace_simulation()
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()  
                        #time.sleep(30)
                        try:
                            results = sesion.comparation_fast_lap_of_two('PER','VER')
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()  
                        #time.sleep(30)
                        
                        try:
                            results = sesion.graph_vel_max_teams()
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                        #time.sleep(30)
                        try:
                            results = sesion.graph_qualy_simulation()
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                        #time.sleep(30)
                        
                        try:    
                            results = sesion.graph_telemetry_fastlap_of_two('PER','VER',4)
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                    elif namesesion in qualy:
                        try:
                            results = sesion.comparation_fast_lap_of_two('PER','VER')
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()  
                        #time.sleep(30)
                        
                        try:
                            results = sesion.graph_vel_max_teams()
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                        #time.sleep(30)
                        try:    
                            results = sesion.graph_telemetry_fastlap_of_two('PER','VER',4)
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                    elif namesesion in carreras:
                        try:
                            results = sesion.comparation_fast_lap_of_two('PER','VER')
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()  
                        #time.sleep(30)
                        
                        try:
                            results = sesion.graph_vel_max_teams()
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                        #time.sleep(30)
                        try:    
                            results = sesion.graph_telemetry_fastlap_of_two('PER','VER',4)
                            tweet(results)
                        except Exception as e:
                            print ('type is:', e.__class__.__name__)
                            print_exc()
                        
                    if  numero_sesion == 5:
                        collection_actualdata.update_one({"id": "1" },{ "$set":
                                {
                                    "numero_sesion": 1,
                                    "sesion":"FP1",
                                    "fin_de_semana": weekend + 1
                                }
                            })
                    else:
                        if weekend in sprint:

                            collection_actualdata.update_one({"id": "1" },{ "$set":
                                    {
                                        "numero_sesion": numero_sesion + 1,
                                        "sesion":name_sesion_sprint[numero_sesion + 1]
                                    }
                                })
                        else:
                            collection_actualdata.update_one({"id": "1" },{ "$set":
                                    {
                                        "numero_sesion": numero_sesion + 1,
                                        "sesion":name_sesion_normal[numero_sesion + 1]
                                    }
                                })
    break
                    
    '''
                    if(len(result) == 1):
                        path = result[1]
                        if(result != "No"):
                            response = client.create_tweet(text=result)
                            idAnterior = response.data['id']
                            client.like(idAnterior)
                            print(response)
                        else:
                            print("No se puede")

                    elif(len(result) == 2):
                        photo_name = result[1]
                        img = image_from_s3("img/"+ photo_name)
                        img.save(photo_name,format="PNG")

                        if(result[0]!= "No"):
                            media = api.media_upload(filename= photo_name)
                            response = client.create_tweet(text=result[0],media_ids=[media.media_id])
                            idAnterior = response.data['id']
                            client.like(idAnterior)
                            os.remove(photo_name)
                            print(response)
                        else:
                            print("No se puede")'''
#respond twit
#response = client.create_tweet(text=i, in_reply_to_tweet_id=idAnterior) 
'''
cont = 0
for i in text1: 
#Reply tweet
    if cont == 0: 
        #response = client.create_tweet(text=i,media_ids=[media.media_id])
        response = client.create_tweet(text=i)
        idAnterior = response.data['id']
        
        a = client.like(idAnterior)
        cont+=1
        print(response)
    else:
        if i != '':
            
            idAnterior = response.data['id']
            a = client.like(idAnterior)
            print(response)
           ''' 

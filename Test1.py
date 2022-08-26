from re import I
import tweepy
import config
import f1



client = tweepy.Client(consumer_key=config.API_KEY,
                    consumer_secret=config.API_KEY_SECRET,
                    access_token=config.ACCES_TOKEN,
                    access_token_secret=config.ACCES_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(consumer_key=config.API_KEY,
                    consumer_secret=config.API_KEY_SECRET,
                    access_token=config.ACCES_TOKEN,
                    access_token_secret=config.ACCES_TOKEN_SECRET)
api = tweepy.API(auth)
    # Upload image
media = api.media_upload(filename="C:/Users/admin/Desktop/Programas/Python/TwitterApi/fotos/Prueba.jpg")
text1 = f1.tweetFastLapPV()
print(text1)
cont = 0
for i in text1: 
#Reply tweet
    if cont == 0: 
        response = client.create_tweet(text=i,media_ids=[media.media_id])
        idAnterior = response.data['id']
        
        a = client.like(idAnterior)
        cont+=1
        print(response)
    else:
        if i != '':
            response = client.create_tweet(text=i, in_reply_to_tweet_id=idAnterior)
            idAnterior = response.data['id']
            a = client.like(idAnterior)
            print(response)







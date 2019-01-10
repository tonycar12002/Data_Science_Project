# -*- coding: utf-8 -*-


import csv
import time
from google.cloud import translate
translate_client = translate.Client()

writer = csv.writer(trans_file)


now = 0 




target = 'en'
source='zh-tw'
trans_file = open('all_videos_trans.csv', 'a')
with open("all_videos.csv", newline="") as file:
    csvCursor = list(csv.reader(file))
  
    if now == 0:
        writer.writerow(csvCursor[0])
        now += 1
        
    for i in range(now+1, now+2001): #len(csvCursor)
        now = i
        row = csvCursor[i]
        
        #print(now, end='  ')
        if i% 30 == 0:
            print(i)
            
        text = row[11]
        translation = translate_client.translate(
                text,
                source_language=source,
                target_language=target)
        row[11] = translation['translatedText']
        #print(row[11])
        
        writer.writerow(row)
        time.sleep(0.1)
        
trans_file.close()



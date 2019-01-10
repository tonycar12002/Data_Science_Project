# -*- coding: utf-8 -*-


import csv
import time
from hanziconv import HanziConv
'''
trans_file = open('all_videos_trans.csv', 'a')
writer = csv.writer(trans_file)
now = 0 

translator = Translator()
with open("all_videos.csv", newline="") as file:
    csvCursor = list(csv.reader(file))
  
    if now == 0:
        writer.writerow(csvCursor[0])
    for i in range(now+1, len(csvCursor)): #len(csvCursor)
        now = i
        row = csvCursor[i]
        
        if i % 10 == 0:
            translator = Translator()
        
        print(now, end='  ')
        if i != 0:
            row[11] = HanziConv.toTraditional(row[11])
            row[11] = translator.translate(row[11], src='zh-CN', dest='en').text
            print(row[11])
        writer.writerow(row)
        time.sleep(0.1)
        
trans_file.close()
'''

def run_quickstart():
    # [START translate_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import translate

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate
    text = u'MAYDAY五月天 [ 私奔到月球 ] feat.陳綺貞 Official Live Video'
    # The target language
    target = 'en'

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))
    # [END translate_quickstart]


if __name__ == '__main__':
    run_quickstart()
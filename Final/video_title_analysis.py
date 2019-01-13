# -*- coding: utf-8 -*-
#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import csv
import re
import jieba
import codecs
import string
from hanziconv import HanziConv
import tkinter as tk
import operator
from collections import defaultdict
from collections import OrderedDict
from PIL import ImageTk, Image
#%%
print("Initailize") 
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif']=['simhei']

data = pd.read_csv("all_videos.csv")
df1 = data['Title']
df2 = data['Category']
df3 = data['Views']
df4 = data['Video_exist_day'] + 13
df = pd.concat([df1, df2, df3, df4], axis=1, join_axes=[df1.index])

# Sentence segmentation
jieba.load_userdict('/home/tony/Data_Science_Project/Final/user_dict.txt')
index = df.index.values
for i in range(0, df.shape[0]):
    if (i%10000) == 0:
        print(i)
        
    sen = HanziConv.toSimplified(df.iloc[i]['Title'])
    
    sen = re.sub(r'[^\w\s]',' ',sen)
    sen = sen.lower()
    for num in range(0, 10):
        sen = sen.replace(str(num), "")
        
    title_seg = ""
    
    seg_list = jieba.cut(sen, cut_all=False)
    for seg in seg_list:
        seg = seg.replace(" ", "")
        seg = seg.replace("\n", "")
        if len(seg) != 0:
            title_seg = title_seg + seg + " "
                
    df.at[index[i], 'Title'] =  title_seg

print("Initial Done") 

# Category mapping
category_mapping={
'Entertainment':0,
'Music':1,
'Comedy':2,
'Nonprofits_and_Activism':3,
'Film_and_Animation':4,
'People_and_Blogs':5,
'Education':6,
'News_and_Politics':7,
'Travel_and_Events':8,
'Science_and_Technology':9,
'Gaming':10,
'Autos_and_Vehicles':11,
'Howto_and_Style':12,
'Sports':13,
'Shows':14,
'Pets_and_Animals':15
}

#%%
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        global category_mapping, df
        self.pack()
        self.th = 1
        self.day_th = 90
        self.grid(column=0,row=0)
        self.create_widgets()

    def create_widgets(self):
        
        row = 0
        # Input Keyword
        self.label_keyword = tk.Label(self, text="Target Keyword",relief = tk.RAISED, width=18)
        self.label_keyword["font"] = ("", 13)
        self.label_keyword.grid(row=row,column=0, padx = 5)

        self.entry_keyword = tk.Entry(self, fg="black", width="20")
        self.entry_keyword["font"] = ("", 15)
        self.entry_keyword.grid(row=row,column=1, pady = 8)
        row += 1
        
        # Frequency Threshold
        self.label_th = tk.Label(self, text="Frequency Threshold",relief = tk.RAISED, width=18)
        self.label_th["font"] = ("", 13)
        self.label_th.grid(row=row,column=0, padx = 5)

        self.entry_th = tk.Entry(self, fg="black", width="20")
        self.entry_th["font"] = ("", 15)
        self.entry_th.insert(tk.END, 5)
        self.entry_th.grid(row=row,column=1, pady = 8)
        row += 1
        
        # Recent Days
        self.label_day = tk.Label(self, text="Days Threshold",relief = tk.RAISED, width=18)
        self.label_day["font"] = ("", 13)
        self.label_day.grid(row=row,column=0, padx = 5)

        self.entry_day = tk.Entry(self, fg="black", width="20")
        self.entry_day["font"] = ("", 15)
        self.entry_day.insert(tk.END, 90)
        self.entry_day.grid(row=row,column=1, pady = 8)
        row += 1       
    
        # ListBox
        self.label_category = tk.Label(self, text="Video Category",relief = tk.RAISED, width=18)
        self.label_category["font"] = ("", 13)
        self.label_category.grid(row=row,column=0, padx = 5)      
        
        self.listbox = tk.Listbox(self)
        for item in category_mapping:
            self.listbox.insert(tk.END, item)
        self.listbox.grid(row=row,column=1, padx = 5)    
        self.listbox.select_set(0)
        row += 1

        # Button 
        self.button_predict = tk.Button(self, width=18)
        self.button_predict["text"] = "Title Analysis"
        self.button_predict["font"] = ("", 13)
        self.button_predict["command"] = self.prediction
        self.button_predict.grid(row=row,column=1, pady = 5)
        row += 1

        self.button_quit = tk.Button(self, text="Quit", fg="red", width=18, 
                              command=self.master.destroy)
        self.button_quit["font"] = ("", 13)
        self.button_quit.grid(row=row,column=1)

    def prediction(self):
        keyword = self.entry_keyword.get()
        category = self.listbox.get(self.listbox.curselection())
        
        if self.entry_th.get().isdigit():
            self.th = int(self.entry_th.get())
        else:
            self.th = 5
            
        if self.entry_day.get().isdigit():
            self.day_th = int(self.entry_day.get())
        else:
            self.day_th = 90
        
        print("Keyword = ", keyword)
        print("Select = ", category)
        print("Frequency Threshold = ", str(self.th))
        print("DayThreshold = ", str(self.day_th))
        
        keyword = HanziConv.toSimplified(keyword)
    
        keyword = re.sub(r'[^\w\s]',' ',keyword)
        keyword = keyword.lower()
        for num in range(0, 10):
             keyword = keyword.replace(str(num), "")
        
        keyword_seg = []
        seg_list = jieba.cut(keyword, cut_all=False)
        for seg in seg_list:
            seg = seg.replace(" ", "")
            seg = seg.replace("\n", "")
            keyword_seg.append(seg)
        
        self.find_top_keyword(keyword_seg, category)
    
    def filter_category(self, category):
        tmp = df.loc[df['Category'] == category]
        tmp = tmp.loc[df['Video_exist_day'] <= self.day_th]
        df1 = tmp['Title']
        df2 = tmp['Views']
        tmp = pd.concat([df1, df2], axis=1, join_axes=[df1.index])      
        return tmp
    
    def find_top_keyword(self, keyword, category):
        df_cate = self.filter_category(category)
        
        words_dict = {"initial":[0, 0, 0]}
        print(df_cate.shape)
        for i in range(0, df_cate.shape[0]):
            
            title = df_cate.iloc[i]['Title']
            views = df_cate.iloc[i]['Views']
            word_list = title.split(" ")
            
            # Check title contain keyword
            if all(key in word_list for key in keyword):
                for word in word_list:
                    if word != " " and len(word) > 1 and word not in keyword:
                        if word in words_dict:
                            value = words_dict[word]
                            value[0] += 1
                            value[1] += views
                            value[2] = value[1]/value[0]
                            words_dict[word] = value
                        else:  
                            values = [1,  views, views]
                            words_dict[word] = values           
        print("Statistics Done")        
        
        self.analysis_dict(words_dict, keyword)
        return
    
    def analysis_dict(self, words_dict, keyword):
        d_sorted_by_value = OrderedDict(sorted(words_dict.items(), key=lambda x: x[1][2], reverse=True))
        
        num = 0
        #print(len(d_sorted_by_value))
            
        # Show data
        x = []
        y = []
        for element in d_sorted_by_value:
            if words_dict[element][0] >= self.th : # and re.search(u'[\u4e00-\u9fff]', element)
                print ("%s: %s" % (element, words_dict[element]))
                x.append(element)
                y.append(words_dict[element][2])
                num += 1
                
            if num >= 11:
                break
            
        print("Analysis Done")
        print("================================")
        
        self.show(x, y)
        
    def show(self, x, y):
        width = 1
        
        plt.figure(figsize=(30, 8),)
        plt.bar(x, y)
        plt.grid()
        plt.show()
        
                
root = tk.Tk()
root.title("Youtube video view count prediction")
root.geometry("500x500")
root.resizable(0, 0)
app = Application(master=root)
app.mainloop()





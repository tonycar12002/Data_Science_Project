#!/usr/bin/python3


import csv
import pandas as pd
import sys
import tkinter as tk


youtuber = pd.read_csv('youtuber.csv')


#print(youtuber.loc[youtuber['User_Name'] == "瑪莎與熊 Masha and The Bear CH"])


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		
		self.pack()
		self.grid(column=0,row=0)
		self.create_widgets()

	def create_widgets(self):

		self.label_title = tk.Label(self, text="Video Title",relief = tk.RAISED, width=18)
		self.label_title["font"] = ("", 13)
		self.label_title.grid(row=1,column=1, padx = 5)

		self.entry_title = tk.Entry(self, fg="black", width="80")
		self.entry_title["font"] = ("", 15)
		self.entry_title.grid(row=1,column=2, pady = 8)

		self.label_channel = tk.Label(self, text="Channel Name",relief = tk.RAISED, width=18)
		self.label_channel["font"] = ("", 13)
		self.label_channel.grid(row=2,column=1, padx = 5)

		self.entry_channel = tk.Entry(self, fg="black", width="80")
		self.entry_channel["font"] = ("", 15)
		self.entry_channel.grid(row=2,column=2, pady = 8)

		self.label_day = tk.Label(self, text="Pulbish Date \nex: 2018-01-03",relief = tk.RAISED, width=18)
		self.label_day["font"] = ("", 13)
		self.label_day.grid(row=3,column=1, padx = 5)

		self.entry_day = tk.Entry(self, fg="black", width="80")
		self.entry_day["font"] = ("", 15)
		self.entry_day.grid(row=3,column=2, pady = 8)


		self.button_predict = tk.Button(self, width=18)
		self.button_predict["text"] = "View Count Predict"
		self.button_predict["font"] = ("", 13)
		self.button_predict["command"] = self.prediction
		self.button_predict.grid(row=4,column=2, pady = 5)


		self.button_quit = tk.Button(self, text="Quit", fg="red", width=18, 
							  command=self.master.destroy)
		self.button_quit["font"] = ("", 13)
		self.button_quit.grid(row=5,column=2)

	def prediction(self):
		title = self.entry_title.get()
		channel = self.entry_channel.get()
		date = self.entry_day.get()


root = tk.Tk()
root.title("Youtube video view count prediction")
root.geometry("1200x300")
root.resizable(0, 0)
app = Application(master=root)
app.mainloop()


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from pytube import YouTube
from threading import Thread


default_path = "/home/aman/Downloads"

path = default_path

file_size = 0

def start_downloading():
	
	global file_size

	try:

		url = url_field.get()
		
		print(url)

		label1.config(text = "Your download started :) ")

		#ClearUrl_button.config(text = "please")
		ClearUrl_button['text']="please"
		
		ClearUrl_button.config(state = DISABLED)

		download_button.config(text = "Wait...")
		
		download_button.config(state = DISABLED)

		yt = YouTube(url)

		itag = select_Quality()

		print(itag)
		
		stream = yt.streams.get_by_itag(itag)

		print(stream.title)
		
		file_size = stream.filesize
		
		print(stream.filesize)

		print("download started")

		stream.download(path)

		print(path)

		download_button.config(text = "Download")
		
		download_button.config(state = NORMAL)

		ClearUrl_button.config(text = "clear")
		
		ClearUrl_button.config(state = NORMAL)

		label1.config(text = "paste YouTube Vedio link here")

		print("download completed ,,,,,,,")

	except Exception as e:
		
		print(e)

def start_downloading_thread():

	thread = Thread(target = start_downloading())
	
	thread.start()

def select_path():
	
	global path

	path = askdirectory()

	if(len(path)<=1):
		path = default_path
	
	Savelabel.config(text="selected path : "+path , font = ("verdana",10,"bold"))

def select_Quality(event = None):

	choice = choices.current()

	if(choice == 0):
		
		return '137'			### itag for 1080p vedio ###

	elif(choice == 1):

		return '22'				### itag for 720p vedio ###

	elif(choice == 2):

		return '18'				### itag for 360p vedio ###

	elif(choice == 3):

		return '140'			### itag for mp4 audio ###

def emptyUrl():

	url_field.delete(0,END)

root = Tk()

root.title("YouTube Video Downloader")

root.geometry("800x600")

root.resizable(width = False , height = False)

root.configure(background = "lightblue")

twitter_img = PhotoImage(file="/home/aman/Documents/my_projects/YouTube_Downloader/youtubedownloader.png")

label2 = Label(root,image = twitter_img)

label2.pack(pady = 10)

label1 = Label(root,text="paste YouTube Vedio link here",fg="red",bg="yellow",font=(" ",15,"bold"))

label1.pack(side = TOP, padx=20, pady = 10)

url_field = Entry(root,width=50,justify=CENTER,font = ("verdana","15"))

url_field.pack()

topframe = Frame(root)

topframe.pack(pady = 10)

download_button = Button(topframe,text="Download",bg = "black", fg = "white",font = (" ",10,"bold"), command = start_downloading_thread)

download_button.pack(side = LEFT)

ClearUrl_button = Button(topframe,width = 10,bg = "black", fg = "white",  text = "clear",font = (" ",10,"bold"), command = emptyUrl)

ClearUrl_button.pack(side=LEFT)

#linkerror = Label(root,fg="red",text="no error")
#linkerror.pack(pady = (0,10))

Savelabel = Label(root,text="select download location",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

Savelabel.pack(pady = 10)

Selectpath_button = Button(root,width = 20,bg = "green",fg = "white", text = "choose folder",font = ("verdana",10,"bold"),command = select_path)

Selectpath_button.pack()

#filelocationError = Label(root,text="")
#filelocationError.pack(pady = (0,0))

selectQuality = Label(root,text="select Quality of vedio to download",font = ("verdana",15,"bold"),fg="red",bg="yellow")

selectQuality.pack(pady = 10)

Quality = ["mp4 1080p vedio only","mp4 720p","mp4 360p","mp4 audio only"]

quality = StringVar()

choices = ttk.Combobox(root,textvariable = quality,values = Quality,width = 30)

choices.pack()

choices.current(1)

choices.bind("<<ComboboxSelected>>",select_Quality)

vedio_image = PhotoImage(file = "/home/aman/Documents/my_projects/YouTube_Downloader/vedio.png")

vedio_image = vedio_image.subsample(1,1)

play_vedio_button = Button(root,image = vedio_image)

play_vedio_button.pack(side = TOP,pady = 10)

root.mainloop()


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from pytube import YouTube , Playlist
from threading import Thread


default_path = "/home/aman/Downloads"

path = default_path

#file_size = 0

def single_download():

	try:

		url = url_field.get()

		yt = YouTube(url)

		itag = select_Quality()

		print(itag)
		
		stream = yt.streams.get_by_itag(itag)

		print(stream.title)
		
		file_size = stream.filesize
		
		print(stream.filesize)

		print("download started")

		stream.download(path)

		print("download completed ,,,,,,,")

		print(path)

	except Exception as e:

		print(e)


def multplie_download():


	try:

		playlist = url_field.get()

		playlist_url = Playlist(playlist)

		l = len(playlist_url)

		print(l)

		for i in range(l):

			yt = YouTube(playlist_url[i])

			itag = select_Quality()

			print(itag)
		
			stream = yt.streams.get_by_itag(itag)

			print(stream.title)
		
			file_size = stream.filesize
		
			print(stream.filesize)

			print("download started")

			stream.download(path)

			print("{} vedio downloaded \n ".format(i+1))

		print("entire playlist downoaded ")

	except Exception as e:

		print(e)


def start_downloading():

	try:

		label1.config(text = "Your download started :) ")

		#ClearUrl_button.config(text = "please")
		ClearUrl_button['text']="please"
		
		ClearUrl_button.config(state = DISABLED)

		download_button.config(text = "Wait...")
		
		download_button.config(state = DISABLED)

		ch = radioVar.get()

		print(ch)

		if(ch=="1"):

			print("single")

			single_download()

		else:

			print("multiple")

			multplie_download()
		
		download_button.config(text = "Download")
		
		download_button.config(state = NORMAL)

		ClearUrl_button.config(text = "clear")
		
		ClearUrl_button.config(state = NORMAL)

		label1.config(text = "paste YouTube Vedio link here")

	except Exception as e:
		
		print(e)

def start_downloading_thread():

	url = url_field.get()

	if(len(url)<2):

		label1.config(text = " Please Enter Valid Url ")

		print("url field is empty")

		return

	if("https://www.youtube.com/" not in url):

		label1.config(text = " Please Enter Valid Url ")

		print("invlaid url")

		return

	if(radioVar.get()=="1" and "playlist" in url):

		label1.config(text = "link not match with its type")

		print("you are trying to download playlist by selcting single vedio Radiobutton")

		return

	if(radioVar.get()=="2" and "watch" in url):

		label1.config(text = " link not match with its type ")

		print("you are trying to download single vedio by selcting playlist Radiobutton")

		return

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

frame = Frame(root,background="black")

frame.pack()

radioVar = StringVar(frame,"1")

#style = ttk.Style(frame)

#style.configure("TRadiobutton", bg = "light green",fg = "red", font = ("arial", 10, "bold"))

single = Radiobutton(frame,text="single vedio",variable = radioVar,value = "1",fg = "black",bg="white",font = ("",10,"bold"))

single.pack(side = LEFT)

multiple = Radiobutton(frame,text="playlist",variable = radioVar,value = "2",fg = "black",bg="white",font = ("",10,"bold"))

multiple.pack(side = LEFT)

url_field = Entry(frame,width=50,font = ("verdana","15"))

url_field.pack(side = LEFT)

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

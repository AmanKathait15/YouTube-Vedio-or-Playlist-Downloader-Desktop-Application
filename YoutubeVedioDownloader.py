from tkinter import *
from threading import *
from tkinter.filedialog import askdirectory
from pytube import *
from PIL import Image, ImageTk

file_size = 0

def show_download_status(stream = None, chunk = None, file_handle = None, remaining = None):

	downloaded = file_size - remaining

	percentage = (downloaded/file_size) * 100

	download_button.config(text = "{} percentage downloaded".format(percentage))

def start_downloading():
	global file_size

	try:

		url = url_field.get()
		print(url)

		Selectpath_button.config(text = "Downloading")
		Selectpath_button.config(state = DISABLED)

		ClearUrl_button.config(text = "Started")
		ClearUrl_button.config(state = DISABLED)

		download_button.config(text = "Wait...")
		download_button.config(state = DISABLED)

		yt = YouTube(url)
		stream = yt.streams.first()

		print(stream.title)
		file_size = stream.filesize
		print(stream.filesize)

		print("download started")

		stream.download(path)

		download_button.config(text = "Download")
		download_button.config(state = NORMAL)

		Selectpath_button.config(text = "choose folder")
		Selectpath_button.config(state = NORMAL)

		ClearUrl_button.config(text = "clear")
		ClearUrl_button.config(state = NORMAL)

		print("download completed ,,,,,,,")

	except Exception as e:
		print(e)

def start_downloading_thread():

	thread = Thread(target = start_downloading())
	thread.start()

path = "/home/aman/Downloads"

def select_path():
	
	global path

	tmp = askdirectory()

	if(tmp is not None):
		path = tmp

def emptyUrl():
	url_field.delete(0,END)

main_window = Tk()

#main_window.iconbitmap('youtube.ico')

main_window.title("YouTube Downloader")
main_window.geometry("300x150")

main_window.resizable(width=False , height = False)

#image_icon = ImageTk.PhotoImage(Image.open('youtube.png').resize(100,200))
#icon = Label(main_window,image = image_icon)
#icon.pack(side = TOP)

label1 = Label(main_window,text="Paste vedio link here",fg="red",bg="yellow",font=(" ",20,"bold"))
label1.pack(side = TOP, pady = 20)

url_field = Entry(main_window,font=("verdana",18),justify = CENTER)
url_field.pack(side = TOP , fill = X, padx = 10)

Selectpath_button = Button(main_window,width = 10,bg = "black", fg = "white",  text = "choose folder",font = (" ",10,"bold"), command = select_path)
Selectpath_button.pack(side = LEFT , padx = 5)

ClearUrl_button = Button(main_window,width = 10,bg = "black", fg = "white",  text = "clear",font = (" ",10,"bold"), command = emptyUrl)
ClearUrl_button.pack(side = LEFT , padx = 5)

download_button = Button(main_window,width = 10,text = "Download",fg="white",bg="black",relief = "ridge",font = (" ",10,"bold"),command = start_downloading_thread)
download_button.pack(side = LEFT, padx = 5)

main_window.mainloop()

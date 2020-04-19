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

		download_button.config(text = "Downloading ...")
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


main_window = Tk()

#main_window.iconbitmap('youtube.ico')

main_window.title("YouTube Downloader")
main_window.geometry("400x200")

#image_icon = ImageTk.PhotoImage(Image.open('youtube.png').resize(100,200))
#icon = Label(main_window,image = image_icon)
#icon.pack(side = TOP)

label1 = Label(main_window,text="Paste YouTube link here",fg="red",bg="yellow",font=(" ",20,"bold"))
label1.pack(side = TOP, pady = 20)

url_field = Entry(main_window,font=("verdana",18),justify = CENTER)
url_field.pack(side = TOP , fill = X, padx = 10, pady = 10)

SaveEntry = Button(main_window,width = 20,bg = "black", fg = "white",  text = "choose folder",font = (" ",10,"bold"), command = select_path)
SaveEntry.pack(side = LEFT , padx = 20)

download_button = Button(main_window,width = 20,text = "Download",fg="white",bg="black",relief = "ridge",font = (" ",10,"bold"),command = start_downloading_thread)
download_button.pack(side = LEFT)

url_field.delete(0,END)

main_window.mainloop()

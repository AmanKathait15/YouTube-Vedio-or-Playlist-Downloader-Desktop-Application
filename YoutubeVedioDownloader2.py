
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

from pytube import YouTube , Playlist
from threading import Thread

from PIL import ImageTk, Image
from urllib import request 

import subprocess, sys


default_path = "/home/aman/Downloads"

path = default_path

#file_size = 0

def single_download():

	try:

		url = url_field.get()

		yt = YouTube(url)

		print(yt.title)

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

		#label1.config(text = "Your download started :) ")

		ClearUrl_button.config(text = "please")
		#ClearUrl_button['text']="please"
		
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

		#label1.config(text = "paste YouTube Vedio link here")

	except Exception as e:
		
		print(e)

def start_downloading_thread():


	url = url_field.get()

	if(len(url)<2):

		label1.config(text = " Url field is empty ")

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

def set_bg_to_grey():

    root.configure(background="grey")

    topframe.configure(background="grey")

    middleframe.configure(background="grey")

def set_bg_to_red():

    root.configure(background="red")

    topframe.configure(background="red")

    middleframe.configure(background="red")

def set_bg_to_pink():

    root.configure(background="pink")

    topframe.configure(background="pink")

    middleframe.configure(background="pink")

def set_bg_to_brown():

    root.configure(background="brown")

    topframe.configure(background="brown")

    middleframe.configure(background="brown")


def set_bg_to_green():

    root.configure(background="green")

    topframe.configure(background="green")

    middleframe.configure(background="green")

def set_bg_to_blue():

    root.configure(background="lightblue")

    topframe.configure(background="lightblue")

    middleframe.configure(background="lightblue")

def createNewWindow():

	url = url_field.get()

	yt = YouTube(url)

	#request.urlretrieve(yt.thumbnail_url,yt.title+".jpeg")

	#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.

	#thumbnail_img = Image.open(yt.title+".jpeg")

	#thumbnail_img = thumbnail_img.resize((300,200),Image.ANTIALIAS)

	desc_window = Toplevel(root)

	desc_window.geometry("600x600")

	color = root["background"]

	desc_window.configure(background = color)

	
	Label(desc_window,text="Title : "+yt.title,fg="black",font = ("",10,"bold")).pack(side = TOP, pady = 10)

	frame = Frame(desc_window , background = "yellow" , height = 40, width = 200).pack()

	Label(frame,text= yt.rating,fg="black",font=("",10,"bold")).pack(side = LEFT , padx = 10)

	Label(frame,text= yt.views,fg="black",font=("",10,"bold")).pack(side = LEFT, padx = (0,10))

	Label(frame,text= yt.video_id,fg="black",font=("",10,"bold")).pack(side = LEFT , padx = (0,10))

	text_editor = Text(desc_window, height = 15)

	text_editor.config(wrap = 'word' , relief = FLAT)

	scroll_bar = Scrollbar(desc_window)

	text_editor.focus_set()

	scroll_bar.pack(side = RIGHT , fill = Y)

	text_editor.pack()

	scroll_bar.config(command = text_editor.yview)

	text_editor.config(yscrollcommand = scroll_bar.set)

	text_editor.insert(END,yt.description)
	
	'''

	#thumbnail_img = ImageTk.PhotoImage(thumbnail_img)

	#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
	#thumbnail = Label(desc_window, image = thumbnail_img,height=400,width=400)

	#The Pack geometry manager packs widgets in rows or columns.
	#thumbnail.pack()

	Label(desc_window,text= yt.rating,fg="black",font=("",10,"bold")).pack(side = LEFT)

	Label(desc_window,text= yt.views,fg="black",font=("",10,"bold")).pack(side = LEFT)

	Label(desc_window,text= yt.video_id,fg="black",font=("",10,"bold")).pack(side = LEFT) '''

def createnewwindow_thread():

	url = url_field.get()

	if(len(url)<2):

		label1.config(text = "Url field is empty")

		print("url field is empty")

		return

	if("https://www.youtube.com/" not in url):

		label1.config(text = "Sorry no description available for vedio")

		print("invlaid url")

		return

	thread = Thread(target = createNewWindow())
	
	thread.start()

def open_downloaded_vedio():

	url = url_field.get()

	if(len(url)<2):

		label1.config(text = " Url field is empty ")

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

	if(radioVar.get()=="2"):

		playlist_url = Playlist(url)

		url = playlist_url[0]

	yt = YouTube(url)

	print(yt.title)

	title = yt.title

	title = re.sub('[\|\/\?\*\+\^\.\$]+','',title)

	url = path+"/"+title+".mp4"

	print(url)

	#url = "/home/aman/Downloads/BANGALORE - THE SILICON VALLEY OF INDIA  BENGALURU CITY VIEW  2019 4K  WORLD EXPLORE.mp4"

	if sys.platform.startswith('linux'):
	    
	    subprocess.Popen(['xdg-open', url],
	                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	elif sys.platform.startswith('win32'):
	    
	    os.startfile(url)
	
	elif sys.platform.startswith('cygwin'):
	    
	    os.startfile(url)
	
	elif sys.platform.startswith('darwin'):
	    
	    subprocess.Popen(['open', url],
	                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
	    
	    subprocess.Popen(['xdg-open', url],
	                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def open_youtube():

	url = "https://www.youtube.com/"

	if sys.platform.startswith('linux'):
	    
	    subprocess.Popen(['xdg-open', url],
	                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	elif sys.platform.startswith('win32'):
	    
	    os.startfile(url)
	
	elif sys.platform.startswith('cygwin'):
	    
	    os.startfile(url)
	
	elif sys.platform.startswith('darwin'):
	    
	    subprocess.Popen(['open', url],
	                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
	    
	    subprocess.Popen(['xdg-open', url],
	                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':

	root = Tk()

	root.title("YouTube Multi Video Downloader")

	root.geometry("800x600")

	root.resizable(width = False , height = False)
	
	root.configure(background = "lightblue")

	label1 = Label(root,text="YouTube MUlti Vedio Downloader",fg="blue",bg="skyblue",font=("",15,"bold"))
    
	label1.pack(side=TOP,pady=20)

	topframe = Frame(root,background="lightblue")

	topframe.pack()

	#Label(set_bg_frame,text="Select background color",fg="red",bg="blue",font=("",12,"bold")).pack()

	darkcolor = Frame(topframe)

	darkcolor.pack(side = LEFT)

	icon_img = PhotoImage(file="youtubedownloader.png")

	icon_img = icon_img.subsample(1,1)

	icon_button = Button(topframe,image = icon_img , command = open_youtube)

	icon_button.pack(side = LEFT,padx = 100)

	lightcolor = Frame(topframe)

	lightcolor.pack(side = LEFT)

	red_image = PhotoImage(file = "red.png")
    
	brown_image = PhotoImage(file = "brown.png")
    
	pink_image = PhotoImage(file = "pink.png")

	grey_image = PhotoImage(file = "grey.png")

	green_image = PhotoImage(file = "green.png")

	blue_image = PhotoImage(file = "blue.png")

	red_image = red_image.subsample(4,4)
    
	brown_image = brown_image.subsample(4,4)
    
	pink_image = pink_image.subsample(4,4)

	grey_image = grey_image.subsample(4,4)

	green_image = green_image.subsample(4,4)

	blue_image = blue_image.subsample(4,4)

	red_button = Button(darkcolor,image = red_image,command = set_bg_to_red)
    
	red_button.pack(side = LEFT)

	brown_button = Button(darkcolor, image = brown_image,command = set_bg_to_brown)
    
	brown_button.pack(side = LEFT)

	green_button = Button(darkcolor,image = green_image,command = set_bg_to_green)
    
	green_button.pack(side = LEFT)

	pink_button = Button(lightcolor,image = pink_image,command = set_bg_to_pink)
    
	pink_button.pack(side = LEFT)

	grey_button = Button(lightcolor, image = grey_image,command = set_bg_to_grey)
    
	grey_button.pack(side = LEFT)

	blue_button = Button(lightcolor,image = blue_image,command = set_bg_to_blue)
    
	blue_button.pack(side = LEFT)

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

	middleframe = Frame(root)

	middleframe.pack(pady = 10)

	download_button = Button(middleframe,text="Download",bg = "black", fg = "white",font = (" ",10,"bold"), command = start_downloading_thread)

	download_button.pack(side = LEFT)

	ClearUrl_button = Button(middleframe,width = 10,bg = "black", fg = "white",  text = "clear",font = (" ",10,"bold"), command = emptyUrl)

	ClearUrl_button.pack(side=LEFT)

	desc_button = Button(middleframe,text="Description",bg = "black", fg = "white",font = (" ",10,"bold"), command = createnewwindow_thread)

	desc_button.pack(side = LEFT)

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

	choices.current(2)

	choices.bind("<<ComboboxSelected>>",select_Quality)

	vedio_image = PhotoImage(file = "/home/aman/Documents/my_projects/YouTube_Downloader/vedio.png")
	
	vedio_image = vedio_image.subsample(1,1)
	
	play_vedio_button = Button(root,image = vedio_image,command = open_downloaded_vedio)
	
	play_vedio_button.pack(side = TOP,pady = 10)
	
	root.mainloop()

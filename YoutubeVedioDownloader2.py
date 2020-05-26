
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

from pytube import YouTube , Playlist
from threading import Thread

from time import strftime,localtime,gmtime
from urllib import request
from pathlib import Path

import subprocess, sys , os

default_path = str(os.path.join(Path.home(), "Downloads"))

print(default_path)

path = default_path

file_size = 0

def on_progress(stream, chunk,bytes_remaining):

	global file_size

	vedio_downloaded = (float(abs(bytes_remaining-file_size)/file_size))*float(100)

	progress_bar['value'] = vedio_downloaded

	root.update_idletasks()

	print(vedio_downloaded)

	desc_button.config(text = "{:.2f} % Downloaded".format(vedio_downloaded))

def on_progress2(current,total):

	progress_bar['value'] = (current/total*100)

	root.update_idletasks()

def single_download():

	global file_size

	try:

		url = url_field.get()

		if(select_Quality() == "1"):

			yt = YouTube(url)

			title = yt.title

			print(title)
			print()

			print(yt.description)
			print()

			print(yt.rating)
			print()

			print(yt.views)
			print()

			print(yt.length)
			print()

			print(yt.thumbnail_url)
			print()

			label2.config(text = "{}/{} thumbnail downloaded".format(0,1))

			label4.config(text = "wait for thumbnail to download completly")

			label3.config(text = "RATING : "+str(yt.rating)+" VIEWS : "+str(yt.views)+" DURATION : "+strftime("%H:%M:%S", gmtime(yt.length)) , font = ("",14,"bold"))

			request.urlretrieve(yt.thumbnail_url,path+"/"+yt.title+".jpeg")

			on_progress2(1,1)

			location = path+"/"+title+".jpeg"

			print(location)

			with open("history.txt","a") as fp:

				fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+Quality[choices.current()]+" ,"+location+", "+url)

		else:

			yt = YouTube(url,on_progress_callback=on_progress)

			title = yt.title

			print(title)
			print()

			print(yt.description)
			print()

			print(yt.rating)
			print()

			print(yt.views)
			print()

			print(yt.length)
			print()

			print(yt.thumbnail_url)
			print()

			label2.config(text = "{}/{} Vedios downloaded".format(0,1))

			label4.config(text = "wait for vedio to download completly")

			label3.config(text = "RATING : "+str(yt.rating)+" VIEWS : "+str(yt.views)+" DURATION : "+strftime("%H:%M:%S", gmtime(yt.length)) , font = ("",14,"bold"))

			root.update_idletasks()

			itag = select_Quality()		

			print(itag)

			stream = yt.streams.get_by_itag(itag)

			print(stream.title)
			
			file_size = stream.filesize
			
			print(stream.filesize//(1024*1024))

			print("download started")

			stream.download(path)

			print("download completed ,,,,,,,")

			print(path)

			label2.config(text = "{}/{} Vedios downloaded".format(1,1))

			title = re.sub('[\|\/\?\*\+\^\.\$\,:]+','',title)

			location = path+"/"+title+".mp4"

			print(location)

			with open("history.txt","a") as fp:

				fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+Quality[choices.current()]+" ,"+location+", "+url)

	except Exception as e:

		print(e)


def multplie_download():

	global file_size

	try:

		playlist = url_field.get()

		playlist_url = Playlist(playlist)

		l = len(playlist_url)

		print(l)

		for i in range(l):

			label2.config(text = "{}/{} thumbnail downloaded".format(i,l))

			url = playlist_url[i]

			if(select_Quality() == "1"):

				yt = YouTube(url)

				title = yt.title

				print(title)
				print()

				print(yt.description)
				print()

				print(yt.rating)
				print()

				print(yt.views)
				print()

				print(yt.length)
				print()

				print(yt.thumbnail_url)
				print()

				label4.config(text = "wait for thumbnail to download completly")

				label3.config(text = "RATING : "+str(yt.rating)+" VIEWS : "+str(yt.views)+" DURATION : "+strftime("%H:%M:%S", gmtime(yt.length)) , font = ("",14,"bold"))

				itag = select_Quality()

				root.update_idletasks()

				request.urlretrieve(yt.thumbnail_url,path+"/"+yt.title+".jpeg")

				root.update_idletasks()

				on_progress2(i+1,l)

				location = path+"/"+title+".jpeg"

				#print(location)

				with open("history.txt","a") as fp:

					fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+Quality[choices.current()]+" ,"+location+", "+url)


			else:

				label2.config(text = "{}/{} Vedios downloaded".format(i,l))

				yt = YouTube(url,on_progress_callback=on_progress)

				title = yt.title

				print(title)
				print()

				print(yt.description)
				print()

				print(yt.rating)
				print()

				print(yt.views)
				print()

				print(yt.length)
				print()

				print(yt.thumbnail_url)
				print()

				label4.config(text = "wait for vedio to download completly")

				label3.config(text = "RATING : "+str(yt.rating)+" VIEWS : "+str(yt.views)+" DURATION : "+strftime("%H:%M:%S", gmtime(yt.length)) , font = ("",14,"bold"))

				itag = select_Quality()

				root.update_idletasks()

				print(itag)

				stream = yt.streams.get_by_itag(itag)

				print(stream.title)
				
				file_size = stream.filesize
				
				print(stream.filesize)

				print("download started")

				stream.download(path)

				print("{} vedio downloaded \n ".format(i+1))

				title = re.sub('[\|\/\?\*\+\^\.\$\,:]+','',title)

				location = path+"/"+title+".mp4"

				print(location)

				with open("history.txt","a") as fp:

					fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+Quality[choices.current()]+" ,"+location+", "+url)


		print("entire playlist downoaded ")

	except Exception as e:

		raise e


def start_downloading():

	try:

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

		Selectpath_button.config(state = NORMAL)

		play_vedio_button.config(state = NORMAL)

		red_button.config(state = NORMAL)

		green_button.config(state = NORMAL)

		orange_button.config(state = NORMAL)

		violet_button.config(state = NORMAL)

		pink_button.config(state = NORMAL)

		brown_button.config(state = DISABLED)

		yellow_button.config(state = NORMAL)

		lightgreen_button.config(state = NORMAL)

		blue_button.config(state = NORMAL)

		grey_button.config(state = NORMAL)

		icon_button.config(state = NORMAL)

		desc_button.config(text = "History")

		label1.config(text = " paste YouTube Vedio link here ")

		label2.config(text="select download location",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

		label3.config(text="select quality of vedio to download",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

		label4.config(text="open downloaded vedio",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

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

	label1.config(text = "Your download started :) ")

	ClearUrl_button.config(text = "please")
	#ClearUrl_button['text']="please"
	
	ClearUrl_button.config(state = DISABLED)

	download_button.config(text = "Wait...")
	
	download_button.config(state = DISABLED)

	Selectpath_button.config(state = DISABLED)

	play_vedio_button.config(state = DISABLED)

	red_button.config(state = DISABLED)

	brown_button.config(state = DISABLED)

	green_button.config(state = DISABLED)

	orange_button.config(state = DISABLED)

	violet_button.config(state = DISABLED)

	icon_button.config(state = DISABLED)

	pink_button.config(state = DISABLED)

	grey_button.config(state = DISABLED)

	blue_button.config(state = DISABLED)

	yellow_button.config(state = DISABLED)

	lightgreen_button.config(state = DISABLED)

	root.update_idletasks()

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

	else:

		return '1'

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

def set_bg_to_orange():

	root.configure(background="orange")

	topframe.configure(background="orange")

	middleframe.configure(background="orange")

def set_bg_to_violet():

	root.configure(background="violet")

	topframe.configure(background="violet")

	middleframe.configure(background="violet")

def set_bg_to_yellow():

	root.configure(background="yellow")

	topframe.configure(background="yellow")

	middleframe.configure(background="yellow")

def set_bg_to_lightgreen():

	root.configure(background="lightgreen")

	topframe.configure(background="lightgreen")

	middleframe.configure(background="lightgreen")

def open_downloaded_vedio():

	global path

	url = ""

	with open("history.txt","r") as f:

		data = f.readlines()

		lastline = data[-1]

		print(lastline)

		url = lastline.split(",")

		url = url[3]

	print(url)

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

	print("Sorry downloaded file can not be open try to open it by going to path : "+path)

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

def open_history():

	url = "history.txt"

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

	root.geometry("800x670")

	root.resizable(width = False , height = False)
	
	root.configure(background = "lightblue")

	label1 = Label(root,text="YouTube MUlti Vedio Downloader",fg="blue",bg="skyblue",font=("",15,"bold"))
    
	label1.pack(side=TOP,pady=20)

	topframe = Frame(root,background="lightblue")

	topframe.pack()

	#Label(set_bg_frame,text="Select background color",fg="red",bg="blue",font=("",12,"bold")).pack()

	darkcolor = Frame(topframe)

	darkcolor.pack(side = LEFT)

	icon_img = PhotoImage(file="image_resource/youtubedownloader.png")

	icon_img = icon_img.subsample(1,1)

	icon_button = Button(topframe,image = icon_img , command = open_youtube)

	icon_button.pack(side = LEFT,padx = 75)

	lightcolor = Frame(topframe)

	lightcolor.pack(side = LEFT)

	red_image = PhotoImage(file = "image_resource/red.png")
    
	brown_image = PhotoImage(file = "image_resource/brown.png")
    
	pink_image = PhotoImage(file = "image_resource/pink.png")

	grey_image = PhotoImage(file = "image_resource/grey.png")

	green_image = PhotoImage(file = "image_resource/green.png")

	blue_image = PhotoImage(file = "image_resource/blue.png")

	violet_image = PhotoImage(file = "image_resource/violet.png")

	orange_image = PhotoImage(file = "image_resource/orange.png")

	yellow_image = PhotoImage(file = "image_resource/yellow.png")

	lightgreen_image = PhotoImage(file = "image_resource/lightgreen.png")

	red_image = red_image.subsample(4,4)
    
	brown_image = brown_image.subsample(4,4)
    
	pink_image = pink_image.subsample(4,4)

	grey_image = grey_image.subsample(4,4)

	green_image = green_image.subsample(4,4)

	blue_image = blue_image.subsample(4,4)

	violet_image = violet_image.subsample(4,4)

	orange_image = orange_image.subsample(4,4)

	yellow_image = yellow_image.subsample(4,4)

	lightgreen_image = lightgreen_image.subsample(4,4)

	red_button = Button(darkcolor,image = red_image,command = set_bg_to_red)
    
	red_button.pack(side = LEFT)

	brown_button = Button(darkcolor, image = brown_image,command = set_bg_to_brown)
    
	brown_button.pack(side = LEFT)

	green_button = Button(darkcolor,image = green_image,command = set_bg_to_green)
    
	green_button.pack(side = LEFT)

	orange_button = Button(darkcolor,image = orange_image,command = set_bg_to_orange)
	   
	orange_button.pack(side = LEFT)

	violet_button = Button(darkcolor,image = violet_image,command = set_bg_to_violet)
	   
	violet_button.pack(side = LEFT)

	pink_button = Button(lightcolor,image = pink_image,command = set_bg_to_pink)
    
	pink_button.pack(side = LEFT)

	grey_button = Button(lightcolor, image = grey_image,command = set_bg_to_grey)
    
	grey_button.pack(side = LEFT)

	blue_button = Button(lightcolor,image = blue_image,command = set_bg_to_blue)
    
	blue_button.pack(side = LEFT)

	yellow_button = Button(lightcolor,image = yellow_image,command = set_bg_to_yellow)
	   
	yellow_button.pack(side = LEFT)

	lightgreen_button = Button(lightcolor,image = lightgreen_image,command = set_bg_to_lightgreen)
	   
	lightgreen_button.pack(side = LEFT)

	label1 = Label(root,text="paste YouTube Vedio link here",fg="red",bg="yellow",font=(" ",15,"bold"))

	label1.pack(side = TOP, padx=20, pady = 10)

	s = ttk.Style()

	s.theme_use('clam')

	s.configure("red.Horizontal.TProgressbar", foreground='blue', background='black')

	progress_bar = ttk.Progressbar(root,style="red.Horizontal.TProgressbar", orient = HORIZONTAL,length = 300, mode = 'determinate')

	progress_bar.pack(side = TOP , pady = (0,10))

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

	desc_button = Button(middleframe,text="History",bg = "black", fg = "white",font = (" ",10,"bold"), command = open_history)

	desc_button.pack(side = LEFT)

	#linkerror = Label(root,fg="red",text="no error")

	#linkerror.pack(pady = (0,10))

	label2 = Label(root,text="select download location",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

	label2.pack(pady = 10)

	Selectpath_button = Button(root,width = 20,bg = "black",fg = "white", text = "choose folder",font = ("verdana",10,"bold"),command = select_path)

	Selectpath_button.pack()

	#filelocationError = Label(root,text="")
	
	#filelocationError.pack(pady = (0,0))

	label3 = Label(root,text="select Quality of vedio to download",font = ("verdana",15,"bold"),fg="red",bg="yellow")

	label3.pack(pady = 10)

	Quality = ["mp4 1080p vedio only","mp4 720p","mp4 360p","mp4 audio only","thumbnail"]

	quality = StringVar()

	choices = ttk.Combobox(root,textvariable = quality,values = Quality,width = 30)

	choices.pack()

	choices.current(1)

	choices.bind("<<ComboboxSelected>>",select_Quality)

	label4 = Label(root,text="open downoaded vedio",font = ("verdana",15,"bold"),fg="red",bg="yellow")

	label4.pack(pady = (10,0))

	vedio_image = PhotoImage(file = "image_resource/vedio.png")
	
	vedio_image = vedio_image.subsample(1,1)
	
	play_vedio_button = Button(root,image = vedio_image,command = open_downloaded_vedio)
	
	play_vedio_button.pack(side = TOP,pady = 10)
	
	root.mainloop()

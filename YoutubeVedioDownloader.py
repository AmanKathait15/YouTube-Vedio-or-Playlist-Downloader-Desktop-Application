
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

from pytube import YouTube , Playlist
from threading import Thread

from time import strftime,localtime,gmtime
from urllib import request
from pathlib import Path

import subprocess, sys , os

print("\n\n<<<<<<<<<<<<<<<<< Default Path >>>>>>>>>>>>>>>>>>\n")

default_path = str(os.path.join(Path.home(), "Downloads"))

print("your default path to download vedio is : "+default_path+"\nHowever you can change it any time by clicking choose folder Button:)")

path = default_path

file_size = 0

sizes = []

no_of_vedios = 1

with open("history.txt","a") as fp:

	if os.stat("history.txt").st_size == 0:

	    fp.write("Date-Time , Vedio Title , Vedio Type , Location , Vedio Link \n")

def on_progress(stream, chunk,bytes_remaining):

	global file_size

	vedio_downloaded = abs(bytes_remaining-file_size)

	downloaded_percent = (float(vedio_downloaded/file_size))*float(100)

	progress_bar['value'] = downloaded_percent

	root.update_idletasks()

	print(downloaded_percent)

	desc_button.config(text = "{:.2f} % Downloaded".format(downloaded_percent))

	label2.config(text = "{}/{} Vedios downloaded [{:.2f}/{:.2f}] MB".format(0,no_of_vedios,vedio_downloaded/(1024*1024),(file_size)/(1024*1024)))

def on_progress2(current,total):

	progress_bar['value'] = (current/total*100)

	root.update_idletasks()

def download_HD(url):

	global file_size

	try:

		yt = YouTube(url,on_progress_callback=on_progress)

		title = yt.title

		file_name = re.sub(r"[^a-zA-Z0-9]","",title) + "_" + str(choices.current())

		root.update_idletasks()

		itag = select_Quality()

		stream = yt.streams.get_by_itag("140")

		file_size = yt.streams.get_by_itag("140").filesize + yt.streams.get_by_itag(itag).filesize

		print("audio download started")

		Audio = "/"+file_name + "audio"

		Vedio = "/"+file_name + "vedio"

		stream.download(path,filename = Audio)

		print("audio downloaded ,,,,,,,")

		print(path)

		os.rename(path + Audio + ".mp4", path+ Audio + ".mp3")

		stream = yt.streams.get_by_itag(itag)

		print(stream.title)

		print("vedio download started")

		stream.download(path,filename = Vedio)

		print("vedio download completed ,,,,,,,")

		print(path)
		print()

		print("merging audio and vedio file with ffmpeg as pytube does not support 1080p and higher stream with audio")
		print()

		label2.config(text = "{}/{} Vedios downloaded".format(1,1))

		if(itag == "137"):

			cmd = 'ffmpeg -y -i ' + path+ Audio +'.mp3  -r 30 -i ' +path + Vedio + '.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy '+ path+ "/" + file_name+'.mkv'

			subprocess.call(cmd, shell=True)

			os.remove(path + Vedio + '.mp4')

		else:

			cmd = 'ffmpeg -y -i ' + path+ Audio +'.mp3  -r 30 -i ' +path + Vedio + '.webm  -filter:a aresample=async=1 -c:a flac -c:v copy '+ path+ "/" + file_name+'.mkv'

			subprocess.call(cmd, shell=True)

			os.remove(path + Vedio + '.webm')

		os.remove(path + Audio + '.mp3')

		location = path+"/"+file_name+".mkv"

		print(location)

		with open("history.txt","a") as fp:

			fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+choices['values'][choices.current()]+" ,"+location+", "+url)

	except Exception as e:

		print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n"+str(e))

def single_download():

	global file_size

	try:

		url = url_field.get()

		if(select_Quality() in ("313","271","137")):

			download_HD(url)

		elif(select_Quality() == "1"):

			yt = YouTube(url)

			title = yt.title

			file_name = re.sub(r"[^a-zA-Z0-9_-]"," ",title)

			label2.config(text = "{}/{} thumbnail downloaded".format(0,1))

			request.urlretrieve(yt.thumbnail_url,path+"/"+file_name+".jpeg")

			on_progress2(1,1)

			location = path+"/"+file_name+".jpeg"

			print("\n>>>>>>>>>>>>>>> download location <<<<<<<<<<<<<<<<< \n"+location)

			with open("history.txt","a") as fp:

				fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+choices['values'][choices.current()]+" ,"+location+", "+url)

		else:

			yt = YouTube(url,on_progress_callback=on_progress)

			title = yt.title

			file_name = re.sub(r"[^a-zA-Z0-9_-]","",title)+ str(choices['values'][choices.current()])

			root.update_idletasks()

			itag = select_Quality()		

			print(itag)

			stream = yt.streams.get_by_itag(itag)

			print(stream.title)
			
			file_size = stream.filesize
			
			print(stream.filesize//(1024*1024))

			print("download started")

			stream.download(path,filename=file_name)

			print("download completed ,,,,,,,")

			print(path)

			label2.config(text = "{}/{} Vedios downloaded".format(1,1))

			location = None

			if(itag == "140"):

				os.rename(path + "/"+ file_name + ".mp4", path+ "/"+ file_name + ".mp3")

				location = path+"/"+file_name+".mp3"

			else:

				location = path+"/"+file_name+".mp4"

			print("\n>>>>>>>>>>>>>>> download location <<<<<<<<<<<<<<<<< \n"+location)

			with open("history.txt","a") as fp:

				fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+choices['values'][choices.current()]+" ,"+location+", "+url)

	except Exception as e:

		print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n"+str(e))


def multplie_download():

	global file_size , no_of_vedios

	try:

		playlist = url_field.get()

		playlist_url = Playlist(playlist)

		l = len(playlist_url)

		no_of_vedios = l

		print("\n>>>>>>>>>>>>>>> Number of vedios in playlist <<<<<<<<<<<<<<<<< \n"+str(l))

		for i in range(l):

			label2.config(text = "{}/{} thumbnail downloaded".format(i,l))

			url = playlist_url[i]

			print("\n>>>>>>>>>>>>>>> Vedio url<<<<<<<<<<<<<<<<< \n"+str(url))

			if(select_Quality() in ("313","271","137")):

				download_HD()

			elif(select_Quality() == "1"):

				yt = YouTube(url)

				title = yt.title

				file_name = re.sub(r"[^a-zA-Z0-9_-]"," ",title)+ str(choices['values'][choices.current()])

				label4.config(text = "wait for thumbnail to download completly")

				label3.config(text = "RATING : "+str(yt.rating)+" VIEWS : "+str(yt.views)+" DURATION : "+strftime("%H:%M:%S", gmtime(yt.length)) , font = ("",14,"bold"))

				itag = select_Quality()

				root.update_idletasks()

				request.urlretrieve(yt.thumbnail_url,path+"/"+file_name+".jpeg")

				root.update_idletasks()

				on_progress2(i+1,l)

				location = path+"/"+file_name+".jpeg"

				print("\n>>>>>>>>>>>>>>> download location <<<<<<<<<<<<<<<<< \n"+location)

				with open("history.txt","a") as fp:

					fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+choices['values'][choices.current()]+" ,"+location+", "+url)


			else:

				label2.config(text = "{}/{} Vedios downloaded".format(i,l))

				yt = YouTube(url,on_progress_callback=on_progress)

				title = yt.title

				file_name = re.sub(r"[^a-zA-Z0-9_-]"," ",title)+ str(choices['values'][choices.current()])

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

				location = None

				if(itag == "140"):

					os.rename(path + "/" + file_name + ".mp4", path + "/" + file_name + ".mp3")

					location = path+"/"+file_name+".mp3"

				elif(itag == "140"):

					os.rename(path + "/" + file_name + ".mp4", path + "/" + file_name + ".mp3")

					location = path+"/"+file_name+".mp3"

				else:

					location = path+"/"+file_name+".mp4"

				print("\n>>>>>>>>>>>>>>> download location <<<<<<<<<<<<<<<<< \n"+location)

				with open("history.txt","a") as fp:

					fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+yt.title+" , "+choices['values'][choices.current()]+" ,"+location+", "+url)


		print("entire playlist downoaded ")

	except Exception as e:

		print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n"+str(e))


def start_downloading():

	try:

		ch = radioVar.get()

		if(ch=="1"):

			print("\n>>>>>>>>>>>>> You are downloading a single vedio <<<<<<<<<<<<\n")

			single_download()

		else:

			print("\n>>>>>>>>>>>>> You are downloading a playlist <<<<<<<<<<<<<<<\n")

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

		brown_button.config(state = NORMAL)

		yellow_button.config(state = NORMAL)

		lightgreen_button.config(state = NORMAL)

		blue_button.config(state = NORMAL)

		grey_button.config(state = NORMAL)

		icon_button.config(state = NORMAL)

		desc_button.config(text = "History")

		label1.config(text=" Your download completed enjoy :) ",fg="yellow",bg="green",font = ("Agency FB",15,"bold"))

		label2.config(text="select download location",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

		label3.config(text="select quality of vedio to download",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

	except Exception as e:
		
		print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n"+str(e))

def start_downloading_thread():

	url = url_field.get()

	if(len(url)<2):

		label1.config(text = " Url field is empty ",fg="yellow",bg="red")

		print("\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> url field is empty <<<<<<<<<<<<<<<<<<\n")

		return

	if("https://www.youtube.com/" not in url):

		label1.config(text = " Please Enter Valid Url ",fg="yellow",bg="red")

		return

	if(radioVar.get()=="1" and "playlist" in url):

		label1.config(text = "link not match with its type",fg="yellow",bg="red")

		print("\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> you are trying to download playlist by selcting single vedio Radiobutton <<<<<<<<<<<<<<<<<<\n")

		return

	if(radioVar.get()=="2" and "watch" in url):

		label1.config(text = " link not match with its type ",fg="yellow",bg="red")

		print("\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> you are trying to download single vedio by selcting playlist Radiobutton <<<<<<<<<<<<<<<<<<\n")

		return

	print("\n>>>>>>>>>>>>>>>> Vedio Download Started :) <<<<<<<<<<<<<<<<< \n")

	label1.config(text = " Your download started :) ",fg="blue",bg="lightgreen",font = ("",15,"bold"))

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

	tmp = path

	if(len(tmp)>55):

		tmp = tmp[:55]
	
	label2.config(text="Path : "+str(tmp) , font = ("verdana",14,"bold"))

def select_Quality(event = None):

	global sizes

	choice = choices.current()

	itag = None

	if(choice == 7):

		itag = '313'			### itag for 2160p vedio ###

	elif(choice == 6):

		itag = '271'			### itag for 1440p vedio ###

	elif(choice == 5):
		
		itag = '137'			### itag for 1080p vedio ###

	elif(choice == 4):

		itag = '22'				### itag for 720p vedio ###

	elif(choice == 3):

		itag = '18'				### itag for 360p vedio ###

	elif(choice == 2):			

		itag = '251'			### itag for webm audio 160 kbps ###

	elif(choice == 1):

		itag = '140'			### itag for mp4 audio ###

	else:

		itag = '1'				### for vedio thumbnail download ###

	label3.config(text = "Quality : " + choices['values'][choice] +" Size : {:.2f} MB".format(sizes[choice]))

	return itag

def check_url(url_var):

	global sizes , path

	url = url_var.get()

	if(len(url)<1):

		label1.config(text = " Url field is empty ",bg="red",fg="yellow")

		#print("url field is empty")

		return

	if("https://www.youtube.com/" not in url):

		label1.config(text = " Please Enter Valid Url ",bg="red",fg="yellow")

		#print("invlaid url")

		return

	if(radioVar.get()=="1" and "playlist" in url):

		label1.config(text = "Error link not match with its type ",bg="red",fg="yellow")

		print("\n<<<<<<<<<<<<<<<<<<<<<<<< Error link not match with its type >>>>>>>>>>>>>>>>>>>>>>>>\n")

		print("you are trying to download playlist by selcting single vedio Radiobutton")

		return

	if(radioVar.get()=="2" and "watch" in url):

		label1.config(text = "Error link not match with its type ",bg="red",fg="yellow")

		print("\n<<<<<<<<<<<<<<<<<<<<<<<< Error link not match with its type >>>>>>>>>>>>>>>>>>>>>>>>\n")

		print("you are trying to download single vedio by selcting playlist Radiobutton")

		return

	if(radioVar.get()=="1" and "watch" in url):

		label1.config(text = " processing vedio link wait .. ",bg="red",fg="yellow")

		root.update_idletasks()

		print("\n<<<<<<<<<<<<<<<<<<<< Vedio Url >>>>>>>>>>>>>>>>>\n\n"+str(url))

		yt = YouTube(url)

		title = str(yt.title)

		print("\n<<<<<<<<<<<<<<<<<<<< Vedio Title >>>>>>>>>>>>>>>>>\n\n"+title)
		print()

		print("\n<<<<<<<<<<<<<<<<<<<< DESCRIPTION >>>>>>>>>>>>>>>>>\n\n"+yt.description)
		print()

		print("\n>>>>>>>>>>>>>>> Rating : {:.2f}".format(yt.rating))
		print()

		print("\n>>>>>>>>>>>>>>> Views : {}".format(yt.views))
		print()

		print("\n>>>>>>>>>>>>>>> Duration : "+strftime("%H:%M:%S", gmtime(yt.length)))
		print()

		print("\n>>>>>>>>>>>>>>> Vedio thumbnail : "+yt.thumbnail_url)
		print()

		title = re.sub(r'[^a-zA-Z0-9_-]','',title)

		if(len(title)>55):

			title = title[0:55]

		quality = ["thumbnail"]

		sizes = [0.5]

		if(yt.streams.get_by_itag("140") != None):

			quality.append("mp3 audio")

			sizes.append((yt.streams.get_by_itag("140").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("251") != None):

			quality.append("webm audio")

			sizes.append((yt.streams.get_by_itag("251").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("18") != None):

			quality.append("360p vedio")

			sizes.append((yt.streams.get_by_itag("18").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("22") != None):

			quality.append("720p vedio")

			sizes.append((yt.streams.get_by_itag("22").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("137") != None):

			quality.append("1080p HD vedio")

			sizes.append((yt.streams.get_by_itag("137").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("271") != None):

			quality.append("1440p vedio")

			sizes.append((yt.streams.get_by_itag("271").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("313") != None):

			quality.append("2160p FULL HD vedio")

			sizes.append((yt.streams.get_by_itag("313").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

		choices['values'] = quality

		if("2160p FULL HD vedio" in quality):

			choices.current(7)

		elif("1440p vedio" in quality):

			choices.current(6)

		elif("1080p HD vedio" in quality):

			choices.current(5)

		elif("720p vedio" in quality):

			choices.current(4)

		elif("360p vedio" in quality):

			choices.current(3)

		elif("webm audio" in quality):

			choices.current(2)

		elif("mp3 audio" in quality):

			choices.current(1)

		else:

			choices.current(0)

		choice = choices.current()

		print("\n<<<<<<<<<<<<<< Vedio avialabe at Quality >>>>>>>>>>>>>>\n")

		print(quality)

		print("\n<<<<<<<<<<<<<< Size coresponding to Quality >>>>>>>>>>>>>>\n")

		print(sizes)

		title = re.sub(r"[^a-zA-Z0-9_-]"," ",title)

		if(len(title)>40):

			title = title[:40]

		label1.config(text = "Title : "+title,fg="red",bg="yellow",font = ("",14,"bold"))

		tmp = path

		if(len(tmp)>55):

			tmp = tmp[:55]
		
		label2.config(text="Path : "+str(tmp) , font = ("verdana",14,"bold"))

		label3.config(text = " Quality : " + choices['values'][choice] +" Size : {:.2f} MB".format(sizes[choice]), font = ("",14,"bold"))

		label4.config(text = " Rating : {:.2f}".format(yt.rating) + " Views : "+str(yt.views)+" Duration : "+strftime("%H:%M:%S", gmtime(yt.length))+" ", font = ("",14,"bold"))

		download_button.config(state = NORMAL)

	elif(radioVar.get()=="2" and "playlist" in url):

		label1.config(text = " processing playlist link wait .. ",bg="red",fg="yellow")

		root.update_idletasks()

		playlist_url = Playlist(url)

		total_vedio = len(playlist_url)

		quality = ["thumbnail"]

		sizes = [1]

		yt = YouTube(playlist_url[0])

		if(yt.streams.get_by_itag("140") != None):

			quality.append("mp3 audio")

			sizes.append((yt.streams.get_by_itag("140").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("251") != None):

			quality.append("webm audio")

			sizes.append((yt.streams.get_by_itag("251").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("18") != None):

			quality.append("360p vedio")

			sizes.append((yt.streams.get_by_itag("18").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("22") != None):

			quality.append("720p vedio")

			sizes.append((yt.streams.get_by_itag("22").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("137") != None):

			quality.append("1080p HD vedio")

			sizes.append((yt.streams.get_by_itag("137").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("271") != None):

			quality.append("1440p vedio")

			sizes.append((yt.streams.get_by_itag("271").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

		if(yt.streams.get_by_itag("313") != None):

			quality.append("2160p FULL HD vedio")

			sizes.append((yt.streams.get_by_itag("313").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

		choices['values'] = quality

		if("2160p FULL HD vedio" in quality):

			choices.current(7)

		elif("1440p vedio" in quality):

			choices.current(6)

		elif("1080p HD vedio" in quality):

			choices.current(5)

		elif("720p vedio" in quality):

			choices.current(4)

		elif("360p vedio" in quality):

			choices.current(3)

		elif("webm audio" in quality):

			choices.current(2)

		elif("mp3 audio" in quality):

			choices.current(1)

		else:

			choices.current(0)

		choice = choices.current()

		print("\n<<<<<<<<<<<<<< Vedio avialabe at Quality >>>>>>>>>>>>>>\n")

		print(quality)

		print("\n<<<<<<<<<<<<<< Size coresponding to Quality >>>>>>>>>>>>>>\n")

		print(sizes)

		label1.config(text = " Playlist contain total {} vedios ".format(total_vedio),fg="red",bg="yellow",font = ("",14,"bold"))

		#label3.config(text = "Quality : " + choices['values'][choice] + " Size : {}".format(file_size))

		#label4.config(text = "Average Rating : {:.2f}".format(avg_rating/total_vedio)+ " Total views : "+str(total_views)+" Total Duration : "+strftime("%H:%M:%S", gmtime(total_time)), font = ("",12,"bold"))

		download_button.config(state = NORMAL)

def emptyUrl():

	url_field.delete(0,END)

	label1.config(text="paste YouTube Vedio link here",fg="red",bg="yellow",font=(" ",15,"bold"))

	label2.config(text="select download location",font = ("verdana",15,"bold"),fg="red",bg="yellow")

	label3.config(text="select Quality of vedio to download",font = ("verdana",15,"bold"),fg="red",bg="yellow")

	label4.config(text = "Open Downloaded Vedio",fg="red",bg="yellow",font=(" ",15,"bold"))

	download_button.config(state = DISABLED)

	choices['values'] = [" please insert link first "]

	choices.current(0)

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

	print("Be patient your vedio will play soon \n You can also go to this "+path+" in your file manager to open it manulay")

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

	flag = 0

	root = Tk()

	root.title("YouTube Multi Video Downloader")

	root.geometry("800x670")

	root.resizable(width = False , height = False)
	
	root.configure(background = "lightblue")

	label1 = Label(root,text="YouTube MUlti Vedio Downloader",fg="blue",bg="skyblue",font=("",15,"bold"))
    
	label1.pack(side=TOP,pady=20)

	topframe = Frame(root,background="lightblue")

	topframe.pack()

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

	single = Radiobutton(frame,text="single vedio",variable = radioVar,value = "1",fg = "black",bg="white",font = ("",10,"bold"))

	single.pack(side = LEFT)

	multiple = Radiobutton(frame,text="playlist",variable = radioVar,value = "2",fg = "black",bg="white",font = ("",10,"bold"))

	multiple.pack(side = LEFT)

	url_var = StringVar()

	url_var.trace("w", lambda name, index, mode, sv=url_var: check_url(url_var))

	url_field = Entry(frame,width=50,font = ("verdana","15") , textvariable = url_var)

	url_field.pack(side = LEFT)

	middleframe = Frame(root)

	middleframe.pack(pady = 10)

	download_button = Button(middleframe,text="Download",bg = "black", fg = "white",font = (" ",10,"bold"),state =DISABLED, command = start_downloading_thread)

	download_button.pack(side = LEFT)

	ClearUrl_button = Button(middleframe,width = 10,bg = "black", fg = "white",  text = "clear",font = (" ",10,"bold"), command = emptyUrl)

	ClearUrl_button.pack(side=LEFT)

	desc_button = Button(middleframe,text="History",bg = "black", fg = "white",font = (" ",10,"bold"), command = open_history)

	desc_button.pack(side = LEFT)

	label2 = Label(root,text="select download location",fg="red",bg="yellow",font = ("Agency FB",15,"bold"))

	label2.pack(pady = 10)

	Selectpath_button = Button(root,width = 20,bg = "black",fg = "white", text = "choose folder",font = ("verdana",10,"bold"),command = select_path)

	Selectpath_button.pack()

	label3 = Label(root,text="select Quality of vedio to download",font = ("verdana",15,"bold"),fg="red",bg="yellow")

	label3.pack(pady = 10)

	#Quality = ["thumbnail","mp3 audio only","webm auio only","mp4 360p","mp4 720p","mp4 1080p vedio only","mkv 1080p HD","mkv 1440p","mkv 2160p FULL HD"]

	quality = StringVar()

	choices = ttk.Combobox(root,textvariable = quality,values = ["please insert link first "],width = 30)

	choices.pack()

	choices.bind("<<ComboboxSelected>>",select_Quality)

	label4 = Label(root,text="open downoaded vedio",font = ("verdana",15,"bold"),fg="red",bg="yellow")

	label4.pack(pady = (10,0))

	vedio_image = PhotoImage(file = "image_resource/vedio.png")
	
	vedio_image = vedio_image.subsample(1,1)
	
	play_vedio_button = Button(root,image = vedio_image,state = DISABLED,command = open_downloaded_vedio)
	
	play_vedio_button.pack(side = TOP,pady = 10)
	
	root.mainloop()

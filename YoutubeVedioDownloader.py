
############################## modules reuired ######################################

from tkinter import *					###	used to craete GUI 
from tkinter import ttk 				###	used to craete GUI
from tkinter.filedialog import askdirectory		###	used to slecet path 

from pytube import YouTube , Playlist 			###	used to download vedio/playlist
from threading import Thread 				###	used to divide process into different threads

from time import strftime,localtime,gmtime 		###	used to find local date and time 
from urllib import request 				###	used to download thumbnail
from pathlib import Path 				###	used to default download path in compter 

import subprocess,sys,os 				###	used to craete subprocess and open other application 
							###	like vedio/audio player browser etc

############################# End of imported modules ###########################################


class YouTube_Downloader():

	"""		docstring for YouTube_Downloader class

	########################### class variable details #############################3

	variable name 		type 			use to

	url 			string 			store youtube url link

	title 			string 			store title of vedio

	duration 		string 			store length of vedio in format Hour : Minute : Second

	rating 			float			store rating of youtube vedio out of 5

	views 			integer			store number ot times vedio watched 

	file_name 		string 			name of downloaded vedio in hardisk

	file_size 		float 			size of vedio in MB

	no_of_vedios 		integer			store total number of vedios in playlist

	path 			string 			store path in which current vedio to be download

	sizes 			list			store different size in MB coresspondig to different
							qualities in which vedio is available

	quality 		list 		        store all available qualities of vedio to download 
							ex 360p 720p 1080p 2160p audio etc

	playlist_urls 		list 			store all single vedio urls (string) of playlist

	#################### class function details ######################

	function name 		task						run/call

	__init__ / constructor 	initialize all variables and assign memory	when object of YouTube_Downoader class is created 
																			  

	history 		create history.txt file if not exist and 	run before creating GUI
				write first row vaues i.e (date-time , 
				file name , vedio type , loaction , vedio link)

	check_url 		this function check if vedio url enter/paste 	run every_time when value at url_field change
				is valid or not or match with its Type 
				i.e sinlge vedio link by single vedio radio
				button and playlist url witb playlist radio 
				button it also display the details
				( like title , description , rating ,size etc)
				of vedio to be download by changing labels text . 

				Also change download button state to normal
				so that vedio can be downoad by click event

	clear_url_field		clear url field content and undo the effect of	 run when clear_button is clicked
				check_url function on label2,label3,label4

	select_Quality		return itag corresponding to selected quality 	run every time when combobox
				Downoading Vedio by itag is easy then by other  current value changes

				itag 		quality

				18 		360p
				22		720p
				137 		1080p withoit audio codec
				140 		only audio
				251 		only audio webm
				271		without audio codec
				313		2160p without audio codec

	select_path 		change path value by selected folder path	run when choose folder button clicked 
				value if no path select i.e cancel operation
				then default vaue reassigned 			

	open_downloaded_vedio	play last downloaded file form history file 	run when play_vedio button is clicked

	open_youtube 		open youtube.com in your default browser 	run when youtube_downoad icon clicked

	open_history 		open history.txt in your default text editor    run when history button is clicked

	downloading_thread 	this function seprate the downloading process  	run when download button is clicked
				by gui process by creating different thread
				for downoading process and hence reduce the
				load of GUI and boost speed of download also
				this function calL start_download function
				also check for url error

	start_downloading 	enable/disable the state of all button and 	run after downloading_thread
				call singel_download or multiple_download()
				on the basis of value of radio_button 

	singel_download 	this function provide code to download.		run when radioVar == "1"/singel vedio
				singel vedio and change value of labels 	and download button is clicked
				accordingly and further call on_progress1()

	multiple download 	provide functionality of downloading 		run when radioVar == "2"/playlist 
				playlist at different qualities 	 	and download button is clicked
				and changes value of labels .

	download_HD 		this function provide functinality of  		run when select_Quality is >= 1080p
				downloading HD vedio with audio as 
				pytube not support download of HD vedio 
				with audio codec.The idea behind is simple 
				download hd vedio witout audio and download
				audio file also and merge them to get one 
				vedio by free cmd/terminal soft like ffmpeg

	on_progress1		this function show vedio downloading status	run when vedio is downloading
				by updating the value of progress bar
				and history button

	on_progress2 		this function show the status of  		run when combobox current value 
				thumbnail downloaded in a playlist 		is "thumbnail" and radioVar is playlist

	update_history		insert new row in history.txt file  		run after dowmload is completed
				when new vedio downloaded

	############### non-class function ###############

	set_bg_to_<color>	change background to <color>			run when associated <color> button clicked

	if __name__ == 'main'	contain most code for GUI 			execution begin from this function

	#################### End of Docstring ################

	"""

	def __init__(self):
		
		self.url = None
		
		self.title = None
		
		self.duration = None
		
		self.rating = None
		
		self.views = None
		
		self.length = None
		
		self.file_name = None

		self.file_size = None
		
		self.no_of_vedios = None
		
		self.path = None
		
		self.sizes = None
		
		self.quality = None

		self.index = None

		self.playlist_urls = None


	def history(self):

		try:
			
			print("\n\n<<<<<<<<<<<<<<<<< Default Path >>>>>>>>>>>>>>>>>>\n")

			default_path = str(os.path.join(Path.home(), "Downloads"))

			print("your default path to download vedio is : "+default_path+"\n\nHowever you can change it any time by clicking choose folder Button:)")

			print("\n<<<<<<<<<<<<<<<<< ||||||||||| >>>>>>>>>>>>>>>>>>\n")

			self.path = default_path

			with open("history.txt","a") as fp:

				if os.stat("history.txt").st_size == 0:

				    fp.write("Date-Time , File Name , Vedio Type , Location , Vedio Link \n")

		except Exception as e:

			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))


	def on_progress1(self , stream, chunk , bytes_remaining):

		try:
			
			vedio_downloaded = (self.file_size - bytes_remaining)

			downloaded_percent = (float(vedio_downloaded/self.file_size))*float(100)

			progress_bar['value'] = downloaded_percent

			root.update_idletasks()

			print(downloaded_percent)

			history_button.config(text = "{:.2f} % Downloaded".format(downloaded_percent))

			label2.config(text = "{}/{} Vedios downloaded [{:.2f}/{:.2f}] MB".format(self.index,self.no_of_vedios,vedio_downloaded/(1024*1024),(self.file_size)/(1024*1024)))

			root.update_idletasks()

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def on_progress2(self , current , total):

		try:
			
			progress_bar['value'] = (current/total*100)

			root.update_idletasks()

		except Exception as e:

			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def update_history(self , extension , url , location = None):

		try:

			if sys.platform.startswith('win32'):

				location = self.path+"\\"+self.file_name + extension

			else:

				location = self.path+"/"+self.file_name + extension

			print("\n>>>>>>>>>>>>>>> download location <<<<<<<<<<<<<<<<< \n"+location)

			with open("history.txt","a") as fp:

				fp.write("\n"+str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+" , "+self.file_name+" , "+choices['values'][choices.current()]+" ,"+location+", "+ url)

			
		except Exception as e:

			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))
			

	def download_HD(self ):

		try:

			yt = YouTube(self.url,on_progress_callback=self.on_progress1)

			self.file_name = re.sub(r"[^a-zA-Z0-9]","",str(self.title)) + str(choices['values'][choices.current()])+ str(self.index)

			root.update_idletasks()

			itag = self.select_Quality()

			stream = yt.streams.get_by_itag("140")

			self.file_size = yt.streams.get_by_itag("140").filesize + yt.streams.get_by_itag(itag).filesize

			#progress_bar["maximum"] = self.file_size

			print("audio download started")

			if sys.platform.startswith('win32'):

				Audio = "\\"+self.file_name + "audio"

			else:

				Audio = "/"+self.file_name + "audio"

			if sys.platform.startswith('win32'):

				Vedio = "\\"+self.file_name + "vedio"

			else:

				Vedio = "/"+self.file_name + "vedio"

			stream.download(self.path,filename = Audio)

			print("audio downloaded ,,,,,,,")

			print(self.path)

			os.rename(self.path + Audio + ".mp4", self.path+ Audio + ".mp3")

			stream = yt.streams.get_by_itag(itag)

			print("vedio download started")

			stream.download(self.path,filename = Vedio)

			print("vedio download completed ,,,,,,,")

			print(self.path)
			print()

			print("merging audio and vedio file with ffmpeg as pytube does not support 1080p and higher stream with audio")
			print()

			location = None

			if sys.platform.startswith('win32'):

				location = self.path+"\\"+self.file_name+".mkv"

			else:

				location = self.path+"/"+self.file_name+".mkv"

			if(itag == "137"):

				cmd = 'ffmpeg -y -i ' + self.path+ Audio +'.mp3  -r 30 -i ' +self.path + Vedio + '.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy '+ location

				subprocess.call(cmd, shell=True)

				os.remove(self.path + Vedio + '.mp4')

			else:

				cmd = 'ffmpeg -y -i ' + self.path+ Audio +'.mp3  -r 30 -i ' +self.path + Vedio + '.webm  -filter:a aresample=async=1 -c:a flac -c:v copy '+ location

				subprocess.call(cmd, shell=True)

				os.remove(self.path + Vedio + '.webm')

			os.remove(self.path + Audio + '.mp3')

			self.update_history(".mkv" , self.url , location)

		except Exception as e:

			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def single_download(self):

		try:

			if(self.select_Quality() in ("313","271","137")):

				self.download_HD()

			elif(self.select_Quality() == "1"):

				self.file_name = re.sub(r"[^a-zA-Z0-9_-]","",self.title)

				label2.config(text = "{}/{} thumbnail downloaded".format(0,1))

				if sys.platform.startswith('win32'):

					request.urlretrieve(self.thumbnail_url,self.path+"\\"+self.file_name+".jpeg")

				else:

					request.urlretrieve(self.thumbnail_url,self.path+"/"+self.file_name+".jpeg")

				self.on_progress2(1,1)

				self.update_history(".jpeg" , self.url , location)

			else:

				yt = YouTube(self.url,on_progress_callback=self.on_progress1)

				self.file_name = re.sub(r"[^a-zA-Z0-9_-]","",self.title)+ str(choices['values'][choices.current()])

				root.update_idletasks()

				itag = self.select_Quality()		

				print(itag)

				stream = yt.streams.get_by_itag(itag)

				print(stream.title)
				
				self.file_size = stream.filesize
				
				print(stream.filesize//(1024*1024))

				print("download started")

				stream.download(self.path,filename=self.file_name)

				print("download completed ,,,,,,,")

				print(self.path)

				location = None

				if sys.platform.startswith('win32'):

					location = self.path+"\\"+self.file_name

				else:

					location = self.path+"/"+self.file_name

				if(itag == "140"):

					os.rename(location + ".mp4", location + ".mp3")

					self.update_history(".mp3",self.url,location)

				elif(itag == "251"):

					os.rename(location + ".webm", location + ".mp3")

					self.update_history(".mp3",self.url,location)

				else:

					self.update_history(".mp4",self.url,location)

		except Exception as e:

			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))


	def multiple_download(self):

		try:

			print("\n>>>>>>>>>>>>>>> Number of vedios in playlist <<<<<<<<<<<<<<<<< \n"+str(self.no_of_vedios))

			if(self.select_Quality() in ("313","271","137")):

				self.index = 0

				for url in self.playlist_urls:

					self.url = url

					print("\n>>>>>>>>>>>>>>> Vedio url<<<<<<<<<<<<<<<<< \n"+self.url)

					self.download_HD()

					self.index += 1

			elif(self.select_Quality() == "1"):

				self.index = 0

				label2.config(text = "{}/{} thumbnail downloaded".format(self.index,self.no_of_vedios))

				for url in self.playlist_urls:

					self.index += 1

					print("\n>>>>>>>>>>>>>>> Vedio url<<<<<<<<<<<<<<<<< \n"+url)

					yt = YouTube(url)

					self.file_name = re.sub(r"[^a-zA-Z0-9_-]","",yt.title)+ str(choices['values'][choices.current()]) + str(self.index)

					root.update_idletasks()

					if sys.platform.startswith('win32'):

						request.urlretrieve(yt.thumbnail_url,self.path+"\\"+self.file_name+".jpeg")

					else:

						request.urlretrieve(yt.thumbnail_url,self.path+"/"+self.file_name+".jpeg")

					root.update_idletasks()

					label2.config(text = "{}/{} thumbnail downloaded".format(self.index,self.no_of_vedios))

					self.on_progress2(self.index,self.no_of_vedios)

					label2.config(text = "{}/{} thumbnail downloaded".format(self.index,self.no_of_vedios))

					self.update_history(".jpeg",url)

			else:

				self.index = 0

				for url in self.playlist_urls:

					#label2.config(text = "{}/{} Vedios downloaded".format(i,self.no_of_vedios))

					yt = YouTube(url,on_progress_callback=self.on_progress1)

					self.file_name = re.sub(r"[^a-zA-Z0-9_-]"," ",yt.title)+ str(choices['values'][choices.current()]) + str(self.index)

					'''print(title)
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
					print()'''

					label4.config(text = "wait for vedio to download completly")

					label3.config(text = "RATING : "+str(yt.rating)+" VIEWS : "+str(yt.views)+" DURATION : "+strftime("%H:%M:%S", gmtime(yt.length)) , font = ("Arial",14,"bold"))

					itag = self.select_Quality()

					root.update_idletasks()

					print(itag)

					stream = yt.streams.get_by_itag(itag)

					print(stream.title)
					
					self.file_size = stream.filesize
					
					print(stream.filesize)

					print("download started")

					stream.download(self.path,filename = self.file_name)

					#print("{} vedio downloaded \n ".format(i+1))

					location = None

					if sys.platform.startswith('win32'):

						location = self.path+"\\"+self.file_name

					else:

						location = self.path+"/"+self.file_name

					if(itag == "140"):

						os.rename(location + ".mp4", location + ".mp3")

						self.update_history(".mp3",url,location)

					elif(itag == "251"):

						os.rename(location + ".webm", location + ".mp3")

						self.update_history(",mp3",url,location)

					else:

						self.update_history(".mp4",url,location)

					self.index += 1

			print("\n<<<<<<<<<<<< entire playlist downoaded >>>>>>>>>>>>>>>>\n")

			print("\n>>>>>>>>>>>>>>> download path <<<<<<<<<<<<<<<<< \n"+self.path)

		except Exception as e:

			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))


	def start_downloading(self):

		try:

			ch = radioVar.get()

			progress_bar['value'] = 0

			if(ch=="1"):

				print("\n>>>>>>>>>>>>> You are downloading a single vedio <<<<<<<<<<<<\n")

				self.single_download()

			else:

				print("\n>>>>>>>>>>>>> You are downloading a playlist <<<<<<<<<<<<<<<\n")

				self.multiple_download()
			
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

			history_button.config(text = "History")

			label1.config(text=" Your download completed enjoy :) ",fg="yellow",bg="green",font = ("Arial",15,"bold"))

			label2.config(text="select download location",fg="red",bg="yellow",font = ("Arial",15,"bold"))

			label3.config(text="select quality of vedio to download",fg="red",bg="yellow",font = ("Arial",15,"bold"))

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))
	
	def start_downloading_thread(self):

		try:

			if(len(self.url)<2):

				label1.config(text = " Url field is empty ",fg="yellow",bg="red")

				print("\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> url field is empty <<<<<<<<<<<<<<<<<<\n")

				return

			if("https://www.youtube.com/" not in self.url):

				label1.config(text = " Please Enter Valid Url ",fg="yellow",bg="red")

				return

			if(radioVar.get()=="1" and "playlist" in self.url):

				label1.config(text = "link not match with its type",fg="yellow",bg="red")

				print("\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> you are trying to download playlist by selcting single vedio Radiobutton <<<<<<<<<<<<<<<<<<\n")

				return

			if(radioVar.get()=="2" and "watch" in self.url):

				label1.config(text = " link not match with its type ",fg="yellow",bg="red")

				print("\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> you are trying to download single vedio by selcting playlist Radiobutton <<<<<<<<<<<<<<<<<<\n")

				return

			print("\n>>>>>>>>>>>>>>>> Vedio Download Started :) <<<<<<<<<<<<<<<<< \n")

			label1.config(text = " 		Your download started :) 		",fg="blue",bg="lightgreen",font = ("Arial",15,"bold"))

			ClearUrl_button.config(text = "please")
			
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

			thread = Thread(target = self.start_downloading())
			
			thread.start()

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def select_path(self):

		try:
			
			self.path = askdirectory()

			if(len(self.path)<=1):
				self.path = default_path

			tmp = self.path

			if(len(tmp)>55):

				tmp = tmp[:55]
			
			label2.config(text="Path : "+str(tmp) , font = ("Arial",14,"bold"))

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def select_Quality(self , event = None):

		try:
			
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

			if(radioVar.get()=="1"):

				label3.config(text = "Quality : " + choices['values'][choice] +" Size : {:.2f} MB".format(self.sizes[choice]))

			return itag

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def check_url(self , url_var):

		try:
			
			self.url = url_var.get()

			if(len(self.url)<1):

				label1.config(text = " Url field is empty ",bg="red",fg="yellow")

				#print("url field is empty")

				return

			if("https://www.youtube.com/" not in self.url):

				label1.config(text = " Please Enter Valid Url ",bg="red",fg="yellow")

				#print("invlaid url")

				return

			if(radioVar.get()=="1" and "playlist" in self.url):

				url_field.delete(0,END)

				label1.config(text = "Error link not match with its type ",bg="red",fg="yellow")

				print("\n<<<<<<<<<<<<<<<<<<<<<<<< Error link not match with its type >>>>>>>>>>>>>>>>>>>>>>>>\n")

				print("you are trying to download playlist by selcting single vedio Radiobutton")

				return

			if(radioVar.get()=="2" and "watch" in self.url):

				self.clear_url_field()

				label1.config(text = "Error link not match with its type ",bg="red",fg="yellow")

				print("\n<<<<<<<<<<<<<<<<<<<<<<<< Error link not match with its type >>>>>>>>>>>>>>>>>>>>>>>>\n")

				print("you are trying to download single vedio by selcting playlist Radiobutton")

				return

			if(radioVar.get()=="1" and "watch" in self.url):

				label1.config(text = "	 processing vedio link wait ... 	",bg="red",fg="yellow")

				root.update_idletasks()

				print("\n<<<<<<<<<<<<<<<<<<<< Vedio Url >>>>>>>>>>>>>>>>>\n\n"+(self.url))

				yt = YouTube(self.url)

				self.title = re.sub(r'[^a-zA-Z0-9_-]','',yt.title)

				self.description = yt.description
				
				self.rating = yt.rating
				
				self.views = yt.views
				
				self.length = strftime("%H:%M:%S", gmtime(yt.length))
				
				self.thumbnail_url = yt.thumbnail_url

				self.index = 0

				self.no_of_vedios = 1


				print("\n<<<<<<<<<<<<<<<<<<<< Vedio Title >>>>>>>>>>>>>>>>>\n\n"+self.title)
				print()

				print("\n<<<<<<<<<<<<<<<<<<<< DESCRIPTION >>>>>>>>>>>>>>>>>\n\n"+self.description)
				print()

				print("\n>>>>>>>>>>>>>>> Rating : {:.2f}".format(self.rating))
				print()

				print("\n>>>>>>>>>>>>>>> Views : {}".format(self.views))
				print()

				print("\n>>>>>>>>>>>>>>> Duration : "+self.length)
				print()

				print("\n>>>>>>>>>>>>>>> Vedio thumbnail : "+self.thumbnail_url)
				print()

				self.quality = ["thumbnail"]

				self.sizes = [0.5]

				if(yt.streams.get_by_itag("140") != None):

					self.quality.append("mp3_audio")

					self.sizes.append((yt.streams.get_by_itag("140").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("251") != None):

					self.quality.append("webm_audio")

					self.sizes.append((yt.streams.get_by_itag("251").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("18") != None):

					self.quality.append("360p_vedio")

					self.sizes.append((yt.streams.get_by_itag("18").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("22") != None):

					self.quality.append("720p_vedio")

					self.sizes.append((yt.streams.get_by_itag("22").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("137") != None):

					self.quality.append("1080p_HD_vedio")

					self.sizes.append((yt.streams.get_by_itag("137").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("271") != None):

					self.quality.append("1440p_vedio")

					self.sizes.append((yt.streams.get_by_itag("271").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("313") != None):

					self.quality.append("2160p_FULL_HD_vedio")

					self.sizes.append((yt.streams.get_by_itag("313").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

				choices['values'] = self.quality

				if("2160p_FULL_HD_vedio" in self.quality):

					choices.current(7)

				elif("1440p_vedio" in self.quality):

					choices.current(6)

				elif("1080p_HD_vedio" in self.quality):

					choices.current(5)

				elif("720p_vedio" in self.quality):

					choices.current(4)

				elif("360p_vedio" in self.quality):

					choices.current(3)

				elif("webm_audio" in self.quality):

					choices.current(2)

				elif("mp3_audio" in self.quality):

					choices.current(1)

				else:

					choices.current(0)

				choice = choices.current()

				print("\n<<<<<<<<<<<<<< Vedio avialabe at Quality >>>>>>>>>>>>>>\n")

				print(self.quality)

				print("\n<<<<<<<<<<<<<< Size coresponding to Quality >>>>>>>>>>>>>>\n")

				print(self.sizes)

				if(len(self.title)>40):

					self.title = self.title[:40]

				label1.config(text = "Title : "+self.title,fg="red",bg="yellow",font = ("Arial",14,"bold"))

				tmp = self.path

				if(len(tmp)>55):

					tmp = tmp[:55]
				
				label2.config(text="Path : "+str(tmp) , font = ("Arial",14,"bold"))

				label3.config(text = " Quality : " + choices['values'][choice] +" Size : {:.2f} MB".format(self.sizes[choice]), font = ("Arial",14,"bold"))

				label4.config(text = " Rating : {:.2f}".format(self.rating) + " Views : "+str(self.views)+" Duration : "+ self.length +" ", font = ("Arial",14,"bold"))

				download_button.config(state = NORMAL)

			elif(radioVar.get()=="2" and "playlist" in self.url):

				label1.config(text = "	processing playlist link wait ...	",bg="red",fg="yellow")

				root.update_idletasks()

				self.playlist_urls = Playlist(self.url)

				print("\n <<<<<<<<<<<< list of url in Playlist >>>>>>>>>>>>>> \n")

				print(self.playlist_urls)

				print("\n <<<<<<<<<<<< ----------------------- >>>>>>>>>>>>>> \n")

				self.no_of_vedios = len(self.playlist_urls)

				if(self.no_of_vedios == 0):

					self.clear_url_field()

					label1.config(text = "playlist is empty try again ",bg="red",fg="yellow")

					print("\n<<<<<<<<<<<<<<<<<<<<<<<< Error playlist is empty please try again by intering the same link >>>>>>>>>>>>>>>>>>>>>>>>\n")

					return

				self.quality = ["thumbnail"]

				self.sizes = [0.5]

				yt = None

				for url in self.playlist_urls:

					yt = YouTube(url)

					break

				if(yt.streams.get_by_itag("140") != None):

					self.quality.append("mp3_audio")

					#self.sizes.append((yt.streams.get_by_itag("140").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("251") != None):

					self.quality.append("webm_audio")

					#self.sizes.append((yt.streams.get_by_itag("251").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("18") != None):

					self.quality.append("360p_vedio")

					#self.sizes.append((yt.streams.get_by_itag("18").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("22") != None):

					self.quality.append("720p_vedio")

					#self.sizes.append((yt.streams.get_by_itag("22").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("137") != None):

					self.quality.append("1080p_HD_vedio")

					#self.sizes.append((yt.streams.get_by_itag("137").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("271") != None):

					self.quality.append("1440p_vedio")

					#self.sizes.append((yt.streams.get_by_itag("271").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

				if(yt.streams.get_by_itag("313") != None):

					self.quality.append("2160p_FULL_HD_vedio")

					#self.sizes.append((yt.streams.get_by_itag("313").filesize + yt.streams.get_by_itag("140").filesize)/(1024*1024))

				choices['values'] = self.quality

				if("2160p_FULL_HD_vedio" in self.quality):

					choices.current(7)

				elif("1440p_vedio" in self.quality):

					choices.current(6)

				elif("1080p_HD_vedio" in self.quality):

					choices.current(5)

				elif("720p_vedio" in self.quality):

					choices.current(4)

				elif("360p_vedio" in self.quality):

					choices.current(3)

				elif("webm_audio" in self.quality):

					choices.current(2)

				elif("mp3_audio" in self.quality):

					choices.current(1)

				else:

					choices.current(0)

				choice = choices.current()

				print("\n<<<<<<<<<<<<<< Vedio avialabe at Quality >>>>>>>>>>>>>>\n")

				print(self.quality)

				#print("\n<<<<<<<<<<<<<< Size coresponding to Quality >>>>>>>>>>>>>>\n")

				#print(self.sizes)

				label1.config(text = " Playlist contain total {} vedios ".format(self.no_of_vedios),fg="red",bg="yellow",font = ("",14,"bold"))

				#label3.config(text = "Quality : " + choices['values'][choice] + " Size : {}".format(file_size))

				#label4.config(text = "Average Rating : {:.2f}".format(avg_rating/total_vedio)+ " Total views : "+str(total_views)+" Total Duration : "+strftime("%H:%M:%S", gmtime(total_time)), font = ("",12,"bold"))

				download_button.config(state = NORMAL)

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))
	

	def clear_url_field(self):

		try:
			
			url_field.delete(0,END)

			label1.config(text="paste YouTube Vedio link here",fg="red",bg="yellow",font=("Arial",15,"bold"))

			label2.config(text="select download location",font = ("Arial",15,"bold"),fg="red",bg="yellow")

			label3.config(text="select Quality of vedio to download",font = ("Arial",15,"bold"),fg="red",bg="yellow")

			label4.config(text = "Open Downloaded Vedio",fg="red",bg="yellow",font=("Arial",15,"bold"))

			download_button.config(state = DISABLED)

			choices['values'] = [" please insert link first "]

			choices.current(0)

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def open_downloaded_vedio(self):

		try:
			
			tmp = ""

			with open("history.txt","r") as f:

				data = f.readlines()

				lastline = data[-1]

				tmp = lastline.split(",")

				print("\n <<<<<<<<<<<<< file details >>>>>>>>>>>>>>\n")

				print("\n\tdownload date and time: "+tmp[0]+"\n\t file name : "+tmp[1]+"\n\t download quality : "+tmp[2]+"\n\tdownload at location: "+tmp[3]+"\ndownload from url : "+tmp[4] )

				print("\n <<<<<<<<<<<<< end of file details >>>>>>>>>>>>>>\n")

				tmp = tmp[3]

			if sys.platform.startswith('linux'):
			    
			    subprocess.Popen(['xdg-open', tmp],
			                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			
			elif sys.platform.startswith('win32'):
			    
			    os.startfile(tmp)
			
			elif sys.platform.startswith('cygwin'):
			    
			    os.startfile(tmp)
			
			elif sys.platform.startswith('darwin'):
			    
			    subprocess.Popen(['open', tmp],
			                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			else:
			    
			    subprocess.Popen(['xdg-open', tmp],
			                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			print("\n    Be patient your vedio will play soon \n You can also go to this "+self.path+" in your file manager to open it manulay")

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def open_youtube(self):

		try:
			
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

		except Exception as e:
			
			print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n"+str(e))

	def open_history(self):

		file = "history.txt"

		if sys.platform.startswith('linux'):
		    
		    subprocess.Popen(['xdg-open', file],
		                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		elif sys.platform.startswith('win32'):
		    
		    os.startfile(file)
		
		elif sys.platform.startswith('cygwin'):
		    
		    os.startfile(file)
		
		elif sys.platform.startswith('darwin'):
		    
		    subprocess.Popen(['open', file],
		                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
		    
		    subprocess.Popen(['xdg-open', file],
		                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

if __name__ == '__main__':

	yd = YouTube_Downloader()

	print(yd.__doc__)

	yd.history()

	root = Tk()

	root.title("YouTube Multi Video Downloader")

	root.geometry("800x700")

	root.resizable(width = False , height = False)
	
	root.configure(background = "lightblue")

	label1 = Label(root,text="YouTube MUlti Vedio Downloader",fg="blue",bg="skyblue",font=("Arial",15,"bold"))
    
	label1.pack(side=TOP,pady=20)

	topframe = Frame(root,background="lightblue")

	topframe.pack()

	darkcolor = Frame(topframe)

	darkcolor.pack(side = LEFT)

	icon_img = PhotoImage(file="image_resource/youtubedownloader.png")

	icon_img = icon_img.subsample(1,1)

	icon_button = Button(topframe,image = icon_img , command = yd.open_youtube)

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

	label1 = Label(root,text="paste YouTube Vedio link here",fg="red",bg="yellow",font=("Arial",15,"bold"))

	label1.pack(side = TOP, padx=20, pady = 10)

	s = ttk.Style()

	s.theme_use('clam')

	s.configure("red.Horizontal.TProgressbar", foreground='blue', background='black')

	progress_bar = ttk.Progressbar(root,style="red.Horizontal.TProgressbar", orient = HORIZONTAL,length = 300, mode = 'determinate')

	progress_bar.pack(side = TOP , pady = (0,10))

	frame = Frame(root,background="black")

	frame.pack()

	radioVar = StringVar(frame,"1")

	single = Radiobutton(frame,text="single vedio",variable = radioVar,value = "1",fg = "black",bg="white",font = ("Arial",10,"bold"))

	single.pack(side = LEFT)

	multiple = Radiobutton(frame,text="playlist",variable = radioVar,value = "2",fg = "black",bg="white",font = ("Arial",10,"bold"))

	multiple.pack(side = LEFT)

	url_var = StringVar()

	url_var.trace("w", lambda name, index, mode, sv=url_var: yd.check_url(url_var))

	url_field = Entry(frame,width=50,font = ("Arial","15") , textvariable = url_var)

	url_field.pack(side = LEFT)

	middleframe = Frame(root)

	middleframe.pack(pady = 10)

	download_button = Button(middleframe,text="Download",bg = "black", fg = "white",font = ("Arial",10,"bold"),state =DISABLED,width = 15, height = 1,command = yd.start_downloading_thread)

	download_button.pack(side = LEFT)

	ClearUrl_button = Button(middleframe,bg = "black", fg = "white",  text = "clear",font = ("Arial",10,"bold"),width = 15, height = 1, command = yd.clear_url_field)

	ClearUrl_button.pack(side=LEFT)

	history_button = Button(middleframe,text="History",bg = "black", fg = "white",font = ("Arial",10,"bold"),width = 15, height = 1, command = yd.open_history)

	history_button.pack(side = LEFT)

	label2 = Label(root,text="select download location",fg="red",bg="yellow",font = ("Arial",15,"bold"))

	label2.pack(pady = 10)

	Selectpath_button = Button(root,width = 20,bg = "black",fg = "white", text = "choose folder",font = ("Arial",10,"bold"),command = yd.select_path)

	Selectpath_button.pack()

	label3 = Label(root,text="select Quality of vedio to download",font = ("Arial",15,"bold"),fg="red",bg="yellow")

	label3.pack(pady = 10)

	#Quality = ["thumbnail","mp3 audio only","webm auio only","mp4 360p","mp4 720p","mp4 1080p vedio only","mkv 1080p HD","mkv 1440p","mkv 2160p FULL HD"]

	quality = StringVar()

	choices = ttk.Combobox(root,textvariable = quality,values = ["please insert link first "],width = 30)

	choices.pack()

	choices.bind("<<ComboboxSelected>>",yd.select_Quality)

	label4 = Label(root,text="open downoaded vedio",font = ("Arial",15,"bold"),fg="red",bg="yellow")

	label4.pack(pady = (10,0))

	vedio_image = PhotoImage(file = "image_resource/vedio.png")
	
	vedio_image = vedio_image.subsample(1,1)
	
	play_vedio_button = Button(root,image = vedio_image,state = NORMAL,command = yd.open_downloaded_vedio)
	
	play_vedio_button.pack(side = TOP,pady = 10)
	
	root.mainloop()

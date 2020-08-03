import tkinter as tk					 
from tkinter import *
import tkinter
from tkinter import filedialog,Listbox,ttk,messagebox

import cv2
import time
import glob
import os
from PIL import ImageTk,Image
import PIL.Image, PIL.ImageTk
from multiprocessing.pool import ThreadPool

from tool.utils import *
from tool.torch_utils import *
from tool.tracker import CentroidTracker
from tool.darknet2pytorch import Darknet

# import pkg_resources.py2_warn
# import scipy

root = tk.Tk() 
root.title("Real Time Detection using YOLO") 
root.geometry("800x750")
root.resizable(0, 0)
menubar = Menu(root)
root.config(menu=menubar)
tabControl = ttk.Notebook(root) 

tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 
tab3 = ttk.Frame(tabControl) 
tab4 = ttk.Frame(tabControl) 
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Home') 
tabControl.add(tab2, text ='Live Detection')
tabControl.add(tab3, text ='Live Tracking & Recognition') 
tabControl.add(tab4, text ='History') 
tabControl.add(tab5, text ='Upload File') 
tabControl.pack(expand = 1, fill ="both") 

def helpwindow():
    pass

def AboutWindow():
    about = Toplevel(root)
    about.geometry("800x750")
    about.resizable(0, 0)
    ttk.Label(about, text ="Real Time Detection and Tracking cars & Tanks using YOLO",font='Helvetica 18 bold').grid(column = 0, 
							row = 0, 
							padx = 20, 
							pady = (0,0))
    ttk.Label(about, text ="About",font='Helvetica 18 bold').grid(column = 0, 
							row = 1, 
							padx = 0, 
							pady = (30,30))
    ttk.Label(about, text ="1.  Home – The Project Logo and Information",anchor='e').grid(column = 0, 
							row = 2,padx = 10,pady = 0,sticky=W)
    point2 = "2.  Real Time Detection – Loads camera frames into the tkinter window.\n     Perform object detection and displays (Name of the object and percentage of identification accuracy).\n     Displays information about FPS, RESOLUTION, CARCOUNT, TANKCOUNT."
    ttk.Label(about, text =point2, anchor='e').grid(column = 0, 
							row = 3,padx = 10,pady = 0,sticky=W)
    point3 = "3.  Real Time Tracking and Recognition – Loads camera frames into the tkinter window.\n     Perform object tracking using Centroid Tracking.\n     Displays information about FPS, RESOLUTION, CARCOUNT, TANKCOUNT, ALERT, STATUS."
    ttk.Label(about, text =point3, anchor='e').grid(column = 0, 
							row = 4,padx = 10,pady = 0,sticky=W)
    point4 = "4.  History – History tabs will have all the information about the \n     database of videos recording during live detection and tracking."
    ttk.Label(about, text =point4, anchor='e').grid(column = 0, 
							row = 5,padx = 10,pady = 0,sticky=W)
    point5 = "5.  Upload File – Upload video to run detection and tracking."
    ttk.Label(about, text =point5, anchor='e').grid(column = 0, 
							row = 6,padx = 10,pady = 0,sticky=W)

def HelpWindow():
    helpw = Toplevel(root)
    helpw.geometry("800x750")
    helpw.resizable(0, 0)
    ttk.Label(helpw, text ="Help",font='Helvetica 18 bold').grid(column = 0, 
							row = 1,padx = 10,pady = (30,30))
    ttk.Label(helpw, text ="Home: Project logo and Information.").grid(column = 0, 
							row = 2,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="Real Time Detection:").grid(column = 0, 
							row = 3,padx = 10,pady = (20,0),sticky=W)
    ttk.Label(helpw, text ="  -> Start – Click start button to start live detection.").grid(column = 0, 
							row = 4,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Stop – Click stop button to stop live detection.").grid(column = 0, 
							row = 5,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Start Recording – Click Start Recording to record live streaming.").grid(column = 0, 
							row = 6,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Stop Recording – Click Stop Recording to stop recording video.").grid(column = 0, 
							row = 7,padx = 10,pady = (0,0),sticky=W)

    ttk.Label(helpw, text ="Real Time Tracking:").grid(column = 0, 
							row = 8,padx = 10,pady = (20,0),sticky=W)
    ttk.Label(helpw, text ="  -> Start – Click start button to start live tracking.").grid(column = 0, 
							row = 9,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Stop – Click stop button to stop live tracking.").grid(column = 0, 
							row = 10,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Start Recording – Click Start Recording to record live streaming.").grid(column = 0, 
							row = 11,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Stop Recording – Click Stop Recording to stop recording video.").grid(column = 0, 
							row = 12,padx = 10,pady = (0,0),sticky=W)
                        
    ttk.Label(helpw, text ="History:").grid(column = 0, 
							row = 13,padx = 10,pady = (20,0),sticky=W)
    ttk.Label(helpw, text ="  -> Click on videos displaying in database tab.").grid(column = 0, 
							row = 14,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Play – To play selected video.").grid(column = 0, 
							row = 15,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Resume – To resume playing video.").grid(column = 0, 
							row = 16,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Pause – TO pause playing video.").grid(column = 0, 
							row = 17,padx = 10,pady = (0,0),sticky=W)
    ttk.Label(helpw, text ="  -> Refresh – TO refresh the database for getting recent videos.").grid(column = 0, 
							row = 18,padx = 10,pady = (0,0),sticky=W)

    ttk.Label(helpw, text ="Upload file:").grid(column = 0, 
							row = 19,padx = 10,pady = (20,0),sticky=W)
    ttk.Label(helpw, text ="  -> FileUpload – Click on fileupload button to run detection and tracking on uploaded video.").grid(column = 0, 
							row = 20,padx = 10,pady = (0,0),sticky=W)


def changetab2():
    tabControl.select(tab2)
    print("tab changed")

def changetab3():
    tabControl.select(tab3)
    print("tab changed")

def changetab4():
    tabControl.select(tab4)
    print("tab changed")

def changetab5():
    tabControl.select(tab5)
    print("tab changed")

def Displayfps():
    global showfps
    print("value changed")
    showfps = 1

def Displaynofps():
    global showfps
    print("value changed")
    showfps = 0

def Displayalerts():
    global showalert
    showalert = 1

def Displaynoalerts():
    global showalert
    showalert = 0

def Displaytime():
    global showtime
    showtime = 1

def Displaynotime():
    global showtime
    showtime = 0

def fileupload():
    videofilename =  filedialog.askopenfilename(initialdir = "/", title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
    print(videofilename)
    LiveDetectionTracking(tab5,video_source=videofilename)
    tabControl.select(tab5)

def donothing():
    print("do nothing")
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Upload video", command=fileupload)
filemenu.add_command(label="Real Time Detection", command=changetab2)
filemenu.add_command(label="Real Time Tracking", command=changetab3)
filemenu.add_command(label="Real Time Recignition", command=changetab3)
filemenu.add_command(label="Database", command=changetab4)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="About", command=AboutWindow)
menubar.add_cascade(label="About", menu=aboutmenu)

settingmenu = Menu(menubar, tearoff=0)
# settingmenu.add_command(label="Show Time", command=Displaytime)
# settingmenu.add_command(label="Dont Show Time", command=Displaynotime)
settingmenu.add_command(label="Show FPS", command=Displayfps)
settingmenu.add_command(label="Dont Show FPS", command=Displaynofps)
settingmenu.add_command(label="Show Alerts", command=Displayalerts)
settingmenu.add_command(label="Dont Show Alerts", command=Displaynoalerts)
menubar.add_cascade(label="Settings", menu=settingmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=HelpWindow)
menubar.add_cascade(label="Help", menu=helpmenu)






ttk.Label(tab1, 
		text ="Real Time Detection using YOLO",font='Helvetica 18 bold').grid(column = 0, 
							row = 0, 
							padx = 200, 
							pady = (50,50))
img = ImageTk.PhotoImage(PIL.Image.open("logo.jpeg"))
panel = Label(tab1, image = img)
panel.grid(row=1,column=0)
ttk.Label(tab1, 
		text ="Real time detection, recognition and tracking system ").grid(column = 0, 
							row = 2, 
							padx = 200, 
							pady = (50,5)) 
ttk.Label(tab1, 
		text ="for tanks and cars in outdoor environment. ").grid(column = 0, 
							row = 3, 
							padx = 200, 
							pady = 5) 

# class Home:
#     def __init__(self, window):
#         self.window = window
#         Label(self.window,text ="Real time detection, recognition and tracking system ").grid(column = 0, 
#                                     row = 0, 
#                                     padx = 150, 
#                                     pady = (100,5)) 
#         Label(self.window,text ="for tanks and cars in outdoor environment. ").grid(column = 0, 
#                                     row = 1, 
#                                     padx = 150, 
#                                     pady = 5) 
#         self.logo_img = ImageTk.PhotoImage(PIL.Image.open("/logo.jpeg"))
#         print(self.logo_img)
#         self.panel = Label(self.window, image = self.logo_img)
#         self.panel.grid(row=2,column=0)
#         Label(self.window,text ="This system is made for real time detection, ").grid(column = 0, 
#                                     row = 3, 
#                                     padx = 150, 
#                                     pady = 5) 
#         Label(self.window,text ="recognition and tracking of cars and tanks in outdoor environment. ").grid(column = 0, 
#                                     row = 4, 
#                                     padx = 150, 
#                                     pady = 5) 

# tab 2 live detection
class LiveDetection:
    def __init__(self, window, video_source=0):
        global showfps,showalert,showtime
        self.window = window

        Label(self.window,text ="Real time detection from webcam").grid(column = 0, 
									row = 0,padx = 30,pady = 5) 
        # self.window.title(window_title)
        self.video_source = video_source#"/home/tl/Downloads/Beautiful German Highway in Germany..mp4"
        self.start_flag = False
        self.start_record_flag = False
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        first_frame = Frame(self.window)
        first_frame.grid(row=2, column=0)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(first_frame, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0, sticky="NESW")

        second_frame = Frame(self.window)
        second_frame.grid(row=3, column=0)

        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(second_frame, text="Snapshot", width=15, command=self.snapshot)
        # self.btn_snapshot.grid(row=0, column=0, sticky="NESW")

        self.btn_start=tkinter.Button(second_frame, text="start", width=15, command=self.start)
        self.btn_start.grid(row=0, column=1, sticky="NESW")

        self.btn_stop=tkinter.Button(second_frame, text="stop", width=15, command=self.stop)
        self.btn_stop.grid(row=0, column=2, sticky="NESW")
        self.btn_stop["state"] = DISABLED

        self.btn_start_record=tkinter.Button(second_frame, text="start record", width=15, command=self.start_record)
        self.btn_start_record.grid(row=0, column=3, sticky="NESW")

        self.btn_stop_record=tkinter.Button(second_frame, text="stop record", width=15, command=self.stop_record)
        self.btn_stop_record.grid(row=0, column=4, sticky="NESW")
        self.btn_stop_record["state"] = DISABLED

        third_frame = Frame(self.window)
        third_frame.grid(row=4, column=0)

        self.fps_lable = Label(third_frame,text="FPS:")
        self.fps_lable.grid(row=0,column=0,padx=30,pady=10)
        self.fps_value = Label(third_frame,text="0")
        self.fps_value.grid(row=0,column=1,padx=30,pady=10)

        self.resolution_lable = Label(third_frame,text="Resolution:")
        self.resolution_lable.grid(row=0,column=2,padx=30,pady=10)
        self.resolution_value = Label(third_frame,text="600*500")
        self.resolution_value.grid(row=0,column=3,padx=30,pady=10)

        self.car_count_lable = Label(third_frame,text="Car count:")
        self.car_count_lable.grid(row=2,column=0,padx=30,pady=10)
        self.car_count_value = Label(third_frame,text="0")
        self.car_count_value.grid(row=2,column=1,padx=30,pady=10)

        self.tank_count_lable = Label(third_frame,text="Tank count:")
        self.tank_count_lable.grid(row=2,column=2,padx=30,pady=10)
        self.tank_count_value = Label(third_frame,text="0")
        self.tank_count_value.grid(row=2,column=3,padx=30,pady=10)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.displayfps()

        # for loding model
        
        self.use_cuda = True
        self.num_classes = 2
        self.namesfile = './custom_cars/obj.names'
        self.cfgfile="./custom_cars/yolov4.cfg"
        self.weightfile="./custom_cars/yolov4.weights"
        self.model = Darknet(self.cfgfile)
        print("model start")
        self.model.load_weights(self.weightfile)
        print("model loaded")
        if self.use_cuda:
            self.model.cuda()
        

    def displayfps(self):
        print("function running",showfps)
        if showfps == 0:
            self.fps_value['text'] = ''
        self.window.after(self.delay, self.displayfps)

    def start(self):
        self.start_flag = True
        self.btn_start["state"] = DISABLED
        self.btn_stop["state"] = NORMAL

    def stop(self):
        self.start_flag = False
        self.btn_start["state"] = NORMAL
        self.btn_stop["state"] = DISABLED

    def start_record(self):
        out_filename = "./output/video-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".mp4"
        self.out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(*"MJPG"), 10.0, (800,500))
        self.start_record_flag = True
        self.btn_start_record["state"] = DISABLED
        self.btn_stop_record["state"] = NORMAL
        print(self.start_record_flag)

    def stop_record(self):
        self.out.release()
        self.stop_record_flag = False
        self.btn_start_record["state"] = NORMAL
        self.btn_stop_record["state"] = DISABLED

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        print("screeshot")
        print(ret)
        if ret:
            print("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def detect_cv2(self, image):
        sized = cv2.resize(image, (self.model.width, self.model.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        fps=0
        prev_time = time.time()
        boxes = do_detect(self.model, sized, 0.5, self.num_classes, 0.4, self.use_cuda)
        fps = 1/(time.time()-prev_time)
        self.fps_value['text'] = str(int(fps))
        class_names = load_class_names(self.namesfile)
        result_img, carCount, tankCount = plot_boxes_cv2(image, boxes, savename=None, class_names=class_names)
        # print("carCount: "+ str(carCount)+" tankCount: "+str(tankCount))
        self.car_count_value['text'] = carCount
        self.tank_count_value['text'] = tankCount
        return result_img


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if self.start_flag:
            frame = self.detect_cv2(frame)
        frame = cv2.resize(frame,(800,500))
        # print(self.start_record_flag,self.start_flag)
        if self.start_record_flag:
            write_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(write_frame)
        
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

 
class MyVideoCapture:
    def __init__(self, video_source):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = 800
        self.height = 500

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
 
# tab3 database
class Database:

    def __init__(self, window):

        self.window = window
        # self.window.title(window_title)
        Label(self.window, text ="Database").grid(column = 0, row = 0, 
									padx = 30, pady = 5)
        top_frame = Frame(self.window)
        top_frame.grid(row=0, column=0)

        self.pause = False   # Parameter that controls pause button

        self.canvas = Canvas(top_frame)
        self.canvas.grid(row=0, column=0)

        middle_frame = Frame(self.window)
        middle_frame.grid(row=1, column=0)

        # Play Button
        self.btn_play=Button(middle_frame, text="Play", width=15, command=self.play_video)
        self.btn_play.grid(row=1, column=1,padx=20)

        # Pause Button
        self.btn_pause=Button(middle_frame, text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=1, column=2,padx=20)

        # Resume Button
        self.btn_resume=Button(middle_frame, text="resume", width=15, command=self.resume_video)
        self.btn_resume.grid(row=1, column=3,padx=20)

        # Refresh database
        self.btn_resume=Button(middle_frame, text="Refresh", width=15, command=self.refresh_database)
        self.btn_resume.grid(row=1, column=4,padx=20)

        bottom_frame = Frame(self.window)
        bottom_frame.grid(row=2, column=0)

        self.filename = "No file selected"
        self.filename_lable = Label(bottom_frame,text=self.filename)
        self.filename_lable.grid(row=0,column=0,pady=10)

        self.listbox = Listbox(bottom_frame, height = 20, width = 45,  
                        bg = "white", activestyle = 'dotbox',  
                        font = "Helvetica", fg = "black") 
        self.listbox.grid(row=1, column=0, sticky='NESW')

        self.scrollbar = Scrollbar(bottom_frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=0, sticky='NS')
        
        self.database_path = "./output/*.mp4"
        for file_path in glob.glob(self.database_path):
            # print(file_path)
            self.listbox.insert(tk.END, file_path)
        self.listbox.bind("<Double-Button>", lambda x: self.play())
        self.delay = 15   # ms

        
        # self.window.mainloop()
    def refresh_database(self):
        self.listbox.delete('0', 'end')
        for file_path in glob.glob(self.database_path):
            # print(file_path)
            self.listbox.insert(tk.END, file_path)

    def play(self):
        self.filename = self.listbox.get(self.listbox.curselection())
        self.filename_lable['text'] = self.filename
        print(self.listbox.get(self.listbox.curselection()))
        self.cap = cv2.VideoCapture(self.filename)
        print(self.filename)
        self.width = 800
        self.height = 500

        self.canvas.config(width = self.width, height = self.height)


    def get_frame(self):   # get only one frame
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        except:
            messagebox.showerror(title='Video file not found', message='Please select a video file.')


    def play_video(self):

        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame()
        frame = cv2.resize(frame,(800,500))
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        if not self.pause:
            self.window.after(self.delay, self.play_video)

    def pause_video(self):
        self.pause = True

    def resume_video(self):
        self.pause=False
        self.play_video()

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

# tab 4 live detection with tracking
class LiveDetectionTracking:
    def __init__(self, window, video_source=0):
        global showfps,showalert,showtime
        self.window = window

        Label(self.window,text ="Real time detection from webcam").grid(column = 0, 
									row = 0,padx = 30,pady = 5) 
        # self.window.title(window_title)
        self.video_source = video_source
        self.start_flag = False
        self.start_record_flag = False
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        first_frame = Frame(self.window)
        first_frame.grid(row=2, column=0)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(first_frame, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(row=0, column=0, sticky="NESW")

        second_frame = Frame(self.window)
        second_frame.grid(row=3, column=0)

        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(second_frame, text="Snapshot", width=15, command=self.snapshot)
        # self.btn_snapshot.grid(row=0, column=0, sticky="NESW")

        self.btn_start=tkinter.Button(second_frame, text="start", width=15, command=self.start)
        self.btn_start.grid(row=0, column=1, sticky="NESW")

        self.btn_stop=tkinter.Button(second_frame, text="stop", width=15, command=self.stop)
        self.btn_stop.grid(row=0, column=2, sticky="NESW")
        self.btn_stop["state"] = DISABLED

        self.btn_start_record=tkinter.Button(second_frame, text="start record", width=15, command=self.start_record)
        self.btn_start_record.grid(row=0, column=3, sticky="NESW")

        self.btn_stop_record=tkinter.Button(second_frame, text="stop record", width=15, command=self.stop_record)
        self.btn_stop_record.grid(row=0, column=4, sticky="NESW")
        self.btn_stop_record["state"] = DISABLED

        third_frame = Frame(self.window)
        third_frame.grid(row=4, column=0)

        self.fps_lable = Label(third_frame,text="FPS:")
        self.fps_lable.grid(row=0,column=0,padx=30,pady=10)
        self.fps_value = Label(third_frame,text="0")
        self.fps_value.grid(row=0,column=1,padx=30,pady=10)

        self.resolution_lable = Label(third_frame,text="RESOLUTION:")
        self.resolution_lable.grid(row=0,column=2,padx=30,pady=10)
        self.resolution_value = Label(third_frame,text="600*500")
        self.resolution_value.grid(row=0,column=3,padx=30,pady=10)

        self.car_count_lable = Label(third_frame,text="CAR COUNT:")
        self.car_count_lable.grid(row=2,column=0,padx=30,pady=10)
        self.car_count_value = Label(third_frame,text="0")
        self.car_count_value.grid(row=2,column=1,padx=30,pady=10)

        self.tank_count_lable = Label(third_frame,text="TANK COUNT:")
        self.tank_count_lable.grid(row=2,column=2,padx=30,pady=10)
        self.tank_count_value = Label(third_frame,text="0")
        self.tank_count_value.grid(row=2,column=3,padx=30,pady=10)

        self.status_lable = Label(third_frame,text="STATUS:")
        self.status_lable.grid(row=4,column=0,padx=30,pady=10)
        self.status_value = Label(third_frame,text="NO Tracking")
        self.status_value.grid(row=4,column=1,padx=30,pady=10)

        self.alert_lable = Label(third_frame,text="ALERT:")
        self.alert_lable.grid(row=4,column=2,padx=30,pady=10)
        self.alert_value = Label(third_frame,text="Situation is Normal")
        self.alert_value.grid(row=4,column=3,padx=30,pady=10)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.displayfps()
        self.displayalerts()
        # for loding model
        
        self.use_cuda = True
        self.num_classes = 2
        self.namesfile = './custom_cars/obj.names'
        self.cfgfile="./custom_cars/yolov4.cfg"
        self.weightfile="./custom_cars/yolov4.weights"
        self.model = Darknet(self.cfgfile)
        print("model start")
        self.model.load_weights(self.weightfile)
        self.ctracker = CentroidTracker()
        print("model loaded")
        if self.use_cuda:
            self.model.cuda()
        
    def displayfps(self):
        print("function running",showfps)
        if showfps == 0:
            self.fps_value['text'] = ''
        self.window.after(self.delay, self.displayfps)

    def displayalerts(self):
        if showalert == 0:
            self.alert_value['text'] = ''
        self.window.after(self.delay, self.displayalerts)

    def start(self):
        self.start_flag = True
        self.btn_start["state"] = DISABLED
        self.btn_stop["state"] = NORMAL

    def stop(self):
        self.start_flag = False
        self.btn_start["state"] = NORMAL
        self.btn_stop["state"] = DISABLED

    def start_record(self):
        out_filename = "/output/video-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".mp4"
        self.out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(*"MJPG"), 10.0, (800,500))
        self.start_record_flag = True
        self.btn_start_record["state"] = DISABLED
        self.btn_stop_record["state"] = NORMAL
        print(self.start_record_flag)

    def stop_record(self):
        self.out.release()
        self.stop_record_flag = False
        self.btn_start_record["state"] = NORMAL
        self.btn_stop_record["state"] = DISABLED

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        print("screeshot")
        print(ret)
        if ret:
            print("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def detect_cv2(self, image):
        sized = cv2.resize(image, (self.model.width, self.model.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
        try:
            fps=0
            prev_time = time.time()
            boxes = do_detect(self.model, sized, 0.5, self.num_classes, 0.4, self.use_cuda)
            fps = 1/(time.time()-prev_time)
            self.fps_value['text'] = str(int(fps))
            class_names = load_class_names(self.namesfile)
            width = image.shape[1]
            height = image.shape[0]
            # print(width)
            rects = []
            for i in range(len(boxes)):
                box = boxes[i]
                xmin = int((box[0] - box[2] / 2.0) * width)
                ymin = int((box[1] - box[3] / 2.0) * height)
                xmax= int((box[0] + box[2] / 2.0) * width)
                ymax = int((box[1] + box[3] / 2.0) * height)
                # print((xmin, ymin, xmax, ymax))
                rects.append((xmin, ymin, xmax, ymax))

            objects = self.ctracker.update(rects)

            for (objectID, centroid) in objects.items():
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                # text = "ID {}".format(objectID)
                text = "ID "+str(int(objectID))
                # print(text)
                # cv2.putText(image, str(text), (centroid[0] + 10, centroid[1] + 10),
                #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255,0), 2)
                cv2.circle(image, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            sized, carCount, tankCount = plot_boxes_cv2(image, boxes, savename=None, class_names=class_names)
            # print("carCount: "+ str(carCount)+" tankCount: "+str(tankCount))
            if carCount==0 and tankCount ==0:
                self.status_value['text'] = 'No Tracking'
            else:
                self.status_value['text'] = 'Tracking'

            if carCount>50 and tankCount>50:
                self.alert_value['text'] = 'Situation is Abnormal'
            else:
                self.alert_value['text'] = 'Situation is Normal'
            self.car_count_value['text'] = carCount
            self.tank_count_value['text'] = tankCount
        except:
            pass
        return sized


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if self.start_flag:
            frame = self.detect_cv2(frame)
        frame = cv2.resize(frame,(800,500))
        # print(self.start_record_flag,self.start_flag)
        if self.start_record_flag:
            write_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(write_frame)
        
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

class FileUpload:
    def __init__(self, window):
        global showfps,showalert,showtime
        self.window = window

        Label(self.window,text ="Real time detection from Video File").grid(column = 0, 
									row = 0,padx = 30,pady = 5) 

        # Button that lets the user take a upload file
        self.btn_snapshot=tkinter.Button(self.window, text="File", width=15, command=self.uploadfilevideo)
        self.btn_snapshot.grid(row=1, column=0, sticky="NESW")

    def uploadfilevideo(self):
        videofilename =  filedialog.askopenfilename(initialdir = "/", title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        print(videofilename)
        LiveDetectionTracking(tab5,video_source=videofilename)


if __name__ == "__main__":
    global showfps,showalert,showtime
    showfps = 1
    showalert = 1
    showtime = 1
    # Home(tab1)
    Database(tab4)
    LiveDetection(tab2,video_source="0")
    LiveDetectionTracking(tab3,video_source="0")
    FileUpload(tab5)
    root.mainloop()
    
     

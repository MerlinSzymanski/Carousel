from class_gpio import Caroussel
import csv
from datetime import datetime
import json
import os
import shutil
from time import sleep
from io import BytesIO
import threading
from threading import Thread


class Experiment(Thread):
    """This class stores everything necessary for the experiment. It contains an instance of the Caroussel, the 
    start-method for the experiment and creates the archive. The necessary data comes from an input_file. Pure informational
    data is not implemented (e.g. rig-number or genotype) but later saved directly into the archive"""
	
    def __init__(self, infile):
        
        #All the data used only for the archive
        with open(infile,'r') as json_file:
            self.indata = (json.load(json_file))
            with open('save_files/temp/exp_template.json','w') as temp:
                json.dump(temp, self.indata, indent=2) #create temp-file for the experiment-folder  
        #some processing
        #TODO: see, if time_string really is necessary... Maybe get the time completely from the raspberry
        date_string = self.indata['date'] +' '+ self.indata['time']  #yyyymmdd hhmmss
        self.timestamp = datetime.strptime(date_string,'%Y%m%d %H%M%S')
        
        #the GPIO - instance
        self.caroussel = Caroussel(self.indata)
  
    #1. Start the CronJob
    def cron(self):
        """starts a python CRON-job in the Main before the experiment even begins Motor and light are therefor independend
        of the beginning of the experiment"""
        t = threading.currentThread()   #used to quit the cron-job later
        
        #1.1 Start the motors 

        self.caroussel.start_motor()
        
        #1.2.regulate the light according to the CircRhythm
        with open('files/settings.json','r') as set_file:
            settings = (json.load(set_file))
            circ = settings[self.indata['circRythm']]
            start_time_white = int(circ['white'])   #z.B. '6'
            start_time_red = int(circ['red'])       #z.B. '22'
        
            while getattr(t,"running",True):
                #Get the current hours
                current_hour = int(datetime.strftime(datetime.now(),"%H"))
                #Check if time is between 6 and 22 --> make white light, else red
                if (start_time_white <= current_hour and current_hour < start_time_red):
                    self.caroussel.set_daylight()
                else:
                    self.caroussel.set_nightlight()
                    sleep(1)


    #2. create temp-file
    def get_experiment_id(self):
        """create unique experiment-ID which contains the current settings"""
        #2.1. create experiment-ID 
        experiment_ID = f'CARO_{self.timestamp.strftime("%y%m%d%H%M")}_{self.indata["rig"]}_{self.indata["sex"]}\
        _{self.indata["genotype"]}_{self.indata["age"]}'
        #2.2. add the new information to the dic
        self.indata['id'] = experiment_ID
        self.indata['status'] = "initiated"
    
    def start_motor_and_disc(self):
        t = threading.currentThread() 
        #lets start with the disc
        self.caroussel.set_disc_position(1,self.indata['disc1_pos'])
        self.caroussel.set_disc_position(2,self.indata['disc2_pos'])
        
        #Now the motor_direction. it starts with motor1 and changes to motor2
        #after the switch-time. and so on and so forth.
        
        direction1 = self.indata['motor1_direction']
        direction2 = self.indata['motor2_direction'] 
        switch_time = int(self.indata['switch'])
        
        while getattr(t,'running',True):
            self.caroussel.turn_motor1(direction1)
            sleep(switch_time)  #let the motor1 turn
            self.caroussel.turn_motor2(direction2)
            sleep(switch_time)  #let the motor2 turn 
            
    ###NOT YET DONE###
    def start_camera(self):
        t = threading.currentThread() 
        
        self.caroussel.camera.start_preview()
        n = 1
        
        while getattr(t,'running',True): 
            #create stream
            stream = BytesIO()
            video_name = f'{self.indata["id"]}_L_{0:03}.h264'.format(n)   
            #start recording to the stream
            self.caroussel.camera.start_recording(stream, format='h264', resize = (768,768))
            #Now the duration of the recording
            #Change that to Frames, not seconds!
            self.caroussel.camera.wait_recording(int(self.indata["pause_time"]))
            self.caroussel.camera.stop_recording()
        
            with open (video_name,'wb') as f:
                # "Rewind" the stream to the beginning so we can flush its content to the file
                stream.seek (0)
                shutil.copyfileobj (stream,f)
                stream.close()
            sleep(0.05)
            
            n += 1
    
    def start(self):
        """Run the actual experiment. Waits until the time is eighter full hour or half hour, then starts the Caroussel (one Thread) and records the caroussels in an 
        never ending loop (Thread2) until the experiment is stopped via Keyboard interrupt"""
       
        #Make the folder-structure
        home = os.getcwd()
        try:
            os.mkdir('save_files/experiment/')
            os.chdir('save_files/experiment/')
        except:
            os.chdir('save_files/experiment/')
            
        #make Folder with the name of the Experiment 
        os.mkdir(f'{self.indata["id"]}/')
        os.chdir(f'{self.indata["id"]}/') 
        
        #Copy the experiment-settings into the folder
        shutil.copy('../../temp/exp_template.json','experiment_settings.json') 
        
        
        #Define the Threads
        motor_and_disc = Thread(target=self.start_motor_and_disc)
        camera = Thread(target=self.start_camera)
        
        #wait, until time is eighter at minute 30 or 00
        while (int(datetime.srftime(datetime.now()),"%M") not in [30,0]):
            sleep(1)   
        
        motor_and_disc.start()
        camera.start()
        
        print("Please keyboard-interrupt the programm")
        try:
            #Now wait for keyboardInterrupt
            while True:
                sleep(1)
        except:
            motor_and_disc.running = False
            camera.running = False
            print("Ending the current filming-cycle. Please wait for the camera to end")
            
            motor_and_disc.join()
            camera.running.join()
            
        finally:
            os.chdir(home) # Go back to original script-directory

    #4. Archive the experiment
    def archive_experiment(self):
        """open THE archive-file and save the Experiment data (the logging)"""
        
        archive = open(f'save_files/ExperimentArchive.csv', 'a')
        with open(f'save_files/temp/temp_{experiment_ID}_log.json','r') as json_file:
            logging = (json.load(json_file))
            writer = csv.writer(archive)
        
            archive_data = [experiment_ID, 
                                logging['date'], 
                                logging['time'],
                                logging['rig'],
                                logging['temperature'],
                                logging['humidity'],
                                logging['circRhytm'],
                                logging['video_length'],
                                logging['FPS'],
                                logging['food'],
                                logging['sex'],
                                logging['genotype'],
                                logging['age'],
                                logging['motor1_direction'],
                                logging['motor2_direction'],
                                logging['motor_switchtime'],
                                logging['disc1_pos'],
                                logging['disc2_pos'],
                                logging['comment'],
                                logging['status']]
                
            writer.writerows(archive_data)
            archive.close()
            #TODO: delete temp-file
            
    def shutdown(self):
        #TODO: Stop everything, crons ended etc.
        self.caroussel.stop_motor()
        self.caroussel.camera.stop_preview()
        self.caroussel.camera_close()
        self.caroussel.shut_light()
        self.caroussel.GPIO.cleanup()
    
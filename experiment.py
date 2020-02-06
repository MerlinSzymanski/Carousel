from caroussel import Caroussel
import csv
from datetime import datetime
import json
import os
import shutil
import time
from io import BytesIO
import threading
from threading import Thread
import glob
from tqdm import tqdm #for fancy progress-bars

class Experiment():
    """This class stores everything necessary for the experiment. It contains an instance of the Caroussel, the 
    start-method for the experiment and creates the archive. The necessary data comes from an input_file. Pure informational
    data is not implemented (e.g. rig-number or genotype) but later saved directly into the archive"""
    def __init__(self, infile):
        
        #All the data used only for the archive
        with open(infile,'r') as json_file:
            self.indata = (json.load(json_file))
            
        self.indata['date'] = time.strftime("%y%m%d")
        self.indata['time'] = time.strftime("%H%M%S")
        self.indata['id'] = 'CARO_{}{}_{}_{}_{}_{}'.format(self.indata["date"],self.indata["time"],self.indata["rig"],self.indata["sex"],self.indata["genotype"],self.indata["age"])

        with open('save_files/temp/exp_settings.json','w') as temp:
            json.dump(self.indata, temp, indent=2) #create temp-file for the later experiment-folder
               
        self.indata['status'] = "Experiment set up, but not started"
        self.terminal_size = shutil.get_terminal_size((80,20))[0]
        #the GPIO - instance
        self.caroussel = Caroussel(self.indata)
        
        #some stats to print at the end
        self.begin = datetime.fromtimestamp(time.time())
        self.end = 0
        self.videos = 0
    
    #1. Start the CronJob
    def cron(self):
        """starts a python CRON-job in the Main before the experiment even begins Motor and light are therefor independend
        of the beginning of the experiment"""
        t = threading.current_thread()   #used to quit the cron-job later
        t.running = True
        
        #1.1 Start the motors 
        self.caroussel.start_motor()
        
        #1.2.regulate the light according to the CircRhythm
        with open('files/circRhythm.json','r') as circ_file:
            settings = (json.load(circ_file))
            for setting in settings:
                if(self.indata['circRhythm'] in setting):
                    circ = setting[self.indata['circRhythm']]
                    
            start_time_white = int(circ['white'])   #z.B. '6'
            start_time_red = int(circ['red'])       #z.B. '22'
        
            while True:
                #Escape the thread, if necessary
                if(t.running == False):
                    break
                
                #Get the current hour
                current_hour = int(time.strftime("%H"))
                #Check if time is between 6 and 22 --> make white light, else red
                if (start_time_white <= current_hour and current_hour < start_time_red):

                    #calculate the remaining seconds:
                    self.caroussel.set_daylight()

                    temp1 = time.strftime("%y%m%d")
                    temp2 = str(start_time_red)+":00:00"
                    timedelta = datetime.strptime('{},{}'.format(temp1,temp2),'%y%m%d,%H:%M:%S') - datetime.now()
                    
                    #print barplot to position 1 showing time until light change
                    pibar = tqdm(range(timedelta.seconds),position = 2, ascii = True, desc = "Current Light: Daylight(White)")
                    for i in pibar:   
                        time.sleep(1)
                        if(t.running == False):
                            break
                else:
                    #calculate the remaining seconds:
                    self.caroussel.set_nightlight()
                    temp1 = time.strftime("%y%m%d")
                    temp2 = str(start_time_white)+":00:00"
                    timedelta = datetime.strptime('{},{}'.format(temp1,temp2),'%y%m%d,%H:%M:%S') - datetime.now()
                    
                    #print a nice barplot to stdout while waiting for light-change
                    pibar = tqdm(range(timedelta.seconds), position = 1, ascii = True, desc = "Current Light: Nightlight(Red)")
                    for i in pibar:
                        time.sleep(1)
                        if(t.running == False):
                            break
        return 1
        
    def start_motor_and_disc(self):
        t = threading.current_thread()
        t.breaking = False
        
        #NO DISC FUNCTION: NAME IS FOR HISTORICAL REASONS
        #Get the motor_direction. it starts with motor1 and changes to motor2
        #after the switch-time. and so on and so forth.
        
        direction1 = self.indata['motor1_direction']
        direction2 = self.indata['motor2_direction'] 
        switch_time = int(self.indata['motor_switchtime'])*60 #we need the time in seconds
        
        while True: #Since this thread runs shorter than the camera, it cant end after this loop
            #To really end the thread -->wait for the camera to finish and break this thread
            if(t.breaking):
                break
            
            #fancy progress bar, showing the spin-direction 
            bar = tqdm(range(switch_time), position = 3, ascii = True, desc = "Motor 1, Spindirection: {}".format(direction1)) 
            self.caroussel.turn_motor1(direction1) #let the motor1 turn
            for i in bar:   
                time.sleep(1) 
                if(t.breaking): #to end the thread
                    break
                
            #Overwrite bar at position 2
            bar = tqdm(range(switch_time), position = 3, ascii = True, desc = "Motor 2, Spindirection: {}".format(direction2))
            self.caroussel.turn_motor2(direction2) #let the motor2 turn 
            for i in bar:
                time.sleep(1)  
                if(t.breaking): #to end the thread
                    break
        return 1 #Necessary for the joining of the threads
        
    def start_camera(self):
        #Thread-related stuff ... to remote-stop the process
        t = threading.current_thread() 
        t.breaking = False #for the hard experiment ending
        
        #Get the Data from the Infile
        self.caroussel.camera.framerate = float(self.indata['FPS'])
        self.caroussel.camera.start_preview()
        pause_time = int(int(self.indata["video_length"])/int(self.indata["FPS"]))   #still only FPS :/
        n = 1
        
        while getattr(t,"running",True): #run_again for the soft experiment ending
            #Check, if Thread is still supposed to run
            if(t.breaking == True):
                break
            
            #Yes: create stream
            stream = BytesIO()
            video_name = '{}_L_{:03d}.h264'.format(self.indata["id"],n)   
            #start recording to the stream
            self.caroussel.camera.start_recording(stream, format='h264', resize = (768,768))
            #TODO: Change that to Frames, not seconds! --> not possible with piCamera
            
            #Set up progress-bar for the Camera-videos
            bar = tqdm(range(pause_time), position = 4, ascii = True, desc="Camera, taking video Nr. {0:03}".format(n))
            for i in bar:
                self.caroussel.camera.wait_recording(1)
                if(t.breaking == True): #Check every second, if thread should be running
                    break
            
            self.caroussel.camera.stop_recording()
            with open (video_name,'wb') as f:
                # "Rewind" the stream to the beginning so we can flush its content to the file
                stream.seek (0)
                shutil.copyfileobj (stream,f)
                stream.close()
                
            time.sleep(0.05)
            n += 1
        return 1 #Necessary for the joining of the threads
        
    def start(self):
        """Run the actual experiment. Waits until the time is eighter full hour or half hour, then starts the Caroussel (one Thread) and records the caroussels in an 
        never ending loop (Thread2) until the experiment is stopped via Keyboard interrupt"""
        time.sleep(2) #to not conflict with the cronjob at the start
        tqdm.write("-"*self.terminal_size)
        tqdm.write("1. Initiation of the Experiment. Starting Light and Motor")
        #Make the folder-structure
        try:
            os.mkdir('save_files/experiment/')
            os.chdir('save_files/experiment/')
        except:
            os.chdir('save_files/experiment/')
            
        #make Folder with the name of the Experiment 
        os.mkdir('{}/'.format(self.indata["id"]))
        os.chdir('{}/'.format(self.indata["id"])) 
        
        #Copy the experiment-settings into the folder
        shutil.copy('../../temp/exp_settings.json','experiment_settings.json') 
        
        #Define the Threads
        motor_and_disc = Thread(target=self.start_motor_and_disc)
        camera = Thread(target=self.start_camera)
        
        #Get timedelta to next Experiment-start (eighter 30:00 or 00:00)
        """
        if(int(time.strftime("%M")) < 30):
            temp1 = time.strftime("%y%m%d, %H")
            time_to_wait = datetime.strptime('{}:30'.format(temp1),'%y%m%d, %H:%M:%S') - datetime.now()
        else:
            #one-liner for the better readability... just get the timedate object for one hour in the future... 
            temp1 = time.strftime("%y%m%d, %H:%M:%S").replace(time.strftime("%H"),str((int(time.strftime("%H"))+1)%24))
            one_hour_later = datetime.strptime('{}'.format(temp1),"%y%m%d, %H:%M:%S")
            temp2 = one_hour_later.strftime("%y%m%d, %H")+":00:00"
            time_to_wait = datetime.strptime('{}'.format(temp2),'%y%m%d, %H:%M:%S') - datetime.now()
        
        #wait, until time is eighter at minute 30 or 00 --> show as progress bar
        tqdm.write("-"*self.terminal_size)
        tqdm.write(" "*self.terminal_size)
        tqdm.write("2. Please wait. The experiments starts at the next full half hour (30:00 or 00:00)")
        bar = tqdm(range(time_to_wait.seconds),position=1, ascii = True, desc="Time until Experiment starts")
        for i in bar:
            time.sleep(1)
        
        #update status-message
        tqdm.write("-"*self.terminal_size)
        tqdm.write(" "*self.terminal_size)
        tqdm.write("3. Experiment runs: Please press Ctr-c to end the Experiment")
        """
        #start the child-threads
        motor_and_disc.start()
        camera.start()
        time.sleep(0.1) #wait for the progress-bars to start
        
        try:
            #Now wait for first (soft) keyboardInterrupt
            while True:
                time.sleep(1)
        except:
            #end the running child-threads
            camera.running = False
            #Wait for second (hard) Keyboard interrupt
            try:
                for i in range(2):
                    tqdm.write("-"*self.terminal_size)
                tqdm.write("4. The Experiment ends after the current camera-cycle is done. Press Ctr-c for instant stop of experiment")
                bar = tqdm(range(30),position = 1, ascii = True, desc = "Press Ctr-c now")
                for i in bar:
                    time.sleep(1)
            except:
               camera.breaking = True

            #wait for the threads to join()
            camera.join()
            motor_and_disc.breaking = True
            motor_and_disc.join()
            
        finally:
            #update status
            if(len(glob.glob("*.h264")) > 1):
                self.videos = len(glob.glob("*.h264"))
                self.indata['status'] = 'Experiment finished {} with {} clips'.format(time.strftime("%d.%m.%y_%H:%M"),str(self.videos))
            else:
                self.indata["status"] = "Experiment startet - but no clips produced"
            return 1

    #4. Archive the experiment
    def archive_experiment(self):
        """open THE archive-file and save the Experiment data"""
        
        archive = open('save_files/ExperimentArchive.tsv', 'a')
        writer = csv.writer(archive, delimiter='\t')
        
        archive_data = [self.indata['id'], 
                        self.indata['date'], 
                        self.indata['time'],
                        self.indata['rig'],
                        self.indata['temperature'],
                        self.indata['humidity'],
                        self.indata['circRhythm'],
                        self.indata['video_length'],
                        self.indata['FPS'],
                        self.indata['food'],
                        self.indata['sex'],
                        self.indata['genotype'],
                        self.indata['age'],
                        self.indata['motor1_direction'],
                        self.indata['motor2_direction'],
                        self.indata['motor_switchtime'],
                        self.indata['disc1_pos'],
                        self.indata['disc2_pos'],
                        self.indata['comment'],
                        self.indata['status']]
                
        writer.writerow(archive_data)
        archive.close()
        
    def print_end_statistics(self):
        self.end = datetime.fromtimestamp(time.time())
        self.runtime = str(self.end - self.begin).split(':')
        
        time.sleep(2) #waiting for the bars 
        #Now some pretty formatting
        for i in range(6):
            print("")
        for i in range(2):
            print("#"*self.terminal_size)
        print(" "*self.terminal_size)

        for thread in ["Light","Camera","Motor"]:
            print("Thread: {} - terminated".format(thread))
        
        print('Experiment {} finished'.format(self.indata["id"]))
        print('The Experiment ran for {} hours, {} minutes and {} seconds'.format(self.runtime[0],self.runtime[1],self.runtime[2]))
        print('{} clips were produced'.format(self.videos))
        print("")
        for i in range(2):
            print("#"*self.terminal_size)
        
    
    def shutdown(self):
        self.caroussel.stop_motors()
        self.caroussel.shut_light()
        self.caroussel.cleanup()        
        self.print_end_statistics()
        self.caroussel.camera.stop_preview()
        self.caroussel.camera.close()



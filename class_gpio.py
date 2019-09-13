from picamera import PiCamera
from io import BytesIO
import RPi.GPIO as GPIO
import json
    
class Caroussel():
    """Here is saved everything related to the Raspberry and the mechanical data. Also the methods for running the camera, the motor etc.
    get settings for the strings from other json files (e.g. what means the circRhythm)"""
    
    def __init__(self, infile):
        indata = (json.load(infile))
        
        #metadata --> Maybe from the device itself?
        self.id = 1
        self.device = '1'
        
        self.CircRhythm = indata["circRhytm"]     #string selected from list 'rhythm'
        
        #Motors
        self.Motor1_direction = indata["motor_direction"]    #str: cw; ccw //clockwise and counterclockwise
        self.Motor2_direction = indata["motor2_direction"]   #str: same, different
        self.Switch_time = indata["motor_switchtime"]        #int: default=5  #Umschalt-Zeit zwischen Kupplungen (min); nur ein Motor drehen, aber immer beide an 
        
        #Disk position --> tiefergelegtes Karussell oder ebenerdig
        self.DiskPosition1 = indata["disc1_pos"]      #float: 0; -1.5 default=0                   
        self.DiskPosition2 = indata["disc2_pos"]      #float: 0; -1.5 default=0                   
        
        #camera
        self.camera_model = "PiCameraIR"
        self.camera = self.set_camera()
        self.camera.framerate = indata['FPS']         #FPS --> int: default=5
        self.Videolength = indata['video_lenghts']     #default = 9000 (frames)
    
        

        
        
        '''New GPIO:
            3 = magnet1
            4 = magnet2
            17 = LED blau
            27 = LED weiß
            22 = LED IR
            18 = motor1 links rechts
            23 = motor2 links rechts
            24 = speed motor1
            25 = speed motor2
            '''
        
        # Use board pin numbering
        GPIO.setmode(GPIO.BOARD)
        #You need to set up every channel you are using as an input or an output.
        #To configure a channel as an input
        
        GPIO.setup(22, GPIO.OUT)    ## Setup redLED
        GPIO.setup(27, GPIO.OUT)    ## Setup whiteLED
        GPIO.setup(17, GPIO.OUT)    ## Setup blueLED
        GPIO.setup(24, GPIO.OUT)    ## Setup Motor1 Speed
        GPIO.setup(25, GPIO.OUT)    ## Setup Motor2 Speed
        GPIO.setup(18, GPIO.OUT)    ## Setup Motor1 Direction
        GPIO.setup(23, GPIO.OUT)    ## Setup Motor2 Direction  
        GPIO.setup(3, GPIO.OUT)     ## Setup Magnet1 
        GPIO.setup(4, GPIO.OUT)     ## Setup Magnet2 
     
        
    def set_camera(self):
            #Maybe move these settings to a file?
        camera = PiCamera()
        camera.resolution = (1296, 972)
        camera.zoom = (0.2,0.1,0.59,0.79)   #Wo kommen die Zahlen her?
        camera.hflip = True
        camera.vflip = True
        camera.exposure_mode = 'auto'
        return camera

    
    def set_light(self,circRythm):
        light = self.settings[circRythm]
        #check according to the rhythm
        self.IR = False                     #off
        self.IR_Intensity = 0.00            #in [%]
        self.White_OnOff = False
        self.White_Intensity = 0.00
        #switch the light if time is right --> always check 
        #before the the new recording session
        
        #red  = GPIO.PWM(22, 100) #set the PWM on port X at 100 Hertz
        #white = GPIO.PWM(27, 100)
        #red.start(100)         # redLED starts off
        #white.start(100)         # whiteLED start on
        
    def switch_light(self,color):
        if(color == 'red'):
            self.IR_OnOff = bool(-1*int(self.IR_OnOff))
        else:
            self.White_OnOff = bool(-1*int(self.White_OnOff))
            
    def switch_motor_direction(self, number):
        if(number == '1'):
            self.Motor2_OnOff = bool(-1*int(self.Motor_OnOff)) 
        else:
            self.Motor2_OnOff = bool(-1*int(self.Motor2_OnOff))
    
    
    def start_motor(self):
    #part of the cronjob started in main
        GPIO.output([18,22],True)  #starts channels 18, 22

    
    def start_recording(self,pause_time):#--> what does pause_time mean?? #oscillation rate in sec (length per video)
        #just copy-pastefrom old script --> check the docs
        while True: #--> break with KeyboardInterrupt... not quite the best style
            stream = io.BytesIO()
            current_date = (time.strftime("%y%m%d"))
            current_time = (time.strftime("%H%M%S"))
            automatic_name = "".join((setupname,"_",rigname,"_",current_date,"_",current_time,"_",exp_name,"_L_", "{0:03d}".format(val), ".h264"))            
            camera.start_recording(stream, format='h264', resize = (px,px))
            camera.wait_recording(pause_time)
            camera.stop_recording()
        
            with open (automatic_name,'w') as f:
                stream.seek (0)
                shutil.copyfileobj (stream,f)
                stream.close()
            time.sleep(0.05)

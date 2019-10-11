from picamera import PiCamera
from io import BytesIO
import RPi.GPIO as GPIO
    
class Caroussel():
    """Here is saved every method related to the Raspberry and the GPIO. Therefor the methods for running the camera, the motor etc.
    The schedule is saved in the experiment-class"""
    
    def __init__(self, indata):  
        #camera
        self.indata = indata
        self.camera_model = "PiCameraIR"
        self.camera = self.set_camera()
        self.videolength = indata['video_lenghts']     #default = 9000 (frames)
    
        #Light
        self.redlight = False
        self.whitelight = False
        
        #TODO: GPIO: maybe shift outside the class? Test with the real Raspian

        # Use board pin numbering
        GPIO.setmode(GPIO.BOARD)
        #You need to set up every channel you are using as an input or an output.
        #To configure a channel as an input
        
        GPIO.setup(22, GPIO.OUT)    ## Setup redLED
        GPIO.setup(27, GPIO.OUT)    ## Setup whiteLED
        GPIO.setup(24, GPIO.OUT)    ## Setup Motor1 Speed
        GPIO.setup(25, GPIO.OUT)    ## Setup Motor2 Speed
        GPIO.setup(18, GPIO.OUT)    ## Setup Motor1 Direction
        GPIO.setup(23, GPIO.OUT)    ## Setup Motor2 Direction  
        GPIO.setup(3, GPIO.OUT)     ## Setup Magnet1 
        GPIO.setup(4, GPIO.OUT)     ## Setup Magnet2 
        """I dont know yet what is responsible for what... Magnet just for discPosition? 
        i thought there is a way of starting the motors without movements? But i think I have to test it directly
        on the Raspberry"""
        #discposition
        self.disc1pos = 0
        self.disc2pos = 0
        
    def set_camera(self):
        camera = PiCamera()
        camera.resolution = (1296, 972)
        camera.zoom = (0.2,0.1,0.59,0.79)   #Wo kommen die Zahlen her?
        camera.hflip = True
        camera.vflip = True
        camera.exposure_mode = 'auto'
        camera.framerate = self.indata['FPS']
        return camera
    
    def start_motor(self):
    #part of the cronjob started in main -> experiment.cron()
        GPIO.output([24,25],True)   #starts channels 24,25 (motors)
        GPIO.output([3,4],True)     #starts the magnets (caroussels dont move) 

    def set_nightlight(self):
    #part of the cronjob started in main -> experiment.cron()
        if(self.redlight == False):
            GPIO.output(27,GPIO.LOW)    #white off
            GPIO.output(22,GPIO.HIGH)   #red on
            self.whitelight = False
            self.redlight = True

    def set_daylight(self):
    #part of the cronjob started in main -> experiment.cron()
        if(self.whitelight == False):
            GPIO.output(27,GPIO.HIGH)   #white on
            GPIO.output(22,GPIO.LOW)    #red off
            self.redlight = False
            self.whitelight = True

    def set_disc_position(self,number,position):
        #Set the disc-number to the corresponding position
        if(number == 1):
            if(position < 0 and self.disc1pos == 0):
                GPIO.output(3, GPIO.HIGH)   #Magnet on - lower disc?
                self.disc1pos = -1
            elif(position == 0 and self.disc1pos < 0):
                GPIO.output(3, GPIO.LOW)   #Magnet off - higher disc?
                self.disc1pos = 0
        if(number == 2):
            if(position < 0 and self.disc2pos == 0):
                GPIO.output(4, GPIO.HIGH)   #Magnet on - lower disc?
                self.disc1pos = -1
            elif(position == 0 and self.disc2pos < 0):
                GPIO.output(4, GPIO.LOW)   #Magnet off - higher disc?
                self.disc1pos = 0                
        
####NOT FULLY IMPLEMENTED BELOW####
    def turn_motor_cw(self,motor): #which motor to turn, True = cw, False = ccw
        #Turn Motor clockwise
        #Checkm that other Motor stands still
        
    def turn_motor_ccw(self,motor):
        #Turn motor ccw
        #check, that other motor stands still

    

    
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

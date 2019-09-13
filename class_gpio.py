from picamera import PiCamera
from io import BytesIO
import RPi.GPIO as GPIO
    
class Caroussel():
    """Here is saved every method related to the Raspberry and the GPIO. Therefor the methods for running the camera, the motor etc.
    The schedule is saved in the experiment-class"""
    
    def __init__(self, indata):  
        
        #Motors
        self.motor1_direction = indata["motor1_direction"]    #str: cw; ccw //clockwise and counterclockwise
        self.motor2_direction = indata["motor2_direction"]   #str: same, different
        self.switch_time = indata["motor_switchtime"]        #int: default=5  #Umschalt-Zeit zwischen Kupplungen (min); nur ein Motor drehen, aber immer beide an 
        
        #Disk position --> tiefergelegtes Karussell oder ebenerdig
        self.diskPosition1 = indata["disc1_pos"]      #float: 0; -1.5 default=0                   
        self.diskPosition2 = indata["disc2_pos"]      #float: 0; -1.5 default=0                   
        
        #camera
        self.camera_model = "PiCameraIR"
        self.camera = self.set_camera()
        self.camera.framerate = indata['FPS']         #FPS --> int: default=5
        self.videolength = indata['video_lenghts']     #default = 9000 (frames)
    
        #TODO: GPIO: maybe shift outside the class? Test with the real Raspian
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
        camera = PiCamera()
        camera.resolution = (1296, 972)
        camera.zoom = (0.2,0.1,0.59,0.79)   #Wo kommen die Zahlen her?
        camera.hflip = True
        camera.vflip = True
        camera.exposure_mode = 'auto'
        return camera
    
    def start_motor(self):
    #part of the cronjob started in main -> experiment.cron()
        GPIO.output([24,25],True)  #starts channels 24,25 (motors)    

    def set_nightlight(self):
    #part of the cronjob started in main -> experiment.cron()
        GPIO.output(27,GPIO.LOW)    #white off
        GPIO.output(22,GPIO.HIGH)   #red on

    def set_daylight(self):
        GPIO.output(27,GPIO.HIGH)   #white on
        GPIO.output(22,GPIO.LOW)    #red off

        
####NOT FULLY IMPLEMENTED BELOW####




    
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

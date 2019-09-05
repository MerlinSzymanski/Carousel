from picamera import PiCamera
import RPi.GPIO as GPIO

class Caroussel():
    """Here is saved everything related to the Raspberry and the mechanical data. Also the methods for running the camera, the motor etc."""
    def __init__(self, items):
        #TODO: define here the default values --> to initialize the Caroussel-settings via the Experiment (with *data) ~ setting
        
        #metadata
        self.id
        self.device
        
        #light: off on initialisation
        self.IR = False                     #off
        self.IR_Intensity = 0.00            #in [%]
        self.White_OnOff = False
        self.White_Intensity = 0.00
        
        #Motor --> How both motors work
        self.Motor1_On = False           #Bool: 1,0
        self.Motor_Intensity = 0            #the speed of the motor
        self.Motor1_direction = items[1]    #str: cw; ccw //clockwise and counterclockwise
        
        self.Motor2_On = False
        self.Motor2_Intensity = 0           
        self.Motor2_direction = items[2]    #str: same, different
        self.Switch_time = 5                #int: default=5
            #Umschalt-Zeit zwischen Kupplungen (min); nur ein Motor drehen, aber immer beide an 
            
        #Disk position --> tiefergelegtes Karussell oder ebenerdig
        self.DiskPosition1 = 0              #float: 0; -1.3 [mm] default=0                   
        self.DiskPosition2 = 0              #float: 0; -1.3 [mm] default=0                   
        
        #sound
        self.Sound = items[3]
        
        #camera
        #--> CameraModel (Constant) PiCameraIR
        #TODO: move this to a method
        self.camera = PiCamera()
        x,y = (1296, 972)
        self.camera.resolution = (x, y)
        px = 768
        xb = (x/2.0 - px/2) / x
        yb = (y/2.0 - px/2) / y
        self.camera.zoom = (xb,yb,px/float(x),px/float(y))
        self.camera.framerate = 5    #FPS --> int: default=5
        self.camera.hflip = True
        self.camera.vflip = True
        self.camera.exposure_mode = 'auto'
        self.camera.start_preview(alpha=250, fullscreen=False, window=(10, 400, 494, 784))
        
        self.Videolength = items[7]     #default = 9000 (frames)
        
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
        
        #TODO: read into GPIO
        #GPIO
        GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
        
        GPIO.setup(22, GPIO.OUT) ## Setup redLED
        GPIO.setup(27, GPIO.OUT) ## Setup whiteLED
        GPIO.setup(17, GPIO.OUT) ## Setup blueLED
        
        GPIO.setup(24, GPIO.OUT) ## Setup Motor1 Speed
        GPIO.setup(25, GPIO.OUT) ## Setup Motor2 Speed
        
        GPIO.setup(18, GPIO.OUT) ## Setup Motor1 Direction
        GPIO.setup(23, GPIO.OUT) ## Setup Motor2 Direction
            #GPIO.output(18,GPIO.LOW)   # Motor turns right
        
        GPIO.setup(3, GPIO.OUT) ## Setup Magnet1 
        GPIO.setup(4, GPIO.OUT) ## Setup Magnet2 


        #red   = GPIO.PWM(15, 100) #set the PWM on port X at 100 Hertz
        #motor = GPIO.PWM(18, 100)
        #white = GPIO.PWM(13, 100)
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
    
    def start_motor(self, motorspeed):
        None
        #Todo: Implement
        #motorspeed == motorintensity
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

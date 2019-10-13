from picamera import PiCamera
import RPi.GPIO as GPIO

  
class Caroussel():
    """Here is saved every method related to the Raspberry and the GPIO. Therefor the methods for running the camera, the motor etc.
    The schedule is saved in the experiment-class"""
    
    def __init__(self, indata):  
        #camera
        self.indata = indata
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
        #motor
        self.motor1dir = True #True = cw, False = ccw
        
        
    def set_camera(self):
        #Data comes from the old script
        camera = PiCamera()
        x,y = (1296, 972)
        camera.resolution = (x, y)
        px = 768
        xb = (x/2.0 - px/2) / x
        yb = (y/2.0 - px/2) / y
        camera.zoom = (xb,yb,px/float(x),px/float(y))
        camera.hflip = True
        camera.vflip = True
        camera.exposure_mode = 'auto'
        camera.framerate = float(self.indata['FPS'])
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

    def shut_light(self):
        if(self.whitelight == True):
            GPIO.output(27,GPIO.LOW)    #white off
        if(self.redlight == True):
            GPIO.output(22,GPIO.LOW)
        
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
        
    def stop_turning_motor2(self):
        #TODO: How to stop turning, without stopping the motor?
        GPIO.output(23, GPIO.LOW)   #Motor2 out?  
        
    def stop_turning_motor1(self):
        GPIO.output(18, GPIO.LOW)   #Motor1 out?               
                
                
    def turn_motor1(self,direction1):
        self.stop_turning_motor2()
        if(direction1 == 'cw'):
            GPIO.output(18, GPIO.HIGH)  #Motor1 clockwise?
            self.motor1dir = True
        elif(direction1 == 'ccw'):
            GPIO.output(18, GPIO.LOW)   #Motor1 counterclockwise?
            self.motor1dir = False
               
    def turn_motor2(self,direction2):
        self.stop_turning_motor1()
        if(direction2 == 'same' and self.motor1dir):
            GPIO.output(23, GPIO.HIGH)  #Motor2 clockwise?
        elif(direction2 == 'same' and not self.motor1dir):
            GPIO.output(23, GPIO.LOW)  #Motor2 counterclockwise?
        elif(direction2 == 'different' and self.motor1dir):
            GPIO.output(23, GPIO.LOW)  #Motor2 counterclockwise?        
        elif(direction2 == 'different' and not self.motor1dir):
            GPIO.output(23, GPIO.HIGH)  #Motor2 clockwise?        

from picamera import PiCamera
import RPi.GPIO as GPIO

  
class Caroussel():
    """Here is saved every method related to the Raspberry and the GPIO. Therefor the methods for running the camera, the motor etc.
    The schedule is saved in the experiment-class"""
    
    def __init__(self, indata):  
        #camera
        self.camera = self.set_camera()
    
        #Light
        self.redlight = False
        self.whitelight = False
        
        #TODO: GPIO outside the class?
        # Use board pin numberingc
        GPIO.setmode(GPIO.BCM)
        #You need to set up every channel you are using as an input or an output.
        #To configure a channel as an input
        
        GPIO.setup(27, GPIO.OUT)    ## Setup redLED --> GPIO.output(27,False) = White LED on
        GPIO.setup(22, GPIO.OUT)    ## Setup whiteLED --> GPIO.output(22,False) = Red LED on
        GPIO.setup(24, GPIO.OUT)    ## Setup Motor1 Speed --> GPIO.output(24,True) = motor1 turns
        GPIO.setup(25, GPIO.OUT)    ## Setup Motor2 Speed --> GPIO.output(25,True) = motor2 turns
        GPIO.setup(18, GPIO.OUT)    ## Setup Motor1 Direction --> GPIO.output(18,True) = ccw
        GPIO.setup(23, GPIO.OUT)    ## Setup Motor2 Direction  --> GPIO.output(23,True) = ccw
        GPIO.setup(3, GPIO.OUT)     ## Setup Magnet1 --> GPIO.output(3,True) = if(motor1): disc1 turns
        GPIO.setup(4, GPIO.OUT)     ## Setup Magnet2 --> GPIO.output(4,True) = if(motor2): disc2 turns

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
        return camera
    
    def start_motor(self):
    #TODO: start the motor without turning the discs?
    #part of the cronjob started in main -> experiment.cron()
        GPIO.output([3,4],False)     #Set the magnets,so that the caroussels don't move
        GPIO.output([24,25],True)   #starts channels 24,25 (motors)

    def stop_motors(self):
        GPIO.output([24,25],False)
        GPIO.output([3,4],False)

    def set_nightlight(self):
    #part of the cronjob started in main -> experiment.cron()
        if(self.redlight == False):
            GPIO.output(27,True)    #white off
            GPIO.output(22,False)   #red on
            self.whitelight = False
            self.redlight = True

    def set_daylight(self):
    #part of the cronjob started in main -> experiment.cron()
        if(self.whitelight == False):
            GPIO.output(27,False)   #white on
            GPIO.output(22,True)    #red off
            self.redlight = False
            self.whitelight = True

    def shut_light(self):
            GPIO.output([22,27],True)    #white off           
        
    def stop_turning_motor2(self):
        GPIO.output(23, False)   #Motor2 out?
        GPIO.output(4,False)
        
    def stop_turning_motor1(self):
        GPIO.output(18, False)   #Motor1 out?
        GPIO.output(3,False)
                
                
    def turn_motor1(self,direction1):
        self.stop_turning_motor2()
        GPIO.output(3,True)
        if(direction1 == 'cw'):
            GPIO.output(18, False)  #Motor1 clockwise?
            self.motor1dir = True
        elif(direction1 == 'ccw'):
            GPIO.output(18, True)   #Motor1 counterclockwise?
            self.motor1dir = False
               
    def turn_motor2(self,direction2):
        self.stop_turning_motor1()
        GPIO.output(4,True)
        if(direction2 == 'same' and self.motor1dir):
            GPIO.output(23, False)  #Motor2 clockwise?
        elif(direction2 == 'same' and not self.motor1dir):
            GPIO.output(23, True)  #Motor2 counterclockwise?
        elif(direction2 == 'different' and self.motor1dir):
            GPIO.output(23, True)  #Motor2 counterclockwise?        
        elif(direction2 == 'different' and not self.motor1dir):
            GPIO.output(23, False)  #Motor2 clockwise?  

    def cleanup(self):
        GPIO.output(27, False)    ## Setup redLED --> GPIO.output(27,False) = White LED on
        GPIO.output(22, False)    ## Setup whiteLED --> GPIO.output(22,False) = Red LED on
        GPIO.output(24, False)    ## Setup Motor1 Speed --> GPIO.output(24,True) = motor1 turns
        GPIO.output(25, False)    ## Setup Motor2 Speed --> GPIO.output(25,True) = motor2 turns
        GPIO.output(3, False)     ## Setup Magnet1 --> GPIO.output(3,True) = if(motor1): disc1 turns
        GPIO.output(4, False)   
        GPIO.cleanup()      

from picamera import PiCamera
import RPi.GPIO as GPIO

  
class Caroussel():
    """Here is saved every method related to the Raspberry and the GPIO. Therefor the methods for running the camera, the motor etc.
    The schedule is saved in the experiment-class"""
    
    def __init__(self, indata):
        #Set pins as global_parameter
        pin_whitelight = 27
        pin_redlight = 22
        pin_motor1 = 24
        pin_motor2 = 25
        pin_motor1_dir = 18
        pin_motor2_dir = 23
        pin_clunch1 = 3
        pin_clunch2 = 4
  
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
        
        GPIO.setup(pin_whitelight, GPIO.OUT)    ## Setup redLED --> GPIO.output(27,False) = White LED on
        GPIO.setup(pin_redlight, GPIO.OUT)    ## Setup whiteLED --> GPIO.output(22,False) = Red LED on
        GPIO.setup(pin_motor1, GPIO.OUT)    ## Setup Motor1 Speed --> GPIO.output(24,True) = motor1 turns
        GPIO.setup(pin_motor2, GPIO.OUT)    ## Setup Motor2 Speed --> GPIO.output(25,True) = motor2 turns
        GPIO.setup(pin_motor1_dir, GPIO.OUT)    ## Setup Motor1 Direction --> GPIO.output(18,True) = ccw
        GPIO.setup(pin_motor2_dir, GPIO.OUT)    ## Setup Motor2 Direction  --> GPIO.output(23,True) = ccw
        GPIO.setup(pin_clunch1, GPIO.OUT)     ## Setup Magnet1 --> GPIO.output(3,True) = if(motor1): disc1 turns
        GPIO.setup(pin_clunch2, GPIO.OUT)     ## Setup Magnet2 --> GPIO.output(4,True) = if(motor2): disc2 turns

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
    #part of the cronjob started in main -> experiment.cron()
        GPIO.output([pin_clunch1,pin_clunch2],False)     #Set the magnets,so that the caroussels don't move
        GPIO.output([pin_motor1,pin_motor2],True)   #starts channels 24,25 (motors)

    def stop_motors(self):
        GPIO.output([pin_motor1,pin_motor2],False)
        GPIO.output([pin_clunch1,pin_clunch2],False)

    def set_nightlight(self):
    #part of the cronjob started in main -> experiment.cron()
        if(self.redlight == False):
            GPIO.output(pin_whitelight,True)    #white off
            GPIO.output(pin_redlight,False)   #red on
            self.whitelight = False
            self.redlight = True

    def set_daylight(self):
    #part of the cronjob started in main -> experiment.cron()
        if(self.whitelight == False):
            GPIO.output(pin_whitelight,False)   #white on
            GPIO.output(pin_redlight,True)    #red off
            self.redlight = False
            self.whitelight = True

    def shut_light(self):
            GPIO.output([pin_redlight,pin_whitelight],True)    #white off           
        
    def stop_turning_motor2(self):
        GPIO.output(pin_motor2_dir, False)   #Motor2 out?
        GPIO.output(pin_clunch2,False)
        
    def stop_turning_motor1(self):
        GPIO.output(pin_motor1_dir, False)   #Motor1 out?
        GPIO.output(pin_clunch1,False)
                          
    def turn_motor1(self,direction1):
        self.stop_turning_motor2()
        GPIO.output(pin_clunch1,True)
        if(direction1 == 'cw'):
            GPIO.output(pin_motor1_dir, False)  #Motor1 clockwise?
            self.motor1dir = True
        elif(direction1 == 'ccw'):
            GPIO.output(pin_motor1_dir, True)   #Motor1 counterclockwise?
            self.motor1dir = False
               
    def turn_motor2(self,direction2):
        self.stop_turning_motor1()
        GPIO.output(pin_clunch2,True)
        if(direction2 == 'same' and self.motor1dir):
            GPIO.output(pin_motor2_dir, False)  #Motor2 clockwise?
        elif(direction2 == 'same' and not self.motor1dir):
            GPIO.output(pin_motor2_dir, True)  #Motor2 counterclockwise?
        elif(direction2 == 'different' and self.motor1dir):
            GPIO.output(pin_motor2_dir, True)  #Motor2 counterclockwise?        
        elif(direction2 == 'different' and not self.motor1dir):
            GPIO.output(pin_motor2_dir, False)  #Motor2 clockwise?  

    def test_functions(self):
        print("#### Welcome to the Functionality-test-regime ####")
        print('Start the Camera')
	self.camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
	time.sleep(2)
        print("### Testing the Light ###")
        print('Red Light')
	self.set_nightlight() 
        time.sleep(5)
        print('White Light') 
        self.set_daylight()  
        print("### Testing the Motors ###")
	self.start_motor() 
        print('Motor 1 - cw')
        self.turn_motor1("cw")
        time.sleep(5)
        print('Motor 1 - ccw')
	self.turn_motor1("ccw")
        time.sleep(5)
        print('Motor 2 - cw')
        self.turn_motor2("cw")
        time.sleep(5)
        print('Motor 2 - ccw')
        self.turn_motor2("ccw")
        time.sleep(5)
        print('Motor 1 and 2 - cw/same')
        self.turn_motor1("cw")
        self.turn_motor2("cw")
        time.sleep(5)
        print('Motor 1 and 2 - cw/different')
        self.turn_motor1("cw")
        self.turn_motor2("ccw")
        time.sleep(5) 
        print('Motor 1 and 2 - ccw/same')
        self.turn_motor1("ccw")
        self.turn_motor2("ccw")
        time.sleep(5)
        print('Motor 1 and 2 - ccw/different')
        self.turn_motor1("ccw")
        self.turn_motor2("cw")
        time.sleep(5)
        print('### Stop Motors ###')
        self.stop_motors()
        print("Shut the Light")
	GPIO.output(pin_redlight, True)
        print("Stop the Camera")
	self.camera.stop_preview()
        self.camera.close()
        print("### End of the Test ###")
	self.cleanup()

    def cleanup(self):
        GPIO.output(pin_whitelight, True)    	# redLED off
        GPIO.output(pin_redlight, True)    	# whiteLED off
        GPIO.output(pin_motor1, False)    	# Motor1 off
        GPIO.output(pin_motor2, False)    	# Motor2 off
        GPIO.output(pin_clunch1, False)     	# Magnet 1 off
        GPIO.output(pin_clunch2, False)   	# Magnet 2 off		
        GPIO.cleanup()      

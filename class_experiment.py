from class_gpio import Caroussel
import json
import os
import shutil


class Experiment():
    """This class stores everything necessary for the experiment. It contains an instance of the Caroussel, the 
    start-method for the experiment and creates the archive. The necessary data comes from an input_file"""
	
    def __init__(self, infile):
        indata = (json.load(infile))
        
        #Environmental Data
        self.date = indata['date']          #yyyymmdd
        self.time = indata['time']          #hhmmss --> 24h   
        self.setup = indata['setup']        #what is the setup?
        self.rig = indata['rig']            #int with 2 digits --> 01,02 etc.
        
        #Metadata
        self.temperature = indata['temperature']        #float
        self.humidity = indata['humidity']              #float in [%]
        self.comment = indata['comment']                #Free text
        
        #Drosophila data        
        self.food = indata['food']                  #string selected from list 'food'
        self.sex  = indata['sex']                   #f, m default = m
        self.genotype = indata['genotype']          #string from list Genotype
        self.age = indata['age']                    #float: 0.2,0.6,1,

        #GPIO and Caroussel-Data
        caroussel_data = (indata['circRythm'])     #Here the regime to set up the caroussel
        self.caroussel = Caroussel(caroussel_data)
    
    def cron(self):
        """start a new python CRON-job over this method or make parallel methods... I have to decide later"""
        
        self.caroussel.start_motor()    #They have to run all the time
        while True:
            self.caroussel.check_light()    #check before every recording-session or cronjob
            #TODO:start the light
            #start the Motor and change the motor every {switchtime} minutes
        None
        
    def start(self):
        """Run experiment --> start the Caroussel and record the experiment in an 
        never ending loop"""
        
        #TODO: Maybe define a save-directory? 
        
        os.mkdir(f'CARO_{self.date}_experiment_testfolder/') #make Folder with the name of the Experiment 
        shutil.copy('template.json',f'CARO_{self.date}_experiment_testfolder/experiment_settings.json') #Copy the experiment-settings into the folder
        os.chdir(f'CARO_{self.date}_experiment_testfolder/') #change to this directory
        
        
        self.caroussel.camera.start_preview(alpha=250, fullscreen=False, window=(10, 400, 494, 784))
                
        while True:
            
        #Now record for 9000 frames  --> look at cronjobs if the time is right
        #red light from 6-22 and white light from 22-6.. start of recording eighter at 30 or 00 min
        
        
            if time_is_right:
                try:
                    self.caroussel.start_recording()
                except:
                    self.caroussel.stop_motor()
                    self.caroussel.camera.stop_preview()
                finally:
                        self.caroussel.GPIO.cleanup()
                            #change dir back to scrip directory
                        self.caroussel.camera_close()
        
    
    def save_experiment(self):
        return None
        '''Open THE database and save the settings (maybe a shelve-file?)'''
        '''
        #from the original script --> avoid global data
        archive_data =  [[time.strftime("%y/%m/%d"),time.strftime("%H:%M"),self.SetupVar.get(),self.RigName.get(),self.Temp.get(),self.Humid.get(),self.CircVar.get(),self.Length.get(),self.FPS.get(),self.SoundVar.get(),self.WaterVar.get(),self.FoodVar.get(),self.Male.get(),self.Female.get(),self.MaleGenVar.get(),
                     self.FemaleGenVar.get(),self.MaleModVar.get(),self.FemaleModVar.get(),self.MaleAgeDays.get(),self.FemaleAgeDays.get(),self.MaleAgeHours.get(),self.FemaleAgeHours.get(),self.MaleWaterStarv.get(),self.FemaleWaterStarv.get(),self.MaleFoodStarv.get(),self.FemaleFoodStarv.get(),
                     self.REDonoffvar.get(),self.REDIntensity.get(),self.WHITEonoffvar.get(),self.WHITEIntensity.get(),self.MOTORonoffvar.get(),self.MOTORIntensity.get(),self.Rotation.get(),Textbox]
                    ]
        global folderfile_data
        folderfile_data = [["date","time","Setup","Rig","Temp_degC","Humidity_perc","CircRhythm","Videolength_sec","FPS","Sound","Water","Food",
                    "Males","Females","Genotype_m","Genotype_f","Modification_m","Modification_f","Age_m_days","Age_f_days","Age_m_hours","Age_f_hours",
                    "WaterStarvation_m_hours","WaterStarvation_f_hours","FoodStarvation_m_hours","FoodStarvation_f_hours","IR_OnOff","IR_Intensity","White_OnOff","White_Intensity","Motor_OnOff","Motor_Intensity","Motor_direction","Add_Information"],
                    archive_data[0]]
        archive_csvfile = open('ExperimentArchive.csv', "a")
        writer = csv.writer(archive_csvfile)
        writer.writerows(archive_data)  '''
    
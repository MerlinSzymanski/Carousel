from class_gpio import Caroussel
import csv

class Experiment():
    """This class stores everything necessary for the experiment. It contains an instance of the Caroussel, the 
    start-method for the experiment and creates the archive. The necessary data should come from an input_file (for now-csv)"""
    #TODO: dont declare unused variables --> Pipe directly into the save_data method
	
    def __init__(self, infile):
        items = read_out_infile 
        
        #Environmental Data
        self.date = items[0]            #yyyymmdd
        self.time = items[1]            #hhmmss --> 24h   
        self.Setup = items[2]           #what is the setup?
        self.Rig = items[3]             #int with 2 digits --> 01,02 etc.
        self.Temperature = items[4]     #float
        self.Humidity = items[5]        #float in [%]

        self.CircRhythm = items[6]      #string selected from list 'rhythm'
        
        #Drosophila data        
        self.Water = items[10]
        self.Food = items[11]           #string selected from list 'food'
        self.Males = items[12]          #just "sex"? --> f, m default = m
        self.Females = items[13]
        self.Genotype_m = items[14]     #string from list Genotype
        self.Genotype_f = items[15]
        self.Modification_m = items[16]
        self.Modification_f = items[17]
        self.Age_m_days = items[18]     #float: 0.2,0.6,1,
        self.Age_f_days = items[19]
        self.Age_f_hours = items[20]
        self.Age_f_hours = items[21]
        self.WaterStarvation_m_hours = items[22]
        self.WaterStarvation_f_hours = items[23]
        self.FoodStarvation_m_hours = items[24]
        self.FoodStarvation_f_hours = items[25]
        
        #comment
        self.comment = items[26]    
    
        #GPIO and Caroussel-Data     
        caroussel_data = items[26:] #Here the regime to set up the caroussel
        self.caroussel = Caroussel(*caroussel_data)
        
        
    def start(self):
        """Run experiment --> start the GPIO and so on.."""
        #make Folder with the name of the Experiment 
        #change to this directory
        #make a 'Folderfile' --> Like a README with the necessary information?
        
        self.caroussel.start_motor()
        
        #Now record for 30 minutes... --> look at cronjobs if the time is right
        #red light from 6-22 and white light from 22-6.. start of recording eighter at 30 or 00 min
        if time_is_right:
            try:
                self.caroussel.start_recording()
            except:
                self.caroussel.motor_stop()
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
    
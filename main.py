from class_experiment import Experiment
from class_GUI import GUI
from threading import Thread
import argparse

def main():
    """This Main method is used to decide, if one wants to provide an input-file with all the necessary experiment-data
    or to open a GUI and type the data in manually"""
    
    #1. DECIDE WHICH INPUT-FORMAT TO CHOOSE
    args = get_arguments()
    
    if(args.gui):
        infile = get_data_from_gui()
        #GUI chosen
        #TODO: load the settings of the previous experiment
        
    else:
        infile = open(args.infile)
        #Default is to provide an input-file and to provide all the data for the new experiment
    
    #2. CREATE THE EXPERIMENT CLASS
    experiment = Experiment(infile)
        #2.1 start the cron_job --> light and motor
    cron_job = Thread(target=experiment.cron)
    cron_job.start()    
        #2.2 save the experiment_data into THE archive
        #get ID for the archive and the logging
    experiment.get_experiment_id() 
        #2.3 start the actual experiment
    experiment.start()
        #2.4 archive the experiment
    experiment.archive_experiment()

def get_arguments():
    '''This method implements argparse to get the user-decision about the input'''
    parser = argparse.ArgumentParser(description='CAROUSSEL: Lets Play. A script to start a motor at the right time. Please choose a way to enter experiment-settings and data')
    
    choice = parser.add_mutually_exclusive_group()  #To not have gui and infile at the same time
    choice.add_argument("-g", "--gui", help='Use this tag to open the GUI in the next step', action="store_true")
    choice.add_argument("-i", "--infile",type = str, default = "./files/template.json", help = 'The experiment-file to run the experiment without GUI. See the template for more information' )
    
    return parser.parse_args()

def get_data_from_gui():
    '''If GUI is chosen, create GUI instance and proceed with the data input'''
    interface = GUI()
    filename = interface.get_data()
    return filename

if(__name__ == "__main__"):
    main()
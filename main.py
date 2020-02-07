from experiment import Experiment
from caroussel import Caroussel
from GUI import GUI
from threading import Thread
import argparse
import os

def main():
    """This Main method is used to decide, if one wants to provide an input-file with all the necessary experiment-data
    or to open a GUI and type the data in manually"""
    #0. RUN A GPIO-TEST OR CLEANUP FUNCTION  
    #get data from argparse 
    args = get_arguments() 

    if(args.test):
        test = Caroussel()
        test.test_functions()
        quit()
    if(args.cleanup):
        clean = Caroussel()
        clean.cleanup()

    #1. DECIDE WHICH INPUT-FORMAT TO CHOOSE
    if(args.gui):
        infile = get_data_from_gui()
    else:
        infile = args.infile #Default = input-file 
    
    #2. CREATE THE EXPERIMENT CLASS
    experiment = Experiment(infile)
        #2.1 start the cron_job --> light and motor
    cron_job = Thread(target=experiment.cron)
    cron_job.start()
    home = os.getcwd()
    try:
        #2.2 start the actual experiment
        experiment.start()
    except:
        print("Experiment terminated with error. please try again")
        #2.3 terminate the cron-job
    finally:  
        os.chdir(home)
        cron_job.running = False
        cron_job.join()
        experiment.archive_experiment()
        experiment.shutdown()
    
def get_arguments():
    '''This method implements argparse to get the user-decision about the input'''
    parser = argparse.ArgumentParser(description='CAROUSSEL: Lets Play. A script to start a motor at the right time. Please choose a way to enter experiment-settings and data')
    choice = parser.add_mutually_exclusive_group()  #To not have gui and infile at the same time
    choice.add_argument("-g", "--gui", help='Use this tag to open the GUI in the next step', action="store_true")
    choice.add_argument("-i", "--infile",type = str, default = "./files/template.json", help = 'The experiment-file to run the experiment without GUI. See the template for more information' )
    choice.add_argument("-t", "--test",help="Use this tag to run a functionality test of all the GPIO-Pins", action="store_true")
    choice.add_argument("-c", "--cleanup", help="Use this tag if the programm crashed and the Caroussel still runs. It will shutdown the GPIO-pins safely")
    
    return parser.parse_args()

def get_data_from_gui():
    '''If GUI is chosen, create GUI instance and proceed with the data input'''
    interface = GUI()
    interface.run() 
    return interface.infile

if(__name__ == "__main__"):
    main()

#from experiment import Experiment
#from caroussel import Caroussel
from threading import Thread
import argparse
import os,shutil
import time
import getpass

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
        quit()
    if(args.setup):
        setup()
        quit()

    #1. DECIDE WHICH INPUT-FORMAT TO CHOOSE
        #Default = GUI
    if(args.infile):
        infile = args.infile
    else:
        infile = get_data_from_gui()
          
    
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
    choice.add_argument("-i", "--infile",type = str, help = 'The experiment-file to run the experiment without GUI. See the template for more information' )
    choice.add_argument("-t", "--test",help="Use this tag to run a functionality test of all the GPIO-Pins", action="store_true")
    choice.add_argument("-c", "--cleanup", help="Use this tag if the programm crashed and the Caroussel still runs. It will shutdown the GPIO-pins safely",action="store_true")
    choice.add_argument("-s", "--setup", help="Use this tag after cloning the repository to setup the program. You can type 'caro' in terminal afterwards to start the gui",action="store_true")    

    return parser.parse_args()

def get_data_from_gui():
    '''If GUI is chosen, create GUI instance and proceed with the data input'''
    os.system("python2 GUI.py")
    while(True):
        #complicated procedure to integrate the python2 script... 
        #create temp file in temp directory to proceed with the main-script
        time.sleep(1)
        print("Waiting for GUI. Press Ctr. + C to interrupt",end="\r")
        if("start.txt" in os.listdir("./save_files/temp/")):
            break
    os.system("rm save_files/temp/start.txt")
    return "./save_files/temp/exp_settings.json"

def setup():
    """Start this method once(!) after cloning the repository to initiate an alias and start the program with one single "caro" in terminal"""
    #Put the caro.sh - file into the bin-directory of the current user
    bindir = "/home/{}/bin/".format(getpass.getuser())
    if(os.path.isdir(bindir)):
        pass
    else:
        os.mkdir(bindir)
    if("caro.sh" not in os.listdir(bindir)):
        if("caro.sh" in os.listdir(".")):

            #Alter the caro.sh-file to point to the current directory
            with open("caro2.sh","w") as outfile:
                for line in [x.strip() for x in open("caro.sh")]:
                    if(line == "cd path/to/caro"):
                        line = "cd {}".format(os.getcwd())
                    outfile.write(line + "\n")

            shutil.copy2("caro2.sh","{}/caro.sh".format(bindir))
            os.system("rm caro.sh")
            os.system("rm caro2.sh")
        #Set the alias in the .bashrc
        os.system("echo 'alias caro=\"source ~/bin/caro.sh\"' >> ~/.bashrc")
    else:
        print("Setup already finished. Aborting")

if(__name__ == "__main__"):
    main()

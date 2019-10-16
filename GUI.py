# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import json
import os

class GUI():
    ''' Make a TKinter GUI. Load the settings from the previous experiment into it'''
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The totally unnecessary GUI")
        self.HEIGHT = 720
        self.WIDTH = 1080
        self.infile = "save_files/temp/exp_settings.json"
        
        try:
            self.last_time = dict(json.load(open("save_files/temp/exp_settings.json")))
        except:
            os.mkdr("save_files/temp/")
            self.last_time = dict(json.load(open("files/template.json")))
        
    def run(self):
        #Build a container for the main-window -> start with canvas
        canvas = tk.Canvas(self.root, height = 720, width = 1080)
        canvas.pack()
        
        #organise the canvas with frames
        style_env = tk.Frame(self.root, bg="grey")
        style_env.place(relx = 0.005, rely = 0.005, relwidth = 0.325, relheight = 0.490)
        environment = tk.Frame(style_env)
        environment.place(relx = 0.01, rely = 0.01, relwidth = 0.98, relheight = 0.98)

        style_fly = tk.Frame(self.root, bg="grey")
        style_fly.place(relx = 0.005, rely = 0.50, relwidth = 0.325, relheight = 0.495)
        fly_data = tk.Frame(style_fly)
        fly_data.place(relx = 0.01, rely = 0.01, relwidth = 0.98, relheight = 0.98)
        
        style_exp = tk.Frame(self.root, bg="grey")
        style_exp.place(relx = 0.335, rely = 0.005, relwidth = 0.33, relheight = 0.99)
        experiment_data = tk.Frame(style_exp)
        experiment_data.place(relx = 0.01, rely = 0.005, relwidth = 0.98, relheight = 0.99)
        
        style_com = tk.Frame(self.root, bg="grey")
        style_com.place(relx = 0.67, rely = 0.005, relwidth = 0.325, relheight = 0.490)
        comments = tk.Frame(style_com)
        comments.place(relx = 0.01, rely = 0.01, relwidth = 0.98, relheight = 0.98)
        
        style_start = tk.Frame(self.root, bg="grey")
        style_start.place(relx = 0.67, rely = 0.50, relwidth = 0.325, relheight = 0.495)
        start_field = tk.Frame(style_start)
        start_field.place(relx = 0.01, rely = 0.01, relwidth = 0.98, relheight = 0.98)
        
        #Now design each frame individually
        
        ###Environment-frame###
        #1. Main - Label
        env_label = tk.Label(environment, text="Environment Data",bg="grey",font='Helvetica 13 bold')
        env_label.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight=0.095)       
        
        #2. Entry-fields and sub-Labels
        info_label = tk.Label(environment, text="Please provide the current\ntemperature and the humidity",justify="center")
        info_label.place(relx = 0.005, rely = 0.1, relwidth = 0.99, relheight=0.195) 
        
        temp_label = tk.Label(environment, text = "Current Temperature",font='Helvetica 8 bold',anchor="e")
        temp_label.place(relx = 0.05, rely = 0.3, relwidth = 0.40, relheight=0.1)
        temp_entry = tk.Entry(environment, bg = "White")
        temp_entry.place(relx = 0.55, rely = 0.3, relwidth = 0.30, relheight=0.1)
        temp_entry.insert("end",self.last_time["temperature"])
        
        hum_label = tk.Label(environment, text = "Current Humidity",font='Helvetica 8 bold',anchor="e")
        hum_label.place(relx = 0.05, rely = 0.45, relwidth = 0.40, relheight=0.10)
        hum_entry = tk.Entry(environment, bg = "White")
        hum_entry.place(relx = 0.55, rely = 0.45, relwidth = 0.30, relheight=0.10)        
        hum_entry.insert("end",self.last_time["humidity"])
        
        ###Fly-Data###
        #1. Main - Label
        fly_label = tk.Label(fly_data, text="Drosophila Data",bg="grey",font='Helvetica 13 bold')
        fly_label.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight=0.095)
        
        #2. Processing Sublists
        #Load possible Food_choices
        food_choices = list(json.load(open("files/food.json")))
        #Load food choices from last experiment
        if(self.last_time["food"] in food_choices): 
            default_food = food_choices.index(self.last_time["food"])
        else:
            default_food = 0
            
        #load possible genotypes
        geno_choices = list(json.load(open("files/genotypes.json")))
        #Load food choices from last experiment
        if(self.last_time["genotype"] in geno_choices): 
            default_geno = geno_choices.index(self.last_time["genotype"])
        else:
            default_geno = 0
        
        #2.Entry-fields and sub-Labels
        info2_label = tk.Label(fly_data, text="Please provide the information\nnecessary for this experiment ",justify="center")
        info2_label.place(relx = 0.005, rely = 0.1, relwidth = 0.99, relheight=0.195) 

        food_label = tk.Label(fly_data, text = "Food Source",font='Helvetica 8 bold',anchor="e")
        food_label.place(relx = 0.05, rely = 0.3, relwidth = 0.40, relheight=0.1)
        food_pop = ttk.Combobox(fly_data,values=food_choices)
        food_pop.place(relx = 0.55, rely = 0.3, relwidth = 0.30, relheight=0.1)
        food_pop.current(default_food) #set as default
        
        sex_label = tk.Label(fly_data, text = "Sex of Fly",font='Helvetica 8 bold',anchor="e")
        sex_label.place(relx = 0.05, rely = 0.45, relwidth = 0.40, relheight=0.10)
        sex_pop = ttk.Combobox(fly_data,values = ["m","f"])
        sex_pop.place(relx = 0.55, rely = 0.45, relwidth = 0.30, relheight=0.10)
        sex_pop.current(0)
            
        geno_label = tk.Label(fly_data, text = "Genotype of Fly",font='Helvetica 8 bold',anchor="e")
        geno_label.place(relx = 0.05, rely = 0.6, relwidth = 0.40, relheight=0.10)
        geno_pop = ttk.Combobox(fly_data, values = geno_choices)
        geno_pop.place(relx = 0.55, rely = 0.6, relwidth = 0.30, relheight=0.10)
        geno_pop.current(default_geno)
        
        age_label = tk.Label(fly_data, text = "Age of the Fly",font='Helvetica 8 bold',anchor="e")
        age_label.place(relx = 0.05, rely = 0.75, relwidth = 0.40, relheight=0.10)
        age_entry = tk.Entry(fly_data, bg = "White")
        age_entry.place(relx = 0.55, rely = 0.75, relwidth = 0.30, relheight=0.10)
        age_entry.insert("end",str(self.last_time["age"]))
        
        ###Experiment-Data###
        #1. Main-Label
         
        exp_label = tk.Label(experiment_data, text="Experiment Settings",bg="grey",font='Helvetica 13 bold')
        exp_label.place(relx = 0.005, rely = 0.0025, relwidth = 0.99, relheight=0.050)
        
        #2.Get default-settings
        #Load possible circ_choices
        circ_choices = [list(x.keys())[0] for x in (json.load(open("files/circrythm.json")))]
        #Load food choices from last experiment
        if(self.last_time["circRythm"] in circ_choices): 
            default_circ = circ_choices.index(self.last_time["circRythm"])
        else:
            default_circ = 0
            
        #load possible genotypes
        if(self.last_time["motor1_direction"] in ["cw","ccw"]):
            motor1_default = ["cw","ccw"].index(self.last_time["motor1_direction"])
        else:
            motor1_default = 0
            
        if(self.last_time["motor2_direction"] in ["same","different"]):
            motor2_default = ["same","different"].index(self.last_time["motor2_direction"])
        else:
            motor2_default = 0
        
        #3.Entry-fields and sub-Labels
        info3_label = tk.Label(experiment_data, text="Please provide the settings\nnecessary for this experiment ",justify="center")
        info3_label.place(relx = 0.005, rely = 0.065, relwidth = 0.99, relheight=0.07) 
        
        camera_label = tk.Label(experiment_data, text = "Name of the Camera",font='Helvetica 8 bold',anchor="e")
        camera_label.place(relx = 0.05, rely = 0.15, relwidth = 0.40, relheight=0.05)
        camera_entry = tk.Entry(experiment_data, bg = "white")
        camera_entry.place(relx = 0.55, rely = 0.15, relwidth = 0.30, relheight=0.05)
        camera_entry.insert("end","PiCamera")
        
        fps_label = tk.Label(experiment_data, text = "FPS (Frames/second)",font='Helvetica 8 bold',anchor="e")
        fps_label.place(relx = 0.05, rely = 0.22, relwidth = 0.40, relheight=0.05)
        fps_entry = tk.Entry(experiment_data, bg ="white")
        fps_entry.place(relx = 0.55, rely = 0.22, relwidth = 0.30, relheight=0.05)
        fps_entry.insert("end",self.last_time["FPS"])
            
        frames_label = tk.Label(experiment_data, text = "Total Frames",font='Helvetica 8 bold',anchor="e")
        frames_label.place(relx = 0.05, rely = 0.29, relwidth = 0.40, relheight=0.05)
        frames_entry = tk.Entry(experiment_data, bg = "white")
        frames_entry.place(relx = 0.55, rely = 0.29, relwidth = 0.30, relheight=0.05)
        frames_entry.insert("end",self.last_time["video_length"])
        
        rig_label = tk.Label(experiment_data, text = "Number of the Rig",font='Helvetica 8 bold',anchor="e")
        rig_label.place(relx = 0.05, rely = 0.36, relwidth = 0.40, relheight=0.05)
        rig_entry = tk.Entry(experiment_data, bg = "White")
        rig_entry.place(relx = 0.55, rely = 0.36, relwidth = 0.30, relheight=0.05)
        rig_entry.insert("end",str(self.last_time["rig"]))
        
        motor1_label = tk.Label(experiment_data, text = "Motor1 direction",font='Helvetica 8 bold',anchor="e")
        motor1_label.place(relx = 0.05, rely = 0.43, relwidth = 0.40, relheight=0.05)
        motor1_pop = ttk.Combobox(experiment_data,values = ["cw","ccw"])
        motor1_pop.place(relx = 0.55, rely = 0.43, relwidth = 0.30, relheight=0.05)
        motor1_pop.current(motor1_default)
        
        motor2_label = tk.Label(experiment_data, text = "Motor2 direction",font='Helvetica 8 bold',anchor="e")
        motor2_label.place(relx = 0.05, rely = 0.50, relwidth = 0.40, relheight=0.05)
        motor2_pop = ttk.Combobox(experiment_data,values = ["same","different"])
        motor2_pop.place(relx = 0.55, rely = 0.50, relwidth = 0.30, relheight=0.05)
        motor2_pop.current(motor2_default)
        
        switch_label = tk.Label(experiment_data, text = "Motor Switch-time",font='Helvetica 8 bold',anchor="e")
        switch_label.place(relx = 0.05, rely = 0.57, relwidth = 0.40, relheight=0.05)
        switch_entry = tk.Entry(experiment_data,bg="white")
        switch_entry.place(relx = 0.55, rely = 0.57, relwidth = 0.30, relheight=0.05)
        switch_entry.insert("end",self.last_time["motor_switchtime"]) #set as default
        
        disc1_label = tk.Label(experiment_data, text = "Disc1 position",font='Helvetica 8 bold',anchor="e")
        disc1_label.place(relx = 0.05, rely = 0.64, relwidth = 0.40, relheight=0.05)
        disc1_entry = tk.Entry(experiment_data, bg = "White")
        disc1_entry.place(relx = 0.55, rely = 0.64, relwidth = 0.30, relheight=0.05)
        disc1_entry.insert("end",str(self.last_time["disc1_pos"]))
        
        disc2_label = tk.Label(experiment_data, text = "Disc2 position",font='Helvetica 8 bold',anchor="e")
        disc2_label.place(relx = 0.05, rely = 0.71, relwidth = 0.40, relheight=0.05)
        disc2_entry = tk.Entry(experiment_data, bg = "White")
        disc2_entry.place(relx = 0.55, rely = 0.71, relwidth = 0.30, relheight=0.05)
        disc2_entry.insert("end",str(self.last_time["disc2_pos"]))
        
        circ_label = tk.Label(experiment_data, text = "Circadian Rythm",font='Helvetica 8 bold',anchor="e")
        circ_label.place(relx = 0.05, rely = 0.78, relwidth = 0.40, relheight=0.05)
        circ_pop = ttk.Combobox(experiment_data, values = circ_choices)
        circ_pop.place(relx = 0.55, rely = 0.78, relwidth = 0.30, relheight=0.05)
        circ_pop.current(default_circ)
        
        ###Comment-Frame###
        #1. Main-label
        comment_label = tk.Label(comments, text="Comments",bg="grey",font='Helvetica 13 bold')
        comment_label.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight=0.095)
        
        #2. Entry-fields and sub-Labels
        info4_label = tk.Label(comments, text="If you want to let\nus know something",justify="center")
        info4_label.place(relx = 0.005, rely = 0.1, relwidth = 0.99, relheight=0.195) 
    
        com_entry = tk.Text(comments, bg = "White")
        com_entry.place(relx = 0.05, rely = 0.3, relwidth = 0.90, relheight=0.6)
        com_entry.insert("end",self.last_time["comment"])
        
        ###start-experiment-Frame###
        #1. Main-label
        start_label = tk.Label(start_field, text="Start the Experiment",bg="grey",font='Helvetica 13 bold')
        start_label.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight=0.095)
        info5_label = tk.Label(start_field, text = "Press the button to start the experiment")
        info5_label.place(relx = 0.05,rely= 0.1, relwidth = 0.99, relheight = 0.195)
        
        #Now the Button and the functionalities
        
        def button_action():
            experiment_data = {}
            experiment_data["rig"] = rig_entry.get()
            experiment_data["temperature"] = float(temp_entry.get())
            experiment_data["humidity"] = float(hum_entry.get())
            experiment_data["comment"] = com_entry.get("1.0","end-1c")
            experiment_data["food"] = food_pop.get()
            experiment_data["sex"] = sex_pop.get()
            experiment_data["genotype"] = geno_pop.get()
            experiment_data["age"] = float(age_entry.get())
            experiment_data["camera"] = camera_entry.get()
            experiment_data["circRythm"] = circ_pop.get()
            experiment_data["motor_switchtime"] = switch_entry.get()
            experiment_data["motor1_direction"] = motor1_pop.get()
            experiment_data["motor2_direction"] = motor2_pop.get()
            experiment_data["disc1_pos"] = float(disc1_entry.get())
            experiment_data["disc2_pos"] = float(disc2_entry.get())
            experiment_data["video_length"] = int(frames_entry.get())
            experiment_data["FPS"]= int(fps_entry.get())
                        
            with open(self.infile,"w") as settings:
                json.dump(experiment_data,settings,indent = 2)
        
            self.root.destroy()
            
        start_button = tk.Button(start_field,text = "Start", bg="red", command = button_action)
        start_button.place(relx = 0.25, rely = 0.5, relwidth = 0.5, relheight = 0.2)
        
        self.root.mainloop()

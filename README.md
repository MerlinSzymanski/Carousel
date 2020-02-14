# Caro #
A Program to run 'THE CAROUSSEL' - A Raspberry/GPIO-based machine built by Dr. Wolf Hütteroth and Dr. Tilman Triphan from the University of Leipzig/Konstanz to test the behavior of Drosophila in the presence of a turning disc. This Script regulates the light, the turning of the discs and the camera. Input = Experiment-File (s. 3.), Output = Video-files for downstream analysis of Drosophila movement-patterns

## Dependencies: ##
- see Point 1.3 and use the caro.yml-file to create a fitting environment! 

## 1. Getting started: ##
(I assume, that you have a Raspberry prepared)
1. Clone this repository onto your Raspberry by typing:
<pre><code>git clone https://github.com/MerlinSzymanski/Carousel</code></pre>
2. Change your working-directory:
<pre><code>cd path/to/Carousel/</code></pre>
3. Create and activate the Environment
<pre><code>conda env create -f caro.yml
conda activate caro </code></pre>
4. Set up a Shortcut in the Terminal by running 
<pre><code>python3 main.py -s</code></pre>
5. Run a functionality-Test
<pre><code>python3 main.py -t</code></pre> 
If something is not working, check the pin-numbering in the Caroussel.py-module

## 2. Running the experiment: ##
You can now access the program by opening the terminal and typing
<pre><code>caro</code></pre>
which start the Userunterface.

If you want to go directly over the python-file, **change to the Carousel/ directory** and type:
<pre><code>python3 main.py</code></pre>
Available flags are: 
- i: The program starts without a GUI and reads the data from a file. Default file = files/template.json
to use the same data as in the previous experiment, you can use -i save_files/temp/exp_settings.json
- g: The program starts with a GUI 
- t: The Functionality test
- c: A cleanup-programm, if the Caroussel runs after the programm crashed

## 3. Data to provide: ##
You can see in the GUI what should be provided...
### Necessary for the Script: ###
- **circRythm**: e.g. "6:22LD" = from 06:00 - 22:00 white light, from 22:00 - 06:00 Red Light. Please specify your regimes in files/circrythm.json
- **motor_switchtime**: e.g. "5" = After 5 minutes one disc stops turning and the other one starts
- **motor1_direction**: "cw" or "ccw" = clockwise or counterclockwise
- **motor2_direction**: "same" or "different" = relative to motor 1
- **video_length**: e.g. "9000" = Lenght in **frames**. Should be switched back to seconds to avoid confusion!
- **FPS**: e.g. "5" = Frames per second

Everything else is just piped into the archive, but can be specified using the files/\*.json files 

## 4. Additional functions ##

If some of the functions dont work - check the pin-numbers in the "caroussel.py" module.
To shutdown a running caroussel after a crash,use
<pre><code>python3 main.py -c</code></pre>  


# Caro #
A Program to run 'THE CAROUSSEL' - A Raspberry/GPIO-based machine built by Dr. Wolf Hütteroth and Dr. Tilman Triphan from the University of Leipzig/Konstanz to test the behavior of Drosophila in the presence of a turning disc. This Script regulates the light, the turning of the discs and the camera. Input = Experiment-File (s. 3.), Output = Video-files for downstream analysis of Drosophila movement-patterns

## Dependencies: ##
- Conda
- Python 3.4
- picamera
- RPi.GPIO
- tqdm

TODO: Create caro.yml-file to just create a fitting environment!

## 1. Getting started: ##
(I assume, that you have a Raspberry prepared)
1. Clone this repository onto your Raspberry by typing:
<pre><code>git clone https://github.com/MerlinSzymanski/Carousel</code></pre>
2. Change your working-directory:
<pre><code>cd path/to/Carousel/</code></pre>
3. Create and activate the Environment
<pre><code>conda env create -f caro.yml
conda activate caro </code></pre>

## 2. Running the experiment: ##
If you are in the Carousel/ directory you can run the help-section by typing:
<pre><code>python3 main.py -h</code></pre>
Available flags are: 
- i: The program starts without a GUI and reads the data from a file. Default = GUI
- o: //TODO: save the videos somewhere else. Default = save_files/experiments/experiment_id/
The programm starts by typing: 
<pre><code>python3 main.py</code></pre>
After providing Data (see 3.), the Raspberry should:
1. Activate Light and Motor of the Caroussel    
When the Time is either %H:30:00 or %H:00:00:
2. Start turning the discs, Start filming
3. Run for eternity     
When the program is interrupted:
4. End the currently running video (or force-quit) and shut down the Caroussel

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
Run <pre><code>python3 main.py -t</code></pre> to run a functionality-test.
If some of the functions dont work - check the pin-numbers in the "caroussel.py" module.
To shutdown a running caroussel after a crash,use
<pre><code>python3 main.py -c</code></pre>  


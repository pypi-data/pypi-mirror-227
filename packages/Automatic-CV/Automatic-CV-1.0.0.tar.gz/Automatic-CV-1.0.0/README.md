# Automatic CV

A library allowing easy control over EC-BioLogic devices via simple Python code. You can integrate this project with your automated robot (such as the OT-2 robot) to achieve automated electrochemical test tasks. At this stage, only the CV experiment can be tested through this library. Further electrochemical experiments are on the way and will be released in the following update.

> Install with `python -m pip install Automatic-CV`

For details of techniques and parameters, please see: the official development user's guide: [EC-Lab Development Package.pdf](https://github.com/DangerLin/easy-biologic/blob/main/EC-Lab%20Development%20Package.pdf).

### Biologic Program
`Abstract Class`
Represents a program to be run on a device.

#### Methods
+ **BiologicProgram( device, params, channels = None, autoconnect = True, barrier = None, stop_event = None, threaded = False ):** Creates a new program.

+ **channel_state( channels = None ):** Returns the state of the channels.

+ **on_data( callback, index = None ):** Registers a callback function to run when data is collected.

+ **run():** Runs the program.

+ **stop():** Sets the stop event flag.

+ **save_data( file, append = False, by_channel = False ):** Saves data to the given file.

+ **sync():** Waits for barrier, if set.

+ **_connect():** Connects to the device

#### Properties
+ **device:** BiologicDevice. <br>
+ **params:** Passed in parameters. <br>
+ **channels:** Device channels. <br>
+ **autoconnect:** Whether connection to the device should be automatic or + not. <br>
+ **barrier:** A threading.Barrier to use for channel syncronization. [See ProgramRummer] <br>
+ **field_titles:** Column names for saving data. <br>
+ **data:** Data collected during the program. <br>
+ **status:** Status of the program. <br>
+ **fields:** Data fields teh program returns. <br>
+ **technqiues:** List of techniques the program uses.

### Base Programs
This project can be used to scan the `CV` experiment only. Further experiments, including `OCV`, `PEIS`, *etc.*, are on the way and will be released in the following update.
    
#### CV
Performs a `CV` scan.

        Ewe ^
            |        E1
            |        /\
            |       /  \        Ef
            |      /    \      /
            |     /      \    /
            |    /        \  /
            |  Ei          \/
            |              E2
            |
            -----------------------> t
        

##### Params
+ **start:** Initial voltage (Ei). 
[Default: 0]

+ **E1:** Boundary potential that first reaches (E1).

+ **E2:** Boundary potential that reaches later.

+ **Ef:** Potential *vs* reference.
[Default: 0]

+ **step:** Voltage step. 
[Default: 0.001]

+ **rate:** Scan rate in V/s. 
[Default: 0.05]

+ **average:** Average over points. 
[Default: False]


### Find Devices
A convenience script for finding connected devices.

#### Use
From a terminal run `python -m automatic_cv.find_devices`.


### EC Errors
Implements EC errors.

#### Classes
+ **EcError( value = None, code = None, message = None )** 

## Example

A basic example that runs a CV experiment on channel 1.
```python
import logging
import automatic_cv as acv
import automatic_cv.base_programs as abp

logging.basicConfig(level=logging.DEBUG)

# create device
bl = acv.BiologicDevice('169.254.72.33')  #IP address is to be confirmed.

# channels to be used
channels = [0]
by_channel = False

# data saving directory
save_path = f'D:\Data\EC lab\data_output' # file name is to be defined.
if not by_channel:  
    save_path += '.csv'

# create CV program
params_CV = {
	
    'start': 0.9,
    'E1': -0.4,
    'E2': 0.3,
    'Ef': 0.9,
    'vs_initial': False,
    'rate': 0.05,                      #unit: V/s
    'step': 0.001,                     #step = dEN/1000
    'N_Cycles': 0,
    'average_over_dE': False, 
    'begin_measuring_I': 0.5,
    'End_measuring_I': 1.0,
    'I_range' : 'KBIO_IRANGE_AUTO',
    'E_range' : 'KBIO_ERANGE_2_5',
    'bandwidth': 'KBIO_BW_5'
}   

CV = abp.CV(
    bl,
    params_CV,     
    channels = [0]   #channel is to be claimed.
)     

# run program
CV.run( 'data' )
CV.save_data(save_path)
```

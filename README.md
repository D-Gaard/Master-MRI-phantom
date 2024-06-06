# Simulating Human Movement in MRI: A Soft Phantom Head Approach with Machine Learning Integration
This repository contains all sharable code/data from our master thesis.

By Mads Daugaard \& Emil Riis-Jacobsen.

Faculty of Science, University of Copenhagen.

Handed in: May 31. 2024.

Below image showcases the physical robot setup and a video demo is availiable [here](https://www.youtube.com/watch?v=Sc_tomtOb3E&ab_channel=MadsDaugaard).


![Robot example](GithubImgs/robotshowcase.png)

# Requirements
## Python
The required python 3.10.13 packages can be found in "environment.yml", and easily be instaled with anaconda using this command:

```
conda env create -f environment.yml --name <new_env_name>
```
## Other software used:
* Blender        - 4.0.2
* Fusion 360     - 2.0.18719 x86_64
* Arduino IDE    - 2.3.2
* KiCad          - 8.0.1
* Geogebra       - 6.0.838.0
* Ultimaker Cura - 5.6.0



# File overview
## Important code/model files
 * motor_controller.ino                                                 - Arduino code for controling the system
 * motor_ui.ipynb                                                       - UI and host computer protocol/communication with the microcontroller
 * robot_sim.ipynb                                                      - Simplified robot simulator
 * ML_train.ipynb                                                       - ML model training
 * ML_predict.ipynb                                                     - Using ML model to predict cable positions for test persons
 * ML_test.ipynb                                                        - Compute metrics on models using train/test data
 * metrics.py                                                           - Compute and plot Euclidedistance, corelation and more
 * dataUtils.py                                                         - Utilities for loading and processing tracking data
 * metricUtils.py                                                       - Utilities for various metrics and ploting
 * Models\Final_models\2hid_32_neu_500epoch_p001lr_norm-11.pth          - The best trained model on 20step data

## Meshes, Data and Tracking
* \Meshes\Final           - All meshes used in final product, and a blender file containing the coil setup
* \Meshes\Simulation      - Meshes used for simulation
* \Meshes\40p             - Meshes for iteration 1 and 2 (see report)
* \Data\ABCD              - ABCD data (not public, add your own to the folder)
* \Data\MRI               - MRI scans of our silicone objects
* \Tracking               - Tracking data of robot from optitrack system using various protocols. Data in grid search folder used 100 steps/s^2 acceleration, unless otherwise specified


## Models and Predictions
* \Models\5fold           - Training/validation MSE loss for 5-fold validation
* \Models\Final_models    - Final model versions trained on the complete training dataset (85% of the grid search data)
* \Predictions            - Absolute moves predicted by the best 5/20 step ML model (see report) for isolation moves/test persons

## Files for creating images for the report
* \Plotting\MRI             - MRI images of head phantom
* \Plotting\Drawings        - Illustrations used for the report
* \Plotting\ML              - Plot ML/tracking results and metrics


## Prototypes
*  \Prototypes\Motorcontrol     - Various motor control setups and UI versions
*  \Prototypes\Simulation       - Various simulation setups for the CSPR system      
*  \Prototypes\Tracking         - Various ml/tracking files
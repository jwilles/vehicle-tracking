# Vehicle Tracking
Autonomous vehicle 3D multi object tracking (MOT) on the KITTI dataset

### Setup
All code was developed an tested in the following environment:
* Ubuntu 18.04
* Python 3.7

In order to setup the virtual environment:
```
git clone git@github.com:codyreading/vehicle-tracking.git                       # Clone this repostitory
cd vehicle-tracking                                                             # Navigate to the project
mkvirtualenv -a $PWD -r requirements.txt -p /usr/bin/python3.7 vehicle_tracking # Create virtual environment with virtualenvwrapper
workon vehicle_tracking                                                         # Activate virtual environment
add2virtualenv src/.                                                            # Add src to PYTHONPATH
```

### Running
```
python scripts/test.py
```
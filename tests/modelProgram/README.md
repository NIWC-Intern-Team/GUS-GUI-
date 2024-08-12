# README 

## Table of Contents 

<!-- - [About](#-about) -->
<!-- - [Certification](#-certification) -->
- [How to Build](#-how-to-build)
- [How to Use Accessibility Features](#how-to-use-accessibility-features)
- [Bugs and Issues](#bugs-and-issues)
- [Feedback and Contributions](#feedback-and-contributions)
- [Contacts](#contacts)
<!-- - [License](#-license) -->





## 📝 How to Build

To build the packages directly from GitHub, follow these steps:

```shell
# Open a terminal (Command Prompt or PowerShell for Windows, Terminal for macOS or Linux)

# Ensure Git is installed
# Visit https://git-scm.com to download and install console Git if not already installed

# Clone the repository
git clone https://github.com/NIWC-Intern-Team/GUS-GUI-.git

# Navigate to the project directory
cd .../modelProgram

# install dependencies 
pip install -r requirements.txt 

# execute the project
python3 __main__.py

```

If running from containerized environment 
```shell 
# various Docker commands 
```
 
## Docker Quick References
```shell
#IMPORTANT: Start Docker daemon first (i.e., Docker desktop)

docker images: List local images 

docker ps: list running containers 

docker ps -all: list all containers (running and stopped)

docker exec -it <mycontainer> bash: 

docker run -it --rm -e DISPLAY=host.docker.internal:0.0 -v /tmp/.X11-unix:/tmp/.X11-unix <mycontainer>: Enables external display of applications from GUI
```

## Additional Manual Install
```shell 
sudo apt-get install libx11-xcb1 libxcb1 libxcomposite1 libxrandr2 libxi6 libxext6 libxfixes3 libxtst6 libxrender1 libxcb1-dev libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev

sudo apt-get install libasound2

sudo apt-get install libxkbcommon0
```

## How to Use Accessibility Features
### UI Mode Selector
1. Click on the UI Mode top menu item.
2. Select "Dark" or "Light" UI mode.

### Font Size Selector
1. Click on the Font Size top menu item.
2. Select "Small", "Medium", or "Large" font size.

## Bugs and Issues 

### Docker 
Installation issues with ipython, numpy, and pandas. They seem to be installed as dependencies with other packages however. 

pyqt5 installed with apt-get due to system wide dependencies. It depends on libqt5gui5 which depends on libgl5 which is managed by system wide package managers like apt-get and snap.

https://stackoverflow.com/questions/74047562/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo

apt-get installation of pyqt conflicts with pip so that additional pip based packages aren't able to be installed, so PyQt5 to be installed via pip and manual installation of system wide dependencies is done instead. 

### Security 
Current interface with AXIS Camera Network disables all security protocols to bypass authentication interface. 

### Frontend 
- Clipping of map widget over other widgets on certain window sizes.
- Dark UI mode is no longer displayed on the map.

### Map Widget 
For the map widget, interface issues with Leaflet & PyQt, so a custom one was implemented. This results in the loss of many of the features of leaflet, but wasn't deemed necessary to much of a loss in the end. Main issue was accessing plotted markers outside of the Leaflet map due to permission issues that PyQt was blocking. 

### Virtual Environments 
With the usage of conda virtual environments on Ubunutu systems, the custom map widget breaks. Potentially due to access to snap installed GCC packages. Not fully diagnosed. 

### Running in Windows 
Must install VcXsrv to allow GUI applications on a windows machine that are forwarded from a Linux-based system. 

### HTML to Python Connection 
Connect variable issue, a lot of customization in terms of communication and not using standard packages. HTML script contains in-line JavaScript as well which is not standard.


## Feedback and Contributions
### Feedback 
The GUS-V engineers have provided valuable feedback, which the development team has implemented based on priority, but there are several features that must be implemented during a future phase of development, including:
- Integration of swarm capabilities​
- Integration of map measuring tool​
- Integration of LiDAR sensors​
- Containerization of the GUI​
- Integration of keyboard control of vessels 

### Contributions 
#### Ben Corriette
- Accessibility features:
    - UI mode selector
    - Font size selector
- Diagnostics visual enhancement
- Documentation:
    - Diagrams:
        - System architecture
        - User flow
    - Scrum board (on GitHub)
    - System requirements
- Project management
- Quality assurance test plan
- User interface/user experience design
- Wireframes

#### Tahseen Hussain
- Axis camera feed integration
- Containerization work
- CSV data integration
- Electronic box construction
- Game controller integration
- Integrated console integration
- IP configuration integration
- Leaflet map integration
- Map plotting
- PyQt Designer layout of GUI
- User interface/user experience design
- User acceptance testing
- Wireframes

#### Rudra Patel
- Wireframes
- Map plotting

#### Mathias Penzes
- Wireframes
- Map plotting

#### Noah Shin
- All tab development:
    - Diagnostics
    - Errors and warnings

#### Isabelle Viraldo
- AHRS data integration
- Axis camera feed integration
- Documentation:
    - Diagrams:
        - System architecture
        - User flow
- Electronic box construction
- IP configuration integration
- Phidget sensor data integration
- Network link data integration

## Contacts
GUS-V Engineers:
- Hannah Brood (hannah.g.brood.civ@us.navy.mil)
- Brian Chhor (brian.t.chhor.civ@us.navy.mil)
- Tanvir Hussain (tanvir.r.hussain.civ@us.navy.mil)

GUS-V Software Development Team:
- Ben Corriette (gentleben8282@yahoo.com)
- Tahseen Hussain
- Rudra Patel
- Mathias Penzes
- Noah Shin (noahshin99@gmail.com)
- Isabelle Viraldo
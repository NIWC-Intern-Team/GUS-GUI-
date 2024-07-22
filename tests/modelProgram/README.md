# README 

## Table of Contents 

<!-- - [About](#-about) -->
<!-- - [Certification](#-certification) -->
- [How to Build](#-how-to-build)
- [Documentation](#-documentation)
- [Feedback and Contributions](#-feedback-and-contributions)
- [License](#-license)
- [Contacts](#%EF%B8%8F-contacts)





## 📝 How to Build

To build the packages directly from github, follow these steps:

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
# various docker commands 
```




## Contacts 
Route through Tanvir, Hannah, or Brian for contact to the team that started the development for questions 
## Docker quick references 
IMPORTANT: Start docker daemon first (ie docker desktop)

docker images: List local images 

docker ps: list running containers 

docker ps -all: list all containers (running and stopped)

docker exec -it <mycontainer> bash: 

docker run -it --rm -e DISPLAY=host.docker.internal:0.0 -v /tmp/.X11-unix:/tmp/.X11-unix <mycontainer>: Enables external display of applications from GUI 


## Feedback and Contributions 
2024 Summer UMV Intern team 



## Bugs & Issues 

### Docker 
Installation issues with ipython, numpy, and pandas. They seem to be installed as dependencies with other packages however. 

pyqt5 installed with apt-get due to system wide dependencies. It depends on libqt5gui5 which depends on libgl5 which is managed by system wide package managers like apt-get and snap.

https://stackoverflow.com/questions/74047562/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo

apt-get installation of pyqt conflicts with pip so that additional pip based packages aren't able to be installed, so PyQt5 to be installed via pip and manual installation of system wide dependencies is done instead. 

### Security 
Current interface with AXIS Camera Network disables all security protocols to bypass authentication interface. 

### FrontEnd 
Clipping of map widget over other widgets on certain window sizes 

### Map Widget 
For the map widget, interface issues with Leaflet & PyQt, so a custom one was implemented. This results in the loss of many of the features of leaflet, but wasn't deemed necessary to much of a loss in the end. Main issue was accessing plotted markers outside of the Leaflet map due to permission issues that PyQt was blocking. 

### Virtual Environments 
With the usage of conda virtual environments on Ubunutu systems, the custom map widget breaks. Potentially due to access to snap installed GCC packages. Not fully diagnosed. 

## Running in Windows 
Must install VcXsrv to allow GUI applications on a windows machine that are forwarded from a Linux-based system 

## HTML to Python connection 
connect variable issue, a lot of customization in terms of communication and not using standard packages. html script contains in-line js as well which is not standard. 



# additional manual install 
sudo apt-get install libx11-xcb1 libxcb1 libxcomposite1 libxrandr2 libxi6 libxext6 libxfixes3 libxtst6 libxrender1 libxcb1-dev libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev


sudo apt-get install libasound2

sudo apt-get install libxkbcommon0
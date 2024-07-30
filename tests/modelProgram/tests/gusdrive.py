#! /bin/python3

import pygame
import time
import socket


USV_IP = "192.168.1.113" #"192.168.0.123"
USV_PORT = 11111

udpOut = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP output

CONTROL_IP = "192.168.1.202" #"192.168.0.33"
CONTROL_PORT = 10101
udpIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpIn.bind((CONTROL_IP, CONTROL_PORT)) # UDP input

pygame.init()


#Xbox controller notes - these match the logitech controller too?
# Axis 1 is left vertical, axis 4 is right vertical, both inverted (-1 is up, 1 is down) 
# A is button 0 (abort)
# start button is 7 (enable)
# left bumper is button 4, right bumper is button 5 (gain down, gain up)

def disableUSV():
    print("Sending DISABLE message")
    udpOut.sendto(b"DISABLE\n", (USV_IP, USV_PORT))
    #time.sleep(0.5)
    udpOut.sendto(b"DISABLE\n", (USV_IP, USV_PORT))
    #time.sleep(0.5)
    udpOut.sendto(b"DISABLE\n", (USV_IP, USV_PORT))
    #time.sleep(0.5)
    
def killUSV():
    print("Sending KILL message")
    udpOut.sendto(b"KILL\n", (USV_IP, USV_PORT))
    #time.sleep(0.5)
    udpOut.sendto(b"KILL\n", (USV_IP, USV_PORT))
    #time.sleep(0.5)
    udpOut.sendto(b"KILL\n", (USV_IP, USV_PORT))
    #time.sleep(0.5)


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Drive USV2")

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}
    
    gain = 10
    enabled = False
    manual = True
    autonano = False
    autopix = False

    done = False
    while not done:
        if enabled:
            udpOut.sendto(b"ENABLE\n", (USV_IP, USV_PORT))
        if autonano:
            udpOut.sendto(b"AUTONANO\n", (USV_IP, USV_PORT))
        if autopix:
            udpOut.sendto(b"AUTOPIX\n", (USV_IP, USV_PORT))
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            
            if event.type == pygame.JOYBUTTONDOWN:
                #Disable with Button 0 (X or Cross)
                if event.button == 0:
                    enabled = False
                    autonano = False
                    autopix = False
                    disableUSV()
                    joystick = joysticks[event.instance_id]
                    joystick.rumble(10, 0.7, 500)
                #Enable Manual with Button 1 (Circle)
                if event.button == 1:
                    enabled = True
                    manual = True
                    autonano = False
                    autopix = False
                    joystick = joysticks[event.instance_id]
                    joystick.rumble(10, 0.7, 500)
                #Enable Auto Nano with Button 2 (Triangle)
                if event.button == 2:
                    enabled = True
                    manual = False
                    autonano = True
                    autopix = False
                 #Enable Auto Pix with Button 3 (Squre)
                if event.button == 3:
                    enabled = True
                    manual = False
                    autonano = False
                    autopix = True
                #Decrease Gain with Button 4 (Left Bumper)
                if event.button == 4:
                    if gain > 10:
                        gain = gain - 10
                    joystick = joysticks[event.instance_id]
                    joystick.rumble(0, 0.7, 500)
                #Increase Gain with Button 5 (Right Bumper)
                if event.button == 5:
                    if gain < 100:
                        gain = gain + 10
                    joystick = joysticks[event.instance_id]
                    joystick.rumble(0, 0.7, 500)
                #Set Waypoint with Button 6 (Left Trigger)
                # if event.button == 6:
                #Go to Waypoint with Button 7 (Right Trigger)
                # if event.button == 7:
                #Start Rosbag with Button 7 (Start, Left Button)
                # if event.button == 8:
                #Kill with Button 10 (Playstation)
                if event.button == 10:
                    enabled = False
                    autonano = False
                    autopix = False
                    killUSV()
                    joystick = joysticks[event.instance_id]
                    joystick.rumble(10, 0.7, 500)
                #Stationkeep with Button 11 (Left Joystick Press In)
                # if event.button == 11:

                #Old work
                # if event.button == 9:
                #     print("Marking EVENT")
                #     #log that transmit is happening
                #     logfile.write((str(time.time())+",EVENT\n").encode('ascii'))
                #     joystick = joysticks[event.instance_id]
                #     joystick.rumble(10, 0.7, 500)
                # if event.button == 10:
                #     print("Marking EVENT 2")
                #     #log that transmit is happening
                #     logfile.write((str(time.time())+",EVENT2\n").encode('ascii'))
                #     joystick = joysticks[event.instance_id]
                #     joystick.rumble(10, 0.7, 500)
                # if event.button == 1: #may need to change button
                #     enabled = True
                #     manual = False
                #     udpOut.sendto(b"GOTO,32.634167,-117.321083\n",(USV_IP, USV_PORT)) #waypoint between two nodes in Alpha field
                #     #udpOut.sendto(b"GOTO,32.705718,-117.236104\n",(USV_IP, USV_PORT)) #waypoint 1 off P169
                #     #udpOut.sendto(b"GOTO,32.705441,-117.236243\n",(USV_IP, USV_PORT)) #waypoint 2 off P169
                #     joystick = joysticks[event.instance_id]
                #     joystick.rumble(10, 0.7, 500)
                # if event.button == 3: #may need to change button
                #     enabled = True
                #     manual = False
                #     udpOut.sendto(b"STAY\n",(USV_IP, USV_PORT))
                #     joystick = joysticks[event.instance_id]
                #     joystick.rumble(10, 0.7, 500)
                
                
                
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        #text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
        #text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
        
            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            text_print.tprint(screen, f"Joystick: {name}")
            
            if enabled and manual:
                text_print.tprint(screen, f"Manual Enabled!")
            
                portaxis = joystick.get_axis(1) #round(*(-gain))
                #print(joystick.get_axis(1))
                #print(portaxis)
                if abs(portaxis) < 0.1: #deadzone is 10%
                    portaxis = 0
                portaxis = round(portaxis*(-gain))
                text_print.tprint(screen, f"Port Thrust: {portaxis}")

                stbdaxis = joystick.get_axis(4) #round(*(-gain))
                if abs(stbdaxis) < 0.1: #deadzone is 10%
                    stbdaxis = 0
                stbdaxis = round(stbdaxis*(-gain))
                text_print.tprint(screen, f"Stbt Thrust: {stbdaxis}")
                drivecmd = "DRIVE," + str(portaxis) + "," + str(stbdaxis) + "\n"
                udpOut.sendto(bytes(drivecmd, 'ascii'), (USV_IP, USV_PORT))

                gaindownbutton = joystick.get_button(4)
                text_print.tprint(screen, f"Gain Down: {gaindownbutton}")

                gainupbutton = joystick.get_button(5)
                text_print.tprint(screen, f"Gain Up: {gainupbutton}")

            elif enabled and autonano:
                text_print.tprint(screen, f"Autonano  Enabled!")
            elif enabled and autopix:   
                text_print.tprint(screen, f"Autopix Enabled!")
                
            else:
                 text_print.tprint(screen, f"Disabled!")           
                

            text_print.tprint(screen,"STATUS,time.time,enabled,state,vbat")
            text_print.tprint(screen,"STATE,time.time,lat,lon,hdg,spd,fixtype,port,stbd")
            text_print.tprint(screen,"DESIRED,time.time, trackangle (GPS), dist_to_tgt, brng_to_tgt")
            #data = udpIn.recv(1024)    
            #text_print.tprint(screen, data[:-1])
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    logfile.close()
    pygame.quit()

import cv2
import mediapipe as mp
import pyautogui as pg 
import time 

#create a method to count the fingers within a hand landmark. 
def fingercounter(lst):
    counter = 0 #counts how many fingers have been raised. 
    tv = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2 #threshold value that calculates the distance between the digits of 0 and 9 within your hand landmarks.
    #the reason we multiply the y values by 100 is because they are between 0 and 1.  
    #now create the if statement for if the distance of your finger (5-8, 9-12, 13-16, or 17-20) is greater than the threshold, it means the finger is up (return true)
    '''if (lst.landmark[5].y*100 - lst.landmark[8].y*100 > tv):
        counter += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100 > tv):
        counter += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100 > tv):
        counter += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100 > tv):
        counter += 1
    
    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 5:
        counter += 1'''
    fingerpairs = [(8, 5), (12, 9), (16, 13), (20, 17)]

    for start, end in fingerpairs: 
        if (lst.landmark[end].y*100 - lst.landmark[start].y*100) > tv: #or (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 5: 
            counter += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 4:
        counter += 1

    return counter 

cap = cv2.VideoCapture(0)
drawing = mp.solutions.drawing_utils #gathers the drawing utils for the map.
hands = mp.solutions.hands
hand_obj = hands.Hands() #detects one hand max in the frame, no matter how many there are in the camera (default setting).
#If you want the camera to detect at least one hand, change the max_num_hands limit to a number greater than 1. 
start_init = False
prev = -1 #a variable used to store the previous counter value.
#the purpose of the prev counter is to make sure the number of counted digits isn't continuously processed. 
#this means if a certain number of digits is presented for the counter, the action for the counter won't repeat. 

command_mapping = {
    1: "right",
    2: "left",
    3: "up",
    4: "down",
    5: "space",
}

while True: 
    endtime = time.time()
    _, frame = cap.read() #reading frames from the camera object. it is stored in the frm object 
    frame = cv2.flip(frame, 1) #flip the camera perspective

    res = hand_obj.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) #result, there may or may not be hands in the frame so it may be null sometimes. 

    if res.multi_hand_landmarks: #returns the list of detected hands in the frame. It isn't empty if the lists length is greater than 0, then we're going to get inside the if statement. 
        
        hand_keyPoints = res.multi_hand_landmarks[0]

        #print(fingercounter(hand_keyPoints))
        
        drawing.draw_landmarks(frame,hand_keyPoints, hands.HAND_CONNECTIONS) #going to draw on the frame for one hand, aka the zeroth element in the list. 
        
        counter = fingercounter(hand_keyPoints)

        #using pythonautogui, it will interact with the ui as mouse clicks/web interactions to skip/rewind the video, pause it, or up/minimize the audio. 
        '''if (counter == 1):
            pg.press("right")
            
        elif (counter == 2):
            pg.press("left")
            
        elif (counter == 3):
            pg.press("up")
            
        elif (counter == 4):
            pg.press("down")
            
        elif (counter == 5):
            pg.press("space")'''
        
        #this if statement checks to make sure prev is not equal to counter. If counter changes but prev still holds the previous counter value, the condition
        #is satisified and the pyautogui commands are processed depending on the new counter's value. 
        if not prev == counter:
            if not start_init: #if the start time has not been initialized (it is still false?) then this condition runs. This only runs when start_init is turned false again at the end of a command. This means another command has been made by a different number of digits present. 
                starttime = time.time()
                start_init = True
            elif (endtime - starttime) > 0.2 and counter in command_mapping:
                print(counter)
                pg.press(command_mapping[counter])
                prev = counter
                start_init = False 
            '''elif (endtime - starttime) > 0.2:
                #if the start time has been intialized, the else if method starts. If start_init is True, we give the user greater than 0.2 seconds to let them raise all the fingers and perform operations. 
                if (counter == 1):
                    pg.press("right")
                
                elif (counter == 2):
                    pg.press("left")
                
                elif (counter == 3):
                    pg.press("up")
                
                elif (counter == 4):
                    pg.press("down")
                
                elif (counter == 5):
                    pg.press("space")
                #after the if statement is finished and the command is initiated, prev is now equal to counter, making the if statement false and the gui commands to not repeat. 
                prev = counter
                start_init = False #the command has been intialized, and we are going to restart the operation
        if not prev == counter: 
            if not start_init:
                starttime = time.time()
                start_init = True'''
            
        
        '''for landmarks in res.multi_hand_landmarks:
            drawing.draw_landmarks(frame, landmarks, hands.HAND_CONNECTIONS)
            #this code is for when you want the camera to detect at least two hands.'''

    cv2.imshow("Camera Capture", frame) #shows the frame to the user. 
    
    if cv2.waitKey(1) == ord('k'): 
        cv2.destroyAllWindows() #destroys all windows, including the one showing to the user. 
        cap.release() #release the camera resource so other applications can use it.
        break
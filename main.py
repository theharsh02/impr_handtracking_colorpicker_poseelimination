import tkinter as tk
import pyperclip
import numpy as np
import cv2
import  time
import mediapipe as mp

def pencilimage():
    #Step - 1 - Load Libraries and Image
    #Step - 2 - Converte Image into Gray Scale
    #Step - 3 - Inveted Gary Scale Image [For Shifting toward selected channel] 
    #Step - 4 - Apply Image Smooting For Shading effect
    #Step - 5 - Invert Blur Image and Apply division between gray and invert_blur.
    #------------------------------------------------------------------------------------------------------------------------
    #Step-1
    #Read Image-------------------
    img = cv2.imread("./images.jpeg")
    img = cv2.resize(img,(800,600))

    #Create Trackbar----

    def nothing(x):
        pass

    #window name
    cv2.namedWindow("Color Adjustments",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Color Adjustments", (300, 300)) 
    cv2.createTrackbar("Scale", "Color Adjustments", 0, 255, nothing)
    cv2.createTrackbar("Color", "Color Adjustments", 0, 255, nothing)

    #Step -2
    #Convert into gray--
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    while True:
        scale =  cv2.getTrackbarPos("Scale", "Color Adjustments")
        clr = cv2.getTrackbarPos("Color", "Color Adjustments") #getting track bar value
        
        
        #Extracting Color Code --
        #Step - 3
        inverted_gray =  clr - gray  #inverted color image
        #Step -4
        blur_img = cv2.GaussianBlur(inverted_gray,(21,21),0)
        #Step -5
        inverted_blur = clr - blur_img  #inverted blured image
        fltr = cv2.divide(gray,inverted_blur,scale = scale)
        
        

        #Output-----------------------
        cv2.imshow("opt",fltr)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
        if k == ord("s"):
            cv2.imwrite("res.jpg",fltr)
            
    
    cv2.destroyAllWindows()



def cordinate_color():
    # Load the image
    image = cv2.imread("images.jpeg")

    # Define a function to handle mouse events
    def get_pixel(event, x, y, flags, param):
        # Check if left mouse button was clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            # Get the color at the specified coordinates
            color = image[y, x]

            # Extract the color intensity
            intensity = color[0] if color[0] == color[1] == color[2] else None

            # Extract the RGB values
            b, g, r = color if intensity is None else (intensity, intensity, intensity)

            # Print the color and coordinates
            print("Color at ({}, {}): {}, {}, {}".format(x, y, r, g, b))

            # Copy the RGB values and coordinates to the clipboard
            pyperclip.copy("({}, {}) - ({}, {}, {})".format(x, y, r, g, b))
            print("Copied to clipboard!")

    # Create a window to display the image
    cv2.namedWindow("image")

    # Set the mouse callback function
    cv2.setMouseCallback("image", get_pixel)

    # Display the image
    cv2.imshow("image", image)
    while True:
        k = cv2.waitKey(0)
        if k == ord("q"):
            break
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Define the function to be connected to the buttons
def harsh():
    print("Button clicked!")
def handtracking():
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    print(id, cx, cy)
                    # if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

def pose_Elemination():
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    cap = cv2.VideoCapture('./harsh.mp4')
    pTime = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        # print(results.pose_landmarks)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
# Create the tkinter window
root = tk.Tk()
root.geometry("400x300")

# Create a frame to hold the buttons
frame = tk.Frame(root)
frame.pack(pady=20)

# Create the buttons and connect them to the function
button1 = tk.Button(frame, text="Color Image to Pencil Image", command=pencilimage)
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = tk.Button(frame, text="cordinate , RGB color", command=cordinate_color)
button2.grid(row=1, column=0, padx=10, pady=10)

button3 = tk.Button(frame, text="hands Tracking",command=handtracking)
button3.grid(row=0, column=1, padx=10, pady=10)

button4 = tk.Button(frame, text="pose elemination", command=pose_Elemination)
button4.grid(row=1, column=1, padx=10, pady=10)

# Run the tkinter event loop
root.mainloop()

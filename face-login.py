import cv2
import face_recognition
from playsound import playsound
import subprocess

# Load known face encodings and names
known_face_encodings = []
known_face_names = []

# Load known face and their names here
# Copy for each person you want to "identify"
path = "assets/people/images/"

known_person1_image = face_recognition.load_image_file(path+"kylep.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_face_encodings.append(known_person1_encoding)
known_face_names.append("Kyle P")

known_person1_image = face_recognition.load_image_file(path+"keatp.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_face_encodings.append(known_person1_encoding)
known_face_names.append("Keat P")

known_person1_image = face_recognition.load_image_file(path+"rdj.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_face_encodings.append(known_person1_encoding)
known_face_names.append("Iron Man")

#Iniitlize the webcam
video_capture = cv2.VideoCapture(0)

soundPlayed = False

while True:
    # capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all face locations in frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            if name == "Kyle P" and soundPlayed == False:
                # this is to determine if I can be detected and take an action - POC only
                playsound("assets/sound/beep-6.wav")
                # print(f"Found - Logging in...")
                soundPlayed = True
                subprocess.Popen("loginctl unlock-session `loginctl list-sessions | grep 'seat0' | awk '{print $1}'`", shell=True)
                exit()



        # Draw a box around the face and label with name
        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0,0), 2)

    #Displayt the resulting frame
    # cv2.imshow("Video", frame)

    # # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and cose OpenCV Windows    
video_capture.release() 
cv2.destroyAllWindows()
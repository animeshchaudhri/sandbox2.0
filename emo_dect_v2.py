import cv2
from deepface import DeepFace


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)



while True:
    
    ret, frame = cap.read()

   
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

   
    for (x, y, w, h) in faces:
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

       
        result = DeepFace.analyze(frame[y:y+h, x:x+w], actions=['emotion'], enforce_detection=False)

       
        if result:
            emotion = result[0]["dominant_emotion"]
            txt = str(emotion)
            cv2.putText(frame, txt, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

  
    cv2.imshow('frame', frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

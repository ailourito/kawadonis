import cv2
import face_recognition
import os
import pickle
import sys

def train_face_recognition(training_images_path, model_path):
    if os.path.exists(model_path):
        print("Loading existing model...")
        with open(model_path, 'rb') as f:
            adonis_encodings = pickle.load(f)
    else:
        print("Training new model...")
        adonis_encodings = []
        image_files = os.listdir(training_images_path)
        total_images = len(image_files)

        for i, image_name in enumerate(image_files):
            image_path = os.path.join(training_images_path, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                adonis_encodings.append(encodings[0])
            
            # Print progress in the same line
            progress = f"Processing image {i + 1}/{total_images}..."
            print(progress, end='\r')
            sys.stdout.flush()
        
        # Save the model
        with open(model_path, 'wb') as f:
            pickle.dump(adonis_encodings, f)
        print("\nModel trained and saved.")
    
    return adonis_encodings

def recognize_adonis(image_path, adonis_encodings):
    # Load the image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check for Adonis characteristics
        matches = face_recognition.compare_faces(adonis_encodings, face_encoding)
        name = "Not Adonis"
        color = (0, 0, 255)
        text_color = (255, 255, 255)

        if True in matches:
            name = "Adonis"
            color = (0, 255, 0)
            text_color = (0, 0, 0)

        # Add the box around the face
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)

        # Give a label
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 0.4, text_color, 1)

    # Display the resulting image
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Main execution
if __name__ == "__main__":
    training_images_path = "adonis/"
    model_path = "model/adonis.pkl"
    adonis_img = "media/adonis-1.jpg"
    team_img = "media/adonis-2.jpg"
    not_adonis = "media/not-adonis.jpeg"

    adonis_encodings = train_face_recognition(training_images_path, model_path)
    recognize_adonis(adonis_img, adonis_encodings)
    recognize_adonis(team_img, adonis_encodings)
    recognize_adonis(not_adonis, adonis_encodings)


    
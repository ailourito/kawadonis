import io
from PIL import Image
import cv2
import face_recognition
import numpy as np
import pickle

# Need to confirm that it is adonis
def adonizer(image_path):
    with open('model/adonis.pkl', 'rb') as f:
        adonis_encodings = pickle.load(f)

    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for face_location, face_encoding in zip(face_locations, face_encodings):
        # Check for Adonis characteristics
        matches = face_recognition.compare_faces(adonis_encodings, face_encoding)

        # If there is a match, process the face
        if True in matches:
            # Call kawaii_adonis with the matched face's location
            kawadonis = kawaii_adonis(image, face_location)  # Pass the matched face's location
            return kawadonis

    # No match found for Adonis
    return None


    

def overlay_image(background, overlay, position):
    h, w = overlay.shape[:2]
    y, x = position[1], position[0]

    # Determine the overlay regions that fit within the background boundaries
    y1, y2 = max(0, y), min(background.shape[0], y + h)
    x1, x2 = max(0, x), min(background.shape[1], x + w)

    # Determine the corresponding overlay region to be used
    overlay_y1, overlay_y2 = max(0, -y), min(h, background.shape[0] - y)
    overlay_x1, overlay_x2 = max(0, -x), min(w, background.shape[1] - x)

    # Ensure that the overlay dimensions make sense
    if y1 >= y2 or x1 >= x2 or overlay_y1 >= overlay_y2 or overlay_x1 >= overlay_x2:
        return background  # If the overlay is completely outside, return the background as is

    # Blend the overlay image onto the background
    for c in range(3):  # Loop over the color channels
        alpha = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, 3] / 255.0
        background[y1:y2, x1:x2, c] = (1 - alpha) * background[y1:y2, x1:x2, c] + alpha * overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, c]

    return background


def add_png_hearts(image, face_landmarks, heart_path):
    face_width = face_landmarks['right_eye'][0][0] - face_landmarks['left_eye'][3][0]
    heart_size = int(face_width * 1)  # Adjust this value to change heart size

    # Read the heart PNG
    heart = cv2.imread(heart_path, cv2.IMREAD_UNCHANGED)
    
    if heart is None:
        print(f"Failed to load heart image from {heart_path}")
        return image

    # fix the alpha channel color issue
    if heart.shape[2] == 4: 
        heart = cv2.cvtColor(heart, cv2.COLOR_BGRA2RGBA)

    # Resize the heart
    heart = cv2.resize(heart, (heart_size, heart_size))

    # Calculate positions for hearts
    left_heart_pos = (int(face_landmarks['left_eye'][0][0] - heart_size * 1.5), int(face_landmarks['left_eye'][0][1]))
    right_heart_pos = (int(face_landmarks['right_eye'][3][0] + heart_size * 0.5), int(face_landmarks['right_eye'][3][1]))

    # Overlay hearts
    image = overlay_image(image, heart, left_heart_pos)
    image = overlay_image(image, heart, right_heart_pos)

    return image

def add_blush(image, face_landmarks, blush_path):
    face_width = face_landmarks['right_eye'][0][0] - face_landmarks['left_eye'][3][0]
    blush_size = int(face_width * 1)  # Adjust this value to change blush size

    # Read the blush PNG
    blush = cv2.imread(blush_path, cv2.IMREAD_UNCHANGED)
    
    if blush is None:
        print(f"Failed to load blush image from {blush_path}")
        return image

    # Fix blue blush problem
    if blush.shape[2] == 4:  
        blush = cv2.cvtColor(blush, cv2.COLOR_BGRA2RGBA)

    # Resize the blush
    blush = cv2.resize(blush, (blush_size, blush_size))

    # Calculate positions for blush
    left_eye_bottom = max(point[1] for point in face_landmarks['left_eye'])
    right_eye_bottom = max(point[1] for point in face_landmarks['right_eye'])
    
    left_blush_pos = (int(face_landmarks['left_eye'][0][0]), int(left_eye_bottom + blush_size * 0.2))
    right_blush_pos = (int(face_landmarks['right_eye'][3][0] - blush_size), int(right_eye_bottom + blush_size * 0.2))

    # Check if the face is visible from both sides
    left_side_visible = face_landmarks['left_eye'][0][0] > 0
    right_side_visible = face_landmarks['right_eye'][3][0] < image.shape[1]

    # Overlay blush
    if left_side_visible:
        image = overlay_image(image, blush, left_blush_pos)
    if right_side_visible:
        image = overlay_image(image, blush, right_blush_pos)

    return image


def kawaii_adonis(image, face_location):
    heart_path = "media/heart.png"
    blush_path = "media/blush.png"

    # Read the image
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect face landmarks; wrap face_location in a list
    face_landmarks_list = face_recognition.face_landmarks(image, [face_location])  # Pass a list with one face location

    if not face_landmarks_list:
        print("No face detected in the image.")
        return None

    face_landmarks = face_landmarks_list[0]  # Work with the detected face landmarks

    # Make kawaii
    image = add_png_hearts(image, face_landmarks, heart_path)
    image = add_blush(image, face_landmarks, blush_path)
    image = add_bunny_ears(image, face_landmarks)

    pil = Image.fromarray(image)

    img_io = io.BytesIO()
    pil.save(img_io, format='JPEG', quality=70)
    img_io.seek(0)

    return img_io

def add_bunny_ears(image, face_landmarks):
    bunny_ears_path = "media/ears.png"

    # Load bunny ears image
    bunny_ears = cv2.imread(bunny_ears_path, cv2.IMREAD_UNCHANGED)

    if bunny_ears is None:
        print(f"Failed to load bunny ears image from {bunny_ears_path}")
        return image
    
    # Fix blue color bug
    if bunny_ears.shape[2] == 4:  
        bunny_ears = cv2.cvtColor(bunny_ears, cv2.COLOR_BGRA2RGBA)

    # Get face dimensions and orientation
    left_eye = np.mean(face_landmarks['left_eye'], axis=0)
    right_eye = np.mean(face_landmarks['right_eye'], axis=0)

    # Calculate the angle of the head tilt
    eye_delta_y = right_eye[1] - left_eye[1]
    eye_delta_x = right_eye[0] - left_eye[0]
    head_tilt_angle = np.degrees(np.arctan2(eye_delta_y, eye_delta_x))  # Angle of tilt

    # Print head rotation (before correction)
    print(f"Calculated head tilt angle: {head_tilt_angle:.2f} degrees")

    ears_rotation_angle = head_tilt_angle 


    # Calculate face width and height
    face_width = np.linalg.norm(right_eye - left_eye)
    face_height = np.linalg.norm(face_landmarks['nose_tip'][0] - np.mean([left_eye, right_eye], axis=0))

    # Calculate ear size based on face dimensions
    ear_width = int(face_width * 6)  # Adjust this multiplier as needed
    ear_height = int(ear_width * bunny_ears.shape[0] / bunny_ears.shape[1])

    # Resize bunny ears
    bunny_ears_resized = cv2.resize(bunny_ears, (ear_width, ear_height))


    # Add extra rotation to fix overcome the png empy part
    if head_tilt_angle < 0:
        ears_rotation_angle -= (head_tilt_angle * 1.6)

    # if head_tilt_angle < 0:
    #     ears_rotation_angle += 10

    if head_tilt_angle > 0:
        ears_rotation_angle -= 10    

    # Print the corrected ears rotation angle
    print(f"Corrected ears rotation angle: {ears_rotation_angle:.2f} degrees")

    # Rotate bunny ears based on calculated angle
    rotation_matrix = cv2.getRotationMatrix2D((ear_width // 2, ear_height // 2), ears_rotation_angle, 1)
    bunny_ears_rotated = cv2.warpAffine(bunny_ears_resized, rotation_matrix, (ear_width, ear_height))


    # Calculate position to place the ears on top of the head
    left_edge = min(point[0] for point in face_landmarks['left_eye'])
    right_edge = max(point[0] for point in face_landmarks['right_eye'])
    center_x = (left_edge + right_edge) // 2

    # Calculate the top of the head
    forehead = min(point[1] for point in face_landmarks['left_eyebrow'] + face_landmarks['right_eyebrow'])
    top_head = max(0, forehead - int(face_height * 0.5))

    # Position the bottom of the ears to align with the top of the head
    x = center_x - ear_width // 2 
    y = top_head - ear_height  # Adjust to position the ears above the head

    
    # fix dislocation of ears
    if head_tilt_angle < 0:
        x -= int(face_width/2)

    # Overlay bunny ears on the image
    image = overlay_image(image, bunny_ears_rotated, (x, y))

    return image

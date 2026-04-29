import cv2
import face_recognition
import os
import pickle

def find_encodings(images_dir):
    """
    Reads images from the specified directory, extracts face encodings,
    and returns a list of encodings and their corresponding names.
    Assumes image files are named in the format "Name.jpg" or "Name.png".
    """
    encode_list = []
    class_names = []
    
    # Check if directory exists
    if not os.path.exists(images_dir):
        print(f"Directory '{images_dir}' not found.")
        return encode_list, class_names

    # List all files in the directory
    my_list = os.listdir(images_dir)
    print(f"Total images found: {len(my_list)}")
    
    for cl in my_list:
        # Load image
        img_path = os.path.join(images_dir, cl)
        # Skip directories and non-image files (rudimentary check)
        if os.path.isdir(img_path) or not cl.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        cur_img = cv2.imread(img_path)
        if cur_img is None:
            print(f"Could not read image: {cl}")
            continue
            
        # Convert BGR (OpenCV) to RGB (face_recognition)
        img_rgb = cv2.cvtColor(cur_img, cv2.COLOR_BGR2RGB)
        
        # Get encoding
        # face_encodings returns a list of encodings found in the image
        # We assume there's only one face per image for training
        encodings = face_recognition.face_encodings(img_rgb)
        if encodings:
            encode_list.append(encodings[0])
            # Remove file extension to get the name
            name = os.path.splitext(cl)[0]
            class_names.append(name)
            print(f"Successfully encoded: {name}")
        else:
            print(f"WARNING: No face found in image: {cl}")
            
    return encode_list, class_names

def train_model(images_dir="images", model_save_path="EncodeFile.p"):
    """
    High-level function to orchestrate the encoding process and save results.
    """
    print(f"Starting face encoding process for directory: '{images_dir}'")
    encode_list_known, class_names = find_encodings(images_dir)
    
    if not encode_list_known:
        print("No encodings were generated. Please check your images.")
        return

    # Combine encodings and names
    encode_list_known_with_ids = [encode_list_known, class_names]
    
    print(f"Encoding complete for {len(class_names)} faces. Saving to file...")
    
    # Save the encodings and names to a pickle file
    with open(model_save_path, 'wb') as file:
        pickle.dump(encode_list_known_with_ids, file)
        
    print(f"Encodings saved successfully to '{model_save_path}'!")

if __name__ == "__main__":
    # Define the directory where images are stored
    images_folder = "images"
    
    # Create the images directory if it doesn't exist
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
        print(f"Created '{images_folder}' directory.")
        print(f"Please add training images (e.g., 'John_Doe.jpg') to the '{images_folder}' folder and run again.")
    else:
        # Run training
        train_model(images_dir=images_folder, model_save_path="EncodeFile.p")

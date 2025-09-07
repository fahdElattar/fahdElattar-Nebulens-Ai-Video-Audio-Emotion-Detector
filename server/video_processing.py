import os
import cv2
import numpy as np
import shutil

############ Upload Folder Clearance ############

def clear_upload_folder(upload_folder):
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

############ Sample Extraction ############

def extract_frames(video_path, frames_folder):
    cap = cv2.VideoCapture(video_path)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(frames_folder, f"frame_{count:04d}.png")
        cv2.imwrite(frame_path, frame)
        count += 1
    cap.release()
    return count

def detect_and_resize_faces(frames_folder, resized_faces_folder, face_cascade_path, target_size=(64, 64)):
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.startswith('frame_')])

    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        img = cv2.imread(frame_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = img[y:y+h, x:x+w]
            resized_face = cv2.resize(face, target_size)
            face_file_path = os.path.join(resized_faces_folder, frame_file)
            cv2.imwrite(face_file_path, resized_face)
            break

def select_most_changed_frames(resized_faces_folder, video_name, target_frames=40):
    frame_files = sorted([f for f in os.listdir(resized_faces_folder) if f.startswith('frame_')])

    if len(frame_files) < target_frames:
        print(f"Error: Only {len(frame_files)} frames available, less than the required {target_frames}.")
        return

    filtered_frames_folder = os.path.join(os.path.dirname(resized_faces_folder), video_name)
    os.makedirs(filtered_frames_folder, exist_ok=True)

    frames = [cv2.imread(os.path.join(resized_faces_folder, f)) for f in frame_files]
    
    differences = []
    for i in range(1, len(frames)):
        diff = cv2.absdiff(frames[i], frames[i - 1])
        diff_sum = np.sum(diff)
        differences.append((diff_sum, i))

    differences.sort(reverse=True, key=lambda x: x[0])
    selected_indices = [0] + [index for _, index in differences[:target_frames - 1]]

    for idx, frame_index in enumerate(selected_indices):
        src_path = os.path.join(resized_faces_folder, frame_files[frame_index])
        dst_path = os.path.join(filtered_frames_folder, f"frame_{idx:04d}.png")
        shutil.copy(src_path, dst_path)

    print(f"{target_frames} frames with the most changes have been copied to {filtered_frames_folder}.")

    for folder in os.listdir(os.path.dirname(resized_faces_folder)):
        folder_path = os.path.join(os.path.dirname(resized_faces_folder), folder)
        if os.path.isdir(folder_path) and folder != video_name:
            shutil.rmtree(folder_path)

def process_video(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frames_folder = os.path.join(os.path.dirname(video_path), video_name, "frames")
    resized_faces_folder = os.path.join(os.path.dirname(video_path), video_name, "resized_faces")

    os.makedirs(frames_folder, exist_ok=True)
    os.makedirs(resized_faces_folder, exist_ok=True)

    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

    total_frames = extract_frames(video_path, frames_folder)
    detect_and_resize_faces(frames_folder, resized_faces_folder, face_cascade_path)
    select_most_changed_frames(resized_faces_folder, video_name, target_frames=40)

def extract_and_preprocess_frames(frames_folder, target_size=(64, 64)):
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.startswith('frame_')])
    frames = []

    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        img = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
        img_resized = cv2.resize(img, target_size)
        img_normalized = img_resized / 255.0
        frames.append(img_normalized)

    frames_array = np.array(frames).reshape(1, 40, 64, 64, 1)
    return frames_array
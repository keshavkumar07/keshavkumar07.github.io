import cv2
import os
import json
import base64
import numpy as np

IMAGES_DIR = "Images"
MODEL_PATH = "model.yml"
LABELS_PATH = "labels.json"
FACE_SIZE = (200, 200)

_face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def _decode_image(image_b64):
    """Accepts a data URL ('data:image/jpeg;base64,...') or raw base64 string."""
    if "," in image_b64:
        image_b64 = image_b64.split(",", 1)[1]
    img_bytes = base64.b64decode(image_b64)
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def _largest_face(gray):
    """Detect faces and return the biggest one, cropped/resized/normalized."""
    faces = _face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
    )
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    face = gray[y:y + h, x:x + w]
    face = cv2.resize(face, FACE_SIZE)
    face = cv2.equalizeHist(face)
    return face


def enroll_face(name, images_b64):
    """images_b64: list of base64 frames captured in the browser for one person."""
    name = (name or "").strip()
    if not name:
        return False, "Please enter a name."

    person_dir = os.path.join(IMAGES_DIR, name)
    os.makedirs(person_dir, exist_ok=True)
    start_index = len(os.listdir(person_dir))

    saved = 0
    for b64 in images_b64:
        img = _decode_image(b64)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = _largest_face(gray)
        if face is None:
            continue
        path = os.path.join(person_dir, f"img_{start_index + saved + 1}.jpg")
        cv2.imwrite(path, face)
        saved += 1

    if saved == 0:
        return False, "No face detected in the captured frames. Face the camera directly with good lighting."

    train_model()
    return True, f"{name} enrolled with {saved} face sample(s). Model retrained."


def train_model():
    """Rebuild the LBPH model from every photo under Images/<name>/."""
    faces, labels, label_names = [], [], {}

    if not os.path.isdir(IMAGES_DIR):
        return False

    label_id = 0
    for person in sorted(os.listdir(IMAGES_DIR)):
        person_dir = os.path.join(IMAGES_DIR, person)
        if not os.path.isdir(person_dir):
            continue

        had_sample = False
        for fname in os.listdir(person_dir):
            img = cv2.imread(os.path.join(person_dir, fname), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(cv2.resize(img, FACE_SIZE))
            labels.append(label_id)
            had_sample = True

        if had_sample:
            label_names[label_id] = person
            label_id += 1

    if not faces:
        return False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)

    with open(LABELS_PATH, "w") as f:
        json.dump(label_names, f)

    return True


def recognize_face(image_b64, threshold=75.0):
    """Returns (name, confidence, error_message). Lower LBPH confidence = better match."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
        return None, 0, "No one is enrolled yet. Enroll at least one face first."

    img = _decode_image(image_b64)
    if img is None:
        return None, 0, "Could not read the captured image."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = _largest_face(gray)
    if face is None:
        return None, 0, "No face detected. Face the camera directly with good lighting."

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    with open(LABELS_PATH) as f:
        label_names = json.load(f)

    label_id, confidence = recognizer.predict(face)
    if confidence > threshold:
        return None, confidence, "Face not recognized. Move closer with even lighting, or enroll first."

    name = label_names.get(str(label_id), "Unknown")
    return name, confidence, None

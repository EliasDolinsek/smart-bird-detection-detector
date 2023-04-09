import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, storage
import uuid

import cv2

DEFAULT_FILE_PATH = "image.jpg"

cred = credentials.Certificate('smart-bird-detection-firebase.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'smart-bird-detection-87b33.appspot.com'
})
bucket = storage.bucket()

def take_and_write_picture(file_path):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(file_path, frame)


def upload_file(path):
    blob = bucket.blob(str(uuid.uuid4()) + ".txt")
    blob.upload_from_filename(path)
    return blob.public_url


def add_detection(species, file_url):
    db = firestore.client()
    birds_document_ref = db.collection("birds").document()
    birds_document_ref.set({
        "species_name": species,
        "detection_timestamp": datetime.now(),
        "image_url": file_url
    })


take_and_write_picture(DEFAULT_FILE_PATH)
image_url = upload_file(DEFAULT_FILE_PATH)
os.remove(DEFAULT_FILE_PATH)

add_detection("Amsel", image_url)

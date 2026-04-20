# analyse_video.py
import cv2
import sys
import os


def charger_video(chemin_video):
    if not os.path.exists(chemin_video):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_video}")

    cap = cv2.VideoCapture(chemin_video)
    if not cap.isOpened():
        raise ValueError(f"Impossible d'ouvrir la vidéo : {chemin_video}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    nb_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    largeur = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hauteur = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duree = round(nb_frames / fps, 2) if fps > 0 else 0

    print(f"Vidéo chargée : {chemin_video}")
    print(f"  Résolution : {largeur}x{hauteur}")
    print(f"  FPS : {fps}")
    print(f"  Nombre de frames : {nb_frames}")
    print(f"  Durée estimée : {duree}s")

    return cap, fps, nb_frames



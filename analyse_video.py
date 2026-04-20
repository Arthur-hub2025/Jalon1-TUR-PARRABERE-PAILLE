import cv2
import sys
import os
import json
import mediapipe as mp


def extraire_bbox(detection, frame_w, frame_h):
    bbox = detection.location_data.relative_bounding_box
    return {
        "x": int(bbox.xmin * frame_w),
        "y": int(bbox.ymin * frame_h),
        "width": int(bbox.width * frame_w),
        "height": int(bbox.height * frame_h),
        "score": round(detection.score[0], 3)
    }


def detecter_visages(chemin_video, dossier_sortie="output"):
    os.makedirs(dossier_sortie, exist_ok=True)

    cap = cv2.VideoCapture(chemin_video)
    if not cap.isOpened():
        raise ValueError(f"Impossible d'ouvrir : {chemin_video}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detector = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)
    resultats = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        bbox = None
        if results.detections:
            meilleure = max(results.detections, key=lambda d: d.score[0])
            bbox = extraire_bbox(meilleure, frame_w, frame_h)

        resultats.append({
            "frame": frame_idx,
            "timestamp": round(frame_idx / fps, 4),
            "face_detected": bbox is not None,
            "bbox": bbox
        })

        frame_idx += 1

    cap.release()
    detector.close()

    chemin_sortie = os.path.join(dossier_sortie, "detection_visage.json")
    with open(chemin_sortie, "w") as f:
        json.dump({"fps": fps, "frames": resultats}, f, indent=2)

    print(f"{frame_idx} frames — sauvegardé : {chemin_sortie}")


if __name__ == "__main__":
    chemin = sys.argv[1] if len(sys.argv) > 1 else "test.mp4"
    detecter_visages(chemin)
from .Class.camera import camera

if __name__ == "__main__":
    plant_classifier = camera.PlantClassifier()

    try:
        while True:
            results = plant_classifier.detect_and_classify()
            if results:  # Stop if detection is made
                print("Detections:", results)
                break  # Exit the loop
    finally:
        plant_classifier.stop()

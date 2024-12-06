import torch
import cv2
from torchvision import models, transforms
from PIL import Image
from picamera2 import Picamera2, Preview

class PlantClassifier:
    def __init__(self, detection_model_path='ultralytics/yolov5', classification_model_path='fine_tuned_mobilenetv2.pth'):
        # Load YOLOv5 for object detection
        self.yolo_model = torch.hub.load(detection_model_path, 'yolov5s')
        
        # Load MobileNetV2 for classification
        self.classification_model = models.mobilenet_v2(pretrained=False)
        num_ftrs = self.classification_model.classifier[1].in_features
        self.classification_model.classifier[1] = torch.nn.Linear(num_ftrs, 2)  # Modify last layer for 2 classes
        self.classification_model.load_state_dict(torch.load(classification_model_path))
        self.classification_model.eval()  # Set to evaluation mode

        # Labels for classification
        self.finetuned_labels = ["golden", "ribbon"]

        # Preprocessing for MobileNetV2
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # Initialize Picamera2
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": (1280, 720)})
        self.picam2.configure(config)
        self.picam2.start_preview(Preview.QTGL)  # Optional preview
        self.picam2.start()

    def detect_and_classify(self):
        # Capture a frame from the camera
        frame = self.picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Run YOLOv5 inference on the frame
        detection_results = self.yolo_model(frame_bgr)

        # Extract labels from detection results
        labels = detection_results.names
        detections = detection_results.xyxy[0]
        results = []

        # Loop through detections
        for detection in detections:
            class_id = int(detection[5])  # Class index
            if labels[class_id] == "potted plant":
                x1, y1, x2, y2 = map(int, detection[:4])  # Bounding box
                cropped_img = frame_bgr[y1:y2, x1:x2]

                # Convert cropped image for classification
                pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
                input_tensor = self.preprocess(pil_img).unsqueeze(0)  # Add batch dimension

                # Perform classification
                with torch.no_grad():
                    output = self.classification_model(input_tensor)
                _, predicted = torch.max(output, 1)
                predicted_label = self.finetuned_labels[predicted.item()]

                # Append results
                results.append({
                    "bounding_box": (x1, y1, x2, y2),
                    "label": predicted_label
                })

                # Draw results on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, predicted_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

                # Display the frame
                cv2.imshow('YOLO Object Detection and Classification', frame)
                return results  # Return results immediately after detection

        # Display the frame without detection
        cv2.imshow('YOLO Object Detection and Classification', frame)
        return None

    def stop(self):
        self.picam2.stop()
        cv2.destroyAllWindows()

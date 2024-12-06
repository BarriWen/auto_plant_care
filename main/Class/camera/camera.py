import torch
import cv2
from torchvision import models, transforms
from PIL import Image
from picamera2 import Picamera2

class PlantClassifier:
    def __init__(self, detection_model_path='./yolov5', classification_model_path='fine_tuned_mobilenetv2.pth'):
        # Load YOLOv5 for object detection
        self.yolo_model = torch.hub.load(detection_model_path, 'custom', path='yolov5s.pt', source='local', force_reload=True)
        
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
        config = self.picam2.create_preview_configuration(main={"size": (640, 360)})
        self.picam2.configure(config)
        self.picam2.start()

    def detect_and_classify(self):
        try:
            while True:
                # Capture a frame from the camera
                frame = self.picam2.capture_array()
                # cv2.imshow("preview", frame)
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # Run YOLOv5 inference on the frame
                detection_results = self.yolo_model(frame_bgr)

                # Extract the labels (object categories) from the YOLOv5 detection results
                labels = detection_results.names
                detections = detection_results.xyxy[0]

                # Loop through all detections and filter for 'potted plant'
                for i, detection in enumerate(detections):
                    class_id = int(detection[5])  # Class index is at position 5 for YOLOv5
                    if labels[class_id] == "potted plant":
                        # Get the bounding box coordinates for the potted plant
                        x1, y1, x2, y2 = map(int, detection[:4])
                        
                        # Crop the potted plant region from the frame
                        cropped_img = frame_bgr[y1:y2, x1:x2]

                        # Convert the cropped image to PIL format for classification
                        pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))

                        # Preprocess the image for MobileNetV2
                        input_tensor = self.preprocess(pil_img).unsqueeze(0)  # Add batch dimension

                        # Perform classification
                        with torch.no_grad():
                            output = self.classification_model(input_tensor)
                        
                        # Get the predicted class label from the output
                        _, predicted = torch.max(output, 1)
                        predicted_label = self.finetuned_labels[predicted.item()]
                        return predicted_label

                # Display the frame (with or without detection overlay)
                cv2.imshow('YOLO Object Detection and Classification', frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return None
        finally:
            self.picam2.stop()
            cv2.destroyAllWindows()


import torch
import cv2
from torchvision import models, transforms
from PIL import Image

# Load a pre-trained YOLOv5 model for object detection
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Load a pre-trained MobileNetV2 model for classification
classification_model = models.mobilenet_v2(pretrained=False)
num_ftrs = classification_model.classifier[1].in_features
classification_model.classifier[1] = torch.nn.Linear(num_ftrs, 2)  # Modify last layer for 2 classes

# Load fine-tuned weights
classification_model.load_state_dict(torch.load('fine_tuned_mobilenetv2.pth'))
classification_model.eval()  # Set the model to evaluation mode

# Download and load the ImageNet labels
finetuned_labels = ["golden", "ribbon"]

# Initialize webcam feed (0 is the default camera, change if using a different one)
cap = cv2.VideoCapture(0)

# Set the frame width and height (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Image transformations for the classification model
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

while cap.isOpened():
    # Capture each frame
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv5 inference on the frame
    detection_results = yolo_model(frame)

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
            cropped_img = frame[y1:y2, x1:x2]

            # Convert the cropped image to PIL format for classification
            pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))

            # Preprocess the image for MobileNetV2
            input_tensor = preprocess(pil_img).unsqueeze(0)  # Add batch dimension

            # Perform classification
            with torch.no_grad():
                output = classification_model(input_tensor)
            
            # Get the predicted class label from the output
            _, predicted = torch.max(output, 1)
            print(predicted)
            predicted_label = finetuned_labels[predicted.item()]

            # Print or display the classification result
            print(f"Classified as: {predicted_label}")

            # Draw the bounding box and the classification label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, predicted_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    # Display the frame (with or without detection overlay)
    cv2.imshow('YOLO Object Detection and Classification', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
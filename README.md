# Auto_Plant_Care

The objective of this project is to create a smart irrigation system (ideally for single/small quantities of landscape/greenery plants or potted plants) using Raspberry Pi 5(support/set camera)and Raspberry Pi Pico (set up various other sensors). The system includes a variety of environmental monitoring and automation features.

The system will continuously monitor soil moisture levels and ambient temperature using humidity and temperature sensors to ensure that plants are watered only when needed according to optimal conditions. A camera will be configured to identify the specific type of plant, configure the relevant watering and lighting plans (linked to the functions of the other two sensors), and also monitor the condition of the plants in real-time. The light/infrared sensor will track the sunlight exposure, use covers to prevent plants from drought and adjust the watering plan according to the light conditions and plant needs. Based on the plant-related data detected by the above-mentioned sensors, such as the daily height of the plant, growth changes, and the impact of light and watering conditions, the system will calculate and simulate the growth of the plant and display it in a visual form on the configured screen (or page). Wireless/Bluetooth control will also be used in the system, and people can remotely control any device in the system through security checks/inputs at any time to deal with all possible situations. Team members will use Raspberry Pi Pico, various sensors, cameras, and robotic arms to design and build the most suitable software/hardware system.

With the help of this system, plants will receive more detailed watering and a more suitable growth environment; people can intuitively see the growth status of plants and even related predictions, all of which make the process of cultivating and caring for plants more convenient and quick.


### Prerequisites

- Ensure you have Python3 installed.
- A terminal or command-line interface to execute the commands.

### Setup Instructions

To ensure this project runs smoothly, please install all dependencies in the Raspberry Pi's global environment. Using a virtual environment may cause issues with accessing the Pi camera and OpenCV.



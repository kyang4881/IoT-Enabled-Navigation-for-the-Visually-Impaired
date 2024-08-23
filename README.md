## VisionRail: IoT-Enabled Navigation for the Visually Impaired

<p align="center">
  <img src="https://github.com/kyang4881/IoT-Enabled-Navigation-for-the-Visually-Impaired/blob/main/media/profile.png" width="1200" />
</p>

---

VisionRail is a wearable device that utilizes a network of sensors and IoT devices to provide visually impaired individuals with real-time navigational assistance. The device offers four primary functions:

1. Route Planning Assistance: Similar to Google Maps, VisionRail allows users to input their destination via audio commands and provides guidance on which train to take.
2. Navigational Assistance: VisionRail instructs users when to turn, stop, or continue walking, helping them navigate through stations confidently.
3. AI Assistant: The AI assistant within VisionRail responds to specific user queries, providing additional information about the surroundings.
4. Obstacle Detection: The device alerts users to obstacles in their path, ensuring a safer navigation experience.

---

### Sensor Integration
VisionRail's design incorporates ultrasonic sensors and Microbits installed in the wearable device. These sensors continuously send out radio signals to detect obstacles and provide directional cues based on the user's location. Additional Microbits are placed at key tactile pavement areas to signal changes in direction, with the data transmitted to a backend server for processing.

### Topology Design
Given the expansive environment of MRT stations, VisionRail employs a tree topology for data communication. This topology ensures efficient data flow from various points within the station to the backend server, allowing for accurate and timely navigation assistance.

### User Positioning and Navigation
To provide accurate navigation, VisionRail uses triangulation-based positioning, supported by strategically placed beacons at critical points within the MRT station. These beacons communicate with the user's wearable device to pinpoint their location and provide precise audio prompts.

### AI Assistant
The AI assistant within VisionRail is powered by the zephyr-7b-alpha model, a fine-tuned variant of Mistral 7b. The assistant utilizes LangChain and RAG (Retrieval Augmented Generation) techniques to provide real-time information and personalized assistance based on the user's queries. The data for the AI assistant is sourced from SMRT's station information, ensuring that users receive relevant and up-to-date information.

---
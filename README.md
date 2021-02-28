# Project: Soil Sensor
Out of curiousity and fun, I designed, build and coded a device that constantly measures the soil value of the ground. These values are every minute sent to the cloud over WiFi and stored in a SQL database. The communication protocol between the device and the database are handled by a MQTT broker. All components are running in a separate Docker container on a local NAS. 

In the figure below, the architecture of this project is visualized. 
![Uploading IMG_1965.jpeg…]()

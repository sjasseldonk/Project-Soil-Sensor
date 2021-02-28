# Project: Soil Sensor
Out of curiousity and fun, I designed, build and coded a device that constantly measures the soil value of the ground. Every minute, these sensor values are sent, through a MQTT broker and a selfwritten Python script (container 1 + 2), to a SQL database (container 3). The communication between the soil sensor and the Python script are handled by a MQTT broker. A separate Docker container deploys a web application (container 4) that is connected with the database to display the sensor values real-time. All components are running in a separate Docker container on a local NAS. This makes the architecture scalable, for example, I can simply add more soil sensors and store the values in the SQL database. 

In the figure below, the architecture of this project is visualized. 
![alt text](../master/architecture.jpeg)



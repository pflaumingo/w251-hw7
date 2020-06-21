# w251-hw3

For the broker containers, this project just used a pre-built eclipse-mosquitto alpine image because the broker is simply a pass through for the data and this solved the need while keeping the image very lean. For the other containers, a Dockerfile has been created that contains the files necessary to fetch and install the packages necessary for each distribution.

The current setup requires remoting into the edge device (Jetson) and building/running the docker containers, as well as doing something similar on the cloud VM. Ideally some bash scripts would be created to simplify this step. Additionally, the paths are hardcoded (i.e. path where the cloud object storage is mounted).

For this project a Quality of Serivce of 0 was used as there wasn't any concern if there was some loss of data a topic of just facial_images was used for simplicity because there was only one edge device and no intention to scale up. That said, should data loss and security be of concern, a QoS of a higher level (1 or 2) could be used. Moreover, if various edge devices were connected then perhaps a topic naming scheme with an extra layer denoting the edge device name or location would be beneficial. Each image was saved with a filename related to the timestamp - given the FPS on my camera there wasn't a concern that two images would have the same timestamp.

**Note the very small files in the object store are not images, but just test text messages saved as bytes**

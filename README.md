## **Job Prepr - UI**

The UI part of JobPrepr, the platform that helps you prepare for your next job interview.

### **1. Description**

This repo hosts the code for the front-end part of our application. We built it with Streamlit (and added some of our own CSS), an open source Python framework. In order to be able to use the Webcam to capture audio and video, we integrated webrtc, a Streamlit plugin. We take the input from our audio and video and send it to out APIs (which are built in the repo Job Prepr Model, link at the end)

### **2. How to run this yourself**

Running the UI part of the project (without any of the interview functionalities) is very simple. Just clone the repo, install all the requirements found in requirements.txt and run “streamlit run Home.py” from your terminal. This should open a browser window on a local port where you will be able to see the Streamlit website.

In order to get the full functionality, you will have to do two things:

- Set up a PostgreSQL database and connect to it
  - We used GCP for this, but you can use anything else, just make sure to modify the db\_connect.py file to suit your needs.
  - We stored all database connection credentials in our secrets.toml, a streamlit functionality similar to a .env file
- Set up our APIs, the guide on how to do this can be found in the complementary directory

### **3. Credits and contact**

For any questions, concerns or curiosities, please get in touch at:

- andrei.c.danila@gmail.com

Authors of this project:

- Milica Scepanovicka
- Martin Skalicky
- Huw Barber
- Andrei Danila

### **4. Useful links**

- The model part: <https://github.com/skoooty/job-prepr-model>
- Streamlit: <https://streamlit.io/>
- WebRTC: <https://blog.streamlit.io/how-to-build-the-streamlit-webrtc-component/>

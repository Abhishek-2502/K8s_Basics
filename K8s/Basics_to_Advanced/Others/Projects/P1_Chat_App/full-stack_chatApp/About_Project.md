## 📝 Introduction:

This project aims to provide a real-time chat experience that's both scalable and secure. With a focus on modern technologies, we're building an application that's easy to use and maintain.


## Detailed Workflow Description:


![image](https://github.com/user-attachments/assets/f845a188-8e70-42f7-8577-30af38e83053)


  - **User Interaction:**
    - Users interact with the frontend application running in their browser. This includes actions like logging in, sending messages, and navigating through the chat interface.Frontend (React App):The frontend is responsible for rendering the user interface and handling user inputs.It communicates with the backend via HTTP requests (for RESTful APIs) and WebSocket connections (for real-time interactions).

    - **Backend (Node.js/Express + Socket.io):**
       - The backend handles all the server-side logic.It processes API requests from the frontend to perform actions such as user authentication, message retrieval, and message storage.Socket.io is used to manage real-time bi-directional communication between the frontend and the backend. This allows for instant messaging features, such as showing when users are typing or when new messages are sent.


    - **MongoDB (Database):**
       - MongoDB stores all persistent data for the application, including user profiles, chat messages, and any other relevant data.The backend interacts with MongoDB to retrieve, add, update, or delete data based on the requests it receives from the frontend.




## ✨ Features:


* **Real-time Messaging**: Send and receive messages instantly using Socket.io 
* **User Authentication & Authorization**: Securely manage user access with JWT 
* **Scalable & Secure Architecture**: Built to handle large volumes of traffic and data 
* **Modern UI Design**: A user-friendly interface crafted with React and TailwindCSS 
* **Profile Management**: Users can upload and update their profile pictures 
* **Online Status**: View real-time online/offline status of users 


## 🛠️ Tech Stack:


* **Backend:** Node.js, Express, MongoDB, Socket.io
* **Frontend:** React, TailwindCSS
* **Containerization:** Docker
* **Orchestration:** Kubernetes (planned)
* **Web Server:** Nginx
* **State Management:** Zustand
* **Authentication:** JWT
* **Styling Components:** DaisyUI


## 🔧 Prerequisites:


* **[Node.js](https://nodejs.org/)** (v14 or higher)
* **[Docker](https://www.docker.com/get-started)** (for containerizing the app)
* **[Git](https://git-scm.com/downloads)** (to clone the repository)


## 📝 Setup .env File:


1. Navigate to the `backend` directory:
```bash
cd backend
```
2. Create a `.env` file and add the following content (modify the values as needed):
```env
MONGODB_URI=mongodb://mongoadmin:secret@mongodb:27017/dbname?authSource=admin
JWT_SECRET=your_jwt_secret_key
PORT=5001
```
> **Note:** Replace `your_jwt_secret_key` with a strong secret key of your choice.

### Clone the Repository

```bash
git clone https://github.com/iemafzalhassan/full-stack_chatApp.git
```

## 🏗️ Build and Run the Application"

Follow these steps to build and run the application:

1. Build & Run the Containers:

```bash
cd full-stack_chatApp
```
```bash
docker-compose up -d --build
```

2. Access the application in your browser:

```
http://localhost
```
---

## 🛠️ Getting Started

Follow these simple steps to get the project up and running on your local Host using docker.

```bash
git clone https://github.com/iemafzalhassan/full-stack_chatApp.git
```

```bash
cd full-stack_chatApp
```
## Create a Docker network:

```bash
docker network create full-stack
```

## 🛠️ Building the Frontend

```bash
cd frontend
```

```bash
docker build -t full-stack_frontend .
```

### Run the Frontend container:

```bash
docker run -d --network=full-stack  -p 5173:5173 --name frontend full-stack_frontend:latest
```
#### The frontend will now be accessible on port 5173.


### Run the MongoDB Container:

```bash
docker run -d -p 27017:27017 --name mongo mongo:latest
```
---

## 🛠️ Building the Backend

```bash
cd backend
```

### Build the Backend image:

```bash
docker build -t full-stack_backend .
```

### Run the Backend container:

```bash
docker run -d --network=full-stack --add-host=host.docker.internal:host-gateway -p 5001:5001 --env-file .env full-stack_backend

```
#### This will build and run the backend container, exposing the backendAPI on port 5001.

`Backend API: http://localhost:5001`

### To Verify the conncetion between backend and databse:
```bash
docker-compose logs -f
```

### Once the backend and frontend containers are running, you can access the application in your browser:

`Frontend: http://localhost`


You can now interact with the real-time chat app and start messaging!

---

## 📚 Project Snapshots:

![Settings](frontend/public/settings.png)

![chat](frontend/public/chat.png)

![logout](/frontend/public/logout.png)

![Login](/frontend/public/login.png)



## 📜 License


This project is licensed under the MIT License. See the LICENSE file for more details.
# 3D Virtual Tour Platform

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![React](https://img.shields.io/badge/React-18-blue?logo=react&logoColor=white)](https://react.dev/)
[![Three.js](https://img.shields.io/badge/Three.js-Graphics-black?logo=threedotjs&logoColor=white)](https://threejs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Node.js](https://img.shields.io/badge/Node.js-Backend-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)

An immersive, web-based 3D virtual tour application that enables users to explore physical locations through interactive 360-degree panoramic scenes. Built using Three.js and React Three Fiber, it features smooth viewport transitions, customizable interactive hotspots, custom maps, and a responsive portal for property managers.

---

## 🔗 System Architecture

```
+--------------------------------------------------------+
|                     Three.js Canvas                    |
|             (React Three Fiber / OrbitControls)        |
+---------------------------+----------------------------+
                            | Interactive Hotspots & Mesh
                            v
+---------------------------+----------------------------+
|                       React Web Portal                 |
+---------------------------+----------------------------+
                            | JWT / REST APIs
                            v
+---------------------------+----------------------------+
|                    Express & Node.js API               |
+---------------------------+----------------------------+
                            | Mongoose ODM
                            v
+---------------------------+----------------------------+
|                     MongoDB Database                   |
|              (Panoramas, coordinates, metadata)        |
+--------------------------------------------------------+
```

---

## ⚡ Features

- **Interactive 360° Panoramic Scenes**: Uses spherical mapping to project high-resolution equirectangular images inside a 3D skybox sphere.
- **Hotspot-Based Transitions**: Clickable 3D mesh indicators positioned in the sphere allowing users to jump between connected rooms/scenes.
- **Smooth Orbit Camera Controls**: Implements inertia and boundary restrictions on zoom and pitch to ensure user comfort.
- **Admin Tour Builder**: Interactive dashboard allowing managers to upload panoramas, place hotspot meshes visually, customize titles, and link scenes together.
- **Fast Loading & Optimization**: Implements progressive loading, image compression pipelines, and WebGL asset caching.

---

## 💻 Tech Stack

- **Graphics & Frontend**: Three.js, React Three Fiber (R3F), @react-three/drei, React, Tailwind CSS
- **Backend API**: Node.js, Express.js
- **Database**: MongoDB (Mongoose ORM)
- **Asset Storage**: AWS S3 (for high-resolution 360 images)

---

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 18+
- MongoDB

### Step 1: Clone the Repository
```bash
git clone https://github.com/Manish-111913/Virtual-Tour-3D.git
cd Virtual-Tour-3D
```

### Step 2: Configure Server Backend
1. Navigate to server:
   ```bash
   cd backend
   ```
2. Create a `.env` file:
   ```env
   PORT=5000
   MONGO_URI=mongodb://localhost:27017/virtual_tours
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_BUCKET_NAME=virtual-tour-panoramas
   JWT_SECRET=your_jwt_signing_key
   ```
3. Install and run:
   ```bash
   npm install
   npm run dev
   ```

### Step 3: Configure Frontend Client
1. Navigate to client:
   ```bash
   cd ../client
   ```
2. Install and run:
   ```bash
   npm install
   npm run dev
   ```

---

## 📂 Folder Structure

```
Virtual-Tour-3D/
├── backend/
│   ├── src/
│   │   ├── config/         # MongoDB and AWS connections
│   │   ├── controllers/    # Tour, Scene, and Hotspot management
│   │   ├── models/         # Tour models (linking multiple Scenes)
│   │   └── routes/         # REST API mounts
│   ├── package.json
│   └── server.js
├── client/
│   ├── public/             # Fallback assets and icons
│   ├── src/
│   │   ├── components/     # ThreeCanvas.jsx, HotspotMesh.jsx, UI Overlay
│   │   ├── pages/          # TourViewer, AdminDashboard, Login
│   │   └── api/            # API call helpers
│   └── package.json
├── README.md
└── architecture.png
```

---

## 🚀 Future Improvements

- Add WebXR support to make the tours fully compatible with VR headsets (Meta Quest, Apple Vision Pro).
- Integration of spatial audio (Web Audio API) to dynamically change environmental sounds based on the user's camera rotation and zoom.

---

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

# AI-Powered Jewelry Design Generation System

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![MERN](https://img.shields.io/badge/MERN-Stack-47A248)](https://mongodb.com/)

A generative deep learning system that turns hand-drawn jewelry sketches into realistic, high-fidelity 3D-like jewelry product designs. Powered by a **Pix2Pix Conditional Generative Adversarial Network (cGAN)** built on TensorFlow and integrated with a MERN web application, it allows designers to rapidly prototype concepts.

---

## 🔗 Deep Learning Workflow

```
+------------------+       +-------------------+       +------------------+
| Designer Sketch  | ----> |   Pre-processor   | ----> | Pix2Pix GAN      |
| (Web Canvas / UI)|       | (OpenCV Contours) |       | (Generator Model)|
+------------------+       +-------------------+       +--------+---------+
                                                                |
+------------------+       +-------------------+                v
| Render Saved in  | <---- | Interactive UI    | <------------+ (Generates 3D
| MongoDB Gallery  |       | (Product Designer)|              |  Realistic Design)
+------------------+       +-------------------+              +------------------+
```

---

## ⚡ Features

- **Conditional GAN Architecture (Pix2Pix)**: Utilizes a U-Net based Generator and PatchGAN Discriminator trained on a curated dataset of jewelry sketches and product renderings.
- **Interactive Web Canvas**: Draw, edit, and crop jewelry templates directly in the browser using HTML5 Canvas.
- **Real-Time Inference Pipeline**: Translates raw drawing strokes into high-fidelity gold, silver, and gem rendering outputs in seconds.
- **OpenCV Image Processing**: Normalizes sketches, enhances boundaries, and extracts clean contours to feed into the tensor pipeline.
- **Design Dashboard Gallery**: Save generation histories, tag designs with categories, and export high-resolution assets for fabrication.

---

## 💻 Tech Stack

- **Model & Processing**: TensorFlow, Python, Keras, NumPy, OpenCV
- **Web Portal**: React.js, Tailwind CSS
- **Backend API**: Node.js, Express.js (Orchestrates calls to Python flask inference service)
- **Database**: MongoDB (Stores design catalogs, configurations, and metadata)

---

## 🛠️ Model Training & Local Setup

### Prerequisites
- Python 3.9+ with CUDA configured (for GPU-accelerated model training/inference)
- Node.js 18+
- MongoDB

### Step 1: Clone the Repository
```bash
git clone https://github.com/Manish-111913/AI-Jewelry-Generation.git
cd AI-Jewelry-Generation
```

### Step 2: Set Up Python AI Service
1. Navigate to the model service folder:
   ```bash
   cd model_service
   ```
2. Create and configure your virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Place your pre-trained weights (`generator_model.h5`) under the `weights/` directory.
4. Run the Flask/FastAPI inference API:
   ```bash
   python app.py
   ```

### Step 3: Set Up Web Server & Client
1. Set up the express server:
   ```bash
   cd ../server
   npm install
   npm run start
   ```
2. Set up the React user interface:
   ```bash
   cd ../client
   npm install
   npm run start
   ```

---

## 📂 Folder Structure

```
AI-Jewelry-Generation/
├── model_service/
│   ├── weights/            # Trained model files (.h5)
│   ├── model/              # Pix2Pix Generator and Discriminator class code
│   ├── utils/              # OpenCV normalization, sizing, and color masks
│   ├── app.py              # Flask server for inference
│   └── requirements.txt
├── server/
│   ├── src/
│   │   ├── config/         # MongoDB setup
│   │   ├── controllers/    # Design gallery backend controllers
│   │   └── server.js
├── client/
│   ├── public/
│   ├── src/
│   │   ├── components/     # HTML5 drawing canvas, image comparisons
│   │   └── App.js
│   └── package.json
└── README.md
```

---

## 🚀 Future Improvements

- Transition from standard GANs to Stable Diffusion ControlNet for high-controllability, material textures, and prompt guiding.
- Export to GLTF/OBJ formats: implement depth estimation models (like MiDaS) to generate true 3D meshes from output images.

---

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

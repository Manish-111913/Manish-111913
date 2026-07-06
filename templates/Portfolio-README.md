# Modern Developer Portfolio Website

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=nextdotjs)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-blue?logo=tailwindcss)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?logo=typescript)](https://www.typescriptlang.org/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?logo=vercel)](https://vercel.com)

A high-performance, dark-themed, and fully responsive personal portfolio website showcasing software projects, experience, technical skills, and blogs. Designed with modern typography, smooth micro-interactions, and glassmorphism.

---

## 🔗 Live Demo
👉 **[Live Link (Replace with your link)](https://your-portfolio.vercel.app)**

---

## 📸 Screenshots

<p align="center">
  <img src="screenshots/hero.png" alt="Hero Section" width="80%" />
</p>

---

## ⚡ Features

- 🌓 **Dynamic Theme Toggle**: Clean light/dark mode transitions.
- 📱 **Fully Responsive**: Optimized for all devices (Mobile, Tablet, Desktop).
- 🧩 **Interactive Projects Showcase**: Categorized filter system for Projects (Full Stack, AI/ML, Cloud).
- 📝 **Markdown Blog**: MDX-based blogging system for tech articles.
- 📬 **Interactive Contact Form**: Configured with Web3Forms / EmailJS for instant notifications.
- 📈 **SEO Optimized**: Meta-tags, JSON-LD schema, and fast page load times.

---

## 💻 Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript
- **Styling**: Tailwind CSS, Framer Motion (for animations)
- **Deployment**: Vercel
- **Form Handling**: EmailJS / Web3Forms

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Manish-111913/Portfolio.git
   cd Portfolio
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up Environment Variables:**
   Create a `.env.local` file in the root directory:
   ```env
   NEXT_PUBLIC_SERVICE_ID=your_emailjs_service_id
   NEXT_PUBLIC_TEMPLATE_ID=your_emailjs_template_id
   NEXT_PUBLIC_PUBLIC_KEY=your_emailjs_public_key
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

---

## 📂 Folder Structure

```
Portfolio/
├── public/              # Static assets (images, icons)
├── src/
│   ├── app/             # Next.js App Router (Layouts & Pages)
│   ├── components/      # Reusable UI components (Button, Cards, Navbar)
│   ├── content/         # MDX files for blogs and resume details
│   ├── hooks/           # Custom React hooks
│   └── utils/           # Utility functions
├── .gitignore
├── next.config.js
├── tailwind.config.ts
└── README.md
```

---

## 🚀 Future Improvements

- Add a 3D Canvas element using Three.js/React Three Fiber.
- Integrate automated project metrics showing real-time GitHub stars/forks.
- Add an interactive chatbot powered by a custom fine-tuned LLM.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

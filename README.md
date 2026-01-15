# AI Sustainability Navigator (SDG 11 & SDG 3)

The AI Sustainability Navigator is a Retrieval-Augmented Generation (RAG) prototype designed to combat the Urban Heat Island effect. It helps citizens in rapidly urbanizing areas find "cool" walking routes, promoting sustainable transit and protecting public health.

## 🚀 The Problem
Traditional navigation tools (like Google Maps) prioritize the *fastest* route. In extreme heat, these routes often expose pedestrians to direct sun, leading to heat exhaustion. This discourages walking (SDG 11) and risks health (SDG 3).

## 💡 The Solution
Our AI agent uses **RAG** to:
1.  **Retrieve** real-time temperature data for any city via the Open-Meteo API.
2.  **Augment** this data with a specialized urban shade database.
3.  **Generate** a health-conscious travel plan using the **Llama-3.3-70b** model on Groq.

## 🏗️ System Architecture
The following diagram illustrates how the RAG pipeline processes user requests:
<img width="1150" height="1891" alt="diagram-export-15-01-2026-20_49_08" src="https://github.com/user-attachments/assets/7b6b29e0-ce03-4e9b-964a-f40d27850e6c" />

## 🛠️ Tech Stack
- **AI Model:** Llama-3.3-70b-versatile (via Groq Cloud)
- **Framework:** Python
- **APIs:** Open-Meteo (Weather), Geopy (Geocoding)
- **SDG Focus:** SDG 3 (Health) & SDG 11 (Sustainable Cities)

## 📦 Installation & Usage
1. Clone the repo:
   ```bash
   git clone https://github.com/ryxnoix/AI-Sustainability-Navigator.git


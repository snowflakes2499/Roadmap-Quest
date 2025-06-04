
# RoadMap Quest: Transforming Learning Complexity into Clarity

This project presents a personalized learning platform powered by **YouTube Data API**, **VADER Sentiment Analysis**, and **machine learning-based recommendation systems**. It aims to enhance student engagement and performance by generating **customized learning paths** using video content.

---

## 🎯 Project Goals

- Recommend high-quality YouTube videos based on the learner's topic of interest.
- Analyze viewer sentiments to ensure video quality and engagement.
- Provide visually structured roadmaps for effective study planning.

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **VADER Sentiment Analysis**
- **Google API Client**
- **YouTube Data API v3**
- **Flask (for UI)**
- **Excel for video metadata handling**

---

## 🧱 Project Structure

- `youtube_api.py`: Handles YouTube search and video metadata extraction.
- `sentiment_analysis.py`: Performs sentiment analysis using VADER.
- `roadmap_generator.py`: Organizes and visualizes learning paths.
- `data/videos.xlsx`: Master file of educational video links and metadata.
- `templates/`: HTML templates for web interface.
- `static/`: Static files (charts, roadmaps, visuals).

---

## 💻 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` and replace:

```python
YOUTUBE_API_KEY = "YOUR_API_KEY"
```

### 3. Run the App

```bash
python app.py
```

Then, open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📊 Features

### 🔍 Input Parameters

- **Topic of Interest** (e.g., AI, Blockchain)
- **Study Time/Day**
- **Student CGPA**

### ⚙️ Functional Layers

1. **Domain Selection**  
2. **YouTube API Integration**  
3. **Sentiment Analysis using VADER**  
4. **Video Ranking & Filtering**  
5. **Top 5 Video Recommendation**  
6. **Roadmap Generation (Flowchart & Table)**  
7. **Excel Update for Ongoing Maintenance**  

---

## 📈 Results & Visualizations

- Increased engagement with higher CGPA and more study time.
- Positive sentiment drives video selection.
- Personalized learning paths enhance academic performance.

---

## 🌱 Future Scope

- Integration with Deep Learning (LSTM, NLP)
- Gamification and VR for immersive learning
- Expansion to support various learning styles
- Industry & academic collaboration
- Real-time feedback & dynamic roadmap tuning

---

## 🧠 Authors

- **Khushi Rahul Bora**
- Prathmesh Sambhaji Deshmukh
- Arohi Pandurang Pachpute
- Suyash Sunil Dongre
- *Guide: Prof. Sheetal Phatangare*

---

## 📚 Reference

Refer to the full methodology and system design in the [`Research paper final.pdf`](./Research%20paper%20final.pdf).

---

## 📝 License

This project is built for academic and research purposes.

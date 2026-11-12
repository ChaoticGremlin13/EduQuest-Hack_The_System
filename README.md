# 💻 EduQuest - Hack The System

**A Matrix-inspired educational quiz game built with Python and Pygame.**

EduQuest is a terminal-style quiz game that challenges players with multiple-choice questions on computers, technology, artificial intelligence, and digital concepts.

Navigate through randomly selected questions, test your knowledge, beat your previous completion time, and secure a place on the leaderboard.

## ✨ Features

- **Matrix-inspired interface:** Dark visuals, animated digital rain, and a simulated system boot sequence.
- **20-question question bank:** Questions cover AI, robotics, computer fundamentals, software, and more.
- **Randomized questions:** The question order changes between game sessions.
- **Interactive gameplay:** Enter answers directly through the keyboard.
- **Scoring system:** Correct answers increase your score. Incorrect answers move you to the next question.
- **Hint and skip commands:** Request a basic hint or skip a question without earning points.
- **Timer:** Tracks your total completion time.
- **Leaderboard:** Saves the top 10 scores locally.
- **Sound effects:** Optional audio for boot sequences, correct answers, and completion.
- **Fullscreen support:** Available in the HTS version.

## 🛠️ Built With

- **Python**
- **Pygame**
- JSON for local leaderboard storage
- Python standard libraries

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

### 2. Navigate to the project directory

```bash
cd YOUR-REPOSITORY
```

### 3. Install the dependency

```bash
pip install pygame
```

### 4. Run the game

For the main HTS version:

```bash
python EduQuest-HTS.py
```

Alternatively, run the other version:

```bash
python EduQuest.py
```

## 🎮 Controls

| Key / Command | Action |
|---|---|
| `1` | Start a new game |
| `2` | View leaderboard |
| `3` | Quit |
| `A / B / C / D` | Submit an answer |
| `ENTER` | Confirm input |
| `BACKSPACE` | Delete input |
| `NEXT` | Skip the current question |
| `HINT` | Request a hint |
| `ESC` | Return to menu / exit |
| `F11` or `F` | Toggle fullscreen (HTS version) |
| `SPACE` | Skip boot sequence |

## 🧠 Question Categories

The question bank includes topics such as:

- Artificial Intelligence
- Robotics and Machine Learning
- Computer Vision
- Radio Waves and Wireless Communication
- Search Engines and Metasearch
- System Software and Utility Software
- Computer Hardware and Storage
- Microsoft Office Applications
- Computer Generations
- Networking and MAC Addresses

## 🏆 Leaderboard

EduQuest maintains a local leaderboard using a JSON file.

- Stores player names, scores, and completion times.
- Keeps a maximum of 10 entries.
- Ranks entries by completion time, with solved questions used as a secondary sorting criterion.

The leaderboard is stored in `leaderboard.json`, which is generated automatically when scores are saved.

## 🔊 Optional Sound Effects

The game supports optional sound files inside an `sfx` directory.

Expected structure:

```text
EduQuest/
│
├── EduQuest-HTS.py
├── EduQuest.py
├── leaderboard.json
│
└── sfx/
    ├── boot.wav
    ├── correct.wav
    └── win.wav
```

Sound effects are optional. The game can run without them.

## 📁 Project Structure

```text
EduQuest/
│
├── EduQuest-HTS.py       # HTS version
├── EduQuest.py           # Alternate version
├── leaderboard.json      # Generated local leaderboard
└── sfx/                  # Optional sound effects
```

## 📝 Notes

- Each question allows only one answer attempt.
- Incorrect answers automatically advance to the next question.
- Skipped questions do not award points.
- Leaderboard data is stored locally on the machine running the game.
- The project is a standalone desktop application, not a web-based game.

## 📜 License

This project is open-source. Add a license file to the repository if you intend to distribute it under a specific license.

---

**EduQuest - Hack The System**

*Knowledge is power. Use it for defense, not destruction.*

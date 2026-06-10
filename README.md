# Ghostbusters 👻🎮

Welcome to **Ghostbusters**, an arcade-style retro mini-game built entirely in Python using the `tkinter` library. This is my **Final Project** for Stanford's **Code in Place 2026** program! 

The project brings together foundational programming concepts learned throughout the course—such as event-driven programming, loops, conditionals, and random coordinates—packaged into a nostalgic, fast-paced Nintendo/Pac-Man inspired aesthetic.

---

## 🕹️ Game Overview

The objective is simple: **Catch the ghosts before they disappear!** Fantasms of different shapes and classic retro colors (*Blinky, Inky, Pinky, Clyde, and Spooky*) will randomly pop up at different locations on a dark arcade canvas. You must react quickly and click on them to score points.

### 📜 Game Rules:
* 🎯 **Score:** Each successful catch rewards you with **100 points**.
* ⚡ **Speed:** Ghosts only stay on screen for **1.5 seconds** before vanishing.
* ⏰ **Too Slow!** If a ghost disappears before you click it, it counts as a miss.
* ❌ **Missed Shots:** Clicking on the empty background also counts as a miss, preventing button-mashing!
* 🏆 **How to Win:** Successfully capture **10 ghosts** to win the game (`YOU WIN!`).
* 💀 **Game Over:** If you accumulate **3 consecutive misses** (either by being too slow or clicking the empty screen), the game ends immediately (`GAME OVER`).

---

## 🛠️ Features & Concepts Applied

* **Graphical User Interface (GUI):** Built using Python's native `tkinter` engine to design a custom 800x600 dark canvas with arcade typography.
* **Procedural Graphic Generation:** The retro ghost shapes (rounded head, body skirt, eyes, and shifting blue pupils) are drawn dynamically using canvas vectors rather than external static images.
* **Asynchronous Game Loop:** Utilizing Tkinter's `.after()` method to keep track of real-time expiration windows without blocking the application.
* **Collision Detection:** Precise coordinate boundary tracking to determine whether the user's mouse click successfully hit the ghost object.

---

## 🚀 How to Run the Project

1. **Prerequisites:** Make sure you have Python installed on your system (`tkinter` comes pre-installed with standard Python distributions).
2. **Clone the repository:**

# Space Invaders 2.0

## **Table of Contents**
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Repository Structure](#repository-structure)
6. [Gameplay Demo](#gameplay-demo)
7. [Authors / Acknowledgments](#authors--acknowledgments)

---

## **Overview**

This project is a recreation of the game Space Invaders. 

---

## **Installation**

### Prerequisites
- Python 3.x
- The Turtle graphics library (included in the Python Standard Library)
- Basic knowledge of running Python scripts

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/space-invaders-2.0.git
   cd space-invaders-2.0
   ```
2. Run the game:
   ```bash
   python space-invaders-2.0.py
   ```

---

## **Usage**
Launch the game and use the following controls:
- Arrow keys to move the player spaceship.
- Spacebar to shoot.

Engage with the waves of enemies, collect power-ups, and defeat the boss to progress through the game.

---

## **Features**

### **1. Player Spaceship: Movement and Shooting**
- **Movement:**
  - Horizontal movement is restricted to within screen boundaries to keep the spaceship visible and accessible.
  - Movement functions include boundary checks using conditions like `self.turtle.xcor() > -380` and `self.turtle.xcor() < 380`.
- **Shooting Mechanics:**
  - Players shoot bullets using a cooldown mechanism, preventing excessive firing to maintain game balance.

### **2. Alien Spaceships: Movement and Attacks**
- **Organized Movement:**
  - Aliens move in coordinated patterns with increasing complexity as waves progress.
  - Position updates are handled by adding displacement values `(dx, dy)` to each alien.
- **Projectile Firing:**
  - Aliens shoot randomly with probabilities increasing as the game advances.

### **3. Homing Bullets and Advanced Behavior**
- **Homing Bullets:**
  - Adds strategic complexity by allowing bullets to track the player's position.
  - Key mechanisms include:
    - **Target Angle Calculation:** Trigonometric calculations ensure precise tracking of the player.
    - **Smooth Curving Control:** Limits angle adjustments to maintain dodgability and fluid movement.
    - **Dynamic Activation:** Curving behavior is signaled by changing the bullet’s color to red.

### **4. Boss Mechanics**
- **Health Bar:**
  - Players receive visual feedback on their progress during boss battles through an interactive health bar.

### **5. Collision Detection**
- **Accuracy:**
  - Implements the Euclidean formula to detect collisions between objects like bullets and spaceships.
  - Collision thresholds trigger appropriate game responses.

### **6. Power-Ups**
- **Dynamic Gameplay:**
  - Randomized power-ups offer temporary enhancements, such as increased fire rate or extra lives.
  - Global variables adjust based on the power-up type, with effects reverting after expiration.

---

## **Repository Structure**
- `space-invaders-2.0.py`: The main Python script containing the game's logic and implementation.
- `Gameplay video.mov`: A demonstration video showcasing the gameplay.
- `Key_Code_Descriptions.pdf`: Detailed descriptions of the key segments of the code, explaining design choices and implementation.
- `Space_Invaders_Pseudocode.pdf`: A document outlining the pseudocode and structure of the game.
- `Complexity_-_Space_Invaders.pdf`: A report analyzing the complexity and advanced features of the game.
- `README.md`: This README file.

---

## **Gameplay Demo**
To see the game in action, watch the demonstration video: `Gameplay video.mov`.

The video highlights key gameplay elements, including:
- Player and enemy interactions.
- The use of power-ups.
- Boss battle mechanics.

---

## **Authors / Acknowledgments**
- We can attest that everyone who regularly attended group meetings contributed equally to the complexity and pseudocode analysis documents.
- Developed by Adam Zeraiki, Augustin Vlandas, Conor Osiadhail, Chris William Karam, Ines Lebard, and Oscar Moulet.

---


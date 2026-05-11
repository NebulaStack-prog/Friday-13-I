## Part 1. Main Document.

### 1. Title and Basic Information.

• **Title:** Friday 13 – I.

• **Purpose:** Project No. 2. Product.

• **Project Phase:** Phase I.

• **Technology Stack:** Python

• **Project Status:** Fully completed.

### 2. Brief Project Description.

The project "Friday 13 - I" combines the model of the classic pixel game "Snake" with the atmosphere of the well-known Friday the 13th.

The player's task is to fill the entire game field with the snake's body by consuming "Tourists," which act as the classic "apples."

The project includes three different levels based on field cell sizes: 8×8, 12×12, and 16×16, each recommended for completion.

The snake is styled with the colors of the NebulaStack Friday 13 emblem.

### 3. Clear Project Goals.

• Transform the classic version of Snake.

• Expand the NebulaStack project showcase and demonstrate an approach to classic IT industry games.

• Create a Friday the 13th atmosphere for full immersion.

• Implement the core gameplay mechanics: snake movement and turning, tail extension when consuming targets, spawning of new targets, and score display.

• Create a playable model with intuitive controls and interface.

### 4. Project Components.

• Scripts for snake movement, snake extension, spawning of "Tourists," etc.

• Main tools/objects: rectangles, colors, functions (Pygame library).

• The entire compiled game is contained in a single file: Friday13-I.py.

### 5. Instructions for Use.

**5.1. Usage:**

• To run the project, launch the code in Python or open the executable ".exe" file.

• After launching the game, press the level number key (1, 2, or 3) to choose the difficulty level based on map size.

• Your objective is to fill the entire map with the snake’s body by increasing its length.

• The snake grows by consuming targets that appear randomly on the map.

• The game ends if the snake touches its own body or a wall ("GAME OVER" screen). Pressing "R" (Restart) returns to the main level selection screen, while pressing "ESC" completely closes the game.

**5.2. Controls:**

• **LEFT Arrow (←):** start moving left.

• **RIGHT Arrow (→):** start moving right.

• **DOWN Arrow (↓):** start moving down.

• **UP Arrow (↑):** start moving up.

• **ESC during gameplay:** return to the main level selection menu.

• **ESC on the GAME OVER screen:** fully exit the game.

• **R on the GAME OVER screen:** return to the main menu.

• Important note: the snake cannot turn 180° and move "into itself." The snake must also avoid colliding with its own body and the map walls.

## Part 2. Technical Document.

### 1. Development Goals.

• Create a playable version of the classic "Snake" game with a Friday the 13th themed design.

• Implement a difficulty level system with different field sizes and game speeds.

• Ensure correct collision handling and food regeneration outside the snake’s body.

### 2. Technologies Used.

• **Programming Languages:** Python.

• **Libraries:** pygame, random.

### 3. Project Architecture.

• The project uses a procedural architecture with separation into functions.

• The show_menu() function is responsible for displaying the main menu, selecting the level, and returning difficulty parameters as a dictionary.

• The game(level) function is the main game loop, receiving level parameters and controlling all gameplay logic.

• Inside the game() function, nested functions are defined: score() for score display, message() for showing messages, and tourists() for rendering the target.

• Global constants define colors, level parameters, and fonts.

• Entry point: calling show_menu() and passing the result into game().

### 4. Project Structure.

• The project consists of one main file: Friday13-I.py.

• This file contains all code: pygame initialization, constants, menu functions, and gameplay logic.

• The project requires the Pygame library to be installed (pip install pygame).

• Module imports (pygame, random)

• Pygame initialization

• Color definitions (black, white, dark_red, blood_red, grid_gray)

• levels dictionary with parameters for the three levels

• Font setup

• show_menu() function

• game(level) function with nested functions and the gameplay loop

• Game startup through show_menu() and game()

### 5. Key System Components.

• **levels dictionary** – stores parameters for each level: grid_size (grid size 8/12/16), cell_size (cell size 45/40/35), speed (game speed 6/8/10), name (level name).

• **Game field** – a discrete grid where object coordinates are always multiples of cell_size.

• **Snake (snake_list)** – a list of body segment coordinates, length_of_snake – current length.

• **Movement** – implemented through x1_change and y1_change variables with a restriction on 180° turns.

• **Collision detection** – with walls (leaving field boundaries) and with the snake’s own body (segments in snake_list).

• **Target consumption** – when the head coordinates (x1, y1) match the food coordinates (foodx, foody), the snake length increases by 1 and the food regenerates in a random free cell.

• **Restart system** – during game_close through the R key (return to menu) and ESC key (exit).

• **Visual styling** – the snake’s head is drawn with eyes and bloody lines, the body with cross-shaped cuts and red stains, and tourists as circles with eyes.

### 6. User Interface Implementation.

• The level selection menu is created through the show_menu() function in a separate 800×600 window.

• The menu displays the game title in red and four options: three levels and exit. Selection is performed using the 1, 2, 3, and ESC keys.

• The game window has a dynamic size depending on the selected level: width and height = grid_size × cell_size.

• The score is displayed in the upper-left corner of the game window as: "Victims: N" in blood-red color.

• A gray grid with a cell_size step is drawn on the field for visual separation of cells.

• During game_close, the message "GAME OVER! ESC - Exit, R - Replay" is displayed in red at the center of the screen.

• All visual elements are created using pygame.draw functions (rectangles, circles, lines) without using loaded images.

### 7. Development Process.

• First, a basic framework of the classic "Snake" game was created in Pygame using the standard algorithm.

• Then, the show_menu() function was added for difficulty level selection.

• Next, level parameters (field size, speed) were moved into the levels dictionary.

• After that, the visual styling was completely redesigned for the Friday the 13th theme: colors were changed to black and shades of red, and "bloody" details were added.

• The nested tourists() function replaced the standard apple with a stylized target.

• Detailed rendering of the snake’s head and body was added (eyes, lines, stains).

• Finally, proper game ending and returning to the menu through the ESC and R keys were implemented.

• The entire process was accompanied by testing on different difficulty levels and bug fixing.

### 8. Main Challenges and Their Solutions.

• **(1) Challenge:** food could appear inside the snake’s body, making the game unfair.

**Solution:** during food regeneration, a while True loop was added to check whether the new coordinates are inside snake_list and generate a new position until a free cell is found.

• **(2) Challenge:** the snake could instantly turn 180 degrees and collide with itself.

**Solution:** before changing direction, a check was added: when pressing left, movement is only allowed if x1_change == 0 (the snake is not moving right), and similarly for all directions.

• **(3) Challenge:** different game speeds and field sizes across levels required flexible configuration.

**Solution:** all level parameters were moved into the levels dictionary, and the game(level) function dynamically adjusts the window, block size, and FPS through clock.tick(snake_speed).

• **(4) Challenge:** visual elements (eyes, lines) looked incorrect with small cell sizes.

**Solution:** for all sizes, max(1, value // divisor) is used, guaranteeing a minimum size of 1 pixel and preventing rendering issues.

• **(5) Challenge:** after game_close, the player could not start a new game without restarting the application.

**Solution:** an internal while game_close loop was added, waiting for the player to press R (calling show_menu() and recursively calling game()) or ESC (exit).

### 9. Current Project Limitations.

• All code is contained in a single file, which may complicate future expansion and maintenance.

• There is no victory mode (filling the entire field with the snake’s body); the game only ends in defeat.

• There is no saving of records or best scores between launches.

• There is no sound support at all (music, eating sounds, losing sounds).

• All colors and level parameters are hardcoded, and changing them requires editing the source code.

### 10. Possible Improvements and Future Plans.

• Add sound effects: tourist consumption, losing, menu selection.

• Implement a victory screen when the entire field is filled with the snake’s body.

• Introduce a leaderboard system (best scores for each level) with JSON file saving.

• Split the code into multiple modules: menu.py, game.py, settings.py for easier maintenance.

• Add a pause feature using the P key or Spacebar.

• Add new difficulty levels with different field shapes (not only square).

• Implement animations for consuming targets and for losing.

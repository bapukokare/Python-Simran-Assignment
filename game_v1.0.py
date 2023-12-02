import curses
import time
import random
import os

# Define gun representations
guns = {
    '1': 'Pistol',
    '2': 'Shotgun',
    '3': 'Rifle',
}
selected_gun = '1'  # Default gun

def main(stdscr):
    global selected_gun

    # Set specific height and width
    sh, sw = 20, 60

    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Create the player
    player = '^'
    # player position
    player_x = sw // 2
    player_y = sh - 1

    # Create the bullets
    bullets = []

    # Create the enemies
    enemies = []
    score = 0
    max_score = 0  # Variable to record the maximum score
    user_name = "SampleUser"  # Default user name

    # Check if the file exists, if not, create it
    filename = "scores.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write("0\nSampleUser")

    # Load previous scores from a text file
    try:
        with open(filename, "r") as file:
            max_score = int(file.readline().strip())
            user_name = file.readline().strip()
    except FileNotFoundError:
        pass

    def save_score():
        nonlocal max_score, user_name
        # Save the new max score to the file
        with open(filename, "w") as file:
            file.write(f"{score}\n{user_name}")

    def reset_level():
        nonlocal player_x, player_y, bullets, enemies, score
        player_x = sw // 2
        player_y = sh - 1
        bullets = []
        enemies = []
        for _ in range(5):
            enemy_x = random.randint(1, sw - 2)
            enemy_y = random.randint(1, sh - 2)
            enemies.append([enemy_y, enemy_x])

    def shoot():
        # Use the selected gun here
        bullet_char = '.'  # Replace with gun-specific bullet representation
        bullets.append([player_y - 1, player_x, bullet_char])

    def draw_menu():
        stdscr.addstr(sh - 2, 2, "Select a Gun (Press 1, 2, or 3):")
        for key, value in guns.items():
            gun_status = " [Selected]" if key == selected_gun else ""
            stdscr.addstr(sh - 3, 2 + int(key) * 5, f"{key}.{value}{gun_status}")

    # Initial level setup
    reset_level()

    player_move_time = time.time()
    enemy_move_time = time.time()
    space_pressed = False

    while True:
        # Get user input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):  # Spacebar
            space_pressed = True
        elif key == curses.KEY_RIGHT and player_x < sw - 1:
            player_x += 1
            player_move_time = time.time()  # Update player move time
        elif key == curses.KEY_LEFT and player_x > 0:
            player_x -= 1
            player_move_time = time.time()  # Update player move time
        elif key in [ord('1'), ord('2'), ord('3')]:
            selected_gun = chr(key)

        # Continuous shooting while spacebar is pressed
        if space_pressed:
            shoot()

        # Move bullets
        new_bullets = []
        for bullet in bullets:
            if bullet[0] > 0:
                new_bullets.append([bullet[0] - 1, bullet[1], bullet[2]])
        bullets = new_bullets

        # Move enemies at a fixed interval
        if time.time() - enemy_move_time > 0.2:
            new_enemies = []
            for enemy in enemies:
                if enemy[0] < sh - 1:
                    new_enemies.append([enemy[0] + 1, enemy[1]])
                else:
                    # Respawn enemies at the top
                    new_enemies.append([0, random.randint(1, sw - 2)])
            enemies = new_enemies
            enemy_move_time = time.time()  # Update enemy move time

        # Check for collisions
        for bullet in bullets:
            if bullet[:2] in enemies:
                enemies.remove(bullet[:2])
                bullets.remove(bullet)
                score += 1

        # Draw everything
        stdscr.clear()
        stdscr.addch(player_y, player_x, player)
        for bullet in bullets:
            stdscr.addch(bullet[0], bullet[1], bullet[2])
        for enemy in enemies:
            stdscr.addch(enemy[0], enemy[1], 'E')
        draw_menu()
        stdscr.addstr(0, 2, f'Score: {score} Max Score: {max_score} User: {user_name}')  # Display score and max score live
        stdscr.refresh()

        # Game over condition
        if [player_y, player_x] in enemies:
            curses.beep()
            stdscr.addstr(sh // 2, sw // 2 - 10, f'Game Over - Your Score: {score}', curses.A_BOLD)
            stdscr.addstr(sh // 2 + 1, sw // 2 - 10, 'Press q to quit', curses.A_BOLD)
            stdscr.refresh()

            # Check if the score is a new max score
            if score > max_score:
                # Save the score only if it's a new max score
                max_score = score
                save_score()

            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    break
            break

        # Check if all enemies are cleared for the current level
        if not enemies:
            reset_level()

        # Call draw_menu to display the menu
        draw_menu()

        # Reset space_pressed to False to handle continuous shooting
        space_pressed = False

curses.wrapper(main)

import curses
import time
import random

# Define gun representations
guns = {
    '1': 'Pistol',
    '2': 'Shotgun',
    '3': 'Rifle',
}

selected_gun = '1'  # Default gun

def main(stdscr):
    global selected_gun

    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()

    # Create the player
    player = '^'
    player_x = sw // 2
    player_y = sh - 1

    # Create the bullets
    bullets = []

    # Create the enemies
    enemies = []
    score = 0

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
        bullets.append([player_y - 1, player_x])

    def draw_menu():
        stdscr.addstr(sh - 1, 2, "Select a Gun (Press 1, 2, or 3):")
        for key, value in guns.items():
            gun_status = " [Selected]" if key == selected_gun else ""
            stdscr.addstr(sh - 1, 20 + int(key) * 5, f"{key}. {value}{gun_status}")

    # Initial level setup
    reset_level()

    while True:
        # Get user input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):  # Spacebar
            shoot()
        elif key == curses.KEY_RIGHT and player_x < sw - 1:
            player_x += 1
        elif key == curses.KEY_LEFT and player_x > 0:
            player_x -= 1
        elif key in [ord('1'), ord('2'), ord('3')]:
            selected_gun = chr(key)

        # Move bullets
        new_bullets = []
        for bullet in bullets:
            if bullet[0] > 0:
                new_bullets.append([bullet[0] - 1, bullet[1]])
        bullets = new_bullets

        # Move enemies
        new_enemies = []
        for enemy in enemies:
            if enemy[0] < sh - 1:
                new_enemies.append([enemy[0] + 1, enemy[1]])
            else:
                # Respawn enemies at the top
                new_enemies.append([0, random.randint(1, sw - 2)])
        enemies = new_enemies

        # Check for collisions
        for bullet in bullets:
            if bullet in enemies:
                enemies.remove(bullet)
                bullets.remove(bullet)
                score += 1

        # Draw everything
        stdscr.clear()
        stdscr.addch(player_y, player_x, player)
        for bullet in bullets:
            stdscr.addch(bullet[0], bullet[1], '*')
        for enemy in enemies:
            stdscr.addch(enemy[0], enemy[1], 'E')
        draw_menu()
        stdscr.addstr(0, 2, f'Score: {score}')  # Display score live
        stdscr.refresh()

        # Game over condition
        if [player_y, player_x] in enemies:
            stdscr.addstr(sh // 2, sw // 2 - 10, f'Game Over - Your Score: {score}', curses.A_BOLD)
            stdscr.addstr(sh // 2 + 1, sw // 2 - 15, 'Press q to quit', curses.A_BOLD)
            stdscr.refresh()
            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    break
            break

        # Check if all enemies are cleared for the current level
        if not enemies:
            reset_level()

curses.wrapper(main)

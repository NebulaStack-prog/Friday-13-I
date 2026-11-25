import pygame
import random
import json
from pathlib import Path
from collections import deque

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (139, 0, 0)
RED = (180, 0, 0)
GRAY = (150, 150, 150)
GRID_GRAY = (30, 30, 30)

WIDTH, HEIGHT = 800, 600
FPS = 60

LEVELS = {
    "1": {"grid_size": 8, "speed": 6, "name": "Easy"},
    "2": {"grid_size": 12, "speed": 8, "name": "Medium"},
    "3": {"grid_size": 16, "speed": 10, "name": "Hard"}
}

SAVE_FILE = (
    Path.home() / ".nestims" / "friday13-i" / "records.json"
)

FONT = pygame.font.SysFont("bahnschrift", 25)
SMALL_FONT = pygame.font.SysFont("bahnschrift", 18)
TITLE_FONT = pygame.font.SysFont("bahnschrift", 48)
SCORE_FONT = pygame.font.SysFont("bahnschrift", 30)

def load_records():
    records = {
        level: {"best": 0, "completed": False}
        for level in LEVELS
    }

    try:
        data = json.loads(
            SAVE_FILE.read_text(encoding="utf-8")
        )

        for level in LEVELS:
            entry = data.get(level, {})
            maximum = LEVELS[level]["grid_size"] ** 2 - 1

            best = int(entry.get("best", 0))
            best = max(0, min(best, maximum))

            records[level]["best"] = best
            records[level]["completed"] = best == maximum

    except (OSError, ValueError, TypeError, AttributeError):
        pass

    return records


def save_records(records):
    try:
        SAVE_FILE.parent.mkdir(
            parents=True, exist_ok=True
        )

        temp = SAVE_FILE.with_suffix(".tmp")

        temp.write_text(
            json.dumps(records, indent=4),
            encoding="utf-8"
        )

        temp.replace(SAVE_FILE)
        return True

    except OSError:
        return False

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Friday 13 - I | NESTIMS"
        )

        self.clock = pygame.time.Clock()
        self.records = load_records()

        self.running = True
        self.state = "MENU"
        self.level_key = "1"

        self.score = 0
        self.new_record = False
        self.save_error = False

    def text(self, message, font, color, x, y):
        surface = font.render(message, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def start_game(self, level_key):
        self.level_key = level_key
        self.level = LEVELS[level_key]

        self.grid_size = self.level["grid_size"]
        self.maximum_score = self.grid_size ** 2 - 1

        self.cell = 480 // self.grid_size
        self.board_size = self.cell * self.grid_size

        self.board_x = (WIDTH - self.board_size) // 2
        self.board_y = 90

        center = self.grid_size // 2

        self.snake = deque([(center, center)])
        self.occupied = {(center, center)}

        self.direction = (0, 0)
        self.next_direction = (0, 0)

        self.score = 0
        self.new_record = False
        self.save_error = False

        self.move_timer = 0.0
        self.move_interval = 1.0 / self.level["speed"]

        self.food = self.spawn_food()
        self.state = "PLAYING"

    def spawn_food(self):
        free_cells = [
            (x, y)
            for y in range(self.grid_size)
            for x in range(self.grid_size)
            if (x, y) not in self.occupied
        ]

        if not free_cells:
            return None

        return random.choice(free_cells)

    def update_record(self):
        record = self.records[self.level_key]

        if self.score > record["best"]:
            record["best"] = self.score
            self.new_record = True

        if self.score == self.maximum_score:
            record["completed"] = True

        self.save_error = not save_records(self.records)

    def finish_game(self, victory=False):
        self.update_record()

        if victory:
            self.state = "WIN"
        else:
            self.state = "GAME_OVER"

    def move(self):
        self.direction = self.next_direction

        if self.direction == (0, 0):
            return

        hx, hy = self.snake[0]
        dx, dy = self.direction

        new_head = (hx + dx, hy + dy)
        x, y = new_head

        # Wall collision
        if not (
            0 <= x < self.grid_size
            and 0 <= y < self.grid_size
        ):
            self.finish_game()
            return

        growing = new_head == self.food
        tail = self.snake[-1]

        # The tail cell becomes free unless growing
        if new_head in self.occupied:
            if growing or new_head != tail:
                self.finish_game()
                return

        if not growing:
            removed = self.snake.pop()
            self.occupied.remove(removed)

        self.snake.appendleft(new_head)
        self.occupied.add(new_head)

        if growing:
            self.score += 1

            # Victory condition
            if self.score == self.maximum_score:
                self.food = None
                self.finish_game(victory=True)
                return

            self.food = self.spawn_food()

    def handle_events(self):
        directions = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1)
        }

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if self.state in ("PLAYING", "PAUSED"):
                    self.update_record()

                self.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

            key = event.key

            if self.state == "MENU":

                if key == pygame.K_ESCAPE:
                    self.running = False

                elif key == pygame.K_1:
                    self.start_game("1")

                elif key == pygame.K_2:
                    self.start_game("2")

                elif key == pygame.K_3:
                    self.start_game("3")

            elif self.state == "PLAYING":

                if key in directions:
                    dx, dy = directions[key]
                    ox, oy = self.direction

                    if (dx, dy) != (-ox, -oy):
                        self.next_direction = (dx, dy)

                elif key in (pygame.K_p, pygame.K_SPACE):
                    self.state = "PAUSED"

                elif key == pygame.K_ESCAPE:
                    self.update_record()
                    self.state = "MENU"

            elif self.state == "PAUSED":

                if key in (pygame.K_p, pygame.K_SPACE):
                    self.state = "PLAYING"

                elif key == pygame.K_ESCAPE:
                    self.update_record()
                    self.state = "MENU"

            elif self.state in ("WIN", "GAME_OVER"):

                if key == pygame.K_r:
                    self.start_game(self.level_key)

                elif key == pygame.K_m:
                    self.state = "MENU"

                elif key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt):
        if self.state != "PLAYING":
            return

        self.move_timer += dt

        while self.move_timer >= self.move_interval:
            self.move_timer -= self.move_interval
            self.move()

            if self.state != "PLAYING":
                break

    def draw_menu(self):
        self.screen.fill(BLACK)

        self.text(
            "NESTIMS", SMALL_FONT, GRAY, 400, 45
        )

        self.text(
            "FRIDAY 13 - I",
            TITLE_FONT, DARK_RED, 400, 105
        )

        self.text(
            "Choose difficulty",
            FONT, WHITE, 400, 165
        )

        for index, (key, level) in enumerate(
            LEVELS.items()
        ):
            y = 235 + index * 90
            size = level["grid_size"]
            record = self.records[key]
            maximum = size ** 2 - 1

            self.text(
                f"{key} - {level['name']} ({size}x{size})",
                SCORE_FONT, WHITE, 400, y
            )

            status = (
                "COMPLETED"
                if record["completed"]
                else f"Best: {record['best']} / {maximum}"
            )

            self.text(
                status, SMALL_FONT, RED, 400, y + 32
            )

        self.text(
            "ESC - Exit",
            FONT, GRAY, 400, 530
        )

        self.text(
            "Version 1.1 | NS-002",
            SMALL_FONT, GRAY, 400, 575
        )

    def draw_food(self):
        if self.food is None:
            return

        gx, gy = self.food

        x = self.board_x + gx * self.cell
        y = self.board_y + gy * self.cell

        cx = x + self.cell // 2
        cy = y + self.cell // 2
        radius = self.cell // 3

        pygame.draw.circle(
            self.screen, RED, (cx, cy), radius
        )

        pygame.draw.circle(
            self.screen, DARK_RED,
            (cx, cy), radius // 2
        )

        eye = max(2, self.cell // 10)

        for offset in (-1, 1):
            pygame.draw.circle(
                self.screen, BLACK,
                (
                    cx + offset * radius // 2,
                    cy - radius // 2
                ),
                eye
            )

    def draw_segment(self, position, is_head):
        gx, gy = position
        size = self.cell

        x = self.board_x + gx * size
        y = self.board_y + gy * size

        pygame.draw.rect(
            self.screen, WHITE,
            (x + 1, y + 1, size - 2, size - 2)
        )

        if is_head:
            surface = pygame.Surface(
                (size, size), pygame.SRCALPHA
            )

            eye_size = max(3, size // 6)

            pygame.draw.circle(
                surface, BLACK,
                (size // 3, size // 3), eye_size
            )

            pygame.draw.circle(
                surface, BLACK,
                (2 * size // 3, size // 3), eye_size
            )

            pygame.draw.line(
                surface, RED,
                (size // 4, size // 6),
                (3 * size // 4, size // 6),
                max(2, size // 10)
            )

            for px in (size // 4, 3 * size // 4):
                pygame.draw.circle(
                    surface, RED,
                    (px, 2 * size // 3),
                    max(1, size // 12)
                )

            angles = {
                (1, 0): 270,
                (-1, 0): 90,
                (0, -1): 0,
                (0, 1): 180,
                (0, 0): 270
            }

            surface = pygame.transform.rotate(
                surface, angles[self.direction]
            )

            self.screen.blit(surface, (x, y))

        else:
            mx = x + size // 2
            my = y + size // 2
            thickness = max(3, size // 6)

            pygame.draw.line(
                self.screen, BLACK,
                (mx, y), (mx, y + size),
                thickness
            )

            pygame.draw.line(
                self.screen, BLACK,
                (x, my), (x + size, my),
                thickness
            )

            for dx in (-1, 1):
                for dy in (-1, 1):
                    pygame.draw.circle(
                        self.screen, RED,
                        (
                            mx + dx * size // 3,
                            my + dy * size // 3
                        ),
                        max(1, size // 10)
                    )

    def progress_bar(self, x, y, width, height):
        progress = self.score / self.maximum_score

        pygame.draw.rect(
            self.screen, GRID_GRAY,
            (x, y, width, height),
            border_radius=4
        )

        filled = int(width * progress)

        if filled > 0:
            pygame.draw.rect(
                self.screen, RED,
                (x, y, filled, height),
                border_radius=4
            )

    def draw_game(self):
        self.screen.fill(BLACK)

        self.text(
            f"{self.level['name']} | "
            f"Score: {self.score}/{self.maximum_score}",
            SCORE_FONT, WHITE, 400, 25
        )

        self.progress_bar(160, 50, 480, 8)

        progress = (
            self.score / self.maximum_score * 100
        )

        self.text(
            f"{progress:.1f}% completed",
            SMALL_FONT, GRAY, 400, 73
        )

        for i in range(self.grid_size + 1):
            offset = i * self.cell

            pygame.draw.line(
                self.screen, GRID_GRAY,
                (self.board_x + offset, self.board_y),
                (
                    self.board_x + offset,
                    self.board_y + self.board_size
                )
            )

            pygame.draw.line(
                self.screen, GRID_GRAY,
                (self.board_x, self.board_y + offset),
                (
                    self.board_x + self.board_size,
                    self.board_y + offset
                )
            )

        self.draw_food()

        for index in range(len(self.snake) - 1, -1, -1):
            self.draw_segment(
                self.snake[index], index == 0
            )

        self.text(
            "P / SPACE - Pause     ESC - Menu",
            SMALL_FONT, GRAY, 400, 585
        )

    def draw_pause(self):
        self.draw_game()

        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        self.text(
            "PAUSED", TITLE_FONT, RED, 400, 250
        )

        self.text(
            "P / SPACE - Continue",
            FONT, WHITE, 400, 320
        )

        self.text(
            "ESC - Main Menu",
            FONT, GRAY, 400, 365
        )

    def draw_ending(self):
        self.screen.fill(BLACK)

        victory = self.state == "WIN"

        self.text(
            "NESTIMS | FRIDAY 13 - I",
            SMALL_FONT, GRAY, 400, 50
        )

        self.text(
            "YOU WIN!" if victory else "GAME OVER",
            TITLE_FONT, RED, 400, 135
        )

        self.text(
            (
                f"{self.level['name']} mode completed"
                if victory
                else f"{self.level['name']} mode"
            ),
            FONT, WHITE, 400, 195
        )

        self.text(
            f"{self.score} / {self.maximum_score}",
            TITLE_FONT, WHITE, 400, 260
        )

        self.progress_bar(160, 310, 480, 12)

        progress = (
            self.score / self.maximum_score * 100
        )

        self.text(
            f"{progress:.1f}% COMPLETED",
            SMALL_FONT, GRAY, 400, 345
        )

        if self.new_record:
            self.text(
                "NEW RECORD!",
                FONT, RED, 400, 385
            )

        self.text(
            "R - Replay",
            FONT, WHITE, 400, 445
        )

        self.text(
            "M - Main Menu",
            FONT, WHITE, 400, 485
        )

        self.text(
            "ESC - Exit",
            FONT, GRAY, 400, 525
        )

        if self.save_error:
            self.text(
                "Unable to save records",
                SMALL_FONT, RED, 400, 575
            )

    def render(self):
        if self.state == "MENU":
            self.draw_menu()

        elif self.state == "PLAYING":
            self.draw_game()

        elif self.state == "PAUSED":
            self.draw_pause()

        elif self.state in ("WIN", "GAME_OVER"):
            self.draw_ending()

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = min(
                self.clock.tick(FPS) / 1000.0,
                0.25
            )

            self.handle_events()

            if not self.running:
                break

            self.update(dt)
            self.render()

        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

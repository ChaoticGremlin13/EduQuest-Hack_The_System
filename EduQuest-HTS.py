import pygame
import sys
import os
import time
import json
import random
import math
from collections import deque

# -------- CONFIG ----------
WINDOW_SIZE = (1200, 720)
FPS = 60
FONT_NAME = "Goudy Old Style"
FONT_SIZE = 20
TITLE_FONT_SIZE = 42
TEXT_COLOR = (255, 255, 255)
INPUT_COLOR = (255, 50, 50)
QUESTION_COLOR = (128, 0, 128)  # purple
BG_COLOR = (0, 0, 0)
BOOT_LINES = [
    "[BOOT SEQUENCE INITIATED]",
    "[LOADING SECURE SUBSYSTEMS...]",
    "[CHECKSUM OK]",
    "[ACCESS LAYERS 1/4 2/4 3/4 4/4]",
    "[AUTHORIZATION FAILED]",
    ">> INITIATE OVERRIDE PROTOCOL",
]
SFX_DIR = "sfx"
LEADERBOARD_FILE = "leaderboard.json"
MAX_LEADERBOARD = 10

# -------- PYGAME INIT ----------
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("EduQuest - Hack The System")
clock = pygame.time.Clock()

# fonts
def get_font(name, size, bold=False):
    try:
        f = pygame.font.SysFont(name, size, bold=bold)
        if f is None:
            raise Exception("font not found")
        return f
    except Exception:
        return pygame.font.SysFont("consolas", size, bold=bold)

font = get_font(FONT_NAME, FONT_SIZE)
font_bold = get_font(FONT_NAME, FONT_SIZE, bold=True)
title_font = get_font(FONT_NAME, TITLE_FONT_SIZE)

# -------- SOUND ----------
SFX_BOOT = SFX_CORRECT = SFX_WIN = None
try:
    pygame.mixer.init()
    def load_sfx(name):
        path = os.path.join(SFX_DIR, name)
        if os.path.exists(path):
            try:
                return pygame.mixer.Sound(path)
            except Exception:
                return None
        return None

    SFX_BOOT = load_sfx("boot.wav")
    SFX_CORRECT = load_sfx("correct.wav")
    SFX_WIN = load_sfx("win.wav")
except Exception:
    def load_sfx(_): return None

def play(sound):
    if sound:
        try:
            sound.play()
        except Exception:
            pass

# -------- LEADERBOARD ----------
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_leaderboard(lb):
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(lb, f, indent=2)
    except Exception as e:
        print("[WARN] Could not save leaderboard:", e)

leaderboard = load_leaderboard()

def add_score(name, seconds, solved):
    entry = {"name": name, "time": round(seconds, 2), "solved": solved, "ts": int(time.time())}
    leaderboard.append(entry)
   
    leaderboard.sort(key=lambda e: (e["time"], -e["solved"]))
    del leaderboard[MAX_LEADERBOARD:]
    save_leaderboard(leaderboard)

# -------- PUZZLES (20) ----------
PUZZLE_POOL = [
    {"question":"1. The field of robotics that deals with making a robot learn from experience is called\n\nA. Machine Learning\nB. Big Data\nC. Embedded Systems\nD. Electrical Engineering","answer":"A"},
    {"question":"2. Which type of AI is currently implemented in real-world applications like voice assistants and recommendation systems?\n\nA. Strong AI\nB. Existential AI\nC. Weak AI\nD. Decision AI","answer":"C"},
    {"question":"3. Which domain of AI is responsible for enabling machines to see and process images like humans?\n\nA. Natural Language Processing\nB. Expert Systems\nC. Computer Vision\nD. Supervised Learning","answer":"C"},
    {"question":"4. Which intelligence has the ability to use language effectively?\n\nA. Naturalistic\nB. Interpersonal\nC. Spatial\nD. Linguistic","answer":"D"},
    {"question":"5. Which of the following statements is/are correct about radio waves?\n\n(i) Wi-Fi and mobile data use radio frequencies to send and receive information.\n(ii) These are non-ionizing and safe for everyday use.\n(iii) They have the longest wavelength and lowest frequency in the electromagnetic spectrum.\n\nA. (i) only\nB. (i) and (ii) only\nC. (ii) and (iii) only\nD. (i), (ii) and (iii)","answer":"D"},
    {"question":"6. Identify the internet service where multiple search engines' responses are merged into one.\n\nA. Binary search\nB. Metasearch\nC. Megasearch\nD. Positive search","answer":"B"},
    {"question":"7. Which of the following statements hold(s) true regarding the system software?\n\nStatement 1: It manages CPU, memory, storage and input/output devices.\nStatement 2: It provides a platform for application software to run.\n\nA. Only Statement 1\nB. Only Statement 2\nC. Both Statement 1 and Statement 2\nD. Neither Statement 1 nor Statement 2","answer":"C"},
    {"question":"8. Which of the following data storage devices includes flash memory with a USB interface?\n\nA. Jump drive\nB. Optical disc drive\nC. Hard disk drive\nD. None of these","answer":"A"},
    {"question":"9. Which of the following is correct about the cache memory in a computer system?\n\nA. It is used to store data permanently.\nB. It is used to provide temporary storage for frequently accessed data.\nC. It is used to store the operating system.\nD. It is used to manage input and output operations.","answer":"B"},
    {"question":"10. Which of the following statements is/are incorrect about Scratch?\n\n(i) A hardware tool for robotics.\n(ii) A block-based visual programming language.\n(iii) A text-based coding language.\n(iv) Image editing software\n\nA. (i) only\nB. (i) and (ii) only\nC. (i), (iii) and (iv) only\nD. (ii), (iii) and (iv) only","answer":"C"},
    {"question":"11. Which of the following window components displays the name of the active worksheet in MS-Excel 2016?\n\nA. Formula Bar\nB. Navigation Bar\nC. Sheet Tab\nD. Name Box","answer":"C"},
    {"question":"12. Which of the following statements is incorrect about action buttons in MS-PowerPoint 2016?\n\nA. It can only be applied to text, not shapes.\nB. It can link to a custom show or external hyperlink.\nC. It can assign mouse click or mouse-over actions.\nD. It can be used to trigger actions like playing a sound.","answer":"A"},
    {"question":"13. Which of the following memory types is typically the fastest but smallest in capacity?\n\nA. Cache memory\nB. RAM\nC. ROM\nD. Hard disk","answer":"A"},
    {"question":"14. Which of the following are characteristics of third-generation computers?\n\n(i) Use of Integrated Circuits (ICs).\n(ii) Use of punched cards for input and output operations.\n(iii) Examples are IBM 370, PDP-11.\n(iv) Supported high-level languages.\n\nA. (i) and (ii) only\nB. (ii) and (iii) only\nC. (i), (iii) and (iv) only\nD. (ii), (iii) and (iv) only","answer":"C"},
    {"question":"15. Bookmark identifies a specific location in a document by assigned name. Which of the following is a valid name for a bookmark in MS-Word 2016?\n\nA. First name\nB. First_name\nC. 1st name\nD. 1st_name","answer":"B"},
    {"question":"16. Which of the following formulas will calculate the average of the numbers in cells A1 through A10, excluding empty cells in MS-Excel 2016?\n\nA. AVERAGE(A1:A10)\nB. =SUM(A1:A10)/COUNT(A1:A10)\nC. =SUM(A1:A10)/Average(A1:A10)\nD. Both A and B","answer":"D"},
    {"question":"17. Identify the following with respect to computer network.\n\nIt is a unique value associated with a network adapter called a NIC.\nIt is a 12-digit hexadecimal physical address that is engraved on NIC at the time of manufacturing.\n\nA. IP address\nB. MAC address\nC. HTTP address\nD. NTP address","answer":"B"},
    {"question":"18. Which of the following statements hold(s) true about the \"utility software\"?\n\nStatement 1: This type of software is used to analyse and maintain a computer.\nStatement 2: This software may come by default with Windows 10 OS like windows defender and disk cleanup tools.\n\nA. Only Statement 1\nB. Only Statement 2\nC. Both Statement 1 and Statement 2\nD. Neither Statement 1 nor Statement 2","answer":"C"},
    {"question":"19. Which of the following options is not found in Windows Ease of Access folder of Windows 10?\n\nA. Narrator\nB. Character Map\nC. Magnifier\nD. On-Screen Keyboard","answer":"B"},
    {"question":"20. Which of the following statements is incorrect regarding MS-PowerPoint 2016?\n\nA. You can apply transition only to the first and the last slide.\nB. You cannot hide any slide.\nC. You can create custom animations using Animation Pane.\nD. Both a and b","answer":"D"},
]

DEFAULT_MAX_LEVELS = 10

def make_question_order(max_levels):
    indices = list(range(len(PUZZLE_POOL)))
    random.shuffle(indices)
    max_levels = min(max_levels, len(indices))
    return indices[:max_levels]

# -------- MATRIX RAIN ----------
class ColumnDrop:
    def __init__(self, x, height, font_height):
        self.x = x
        self.chars = deque()
        self.reset(height, font_height)
    def reset(self, height, font_height):
        self.speed = random.uniform(50,300)
        self.length = random.randint(5, max(6, int(height/font_height/2)))
        self.y_positions = [-(i*font_height) for i in range(self.length)]
        self.chars = deque([chr(random.randint(33,126)) for _ in range(self.length)])
    def update(self, dt, height, font_height):
        for i in range(len(self.y_positions)):
            self.y_positions[i] += self.speed * dt
            if self.y_positions[i] > height:
                self.y_positions[i] = random.uniform(-height*0.5, 0)
        if random.random() < 0.08:
            idx = random.randrange(len(self.chars))
            self.chars[idx] = chr(random.randint(33,126))

FONT_H = FONT_SIZE + 6
COLUMNS = []
def init_rain():
    COLUMNS.clear()
    cols = max(10, WINDOW_SIZE[0] // FONT_H)
    for i in range(cols):
        x = i * FONT_H
        COLUMNS.append(ColumnDrop(x, WINDOW_SIZE[1], FONT_H))
init_rain()

class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.vx = random.uniform(-200,200)
        self.vy = random.uniform(-400,-150)
        self.size = random.randint(3,6)
        self.life = random.uniform(0.8,1.8)
        self.birth = time.time()
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
    def update(self, dt):
        self.vy += 800 * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
    def alive(self):
        return (time.time() - self.birth) < self.life

particles = []
def spawn_confetti(center, amount=40):
    for _ in range(amount):
        particles.append(Particle(center))

# -------- GAME STATE ----------
LINE_HEIGHT = FONT_SIZE + 6
PADDING = 24

class GameState:
    def __init__(self):
        self.stage = "boot"
        self.boot_timer = time.time()
        self.boot_sound_played = False
        self.puzzle_order = []
        self.current_index = -1  
        self.current = None
        self.input_text = ""
        self.messages = deque(maxlen=12)
        self.start_time = None
        self.solved = 0
        self.max_levels = DEFAULT_MAX_LEVELS
        self.level_start_time = None
        self.total_time = 0.0
        self.all_answers = []
        self.fullscreen = False

    def start_game(self):
        self.stage = "playing"
        self.puzzle_order = make_question_order(self.max_levels)
        self.current_index = -1
        self.current = None
        self.input_text = ""
        self.messages.clear()
        self.start_time = time.time()
        self.solved = 0
        self.all_answers = []
        self.level_start_time = None
        particles.clear()
        init_rain()
        self.next_level()

    def next_level(self):
        self.current_index += 1
        if self.current_index >= len(self.puzzle_order):
            self.finish()
            return
        q_idx = self.puzzle_order[self.current_index]
        self.current = PUZZLE_POOL[q_idx]
        self.level_start_time = time.time()
        self.input_text = ""
        self.messages.appendleft(f"LEVEL {self.current_index+1}/{self.max_levels}: Type NEXT to skip. Only single CAPITAL letters (A/B/C/D) accepted.")

    def check_answer(self, ans):
        if not self.current:
            self.messages.appendleft("> No active puzzle.")
            return
        ans_norm = ans.strip().upper()
        correct = str(self.current["answer"]).strip().upper()
        if ans_norm == "NEXT":
            self.messages.appendleft("> Question skipped. No points awarded.")
            self.next_level()
            return
        if len(ans_norm) != 1 or ans_norm not in ("A","B","C","D"):
            self.messages.appendleft("> Invalid format. Type a single CAPITAL letter (A/B/C/D) or NEXT to skip.")
            return
        if ans_norm == correct:
            delta = time.time() - (self.level_start_time or time.time())
            self.messages.appendleft(f"> Correct! Solved in {delta:.2f}s")
            self.solved += 1
            self.all_answers.append(correct)
            spawn_confetti((WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), amount=30)
            play(SFX_CORRECT)
            self.next_level()
        else:
            self.messages.appendleft("> Incorrect. Only one attempt — moving to next question.")

            self.next_level()

    def request_hint(self):
        if self.current:
            self.messages.appendleft("> Hint: Read the options carefully.")
        else:
            self.messages.appendleft("> No hint available.")

    def finish(self):
        self.total_time = time.time() - (self.start_time or time.time())
        self.stage = "win"
        play(SFX_WIN)

game = GameState()

# -------- DRAW HELPERS ----------
def draw_text(surf, text, pos, font_obj=font, color=TEXT_COLOR):
    txt = font_obj.render(text, True, color)
    surf.blit(txt, pos)

def draw_matrix(surface, dt):
    for col in COLUMNS:
        col.update(dt, WINDOW_SIZE[1], FONT_H)
        for i, y in enumerate(col.y_positions):
            if 0 <= y < WINDOW_SIZE[1]:
                ch = col.chars[i]
                surf_char = font.render(ch, True, (0, 255, 80))
                surface.blit(surf_char, (col.x, y))

# -------- SCREENS ----------
def draw_boot():
    screen.fill(BG_COLOR)
    if not game.boot_sound_played:
        play(SFX_BOOT)
        game.boot_sound_played = True

    draw_matrix(screen, 0)
    elapsed = time.time() - game.boot_timer
    for i, line in enumerate(BOOT_LINES):
        if elapsed > i * 0.6:
            draw_text(screen, line, (PADDING, 80 + i * LINE_HEIGHT))
    draw_text(screen, "Press SPACE to skip boot...", (PADDING, WINDOW_SIZE[1] - 60))

def draw_menu():
    screen.fill(BG_COLOR)
    draw_matrix(screen, 0)
    title = "=== HACK THE SYSTEM ==="
    pulse = 1.0 + 0.06 * (1 + math.sin(time.time() * 2))
    title_font_local = get_font(FONT_NAME, max(18, int(TITLE_FONT_SIZE * pulse)))
    draw_text(screen, title, (PADDING, 40), title_font_local)
    lines = [
        "",
        "1) Start Game",
        "2) Leaderboard",
        "3) Quit",
        "",
        "Controls: Type your answer, ENTER to submit, BACKSPACE to edit.",
        "Answers must be a single CAPITAL letter: A / B / C / D",
        "Type 'NEXT' to skip a question (no points). Type 'HINT' for a hint."
    ]
    for i, l in enumerate(lines):
        draw_text(screen, l, (PADDING, 140 + i * LINE_HEIGHT))

def draw_playing(dt):
    screen.fill(BG_COLOR)
    draw_matrix(screen, dt)

    # Instructions
    draw_text(screen, "Answer MUST be a SINGLE CAPITAL letter (A/B/C/D). Type NEXT to skip.", (PADDING, PADDING))
    # Level & progress
    draw_text(screen, f"Level: {game.current_index+1}/{game.max_levels}   Solved: {game.solved}", (PADDING, PADDING + 30))

    # Progress bar (green)
    bar_w = WINDOW_SIZE[0] - PADDING * 4
    bar_h = 14
    bar_x = PADDING
    bar_y = PADDING + 60
    progress = (game.solved / game.max_levels) if game.max_levels else 0
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
    pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, int(bar_w * progress), bar_h))

    # Current question — bold + purple
    if game.current:
        prompt_lines = game.current.get("question", "").split("\n")
        for i, line in enumerate(prompt_lines):
            draw_text(screen, line, (PADDING, PADDING + 100 + i * LINE_HEIGHT), font_bold, QUESTION_COLOR)

    # Messages (bottom-left)
    for i, m in enumerate(list(game.messages)[:8]):
        draw_text(screen, m, (PADDING, WINDOW_SIZE[1] - 220 + i * LINE_HEIGHT))

    # Input overlay + text
    overlay_height = 60
    overlay = pygame.Surface((WINDOW_SIZE[0], overlay_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, WINDOW_SIZE[1] - overlay_height))
    cursor = "_" if int(time.time() * 2) % 2 else ""
    input_surf = font.render("> " + game.input_text + cursor, True, INPUT_COLOR)
    screen.blit(input_surf, (PADDING, WINDOW_SIZE[1] - 45))

    # Confetti
    for p in particles:
        if p.alive():
            pygame.draw.rect(screen, p.color, (int(p.x), int(p.y), p.size, p.size))

def draw_win():
    screen.fill(BG_COLOR)
    draw_matrix(screen, 0)
    lines = [
        "=== MISSION COMPLETE ===",
        "",
        f"Solved: {game.solved}/{game.max_levels}",
        f"Total time: {game.total_time:.2f}s",
        "",
        "\"Knowledge is power — use it for defense, not destruction.\"",
        "",
        "Enter your name to save score and press ENTER:"
    ]
    for i, l in enumerate(lines):
        draw_text(screen, l, (PADDING, 40 + i * LINE_HEIGHT))
    draw_text(screen, "Session Answers: " + ", ".join(game.all_answers or ["<none>"]), (PADDING, WINDOW_SIZE[1] - 180))
    overlay_height = 60
    overlay = pygame.Surface((WINDOW_SIZE[0], overlay_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, WINDOW_SIZE[1] - overlay_height))
    cursor = "_" if int(time.time() * 2) % 2 else ""
    name_surf = font.render("> " + game.input_text + cursor, True, INPUT_COLOR)
    screen.blit(name_surf, (PADDING, WINDOW_SIZE[1] - 120))

def draw_leaderboard():
    screen.fill(BG_COLOR)
    draw_matrix(screen, 0)
    lines = ["=== LEADERBOARD ===", ""]
    if not leaderboard:
        lines.append("No scores yet.")
    else:
        for i, e in enumerate(leaderboard):
            lines.append(f"{i+1}. {e['name'][:15]:15} | Time: {e['time']:6} | Solved: {e['solved']}")
    lines.append("")
    lines.append("Press ESC to return to menu.")
    for i, l in enumerate(lines):
        draw_text(screen, l, (PADDING, 40 + i * LINE_HEIGHT))

# -------- INPUT HANDLERS ----------
def handle_menu_key(key):
    if key in (pygame.K_1,):
        game.start_game()
    elif key == pygame.K_2:
        game.stage = "leaderboard"
    elif key == pygame.K_3:
        save_leaderboard(leaderboard)
        pygame.quit()
        sys.exit()

def handle_playing_keydown(event):
    if event.key == pygame.K_BACKSPACE:
        game.input_text = game.input_text[:-1]
        return
    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        text = game.input_text.strip()
        tclean = text.upper()
        if tclean == "":
            pass
        elif tclean == "HINT":
            game.request_hint()
        elif tclean == "NEXT":
            game.messages.appendleft("> Skipped (no points).")
            game.next_level()
        elif len(tclean) == 1 and tclean in ("A", "B", "C", "D"):
            game.check_answer(tclean)
        else:
            game.messages.appendleft("> Invalid format. Type a single CAPITAL letter (A/B/C/D) or NEXT.")
        game.input_text = ""
        return
    if event.key == pygame.K_F11 or event.key == pygame.K_f:
        game.fullscreen = not game.fullscreen
        if game.fullscreen:
            pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(WINDOW_SIZE)
        return
    if hasattr(event, "unicode") and event.unicode and ord(event.unicode) >= 32:
        # append printable characters
        game.input_text += event.unicode

def handle_win_keydown(event):
    if event.key == pygame.K_BACKSPACE:
        game.input_text = game.input_text[:-1]
        return
    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        name = game.input_text.strip() or "anonymous"
        add_score(name, game.total_time, game.solved)
        game.input_text = ""
        game.stage = "leaderboard"
        return
    if hasattr(event, "unicode") and event.unicode and ord(event.unicode) >= 32:
        game.input_text += event.unicode

# -------- MAIN LOOP ----------
def main():
    last_time = time.time()
    running = True
    while running:
        dt = time.time() - last_time
        last_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_leaderboard(leaderboard)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.stage == "menu":
                        save_leaderboard(leaderboard)
                        running = False
                    elif game.stage in ("win", "leaderboard"):
                        game.stage = "menu"
                        game.input_text = ""
                    else:
                        game.stage = "menu"
                        game.input_text = ""
                    continue

                if game.stage == "boot" and event.key == pygame.K_SPACE:
                    game.stage = "menu"
                    
                    continue
                if game.stage == "menu":
                    if event.key == pygame.K_1:
                        game.start_game()
                        continue
                    if event.key == pygame.K_2:
                        game.stage = "leaderboard"
                        continue
                    if event.key == pygame.K_3:
                        save_leaderboard(leaderboard)
                        running = False
                        continue

            
                if game.stage == "playing":
                    handle_playing_keydown(event)
                elif game.stage == "win":
                    handle_win_keydown(event)
                elif game.stage == "leaderboard":
        
                    game.stage = "menu"
                    game.input_text = ""
           

       
        if game.stage == "playing":
            for p in particles:
                p.update(dt)


        if game.stage == "boot":
            draw_boot()
            if time.time() - game.boot_timer > 6:
                game.stage = "menu"
        elif game.stage == "menu":
            draw_menu()
        elif game.stage == "playing":
            draw_playing(dt)
        elif game.stage == "win":
            draw_win()
        elif game.stage == "leaderboard":
            draw_leaderboard()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

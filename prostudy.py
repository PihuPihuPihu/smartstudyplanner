import pygame
import sys
import pandas as pd
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Study Planner")

# Colors and Fonts
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
DARK_BLUE = (47, 86, 233)
LIGHT_BLUE = (100, 181, 246)
BLACK = (0, 0, 0)
GRAY = (240, 240, 240)
RED = (255, 99, 71)
GREEN = (50, 205, 50)
SHADOW_COLOR = (0, 0, 0, 100)  # Shadow effect
ACTIVE_COLOR = (70, 80, 160)

try:
    font = pygame.font.Font("arial.ttf", 36)
    small_font = pygame.font.Font("arial.ttf", 24)
    title_font = pygame.font.Font("arialbd.ttf", 48)
except:
    font = pygame.font.SysFont('arial', 36)
    small_font = pygame.font.SysFont('arial', 24)
    title_font = pygame.font.SysFont('arial', 48)

# Task data
study_data = pd.DataFrame(columns=['Subject', 'Duration', 'Priority', 'Deadline'])
schedule_display = pd.DataFrame()
SAVE_FILE = 'study_tasks.csv'
if not os.path.exists(SAVE_FILE):
    pd.DataFrame(columns=['Subject', 'Duration', 'Priority', 'Deadline']).to_csv(SAVE_FILE, index=False)

# Message Settings
message = {"text": "", "color": BLACK, "timer": 0}

class FancyButton:
    def __init__(self, text, rect, color, shadow=True):
        self.text = text
        self.rect = rect
        self.color = color
        self.shadow = shadow
    
    def draw(self):
        if self.shadow:
            shadow_rect = pygame.Rect(self.rect.x + 4, self.rect.y + 4, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=15)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        text_surf = font.render(self.text, True, WHITE)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buttons with shadow effects
buttons = {
    "Add Task": FancyButton("Add Task", pygame.Rect(50, 100, 220, 60), DARK_BLUE),
    "Generate Schedule": FancyButton("Generate Schedule", pygame.Rect(50, 180, 220, 60), DARK_BLUE),
    "Save Tasks": FancyButton("Save Tasks", pygame.Rect(50, 260, 220, 60), DARK_BLUE),
    "Load Tasks": FancyButton("Load Tasks", pygame.Rect(50, 340, 220, 60), DARK_BLUE),
    "View Schedule": FancyButton("View Schedule", pygame.Rect(50, 420, 220, 60), DARK_BLUE),
    "Clear All": FancyButton("Clear All", pygame.Rect(50, 500, 220, 60), RED)
}

def draw_gradient_background():
    gradient_top = (235, 245, 255)
    gradient_bottom = (255, 255, 255)
    for y in range(HEIGHT):
        progress = y / HEIGHT
        color = [int(gradient_top[i] + (gradient_bottom[i] - gradient_top[i]) * progress) for i in range(3)]
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def show_message(text, color=BLACK, duration=180):
    global message
    message = {"text": text, "color": color, "timer": duration}

def update_message():
    global message
    if message["timer"] > 0:
        message["timer"] -= 1
        if message["timer"] == 0:
            message["text"] = ""

def draw_buttons():
    for button in buttons.values():
        button.draw()

def draw_input_screen(task_input, active_field):
    input_panel = pygame.Rect(300, 50, WIDTH - 350, 600)
    pygame.draw.rect(screen, GRAY, input_panel, border_radius=20)
    
    title = title_font.render("Add New Task", True, DARK_BLUE)
    screen.blit(title, (350, 70))
    
    input_fields = ["Subject", "Duration", "Priority", "Deadline"]
    field_info = [
        "Enter task name",
        "Time (HH:MM)",
        "Priority (1-5)",
        "Day (e.g., Monday)"
    ]
    
    for i, (field, value) in enumerate(task_input.items()):
        y_pos = 150 + i * 100
        label = font.render(f"{field.capitalize()}:", True, DARK_BLUE)
        screen.blit(label, (350, y_pos))
        
        hint_text = small_font.render(field_info[i], True, BLUE)
        screen.blit(hint_text, (350, y_pos + 30))
        
        input_box = pygame.Rect(600, y_pos, 250, 40)
        color = ACTIVE_COLOR if active_field == field else WHITE
        pygame.draw.rect(screen, color, input_box, border_radius=8)
        
        text_surface = font.render(value, True, BLACK)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))

# Main game loop
def main():
    task_input = {"subject": "", "duration": "", "priority": "", "deadline": ""}
    active_field = "subject"
    clock = pygame.time.Clock()
    screen_mode = "main"
    
    while True:
        screen.fill(WHITE)
        draw_gradient_background()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if screen_mode == "main":
                    if buttons["Add Task"].is_clicked(pos):
                        screen_mode = "add_task"
                        show_message("Add Task screen opened!", GREEN)
                    elif buttons["Generate Schedule"].is_clicked(pos):
                        show_message("Schedule generated!", GREEN)
                    elif buttons["Save Tasks"].is_clicked(pos):
                        study_data.to_csv(SAVE_FILE, index=False)
                        show_message("Tasks saved!", GREEN)
                    elif buttons["Load Tasks"].is_clicked(pos):
                        show_message("Tasks loaded!", GREEN)
                    elif buttons["View Schedule"].is_clicked(pos):
                        show_message("Viewing schedule!", GREEN)
                    elif buttons["Clear All"].is_clicked(pos):
                        study_data.drop(study_data.index, inplace=True)
                        show_message("All tasks cleared!", RED)
        
        if screen_mode == "main":
            draw_buttons()
        elif screen_mode == "add_task":
            draw_input_screen(task_input, active_field)
        
        update_message()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()



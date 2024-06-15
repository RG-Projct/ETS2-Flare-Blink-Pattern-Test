import pygame
import time
import glob
import re

# Konfigurasi layar
LED_RADIUS = 10            # Radius LED
LED_COLOR = (0, 0, 255)    # Warna biru
BG_COLOR = (0, 0, 0)       # Warna hitam
MARGIN = 20                # Margin antara LED

blink_step_length = 0.15   # Lama kedip LED

# Inisialisasi pygame
pygame.init()
pygame.display.set_caption('Simulasi Kedip LED')
screen = None  # Menginisialisasi variabel screen

# Fungsi untuk membaca pola LED dari file .sii
def read_led_patterns_from_sii(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        patterns = re.findall(r'blink_pattern: "(.*?)"', content, re.DOTALL)
        return patterns

# Fungsi untuk menggambar LED
def draw_led(screen, on, position):
    pygame.draw.circle(screen, LED_COLOR if on else (50, 50, 50), position, LED_RADIUS)

# Simulasi kedipan LED
def main():
    global screen  # Menandai variabel screen sebagai global

    # Membaca semua file .sii dalam folder saat ini
    led_files = glob.glob("*.sii")

    # Memastikan ada file .sii yang diproses
    if not led_files:
        print("Tidak ada file LED (.sii) ditemukan dalam folder ini.")
        return

    # Membaca pola LED dari setiap file .sii
    led_patterns = []
    for file_path in led_files:
        patterns = read_led_patterns_from_sii(file_path)
        led_patterns.extend(patterns)  # Menambahkan semua pola dari file ke dalam list

    # Memperoleh jumlah baris dan kolom dari pola LED yang terdeteksi
    num_led_rows = len(led_files)
    num_led_cols = len(led_patterns) // num_led_rows

    # Menentukan panjang dan lebar jendela berdasarkan jumlah baris dan kolom LED yang terdeteksi
    screen_width = (2 * LED_RADIUS + MARGIN) * num_led_cols + MARGIN
    screen_height = (2 * LED_RADIUS + MARGIN) * num_led_rows + MARGIN
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Menentukan posisi LED
    led_positions = []
    for row in range(num_led_rows):
        row_positions = []
        for col in range(num_led_cols):
            x = MARGIN + col * (2 * LED_RADIUS + MARGIN)
            y = MARGIN + row * (2 * LED_RADIUS + MARGIN)
            row_positions.append((x, y))
        led_positions.append(row_positions)

    running = True
    indices = [0] * (num_led_rows * num_led_cols)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BG_COLOR)

        for i in range(len(led_patterns)):
            pattern = led_patterns[i]
            row = i // num_led_cols
            col = i % num_led_cols
            index = indices[i]
            draw_led(screen, pattern[index % len(pattern)] == 'X', led_positions[row][col])
            indices[i] = (indices[i] + 1) % len(pattern)

        pygame.display.flip()
        time.sleep(blink_step_length)

    pygame.quit()

if __name__ == "__main__":
    main()

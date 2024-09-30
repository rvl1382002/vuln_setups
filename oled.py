import time
import board
import busio
import paho.mqtt.client as mqtt
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont
import threading

# Define the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Define the display
display = SSD1306_I2C(128, 64, i2c)

# Create blank image for drawing.
image = Image.new("1", (display.width, display.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load a TTF font.
font = ImageFont.truetype("DejaVuSans.ttf", 18)  # Ensure you have this font in your environment

# Define text lines for scrolling
scrolling_lines = [
    "Initializing system...",
    "Loading modules...",
    "Connecting to server...",
    "System check complete.",
    "Monitoring started...",
    "Checking network status...",
    "Updating software packages...",
    "Disk space: 75% used",
    "CPU load: 45%",
    "Memory usage: 60%",
    "New log entry detected...",
    "Error: Network timeout",
    "Restarting services...",
    "Applying security patches...",
    "Backup completed successfully.",
    "User login detected: admin",
    "New device connected: USB drive",
    "Database synchronization complete.",
    "Analyzing traffic patterns...",
    "Firewall status: Active",
    "Temperature: 32°C",
    "Power supply: Stable",
    "Scheduled maintenance at 02:00 AM",
    "System uptime: 24 days",
    "Alert: High CPU usage",
    "Email server status: Online",
    "File transfer initiated...",
    "No threats detected.",
    "Service 'nginx' restarted.",
    "Network speed: 1Gbps",
    "Connected users: 5",
    "VPN connection established.",
    "Scanning for vulnerabilities...",
    "Log rotation completed.",
    "Storage array status: Healthy"
]

# MQTT Configuration
MQTT_BROKER = "172.16.18.226"
MQTT_TOPIC = "office/hacked"

# Global variable to track if we are in hacked mode
hacked = False
hacked_file_path = "/home/alpha/hacked.txt"

# Function to clear the display
def clear_display():
    display.fill(0)
    display.show()

# Function to draw text with optional inversion
def draw_text(draw, x, y, text, font, invert=False):
    if invert:
        text_width, text_height = draw.textsize(text, font=font)
        draw.rectangle((x, y, x + text_width, y + text_height), outline=1, fill=1)
        draw.text((x, y), text, font=font, fill=0)
    else:
        draw.text((x, y), text, font=font, fill=1)

# Function to check the hacked.txt file and update the hacked variable
def check_hacked_file():
    global hacked
    while True:
        try:
            with open(hacked_file_path, 'r') as f:
                content = f.read().strip().lower()
                if content == "true" and not hacked:
                    hacked = True
                    print("File indicates hacked")
                    display_hacked_message()
                elif content == "false" and hacked:
                    hacked = False
                    print("File indicates reset")
                    clear_display()  # Clear the display when reset
        except FileNotFoundError:
            print(f"File {hacked_file_path} not found!")
        except Exception as e:
            print(f"Error reading hacked file: {e}")
        
        time.sleep(5)  # Check every 5 seconds

# Function to display the "hacked" message
def display_hacked_message():
    clear_display()  # Clear the display immediately
    draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
    draw_text(draw, 0, 5, "You have been", font)
    draw_text(draw, 0, 25, "hacked!", font)
    draw_text(draw, 0, 45, "😱", font)
    display.image(image)
    display.show()

# MQTT message callback
def on_message(client, userdata, msg):
    global hacked
    message = msg.payload.decode("utf-8")
    if message == "True" and not hacked:
        hacked = True
        print("MQTT: hacked")
        display_hacked_message()
    elif message == "reset" and hacked:
        hacked = False
        print("MQTT: reset")
        clear_display()

# Main function to run the display
def run_display():
    global hacked
    print("In the display function: hacked is ", hacked)
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()

    clear_display()
    y = 0

    while True:
        if hacked:
            time.sleep(0.5)
            continue
        else:
            for i in range(len(scrolling_lines)):
                if hacked:
                    break  # Stop normal flow if hacked becomes True

                # Clear the image
                draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)

                # Draw scrolling text
                for j in range(len(scrolling_lines)):
                    if hacked:
                        break
                    draw_text(draw, 0, y + (j - i) * 20, scrolling_lines[j], font)  # Adjusted for larger font size

                # Update the display with the image
                display.image(image)
                display.show()

                # Pause for a moment
                time.sleep(0.5)

                # Check if we've reached the bottom of the scrolling text
                if i == len(scrolling_lines) - 1:
                    i = 0
        time.sleep(0.5)

if __name__ == "__main__":
    # Start the thread to monitor the hacked.txt file
    hacked_file_thread = threading.Thread(target=check_hacked_file)
    hacked_file_thread.daemon = True  # Daemon thread will exit when the main program exits
    hacked_file_thread.start()

    try:
        run_display()
    finally:
        clear_display()

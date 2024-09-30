#!/bin/bash

# Variables for file URLs
OLED_PY_URL="https://raw.githubusercontent.com/rvl1382002/vuln_setups/refs/heads/main/oled.py"
CHECK_HACK_SH_URL="https://raw.githubusercontent.com/rvl1382002/vuln_setups/refs/heads/main/check_hack.sh"
OLED_PY_PATH="/home/alpha/oled.py"
CHECK_HACK_SH_PATH="/home/alpha/check_hack.sh"

# Function to install required Python packages
install_dependencies() {
    echo "Installing Python dependencies..."
    sudo apt update
    sudo apt install -y python3-pip python3-pil python3-paho-mqtt fonts-dejavu sshpass
    pip3 install adafruit-circuitpython-ssd1306
}

# Function to download the oled.py and check_hack.sh scripts
download_scripts() {
    echo "Downloading oled.py..."
    wget -O "$OLED_PY_PATH" "$OLED_PY_URL"
    echo "Downloading check_hack.sh..."
    wget -O "$CHECK_HACK_SH_PATH" "$CHECK_HACK_SH_URL"
}

# Function to set executable permissions on check_hack.sh and oled.py
set_permissions() {
    echo "Setting executable permissions..."
    sudo chmod +x "$CHECK_HACK_SH_PATH"
    sudo chmod +x "$OLED_PY_PATH"
}

# Function to set up the cron job
setup_cron() {
    echo "Setting up cron job for check_hack.sh..."
    # Add the cron job to run check_hack.sh every minute
    (sudo crontab -l 2>/dev/null; echo "* * * * * /home/alpha/check_hack.sh") | sudo crontab -
}

# Function to check if a cron job already exists
check_cron_exists() {
    echo "Checking if cron job exists..."
    cron_job_exists=$(sudo crontab -l | grep "$CHECK_HACK_SH_PATH" | wc -l)
    if [ "$cron_job_exists" -eq "0" ]; then
        setup_cron
    else
        echo "Cron job for check_hack.sh already exists."
    fi
}

# Main setup function
main() {
    echo "Starting setup for OLED and hack check..."
    install_dependencies
    download_scripts
    set_permissions
    check_cron_exists
    run_oled_script
    echo "Setup completed."
}

# Execute main setup
main

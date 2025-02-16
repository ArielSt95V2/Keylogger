import keyboard
import csv

key_codes = set()

def on_key(event):
    vk = event.scan_code
    print(f"Key pressed: {event.name} (Scan Code: {vk})")
    key_codes.add((event.name, vk))

print("Press keys to collect their codes. Press ESC to finish.")
keyboard.on_press(on_key)

# Wait until ESC key is pressed
keyboard.wait('esc')

# Save results to a CSV file
csv_file = "keyboard_key_codes.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Key", "Scan Code"])
    for name, vk in sorted(key_codes, key=lambda x: x[1]):
        writer.writerow([name, vk])

print(f"\nCollected Key Codes saved to {csv_file}")

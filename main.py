import machine
import os


if __name__ == "__main__":
    files = os.listdir("/sd")
    for file in files:
        print(file)

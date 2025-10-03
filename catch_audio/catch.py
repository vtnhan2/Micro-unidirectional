import serial
import wave
import os
import time

SERIAL_PORT = 'COM14'          # Thay bằng cổng serial Arduino thực tế
BAUD_RATE = 115200
SAMPLE_RATE = 8000             # Khớp với sample rate Arduino (~8kHz)
RECORD_SECONDS = 10            # Thời gian thu âm (giây)

OUTPUT_DIR = r'D:\Sync_Drive\Naiscorp\mic_unidirector\catch_audio'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'output_8bit.wav')

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        print("Mở cổng serial, đợi Arduino khởi động...")
        time.sleep(2)  # Đợi Arduino reset và bắt đầu gửi dữ liệu

        print("Bắt đầu thu dữ liệu 8 bit...")
        data = bytearray()
        num_samples = SAMPLE_RATE * RECORD_SECONDS

        while len(data) < num_samples:
            if ser.in_waiting >= 1:
                sample = ser.read(1)
                data.append(sample[0])
            else:
                time.sleep(0.001)  # Đợi dữ liệu, tránh CPU chạy quá nhanh

        print(f"Ghi file WAV ở {OUTPUT_FILE} ...")
        with wave.open(OUTPUT_FILE, 'wb') as wav_file:
            wav_file.setnchannels(1)       # Mono
            wav_file.setsampwidth(1)       # 8 bit sample
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(data)

        print("Hoàn tất.")

if __name__ == '__main__':
    main()

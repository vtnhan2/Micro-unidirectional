import serial
import wave
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Cấu hình cổng Serial và thông số
SERIAL_PORT = 'COM14'       # Thay bằng cổng serial Arduino thực tế
BAUD_RATE = 115200
SAMPLE_RATE = 8000          # Sample rate khoảng 8kHz
RECORD_SECONDS = 10         # Thời gian thu âm (giây)

# Thư mục lưu file WAV
OUTPUT_DIR = r'D:\Sync_Drive\Naiscorp\mic_unidirector\catch_audio'

def plot_wav(filename):
    # Đọc file WAV
    with wave.open(filename, 'rb') as wav_file:
        n_frames = wav_file.getnframes()
        framerate = wav_file.getframerate()
        frames = wav_file.readframes(n_frames)

    # Chuyển sang numpy array 8-bit unsigned
    audio_data = np.frombuffer(frames, dtype=np.uint8)

    # Tạo trục thời gian tính theo giây
    time_axis = np.linspace(0, n_frames / framerate, num=n_frames)

    # Vẽ đồ thị
    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, audio_data)
    plt.title(f'Waveform - {os.path.basename(filename)}')
    plt.xlabel('Thời gian (s)')
    plt.ylabel('Biên độ')
    plt.grid(True)
    plt.show()


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    timestamp = datetime.now().strftime("%H_%M_%S - %d-%m-%y")  
    output_file = os.path.join(OUTPUT_DIR, f"{timestamp}.wav")

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Mở cổng serial, đợi Arduino khởi động...")
        time.sleep(2)

        print("Bắt đầu thu dữ liệu...")
        data = bytearray()
        num_samples = SAMPLE_RATE * RECORD_SECONDS

        start_time = time.time()

        while len(data) < num_samples:
            bytes_to_read = ser.in_waiting
            if bytes_to_read:
                to_read = min(bytes_to_read, num_samples - len(data))
                data += ser.read(to_read)
            else:
                time.sleep(0.001)

        end_time = time.time()
        actual_record_time = end_time - start_time
        expected_record_time = len(data) / SAMPLE_RATE
        actual_sample_rate = len(data) / actual_record_time

        print(f"Thời gian thực tế thu dữ liệu: {actual_record_time:.3f} giây")
        print(f"Thời gian âm thanh trong file WAV: {expected_record_time:.3f} giây")
        print(f"Sample rate thực tế: {actual_sample_rate:.2f} mẫu/giây")

        print(f"Ghi file WAV tại {output_file} ...")
        with wave.open(output_file, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(1)
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(data)

        print("Hoàn tất.")

    # Vẽ đồ thị waveform
    plot_wav(output_file)


if __name__ == '__main__':
    main()

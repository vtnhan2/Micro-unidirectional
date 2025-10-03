import serial
import wave
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

SERIAL_PORT = 'COM14'
BAUD_RATE = 115200
SAMPLE_RATE = 8000
RECORD_SECONDS = 10

OUTPUT_DIR = r'D:\Sync_Drive\Naiscorp\mic_unidirector\catch_audio\audio'
PLOT_DIR = os.path.join(OUTPUT_DIR, 'plots')  # Thư mục con để lưu ảnh plot

def plot_full_waveform(filename):
    # Đọc file WAV
    with wave.open(filename, 'rb') as wav_file:
        n_frames = wav_file.getnframes()
        framerate = wav_file.getframerate()
        frames = wav_file.readframes(n_frames)

    audio_data = np.frombuffer(frames, dtype=np.uint8)
    time_axis = np.linspace(0, n_frames / framerate, num=n_frames)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(time_axis, audio_data, color='blue')
    ax.set_title(f'Full Waveform - {os.path.basename(filename)}')
    ax.set_xlabel('Thời gian (s)')
    ax.set_ylabel('Biên độ')
    ax.grid(True)

    # Mặc định matplotlib hỗ trợ zoom, pan
    plt.show()

    # Lưu ảnh plot dưới file PNG trong thư mục PLOT_DIR
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)
    plot_file = os.path.join(PLOT_DIR, os.path.basename(filename).replace('.wav', '.png'))
    fig.savefig(plot_file)
    print(f'Đã lưu đồ thị toàn bộ tại: {plot_file}')


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    timestamp = datetime.now().strftime("%H_%M_%S - %d-%m-%y")
    output_file = os.path.join(OUTPUT_DIR, f"{timestamp}.wav")

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Mở cổng serial, đợi Arduino khởi động...")
        time.sleep(2)

        print("Bắt đầu thu dữ liệu...")
        num_samples = SAMPLE_RATE * RECORD_SECONDS
        data = bytearray()

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

    plot_full_waveform(output_file)


if __name__ == '__main__':
    main()

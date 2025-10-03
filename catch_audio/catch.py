import serial
import wave
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

SERIAL_PORT = 'COM14'       # Cổng serial Arduino
BAUD_RATE = 115200
SAMPLE_RATE = 8000
RECORD_SECONDS = 10

OUTPUT_DIR = r'D:\Sync_Drive\Naiscorp\mic_unidirector\catch_audio'


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    timestamp = datetime.now().strftime("%H_%M_%S - %d-%m-%y")
    output_file = os.path.join(OUTPUT_DIR, f"{timestamp}.wav")

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Mở cổng serial, đợi Arduino khởi động...")
        time.sleep(2)

        print("Bắt đầu thu dữ liệu và vẽ đồ thị realtime...")
        num_samples = SAMPLE_RATE * RECORD_SECONDS
        data = bytearray()

        plt.ion()
        fig, ax = plt.subplots()
        x = np.arange(0, 200)  # Hiển thị 200 mẫu trong plot window
        y = np.zeros(200)
        line, = ax.plot(x, y)
        ax.set_ylim(0, 255)
        ax.set_xlim(0, len(x))
        plt.title("Realtime audio waveform (8-bit PCM)")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")

        start_time = time.time()

        while len(data) < num_samples:
            bytes_to_read = ser.in_waiting
            if bytes_to_read:
                to_read = min(bytes_to_read, num_samples - len(data))
                new_data = ser.read(to_read)
                data += new_data

                # Cập nhật plot với dữ liệu mới nhất
                for b in new_data:
                    y = np.append(y[1:], b)
                line.set_ydata(y)
                fig.canvas.draw()
                fig.canvas.flush_events()
            else:
                time.sleep(0.001)

        end_time = time.time()
        plt.ioff()
        plt.show()

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


if __name__ == '__main__':
    main()

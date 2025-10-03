import serial
import wave
import os
import time

# Cấu hình cổng Serial và thông số
SERIAL_PORT = 'COM14'       # Thay bằng cổng serial Arduino thực tế
BAUD_RATE = 115200          # Phù hợp baudrate Arduino
SAMPLE_RATE = 8000          # Khớp với sample rate ~8kHz
RECORD_SECONDS = 10         # Thời gian thu âm (giây)

# Thư mục lưu file WAV
OUTPUT_DIR = r'D:\Sync_Drive\Naiscorp\mic_unidirector\catch_audio'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'output.wav')

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

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
                time.sleep(0.001)  # Ngủ 1ms tránh CPU quá tải

        end_time = time.time()
        actual_record_time = end_time - start_time
        expected_record_time = len(data) / SAMPLE_RATE
        actual_sample_rate = len(data) / actual_record_time

        print(f"Thời gian thực tế thu dữ liệu: {actual_record_time:.3f} giây")
        print(f"Thời gian âm thanh trong file WAV: {expected_record_time:.3f} giây")
        print(f"Sample rate thực tế: {actual_sample_rate:.2f} mẫu/giây")

        print(f"Ghi file WAV tại {OUTPUT_FILE} ...")
        with wave.open(OUTPUT_FILE, 'wb') as wav_file:
            wav_file.setnchannels(1)       # Mono
            wav_file.setsampwidth(1)       # 8-bit sample
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(data)

        print("Hoàn tất.")

if __name__ == '__main__':
    main()

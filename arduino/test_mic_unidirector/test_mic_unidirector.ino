// Đọc tín hiệu analog từ A0 và hiển thị lên Serial Plotter

void setup() {
  Serial.begin(9600);   // Khởi tạo Serial ở tốc độ 9600 baud
}

void loop() {
  int value = analogRead(A1);   // Đọc giá trị ADC (0 - 1023)
  Serial.println(value);        // Gửi giá trị lên Serial Plotter
  delay(10);                    // Delay nhỏ để ổn định (giảm tốc độ gửi)
}

# Thuật toán Fourier-Motzkin

Dự án này cài đặt thuật toán Fourier-Motzkin để giải bài toán tối ưu tuyến tính với 2 và 3 biến.

## Mô tả

Thuật toán Fourier-Motzkin là một phương pháp khử biến để giải hệ bất phương trình tuyến tính. Thuật toán hoạt động bằng cách loại bỏ từng biến một cách có hệ thống để tìm ra nghiệm tối ưu.

## Cấu trúc dự án

- `Fourier_motzkin_2.py`: Cài đặt thuật toán cho bài toán 3 biến (x, y, z)
- `Fourier_motzkin_3.py`: Cài đặt thuật toán cho bài toán 4 biến (x, y, z, t)
- `input1.txt`, `input2.txt`: Các file dữ liệu đầu vào mẫu

## Tính năng chính

### Fourier_motzkin_2.py (3 biến)
- Giải bài toán tối ưu với format: `ax + by + cz <= d`
- Hỗ trợ tìm giá trị lớn nhất (max) hoặc nhỏ nhất (min) của biến z
- Khử lần lượt biến x, y để tìm giá trị tối ưu của z
- Tìm ngược các giá trị tối ưu của y, x

### Fourier_motzkin_3.py (4 biến)  
- Giải bài toán tối ưu với format: `ax + by + cz + dt <= e`
- Hỗ trợ tìm giá trị lớn nhất (max) hoặc nhỏ nhất (min) của biến t
- Khử lần lượt biến x, y, z để tìm giá trị tối ưu của t
- Tìm ngược các giá trị tối ưu của z, y, x

## Cách sử dụng

### Nhập dữ liệu

Bạn có thể nhập dữ liệu theo 2 cách:

1. **Nhập thủ công**: Chạy chương trình và nhập từng dòng bất phương trình theo hướng dẫn trên màn hình. Kết thúc bằng một dòng trống.
2. **Đọc từ file input.txt**: Sử dụng file đầu vào (ví dụ: input1.txt, input2.txt, ...) theo đúng format, sau đó chạy chương trình với lệnh redirect:
   
   ```bash
   python3 Fourier_motzkin_2.py < input1.txt
   python3 Fourier_motzkin_3.py < input4.txt
   ```

### Chạy chương trình 3 biến:
```bash
python3 Fourier_motzkin_2.py
```

### Chạy chương trình 4 biến:
```bash
python3 Fourier_motzkin_3.py
```

## Định dạng đầu vào

### Cho 3 biến (x, y, z):
Nhập từng bất phương trình trên một dòng theo format: `a b c d`
Tương ứng với: `ax + by + cz <= d`

Ví dụ:
```
1 2 3 6
2 -1 1 4
-1 1 2 3

```
(Kết thúc bằng dòng trống)

### Cho 4 biến (x, y, z, t):
Nhập từng bất phương trình trên một dòng theo format: `a b c d e`
Tương ứng với: `ax + by + cz + dt <= e`

Ví dụ:
```
1 2 3 1 10
2 -1 1 2 8
-1 1 2 -1 5

```
(Kết thúc bằng dòng trống)

## Thuật toán

1. **Khử biến tuần tự**: Loại bỏ từng biến một cách có hệ thống
2. **Chuẩn hóa hệ số**: Đưa hệ số của biến mục tiêu về 1 (max) hoặc -1 (min)
3. **Kiểm tra tính khả thi**: Phát hiện các bất phương trình vô lý
4. **Tìm nghiệm tối ưu**: Xác định giá trị tối ưu của biến mục tiêu
5. **Tìm ngược nghiệm**: Xác định giá trị của các biến còn lại

## Xử lý lỗi

- Phát hiện bài toán vô nghiệm
- Phát hiện bài toán không có giá trị tối ưu (vô hạn)
- Loại bỏ các bất phương trình trùng lặp
- Xử lý các bất phương trình có hệ số biến bằng 0

## Ghi chú

- Chỉ dành cho mục đích tham khảo và học tập
- Không sao chép cho mục đích thương mại
- Code được viết với mục đích minh họa thuật toán
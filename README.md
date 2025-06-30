# Thuật toán Fourier-Motzkin

**Repo gốc:** [https://github.com/lechihoang/Fourier_Motzkin](https://github.com/lechihoang/Fourier_Motzkin)

Repo này cài đặt thuật toán Fourier-Motzkin để giải bài toán tối ưu tuyến tính với 2 và 3 biến.

## Mô tả

Thuật toán Fourier-Motzkin là một phương pháp khử biến để giải hệ bất phương trình tuyến tính. Thuật toán hoạt động bằng cách loại bỏ từng biến một cách có hệ thống để tìm ra nghiệm tối ưu.

## Cấu trúc 

- `Fourier_motzkin_2.py`: Cài đặt thuật toán cho bài toán 2 biến (x, y)
- `Fourier_motzkin_3.py`: Cài đặt thuật toán cho bài toán 3 biến (x, y, z)
- `input1.txt`, `input2.txt`: Các file dữ liệu đầu vào mẫu

## Tính năng chính

### Fourier_motzkin_2.py (2 biến)
- Sử dụng thêm biến mục tiêu z 
- Giải bài toán tối ưu với format: `ax + by + cz <= d`
- Hỗ trợ tìm giá trị lớn nhất (max) hoặc nhỏ nhất (min) của biến z
- Khử lần lượt biến x, y để tìm giá trị tối ưu của z
- Tìm ngược các giá trị tối ưu của y, x

### Fourier_motzkin_3.py (3 biến)  
- Sử dụng thêm biến mục tiêu t
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

### Chạy chương trình 2 biến:
```bash
python3 Fourier_motzkin_2.py
```

### Chạy chương trình 3 biến:
```bash
python3 Fourier_motzkin_3.py
```

## Định dạng đầu vào

### Cho 2 biến (x, y):
Nhập từng bất phương trình trên một dòng theo format: `a b c d`
Tương ứng với: `ax + by + cz <= d`

Ví dụ:
```
1 2 3 6
2 -1 1 4
-1 1 2 3
(Kết thúc bằng một dòng trống)

(Điền max \ min tùy theo yêu cầu tìm gía trị lớn nhất \ nhỏ nhất của hàm mục tiêu)
```

### Cho 3 biến (x, y, z):
Nhập từng bất phương trình trên một dòng theo format: `a b c d e`
Tương ứng với: `ax + by + cz + dt <= e`

Ví dụ:
```
1 2 3 1 10
2 -1 1 2 8
-1 1 2 -1 5
(Kết thúc bằng một dòng trống)

(Điền max \ min tùy theo yêu cầu tìm gía trị lớn nhất \ nhỏ nhất của hàm mục tiêu)
```


## Thuật toán

Quy trình giải bài toán tối ưu tuyến tính bằng phương pháp Fourier-Motzkin:

1. **Nhập hệ bất phương trình**
   - Nhập từng dòng bất phương trình theo đúng format.
   - Xác định biến mục tiêu cần tối ưu (z hoặc t).

2. **Khử biến tuần tự**
   - Lần lượt loại bỏ các biến không phải biến mục tiêu (ví dụ: x, y).
   - Ở mỗi bước, kết hợp các bất phương trình có hệ số dương và âm của biến đang khử để tạo ra hệ mới không còn biến đó.
   - Giữ lại các bất phương trình không chứa biến đang khử.

3. **Kiểm tra tính khả thi**
   - Nếu xuất hiện bất phương trình dạng `0 <= b` với `b < 0` thì hệ vô nghiệm, dừng thuật toán.
   - Loại bỏ các bất phương trình trùng lặp.

4. **Chuẩn hóa hệ số biến mục tiêu**
   - Đưa hệ số của biến mục tiêu về 1 (nếu tìm max) hoặc -1 (nếu tìm min) bằng cách chia cả hai vế cho hệ số đó.

5. **Tìm miền giá trị của biến mục tiêu**
   - Xác định các bất phương trình dạng `z <= b` (hoặc `t <= b`) và `-z <= b` (hoặc `-t <= b`).
   - Tìm giá trị lớn nhất (min các upper bound) hoặc nhỏ nhất (max các lower bound) thỏa mãn tất cả các ràng buộc.
   - Nếu không tồn tại miền giá trị hợp lệ, kết luận không có giá trị tối ưu.

6. **Tìm ngược nghiệm các biến còn lại**
   - Thay giá trị tối ưu của biến mục tiêu vào hệ bất phương trình trước đó để tìm miền giá trị của biến tiếp theo (ví dụ: tìm y, rồi x).
   - Lặp lại cho đến khi xác định được giá trị của tất cả các biến.

7. **Kết luận**
   - Nếu tìm được bộ giá trị thỏa mãn tất cả các ràng buộc, in ra nghiệm tối ưu.
   - Nếu ở bất kỳ bước nào miền giá trị rỗng, kết luận bài toán vô nghiệm.

## Xử lý lỗi

- Phát hiện bài toán vô nghiệm
- Phát hiện bài toán không có giá trị tối ưu 
- Loại bỏ các bất phương trình trùng lặp
- Xử lý các bất phương trình có hệ số biến bằng 0

## Ghi chú

- Code được viết với mục đích minh họa thuật toán
- Chỉ dành cho mục đích tham khảo và học tập, không sao chép dưới bất kì hình thức nào
import sys

# In ra các bất phương trình theo định dạng của ma trận
def print_matrix(ineqs):
    for ineq in ineqs:
        print("{:6.2f}x + {:6.2f}y + {:6.2f}z <= {:6.2f}".format(ineq[0], ineq[1], ineq[2], ineq[3]))

# Đưa hệ số của biến mục tiêu trong bất phương về 1 (hoặc -1 tùy bài toán)
def normalize_objective(ineqs):
    result = []
    for ineq in ineqs:
        a3 = ineq[2]
        if a3 > 0:
            result.append(tuple(x / a3 for x in ineq))
        elif a3 < 0:
            result.append(tuple(-x / abs(a3) for x in ineq))
        else:
            result.append(ineq)
    return result

# Bỏ các bất phương trình trùng nhau
def dedupe(ineqs):
    seen = set()
    return [x for x in ineqs if not (x in seen or seen.add(x))]

# Bỏ qua không xét tiếp hoặc kết luận vô nghiệm cho các hàng có hệ số biến đều bằng 0
def check_zero_row(ineqs):
    result = []
    for ineq in ineqs:
        if all(coef == 0 for coef in ineq[:-1]):
            if ineq[-1] < 0:
                print(f"Bất phương trình vô lý: 0 <= {ineq[-1]:.4f} => Bài toán vô nghiệm!")
                exit()
        else:
            result.append(ineq)
    return result

# Loại các bất phương trình theo từng biến
def eliminate(var_idx, ineqs):
    # Nhóm các bất phương trình hệ số của biến cần loại
    P = [ineq for ineq in ineqs if ineq[var_idx] > 0]
    N = [ineq for ineq in ineqs if ineq[var_idx] < 0]
    Z = [ineq for ineq in ineqs if ineq[var_idx] == 0]

    # Giữ nguyên bất phương trình nếu hệ số biến cần loại = 0, 
    # kết hợp hai bất phương trình bất kì có hệ số biến cần loại ngược dấu nhau để đưa hệ số biến cần loại = 0

    result = Z + [tuple(-n[var_idx]*p[i] + p[var_idx]*n[i] for i in range(4)) for p in P for n in N]
    result = dedupe(result)
    return result

# Fourier-Motzkin cho bài toán tối ưu hai biến
def fourier_motzkin_2var(constraints, sense):
    matrices = []

    # Khử x
    m1 = eliminate(0, constraints)
    m1 = check_zero_row(m1)
    matrices.append(m1)
    print("Sau khi khử x, có các bất phương trình như sau: ")
    print_matrix(m1)

    # Khử y
    m2 = eliminate(1, matrices[0])
    m2 = check_zero_row(m2)
    matrices.append(m2)
    print("Sau khi khử y, có các bất phương trình như sau: ")
    print_matrix(m2)

    # Chuẩn hóa hệ số z
    m3 = normalize_objective(matrices[1])
    m3 = check_zero_row(m3)
    matrices.append(m3)

    # Nếu tìm max, đưa hệ số về 1, ngược lại thì -1
    z_coef = 1 if sense == 'max' else -1
    print(f"Đưa hệ số của z về {z_coef}, ta được: ")
    print_matrix(m3)

    # Chỉ xét giá trị nếu hệ số của z khác 0
    bounds = [ineq[3] for ineq in m3 if ineq[2] > 0]
    if not bounds:
        print("Không tìm ra giá trị tối ưu thỏa mãn")
        exit()
    return (min(bounds) if sense == 'max' else max(bounds)), matrices

# Tìm khoảng giá trị tối ưu của một biến sau khi biết được các gía trị tối ưu trước đó 
def find_bound(matrix, known_indices, known_values, target_idx):
    new_ineqs = []

    # Thế các giá trị đã biết, chuyển vế đổi dấu vào hệ số tự do
    for ineq in matrix:
        coeffs = list(ineq[:3])
        b = ineq[3]
        for idx, val in zip(known_indices, known_values):
            b -= coeffs[idx] * val
            coeffs[idx] = 0.0
        a = coeffs[target_idx]
        if a != 0:
            sign = 1.0 if a > 0 else -1.0
            new_coeffs = [0.0, 0.0, 0.0]
            new_coeffs[target_idx] = sign
            new_ineqs.append(tuple(new_coeffs + [sign * b / abs(a)]))
        else:
            new_coeffs = [0.0, 0.0, 0.0]
            new_ineqs.append(tuple(new_coeffs + [b]))
            
    # Chia hệ số tự do thành hai trường hợp dựa trên hệ số của biến cần tính âm hay dương
    upper = [ineq[3] for ineq in new_ineqs if ineq[target_idx] > 0]
    lower = [ineq[3] for ineq in new_ineqs if ineq[target_idx] < 0]

    # Tìm khoảng giá trị hợp lệ
    var_max = min(upper) if upper else float('inf')
    var_min = max(lower) if lower else float('-inf')

    # In kết quả
    print_matrix(new_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của biến {['x','y','z'][target_idx]} cho giá trị tối ưu là: {var_min:.4f} <= {['x','y','z'][target_idx]} <= {var_max:.4f}")
    return var_min, var_max

if __name__ == '__main__':
    # Nhập ma trận hệ số 
    print("Nhập toàn bộ ma trận bất phương trình (mỗi dòng: a b c d, kết thúc bằng dòng rỗng).\nLưu ý: Ghi đúng format: ax + by + cz <= d")
    matrix = []
    for line in sys.stdin:
        if not line.strip():
            break
        parts = [float(x) for x in line.replace(',',' ').split()]
        matrix.append(tuple(parts))

    # Nhập lựa chọn tìm max hay min
    sense = input("Bạn muốn tìm giá trị lớn nhất (max) hay nhỏ nhất (min) của z? (max/min): ").strip().lower()

    # In ra các điều kiện của bài toán
    print("Bất phương trình của bài toán đã cho:");
    print_matrix(matrix)

    # Thực hiện giải bài toán bằng Fourier-Motzkin
    z_optimal, matrices = fourier_motzkin_2var(matrix, sense)
    print(f"Giá trị cực trị z = {z_optimal:.4f}")

    # Thay ngược z để tìm y lúc giá trị tối ưu
    print("Thay giá trị của z vào các bất phương trình có sau khi khử x ta được: ")
    y_min, y_max = find_bound(matrices[0], [2], [z_optimal], 1)
    if y_min > y_max:
        print("Bài toán vô nghiệm ở biến y!")
        exit()

    # Thay ngược y, z để tìm x lúc giá trị tối ưu
    print("Thay giá trị của y, z vào các bất phương trình lúc đầu ta được: ")
    x_min, x_max = find_bound(matrix, [1,2], [y_max, z_optimal], 0)
    if x_min > x_max:
        print("Bài toán vô nghiệm ở biến x!")
        exit()

    # In bộ ngiệm tối ưu
    print(f"Bài toán có nghiệm với bộ nghiệm tối ưu: x = {x_max:.4f}, y = {y_max:.4f}, z = {z_optimal:.4f}")


import sys

# In ra các bất phương trình theo định dạng của ma trận (4 biến: x, y, z, t)
def print_matrix(ineqs):
    for ineq in ineqs:
        print("{:6.2f}x + {:6.2f}y + {:6.2f}z + {:6.2f}t <= {:6.2f}".format(ineq[0], ineq[1], ineq[2], ineq[3], ineq[4]))

# Đưa hệ số của biến mục tiêu trong bất phương về 1 (hoặc -1 tùy bài toán)
def normalize_objective(ineqs):
    result = []
    for ineq in ineqs:
        a4 = ineq[3]
        if a4 > 0:
            result.append(tuple(x / a4 for x in ineq))
        elif a4 < 0:
            result.append(tuple(-x / abs(a4) for x in ineq))
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
    result = Z + [tuple(-n[var_idx]*p[i] + p[var_idx]*n[i] for i in range(5)) for p in P for n in N]
    result = dedupe(result)
    return result

# Fourier-Motzkin cho bài toán tối ưu ba biến (4 biến x, y, z, t)
def fourier_motzkin_3var(constraints, sense):
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

    # Khử z
    m3 = eliminate(2, matrices[1])
    m3 = check_zero_row(m3)
    matrices.append(m3)
    print("Sau khi khử z, có các bất phương trình như sau: ")
    print_matrix(m3)

    # Chuẩn hóa hệ số t
    m4 = normalize_objective(matrices[2])
    m4 = check_zero_row(m4)
    matrices.append(m4)
    t_coef = 1 if sense == 'max' else -1
    print(f"Đưa hệ số của t về {t_coef}, ta được: ")
    print_matrix(m4)

    # Chỉ xét giá trị nếu hệ số của t khác 0
    bounds = [ineq[4] for ineq in m4 if ineq[3] > 0]
    if not bounds:
        print("Không tìm ra giá trị tối ưu thỏa mãn")
        exit()
    return (min(bounds) if sense == 'max' else max(bounds)), matrices

# Tìm khoảng giá trị tối ưu của một biến sau khi biết được các giá trị tối ưu trước đó 
def find_bounds(matrix, known_indices, known_values, target_idx):
    new_ineqs = []

    # Thế các giá trị đã biết, chuyển vế đổi dấu vào hệ số tự do
    for ineq in matrix:
        coeffs = list(ineq[:4])
        b = ineq[4]
        for idx, val in zip(known_indices, known_values):
            b -= coeffs[idx] * val
            coeffs[idx] = 0.0
        a = coeffs[target_idx]
        if a != 0:
            sign = 1.0 if a > 0 else -1.0
            new_coeffs = [0.0, 0.0, 0.0, 0.0]
            new_coeffs[target_idx] = sign
            new_ineqs.append(tuple(new_coeffs + [sign * b / abs(a)]))
        else:
            new_coeffs = [0.0, 0.0, 0.0, 0.0]
            new_ineqs.append(tuple(new_coeffs + [b]))

    # Chia hệ số tự do thành hai trường hợp dựa trên hệ số của biến cần tính âm hay dương
    upper = [ineq[4] for ineq in new_ineqs if ineq[target_idx] > 0]
    lower = [ineq[4] for ineq in new_ineqs if ineq[target_idx] < 0]

    # Tìm khoảng giá trị hợp lệ
    var_max = min(upper) if upper else float('inf')
    var_min = max(lower) if lower else float('-inf')
    
    # In kết quả
    print_matrix(new_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của biến {['x','y','z','t'][target_idx]} cho giá trị tối ưu là: {var_min:.4f} <= {['x','y','z','t'][target_idx]} <= {var_max:.4f}")
    return var_min, var_max

if __name__ == '__main__':
    # Nhập ma trận hệ số 
    print("Nhập toàn bộ ma trận bất phương trình (mỗi dòng: a b c d e, kết thúc bằng dòng rỗng).\nLưu ý: Ghi đúng format: ax + by + cz + dt <= e")
    matrix = []
    for line in sys.stdin:
        if not line.strip():
            break
        parts = [float(x) for x in line.replace(',', ' ').split()]
        matrix.append(tuple(parts))

    # Nhập lựa chọn tìm max hay min
    sense = input("Bạn muốn tìm giá trị lớn nhất (max) hay nhỏ nhất (min) của t? (max/min): ").strip().lower()

    # In ra các điều kiện của bài toán
    print("Bất phương trình của bài toán đã cho:")
    print_matrix(matrix)

    # Thực hiện giải bài toán bằng Fourier-Motzkin
    t_optimal, matrices = fourier_motzkin_3var(matrix, sense)
    print(f"Giá trị cực trị t = {t_optimal:.4f}")

    # Thay ngược t để tìm z lúc giá trị tối ưu
    print("Thay giá trị của t vào các bất phương trình sau khi khử x, y ta được: ")
    z_min, z_max = find_bounds(matrices[0], [3], [t_optimal], 2)
    if z_min > z_max:
        print("Bài toán vô nghiệm ở biến z!")
        exit()

    # Thay ngược z, t để tìm y lúc giá trị tối ưu
    print("Thay giá trị của z, t vào các bất phương trình sau khi khử x ta được: ")
    y_min, y_max = find_bounds(matrix, [2,3], [z_max, t_optimal], 1)
    if y_min > y_max:
        print("Bài toán vô nghiệm ở biến y!")
        exit()

    # Thay ngược y, z, t để tìm x lúc giá trị tối ưu
    print("Thay giá trị của y, z, t vào các bất phương trình lúc đầu ta được: ")
    x_min, x_max = find_bounds(matrix, [1,2,3], [y_max, z_max, t_optimal], 0)
    if x_min > x_max:
        print("Bài toán vô nghiệm ở biến x!")
        exit()
    
    # In ra bộ nghiệm tối ưu
    print("Bài toán có nghiệm với bộ nghiệm tối ưu:")
    print(f"x = {x_max:.4f}, y = {y_max:.4f}, z = {z_max:.4f}, t = {t_optimal:.4f}")

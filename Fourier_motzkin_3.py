def print_matrix(ineqs):
    for ineq in ineqs:
        print("{:6.2f}x + {:6.2f}y + {:6.2f}z + {:6.2f}t <= {:6.2f}".format(ineq[0], ineq[1], ineq[2], ineq[3], ineq[4]))

def normalize_t(ineqs):
    normalized = []
    for ineq in ineqs:
        a4 = ineq[3]
        if a4 > 0:
            normalized.append(tuple(x / a4 for x in ineq))
        elif a4 < 0:
            normalized.append(tuple(-x / abs(a4) for x in ineq))
        else:
            normalized.append(ineq)
    return normalized

def dedupe(ineqs):
    seen = set()
    return [x for x in ineqs if not (x in seen or seen.add(x))]

def eliminate(var_idx, ineqs):
    P = [ineq for ineq in ineqs if ineq[var_idx] > 0]
    N = [ineq for ineq in ineqs if ineq[var_idx] < 0]
    Z = [ineq for ineq in ineqs if ineq[var_idx] == 0]
    result = Z + [tuple(-n[var_idx]*p[i] + p[var_idx]*n[i] for i in range(5)) for p in P for n in N]
    result = dedupe(result)
    return result

def check_zero_row_5(ineqs):
    filtered = []
    for ineq in ineqs:
        # Kiểm tra đúng nghĩa đen: tất cả hệ số biến đều bằng 0
        if all(coef == 0 for coef in ineq[:-1]):
            if ineq[-1] < 0:
                print(f"Bất phương trình vô lý: 0 <= {ineq[-1]:.4f} => Bài toán vô nghiệm!")
                exit()
            # Nếu luôn đúng thì bỏ qua
        else:
            filtered.append(ineq)
    return filtered

def fourier_motzkin_3var(constraints, sense):
    matrix1 = eliminate(0, constraints)
    matrix1 = check_zero_row_5(matrix1)
    print("Sau khi khử x, có các bất phương trình như sau: ")
    print_matrix(matrix1)
    matrix2 = eliminate(1, matrix1)
    matrix2 = check_zero_row_5(matrix2)
    print("Sau khi khử y, có các bất phương trình như sau: ")
    print_matrix(matrix2)
    matrix3 = eliminate(2, matrix2)
    matrix3 = check_zero_row_5(matrix3)
    print("Sau khi khử z, có các bất phương trình như sau: ")
    print_matrix(matrix3)
    matrix4 = normalize_t(matrix3)
    matrix4 = check_zero_row_5(matrix4)
    print("Đưa hệ số của t về 1, ta được: ")
    print_matrix(matrix4)
    bounds = [ineq[4] for ineq in matrix4 if ineq[3] > 0]
    if not bounds:
        raise ValueError('Không có giá trị thỏa mãn bài toán')
    return min(bounds) if sense == 'max' else max(bounds), matrix1, matrix2, matrix3, matrix4

def find_z_bounds(matrix2, t_optimal):
    z_ineqs = []
    for ineq in matrix2:
        a1, a2, a3, a4, b = ineq
        b_new = b - a4 * t_optimal
        if a3 != 0:
            sign = 1 if a3 > 0 else -1
            z_ineqs.append((sign * a1 / abs(a3), sign * a2 / abs(a3), sign * 1.0, 0.0, sign * b_new / abs(a3)))
        else:
            z_ineqs.append((a1, a2, a3, 0, b_new))
    z_upper = [ineq[4] for ineq in z_ineqs if ineq[2] > 0]
    z_lower = [ineq[4] for ineq in z_ineqs if ineq[2] < 0]
    z_max = min(z_upper) if z_upper else float('inf')
    z_min = max(z_lower) if z_lower else float('-inf')
    print("Thay giá trị của t vào các bất phương trình chỉ có z, ta được: ")
    print_matrix(z_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của z cho giá trị tối ưu là: {z_min} <= z <= {z_max}")
    return z_min, z_max

def find_y_bounds(matrix1, z_value, t_value):
    y_ineqs = []
    for ineq in matrix1:
        a1, a2, a3, a4, b = ineq
        b_new = b - a3 * z_value - a4 * t_value
        if a2 != 0:
            sign = 1 if a2 > 0 else -1
            y_ineqs.append((sign * a1 / abs(a2), sign * 1.0, 0.0, 0.0, sign * b_new / abs(a2)))
        else:
            y_ineqs.append((a1, a2, 0, 0, b_new))
    y_upper = [ineq[4] for ineq in y_ineqs if ineq[1] > 0]
    y_lower = [ineq[4] for ineq in y_ineqs if ineq[1] < 0]
    y_max = min(y_upper) if y_upper else float('inf')
    y_min = max(y_lower) if y_lower else float('-inf')
    print("Thay giá trị của z, t vào các bất phương trình chỉ có y, ta được: ")
    print_matrix(y_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của y cho giá trị tối ưu là: {y_min} <= y <= {y_max}")
    return y_min, y_max

def find_x_bounds(matrix, y_value, z_value, t_value):
    x_ineqs = []
    for ineq in matrix:
        a1, a2, a3, a4, b = ineq
        b_new = b - a2 * y_value - a3 * z_value - a4 * t_value
        if a1 != 0:
            sign = 1 if a1 > 0 else -1
            x_ineqs.append((sign * 1.0, 0.0, 0.0, 0.0, sign * b_new / abs(a1)))
        else:
            x_ineqs.append((a1, 0.0, 0.0, 0.0, b_new))
    x_upper = [ineq[4] for ineq in x_ineqs if ineq[0] > 0]
    x_lower = [ineq[4] for ineq in x_ineqs if ineq[0] < 0]
    x_max = min(x_upper) if x_upper else float('inf')
    x_min = max(x_lower) if x_lower else float('-inf')
    print("Thay giá trị của y, z, t vào các bất phương trình chỉ có x, ta được: ")
    print_matrix(x_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của x cho giá trị tối ưu là: {x_min} <= x <= {x_max}")
    return x_min, x_max

if __name__ == '__main__':
    matrix = [
        # (a1, a2, a3, a4, b)
        (-2, -3, -4, -1, 0),   # -2x -3y -4z - t <= 0 (hàm mục tiêu)
    (3, 2, 1, 0, 10),      # 3x + 2y + z <= 10
    (2, 5, 3, 0, 15),      # 2x + 5y + 3z <= 15
    (1, 0, 0, 0, 0),       # x >= 0
    (0, 1, 0, 0, 0),       # y >= 0
    (0, 0, 1, 0, 0) 
    ]
    t_optimal, matrix1, matrix2, matrix3, matrix4 = fourier_motzkin_3var(matrix, 'max')
    print("Giá trị cực trị t =", t_optimal)
    z_min, z_max = find_z_bounds(matrix2, t_optimal)
    if z_min > z_max:
        print("Bài toán vô nghiệm ở biến z!")
        exit()
    y_min, y_max = find_y_bounds(matrix1, z_max, t_optimal)
    if y_min > y_max:
        print("Bài toán vô nghiệm ở biến y!")
        exit()
    x_min, x_max = find_x_bounds(matrix, y_max, z_max, t_optimal)
    if x_min > x_max:
        print("Bài toán vô nghiệm ở biến x!")
        exit()
    print(f"Bộ nghiệm tối ưu: x = {x_max}, y = {y_max}, z = {z_max}, t = {t_optimal}")

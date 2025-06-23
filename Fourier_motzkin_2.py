def print_matrix(ineqs):
    for ineq in ineqs:
        print("{:6.2f}x + {:6.2f}y + {:6.2f}z <= {:6.2f}".format(ineq[0], ineq[1], ineq[2], ineq[3]))

def normalize_z(ineqs):
    normalized = []
    for ineq in ineqs:
        a3 = ineq[2]
        if a3 > 0:
            normalized.append(tuple(x / a3 for x in ineq))
        elif a3 < 0:
            # Đổi dấu toàn bộ để đưa về dạng <= rồi chia cho |a3|
            normalized.append(tuple(-x / abs(a3) for x in ineq))
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
    result = Z + [tuple(-n[var_idx]*p[i] + p[var_idx]*n[i] for i in range(4)) for p in P for n in N]
    result = dedupe(result)
    return result

def check_zero_row(ineqs):
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

def fourier_motzkin_2var(constraints, sense):
    matrix1 = eliminate(0, constraints)
    matrix1 = check_zero_row(matrix1)
    print("Sau khi khử x, có các bất phương trình như sau: ")
    print_matrix(matrix1)
    matrix2 = eliminate(1, matrix1)
    matrix2 = check_zero_row(matrix2)
    print("Sau khi khử y, có các bất phương trình như sau: ")
    print_matrix(matrix2)
    matrix3 = normalize_z(matrix2)  # Bước chuẩn hóa hệ số z
    matrix3 = check_zero_row(matrix3)
    print("Đưa hệ số của z về 1, ta được: ")
    print_matrix(matrix3)

    bounds = [ineq[3] for ineq in matrix3 if ineq[2] > 0]
    if not bounds:
        raise ValueError('Không có giá trị thỏa mãn bài toán')
    return min(bounds) if sense == 'max' else max(bounds), matrix1, matrix2, matrix3

def find_y_bounds(matrix1, z_optimal):
    y_ineqs = []
    for ineq in matrix1:
        a1, a2, a3, b = ineq
        b_new = b - a3 * z_optimal
        if a2 != 0:
            sign = 1 if a2 > 0 else -1
            y_ineqs.append((sign * a1 / abs(a2), sign * 1.0, 0.0, sign * b_new / abs(a2)))
        else:
            y_ineqs.append((a1, a2, 0, b_new))
    y_upper = [ineq[3] for ineq in y_ineqs if ineq[1] > 0]
    y_lower = [ineq[3] for ineq in y_ineqs if ineq[1] < 0]
    y_max = min(y_upper) if y_upper else float('inf')
    y_min = max(y_lower) if y_lower else float('-inf')
    print("Thay giá trị của z vào các bất phương trình chỉ có y, ta được: ")
    print_matrix(y_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của y cho giá trị tối ưu là: {y_min:.4f} <= y <= {y_max:.4f}")
    return y_min, y_max

def find_x_bounds(matrix, y_value, z_value):
    x_ineqs = []
    for ineq in matrix:
        a1, a2, a3, b = ineq
        b_new = b - a2 * y_value - a3 * z_value
        if a1 != 0:
            sign = 1 if a1 > 0 else -1
            x_ineqs.append((sign * 1.0, 0.0, 0.0, sign * b_new / abs(a1)))
        else:
            x_ineqs.append((a1, 0.0, 0.0, b_new))
    x_upper = [ineq[3] for ineq in x_ineqs if ineq[0] > 0]
    x_lower = [ineq[3] for ineq in x_ineqs if ineq[0] < 0]
    x_max = min(x_upper) if x_upper else float('inf')
    x_min = max(x_lower) if x_lower else float('-inf')
    print("Thay giá trị của y, z vào các bất phương trình chỉ có x, ta được: ")
    print_matrix(x_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của x cho giá trị tối ưu là: {x_min:.4f} <= x <= {x_max:.4f}")
    return x_min, x_max

if __name__ == '__main__':
    matrix = [
    (2, 1, 0, 6),
    (1, 2, 0, 8),
    (1, -1, 0, 1),
    (1, 0, 0, 2),
    (-1, 0, 0, 0),
    (0, -1, 0, 0),
    (-2000, -3000, 1, 0)
    ]
    z_optimal, matrix1, matrix2, matrix3 = fourier_motzkin_2var(matrix, 'max')
    print(f"Giá trị cực trị z = {z_optimal:.4f}")
    y_min, y_max = find_y_bounds(matrix1, z_optimal)
    if y_min > y_max:
        print("Bài toán vô nghiệm ở biến y!")
        exit()
    # Lấy giá trị y_optimal là y_max (tối đa hóa z)
    x_min, x_max = find_x_bounds(matrix, y_max, z_optimal)
    if x_min > x_max:
        print("Bài toán vô nghiệm ở biến x!")
        exit()
    print(f"Bộ nghiệm tối ưu: x = {x_max:.4f}, y = {y_max:.4f}, z = {z_optimal:.4f}")
    # Nếu muốn in lại các ma trận:
    # print_matrix(matrix1, 1)
    # print_matrix(matrix2, 2)
    # print_matrix(matrix3, 3)

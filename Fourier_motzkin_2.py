import sys

def print_matrix(ineqs):
    for ineq in ineqs:
        print("{:6.2f}x + {:6.2f}y + {:6.2f}z <= {:6.2f}".format(ineq[0], ineq[1], ineq[2], ineq[3]))

def normalize_objective(ineqs, sense):
    result = []
    for ineq in ineqs:
        a3 = ineq[2]
        if sense == 'max':
            if a3 > 0:
                result.append(tuple(x / a3 for x in ineq))
            elif a3 < 0:
                result.append(tuple(-x / abs(a3) for x in ineq))
            else:
                result.append(ineq)
        else:
            if a3 > 0:
                result.append(tuple(-x / abs(a3) for x in ineq))
            elif a3 < 0:
                result.append(tuple(x / a3 for x in ineq))
            else:
                result.append(ineq)
    return result

def dedupe(ineqs):
    seen = set()
    return [x for x in ineqs if not (x in seen or seen.add(x))]

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

def eliminate(var_idx, ineqs):
    P = [ineq for ineq in ineqs if ineq[var_idx] > 0]
    N = [ineq for ineq in ineqs if ineq[var_idx] < 0]
    Z = [ineq for ineq in ineqs if ineq[var_idx] == 0]

    result = Z + [tuple(-n[var_idx]*p[i] + p[var_idx]*n[i] for i in range(4)) for p in P for n in N]
    result = dedupe(result)
    return result

def fourier_motzkin_2var(constraints, sense):
    matrices = []

    m1 = eliminate(0, constraints)
    m1 = check_zero_row(m1)
    matrices.append(m1)
    print("Sau khi khử x, có các bất phương trình như sau: ")
    print_matrix(m1)

    m2 = eliminate(1, matrices[0])
    m2 = check_zero_row(m2)
    matrices.append(m2)
    print("Sau khi khử y, có các bất phương trình như sau: ")
    print_matrix(m2)

    m3 = normalize_objective(matrices[1], sense)
    m3 = check_zero_row(m3)
    matrices.append(m3)

    z_coef = 1 if sense == 'max' else -1
    print(f"Đưa hệ số của z về {z_coef}, ta được: ")
    print_matrix(m3)

    upper_bounds = [ineq[3] for ineq in m3 if ineq[2] > 0]
    lower_bounds = [ineq[3] for ineq in m3 if ineq[2] < 0]

    z_max = min(upper_bounds) if upper_bounds else float('inf')
    z_min = max([-b for b in lower_bounds]) if lower_bounds else float('-inf')

    if z_min > z_max:
        print("Không tìm ra giá trị tối ưu thỏa mãn")
        exit()
    if sense == 'max':
        if z_max == float('inf'):
            print("Không tìm ra giá trị tối ưu thỏa mãn")
            exit()
        z_opt = z_max
    else:
        if z_min == float('-inf'):
            print("Không tìm ra giá trị tối ưu thỏa mãn")
            exit()
        z_opt = z_min
    return z_opt, matrices

def find_bound(matrix, known_indices, known_values, target_idx):
    new_ineqs = []

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
            
    upper = [ineq[3] for ineq in new_ineqs if ineq[target_idx] > 0]
    lower = [ineq[3] for ineq in new_ineqs if ineq[target_idx] < 0]

    var_max = min(upper) if upper else float('inf')
    var_min = max(lower) if lower else float('-inf')

    print_matrix(new_ineqs)
    print(f"Tổng hợp các bất phương trình lại, tìm ra khoảng giá trị của biến {['x','y','z'][target_idx]} cho giá trị tối ưu là: {var_min:.4f} <= {['x','y','z'][target_idx]} <= {var_max:.4f}")
    return var_min, var_max

if __name__ == '__main__':
    print("Nhập toàn bộ ma trận bất phương trình (mỗi dòng: a b c d, kết thúc bằng dòng rỗng).\nLưu ý: Ghi đúng format: ax + by + cz <= d")
    matrix = []
    for line in sys.stdin:
        if not line.strip():
            break
        parts = [float(x) for x in line.replace(',',' ').split()]
        matrix.append(tuple(parts))

    sense = input("Bạn muốn tìm giá trị lớn nhất (max) hay nhỏ nhất (min) của z? (max/min): ").strip().lower()

    print("Bất phương trình của bài toán đã cho:");
    print_matrix(matrix)

    z_optimal, matrices = fourier_motzkin_2var(matrix, sense)
    print(f"Giá trị cực trị z = {z_optimal:.4f}")

    print("Thay giá trị của z vào các bất phương trình có sau khi khử x ta được: ")
    y_min, y_max = find_bound(matrices[0], [2], [z_optimal], 1)
    if y_min > y_max:
        print("Bài toán vô nghiệm ở biến y!")
        exit()

    print("Thay giá trị của y, z vào các bất phương trình lúc đầu ta được: ")
    x_min, x_max = find_bound(matrix, [1,2], [y_max, z_optimal], 0)
    if x_min > x_max:
        print("Bài toán vô nghiệm ở biến x!")
        exit()

    print(f"Bài toán có nghiệm với bộ nghiệm tối ưu: x = {x_max:.4f}, y = {y_max:.4f}, z = {z_optimal:.4f}")


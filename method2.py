def print_matrix(ineqs, step):
    print(f"\nMa trận sau khi loại biến thứ {step}:")
    for ineq in ineqs:
        print("{:6.2f}x + {:6.2f}y + {:6.2f}z <= {:6.2f}".format(ineq[0], ineq[1], ineq[2], ineq[3]))

def normalize_z(ineqs, step):
    normalized = []
    for ineq in ineqs:
        a3 = ineq[2]
        if a3 > 0:
            normalized.append(tuple(x / a3 for x in ineq))
        else:
            normalized.append(ineq)
    print_matrix(normalized, step)
    return normalized

def dedupe(ineqs):
    seen = set()
    return [x for x in ineqs if not (x in seen or seen.add(x))]

def eliminate(var_idx, ineqs, step):
    P = [ineq for ineq in ineqs if ineq[var_idx] > 0]
    N = [ineq for ineq in ineqs if ineq[var_idx] < 0]
    Z = [ineq for ineq in ineqs if ineq[var_idx] == 0]
    result = Z + [tuple(-n[var_idx]*p[i] + p[var_idx]*n[i] for i in range(4)) for p in P for n in N]
    result = dedupe(result)
    print_matrix(result, step)
    return result

def fourier_motzkin_2var(constraints, sense):
    matrix1 = eliminate(0, constraints, 1)
    matrix2 = eliminate(1, matrix1, 2)
    matrix3 = normalize_z(matrix2, 3)  # Bước chuẩn hóa hệ số z
    bounds = [ineq[3] for ineq in matrix3 if ineq[2] > 0]
    if not bounds:
        raise ValueError('No bound for objective')
    # Có thể trả về các ma trận nếu muốn sử dụng tiếp
    return min(bounds) if sense == 'max' else max(bounds), matrix1, matrix2, matrix3

if __name__ == '__main__':
    matrix = [
        (2, 1, 0, 6), (1, 2, 0, 8),
        (1, -2, 0, 1), (1, 0, 0, 2),
        (-1, 0, 0, 0), (0, -1, 0, 0),
        (-2, -3, 1, 0)
    ]
    print_matrix(matrix, 0)
    result, matrix1, matrix2, matrix3 = fourier_motzkin_2var(matrix, 'max')
    print("Giá trị cực đại z =", result)
    # Nếu muốn in lại các ma trận:
    # print_matrix(matrix1, 1)
    # print_matrix(matrix2, 2)
    # print_matrix(matrix3, 3)

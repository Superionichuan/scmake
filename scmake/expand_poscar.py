import numpy as np
import time
import sys

def expand_poscar(exa, exb, exc, input_file='POSCAR'):
    # 记录开始时间
    start_time = time.time()
    with open(input_file, 'r') as infile,  open(f'POSCAR_{exa}x{exb}x{exc}', 'w') as outfile:
        filename = infile.readline()
        scale = float(infile.readline().strip())

        # 读取并处理晶胞参数
        a0 = [float(x) * scale for x in infile.readline().split()]
        b0 = [float(x) * scale for x in infile.readline().split()]
        c0 = [float(x) * scale for x in infile.readline().split()]

        # 扩展晶胞
        a = [x * exa for x in a0]
        b = [x * exb for x in b0]
        c = [x * exc for x in c0]

        vec_a0 = np.array(a0)
        vec_b0 = np.array(b0)
        vec_c0 = np.array(c0)

        length_vec_a0 = np.linalg.norm(vec_a0)
        length_vec_b0 = np.linalg.norm(vec_b0)
        length_vec_c0 = np.linalg.norm(vec_c0)

        # 读取原子类型和数量
        atom_types = infile.readline().split()
        num0 = [int(x) for x in infile.readline().split()]
        num = [x * exa * exb * exc for x in num0]
        coordnumb = sum(num0)

        # 写入新的POSCAR文件
        outfile.write(filename)  # 注释行
        outfile.write('1.0\n')  # scale 设置为1.0
        for vec in [a, b, c]:
            outfile.write('  '.join(f'{num:>24.16f}' for num in vec) + '\n')
        outfile.write('  '.join(atom_types) + '\n')
        outfile.write('  '.join(map(str, num)) + '\n')

        coord_type = infile.readline().strip()
        outfile.write(coord_type + '\n')
        type_direct = coord_type.lower().startswith('d')
        type_cartesian = coord_type.lower().startswith('c')

        if type_direct:
            for line in range(coordnumb):
                xi0, yi0, zi0 = [float(x) for x in infile.readline().split()]
                for i in range(exa):
                    for j in range(exb):
                        for k in range(exc):
                            xi = ((xi0 + i) / exa) % 1.0
                            yi = ((yi0 + j) / exb) % 1.0
                            zi = ((zi0 + k) / exc) % 1.0
                            outfile.write(f'{xi:>24.16f} {yi:>24.16f} {zi:>24.16f}\n')
        elif type_cartesian:
            for line in range(coordnumb):
                xi0, yi0, zi0 = [float(x) for x in infile.readline().split()]
                for i in range(exa):
                    xi = (xi0 + i * length_vec_a0)
                    for j in range(exb):
                        yi = (yi0 + j * length_vec_b0)
                        for k in range(exc):
                            zi = (zi0 + k * length_vec_c0)
                            outfile.write(f'{xi:>24.16f} {yi:>24.16f} {zi:>24.16f}\n')
        else:
            print("Fatal error, Cartesian or Direct type in POSCAR format is not specified, please check")
            sys.exit(1)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")


def main():
    if len(sys.argv) < 4:
        print("Usage: scmake <exa> <exb> <exc> [input_file]")
        sys.exit(1)

    exa = int(sys.argv[1])
    exb = int(sys.argv[2])
    exc = int(sys.argv[3])
    input_file = sys.argv[4] if len(sys.argv) > 4 else 'POSCAR'

    expand_poscar(exa, exb, exc, input_file)



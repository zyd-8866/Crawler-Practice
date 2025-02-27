import sys


def remove_duplicates(file_path, keep_one=False):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    line_count = {}
    for line in lines:
        stripped_line = line.strip()
        if stripped_line in line_count:
            line_count[stripped_line] += 1
        else:
            line_count[stripped_line] = 1

    unique_lines = []
    if keep_one:
        # 保留所有唯一的行
        for line in lines:
            stripped_line = line.strip()
            if line_count[stripped_line] == 1:
                unique_lines.append(line)
    else:
        # 保留每个重复行的一个实例
        seen = set()
        for line in lines:
            stripped_line = line.strip()
            if stripped_line not in seen:
                unique_lines.append(line)
                seen.add(stripped_line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python deduplicate.py <文件路径> [-del]")
        exit(1)

    file_path = sys.argv[1]
    keep_one = '-del' in sys.argv

    remove_duplicates(file_path, keep_one)
    print(f"处理完成: {file_path}")

import csv


def read_csv(file, parse_row, parse_header):
    with open(file, "r", encoding='utf-8') as f:
        parsed = []
        header = None
        reader = csv.reader(f, delimiter=',')
        for index, row in enumerate(reader):
            if index == 0:
                header = parse_header(row)
                continue
            parsed.append(parse_row(row))
        return header, parsed


def write_csv(file, rows):
    with open(file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(rows)


def write_rows(file, rows):
    with open(file, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(row+"\n")

import sys
from collections import defaultdict

def process_text(lines):
    output = []
    data = defaultdict(list)

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.endswith(':'):
            # Process previous section and start a new one
            if data:
                for (key, rest), values in data.items():
                    merged_values = ','.join(values)
                    merged_values = merge_zeroes(merged_values)
                    output.append('    ' + ' '.join(key) + ' ' + merged_values + ' ' + ' '.join(rest))
                data.clear()

            # Handle label lines
            output.append(stripped_line)
        else:
            fields = stripped_line.split()
            if len(fields) < 5:
                print(f"Warning: Misformatted line skipped - '{line.strip()}'", file=sys.stderr)
                continue

            key = tuple(fields[:3] + [fields[3].replace('0-0', '0')])
            value = fields[4]
            rest = fields[5:]

            data[(key, tuple(rest))].append(value)

    # Process the last section
    if data:
        for (key, rest), values in data.items():
            merged_values = ','.join(values)
            merged_values = merge_zeroes(merged_values)
            output.append('    ' + ' '.join(key) + ' ' + merged_values + ' ' + ' '.join(rest))

    return '\n'.join(output)


def merge_zeroes(value):
    value_parts = value.split(',')
    value_parts = [part.strip() for part in value_parts]
    if value_parts[0] == '0-0':
        value_parts[0] = '0'
    value_parts = list(filter(lambda part: part != '0-0', value_parts))
    return ','.join(value_parts)


if __name__ == "__main__":
    input_lines = [line for line in sys.stdin]
    print(process_text(input_lines))

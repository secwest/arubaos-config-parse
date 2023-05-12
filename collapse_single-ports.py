import sys
import re

def filter_numbers(input_string):
    # Replace "0-65535" with "all"
    input_string = input_string.replace("0-65535", "all")

    # Find repeated numbers separated by a dash and swap them
    output_parts = []
    lines = input_string.split('\n')
    for line in lines:
        if re.search(r"\b\d+-\d+\b", line):
            output_line = re.sub(r"\b(\d+)-\1\b", r"\1", line)
        else:
            output_line = line
        output_parts.append(output_line)

    output_string = '\n'.join(output_parts)
    return output_string


# Read input from stdin
input_string = sys.stdin.read().strip()

# Apply the filter and write output to stdout
output_string = filter_numbers(input_string)
sys.stdout.write(output_string)

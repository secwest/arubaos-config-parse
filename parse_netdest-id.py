import sys
import re

def parse_file1(file1):
    with open(file1, 'r') as f:
        lines = f.readlines()
    memory_table = {}
    for line in lines:
        line = line.strip()
        netdest_id, ip_address, netmask_or_name, comment_or_name = line.split(',')
        if netdest_id not in memory_table:
            memory_table[netdest_id] = []
        memory_table[netdest_id].append(f"{ip_address}/{netmask_or_name}({comment_or_name})")
    return memory_table

def parse_file2(file2, memory_table):
    with open(file2, 'r') as f:
        lines = f.readlines()
    output = []
    for line in lines:
        original_line = line
        line = line.strip()
        if original_line.lstrip() == original_line:  # if the line does not start with a whitespace
            output.append(original_line.rstrip())
            continue  # skip the remaining part of this loop iteration
        matches = re.findall(r'netdest-id: (\d+)', line)
        if matches:
            for match in matches:
                if match in memory_table:
                    for ip in memory_table[match]:
                        line = line.replace(f'netdest-id: {match}', ip, 1)
        
        # Remove the rule number (until the first colon) and replace it with whitespace
        line = re.sub(r'^[^:]*:', ' ', line)

        # Remove the 'f<number>:' field before 'permit' or 'deny'
        line = re.sub(r'f\d+:', '', line)

        # Remove the spaces after 'userrole:' 
        line = re.sub(r'(userrole:)\s+', r'\1', line)

        # Split the line into fields
        fields = line.split()

        # Check if field three exists before modifying the line
        if len(fields) > 2:
            # Translate protocol number to text if it exists in the mapping
            if fields[2].isdigit():
                protocol_number = int(fields[2])
                if protocol_number in protocol_mapping:
                    protocol_name = protocol_mapping[protocol_number]
                    fields[2] = protocol_name

        modified_line = ' '.join(fields)
        if original_line.rstrip() != modified_line:
            output.append("    " + modified_line)
        else:
            output.append(original_line.rstrip())
    
    return output


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py file1 file2")
        sys.exit(1)
    file1, file2 = sys.argv[1], sys.argv[2]
    memory_table = parse_file1(file1)
    output = parse_file2(file2, memory_table)
    for line in output:
        print(line)


if __name__ == "__main__":
    # Mapping of protocol numbers to names
    protocol_mapping = {
        0: "Zero",
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        58: "ICMPv6",
        47: "GRE",
        50: "ESP",
        51: "AH",
        89: "OSPF",
        132: "SCTP",
        255: "ANY",
        # Add more protocol mappings as needed
    }

    main()

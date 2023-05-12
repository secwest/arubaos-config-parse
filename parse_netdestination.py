import re
import sys

# check if an input file name was provided as a command line argument
if len(sys.argv) < 2:
    print('Usage: python parse_arubaos_config.py <input_file>')
    sys.exit()

input_file = sys.argv[1]

# define the regular expression patterns to match each section of the configuration information
name_pattern = re.compile(r'^Name:\s+(.*)$')
id_pattern = re.compile(r'^Destination ID:\s+(\d+)$')
entry_pattern = re.compile(r'^\s*(\d+)\s+(\S+)\s+([\d\.]+|\S+)\s+([\d\.]+|\d+)\s*$')

# initialize variables to store the current section's information
current_name = None
current_id = None
current_entries = []

# function to output an entry
def output_entry(id, ip_address, mask_len_range, dns_name):
    print(f"{id},{ip_address},{mask_len_range},{dns_name}")

# iterate over each line in the input file
with open(input_file, 'r') as infile:
    for line in infile:
        # check if the line matches the "Name:" pattern
        match = name_pattern.match(line)
        if match:
            # output the previous section's entries, including empty ones
            if current_id is not None:
                for entry in current_entries:
                    output_entry(current_id, entry[2], entry[3], current_name)
                if not current_entries:
                    output_entry(current_id, 'Empty', '*', current_name)
            current_entries = []

            # reset the current section's information
            current_name = match.group(1)
            current_id = None

        # check if the line matches the "Destination ID:" pattern
        match = id_pattern.match(line)
        if match:
            # output the previous section's entries, including empty ones
            if current_id is not None:
                for entry in current_entries:
                    output_entry(current_id, entry[2], entry[3], current_name)
                if not current_entries:
                    output_entry(current_id, 'Empty', '*', current_name)
            current_entries = []

            # update the current section's destination ID
            current_id = match.group(1)

        # check if the line matches the entry pattern
        match = entry_pattern.match(line)
        if match:
            # append the current entry's information to the list of entries for the current section
            current_entries.append(match.groups())

    # output the last section's entries, including empty ones
    if current_id is not None:
        for entry in current_entries:
            output_entry(current_id, entry[2], entry[3], current_name)
        if not current_entries:
            output_entry(current_id, 'Empty', '*', current_name)

# check if there are any IDs without an entry and write "Empty" as the entry
with open(input_file, 'r') as infile:
    all_ids = set(entry[0] for entry in entry_pattern.findall(infile.read()))
    all_ids.update(id_pattern.findall(infile.read()))
    for id in all_ids:
        if id != current_id:
            output_entry(id, 'Empty', '*', '')

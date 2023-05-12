mport sys
import re

def parse_ace_list(file_path):
    ace_list = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_ace = None
        for line in lines:
            if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                current_ace = line.strip()
                ace_list[current_ace] = []
            elif current_ace is not None:
                ace_list[current_ace].append(line.strip())
    return ace_list

def parse_user_roles(file_path):
    user_roles = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_role = None
        for line in lines:
            if line.strip() and line.startswith("user-role"):
                parts = line.strip().split(" ")
                if len(parts) > 1:
                    current_role = parts[1]
                    user_roles[current_role] = [line.strip()]  # Store the header
                else:
                    current_role = None
            elif current_role is not None and line.startswith("access-list"):
                user_roles[current_role].append(line.strip().split(" ")[2])
    return user_roles

def main(ace_list_path, user_roles_path):
    acl_dict = parse_ace_list(ace_list_path)
    user_roles = parse_user_roles(user_roles_path)

    substituted_user_roles = {}
    for role, acl_names in user_roles.items():
        substituted_user_roles[role] = []
        substituted_user_roles[role].append(acl_names[0])  # Add the header
        for acl_name in acl_names[1:]:
            if acl_name in acl_dict:
                for rule in acl_dict[acl_name]:
                    substituted_user_roles[role].append(rule + " (ACL: " + acl_name + ")")

    print("Parsed User Roles:")
    for role, rules in substituted_user_roles.items():
        print("\n".join(rules))  # Print the role's lines with line breaks
        print()  # Add an empty line after each section

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <path_to_ace_list_file> <path_to_user_roles_file>")
        sys.exit(1)
    ace_list_path = sys.argv[1]
    user_roles_path = sys.argv[2]
    main(ace_list_path, user_roles_path)

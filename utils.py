# utils.py

def list_option(actions):
    options = ""
    for idx, action in enumerate(actions, 1):
        options += f"[{idx}] {action.get_name()}\n"
    return options

def get_selection(conn, actions):
    try:
        selection = conn.recv(1024).decode('utf-8').strip()
        if not selection.isdigit():
            conn.send("Invalid selection. Please enter a number corresponding to the options.\n".encode('utf-8'))
            return get_selection(conn, actions)
        selection = int(selection)
        if not 1 <= selection <= len(actions):
            conn.send("Selection out of range. Please try again.\n".encode('utf-8'))
            return get_selection(conn, actions)
        return actions[selection - 1]
    except Exception as e:
        print(f"Get selection error: {e}")
        return None

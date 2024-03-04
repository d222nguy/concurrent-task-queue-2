# ANSI escape sequences for some colors
class Colors:
    RED = "\033[31m"  # Red text
    GREEN = "\033[32m"  # Green text
    YELLOW = "\033[33m"  # Yellow text
    BLUE = "\033[34m"  # Blue text
    MAGENTA = "\033[35m"  # Magenta text
    CYAN = "\033[36m"  # Cyan text
    RESET = "\033[0m"  # Reset to default color


def print_color(color, text):
    print(f"{color}{text}\n{Colors.RESET}")


# Example usage
# print(f"{Colors.RED}This text will be red!{Colors.RESET}")
# print(f"{Colors.GREEN}This text will be green!{Colors.RESET}")
# print(f"{Colors.YELLOW}This text will be yellow!{Colors.RESET}")
# print(f"{Colors.BLUE}This text will be blue!{Colors.RESET}")
# print(f"{Colors.MAGENTA}This text will be magenta!{Colors.RESET}")
# print(f"{Colors.CYAN}This text will be cyan!{Colors.RESET}")

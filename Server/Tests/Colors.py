class Colors:
    """ANSI color codes for terminal text coloring"""
    RESET: str = "\033[0m"
    WHITE: str = "\033[38;5;255m"
    RED: str = "\033[38;5;001m"
    GREEN: str = "\033[38;5;002m"
    YELLOW: str = "\033[38;5;226m"
    BLUE: str = "\033[38;5;004m"
    MAGENTA: str = "\033[38;5;005m"
    ORANGE: str = "\033[38;5;214m"
    PURPLE: str = "\033[38;5;129m"
    LIGHT_GRAY: str = "\033[38;5;250m"
    DARK_GRAY: str = "\033[38;5;240m"

    colors: list[str] = ["WHITE", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "ORANGE", "PURPLE", "LIGHT_GRAY", "DARK_GRAY"]

    @staticmethod
    def get_colors() -> None:
        """Display all available colors with their names"""
        for color_name in Colors.colors:
            color_code = getattr(Colors, color_name)
            print(f"{color_code}{color_name}{Colors.RESET}")

    @staticmethod
    def printcol(color: str, msg: str) -> None:
        """Print colored message to terminal"""
        if not hasattr(Colors, color) and not color.startswith('\033'):
            raise ValueError(f"Invalid color: {color}. Use Colors constants or ANSI codes")
        print(f"{color}{msg}{Colors.RESET}")

if __name__ == "__main__":
    Colors.get_colors()

import os

if os.name == 'nt':
    import msvcrt
else:
    import termios, atexit, select.select as select

class lxTERM:
    """Provides cross-platform non-blocking keyboard input functionality."""
    _auto_cleanup_ = False

    def getch(self) -> str:
        """Returns a single keyboard character without waiting for Enter.
        Use kb_hit() to check if a key has been pressed before calling this."""
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            try:
                if self._auto_cleanup_:
                    self._setup_posix_term()
                return sys.stdin.read(1)
            finally:
                if self._auto_cleanup_:
                    self._reset_posix_term()

    def kb_hit(self) -> bool:
        """Checks if a key has been pressed without pausing the program."""
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            # Lists file descriptors, [readable, writable, errors]
            try:
                if self._auto_cleanup_:
                    self._setup_posix_term()
                dr, _, _ = select([sys.stdin], [], [], 0)
                return dr != [] # True if input is available
            finally:
                if self._auto_cleanup_:
                    self._reset_posix_term()

    def _setup_posix_term(self) -> None:
        """Sets up the terminal for unbuffered input."""
        if os.name != 'nt':
            self.fd = sys.stdin.fileno()
            self.posix_term = termios.tcgetattr(self.fd)
            self.default_term = termios.tcgetattr(self.fd)
            # Modify posix-terminal settings for unbuffered input:
            self.posix_term[3] &= ~(termios.ICANON | termios.ECHO) # BreakSupport: termios.IGNBRK | termios.BRKINT
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.posix_term)

            # Register the cleanup function to reset on exit.
            atexit.register(self._reset_posix_term)

    def _reset_posix_term(self) -> None:
        """Resets the terminal to its original settings."""
        if os.name != 'nt' and self.fd:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.default_term)

    def __enter__(self):
        self._auto_cleanup_ = True
        self._setup_posix_term()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb, /):
        self._reset_posix_term()
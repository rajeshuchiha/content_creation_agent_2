import logging
import sys

def setup_logger(name):
    """
    Creates a logger that writes to console.
    
    Why this function?
    - Centralizes logging configuration
    - Easy to import and use in any file
    - Consistent format across your application
    
    Args:
        name: Pass __name__ from your module
    
    Returns:
        Configured logger instance
    """
    
    # Create logger
    # Why? Each module gets its own logger to track where logs come from
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Minimum level to log
    
    # Prevent adding duplicate handlers if logger already exists
    # Why? Without this check, you get duplicate log messages
    if logger.handlers:
        return logger
    
    # Console handler - prints logs to terminal/docker logs
    # Why? In Docker, you want logs in stdout so 'docker logs' command works
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter - defines how log messages look
    # Why? Structured format helps you debug issues quickly
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Attach handler to logger
    logger.addHandler(console_handler)
    
    return logger
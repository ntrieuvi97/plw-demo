# LoggerController Documentation

## Overview

The `LoggerController` is a comprehensive logging solution for your test automation framework. It provides in-memory log storage, test step tracking, performance monitoring, and multiple output formats.

## Features

- ✅ **In-memory log storage** for test duration
- ✅ **Test step tracking** with automatic context management
- ✅ **Performance monitoring** with timing capabilities
- ✅ **Screenshot attachment** support
- ✅ **Multiple log levels** (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- ✅ **Export to multiple formats** (JSON, TXT, CSV)
- ✅ **Integration with pytest** and existing test controllers
- ✅ **Detailed test summaries** and reporting

## Basic Usage

### 1. Using with Fixtures (Recommended)

```python
def test_example(page, logger_controller, test_controller, assertions):
    """Test using the integrated logging fixtures."""
    
    # Set current step for context
    logger_controller.set_current_step("Setup")
    logger_controller.info("Starting test")
    
    try:
        # Log actions
        logger_controller.log_action("Navigate to page", {"url": "https://example.com"})
        page.goto("https://example.com")
        
        # Log assertions
        title = page.title()
        logger_controller.log_assertion("Page has title", bool(title), {"title": title})
        
        # Log performance
        import time
        start = time.time()
        page.wait_for_load_state("networkidle")
        duration = time.time() - start
        logger_controller.log_performance("Page load", duration)
        
        # Use enhanced assertions
        assertions.verify_that_all_posts_are_displayed(10)
        
        # Step completion
        logger_controller.step_passed("Setup", "All setup completed successfully")
        
    except Exception as e:
        logger_controller.step_failed("Setup", str(e))
        test_controller.capture_screenshot_with_log("Error screenshot")
        raise
    finally:
        logger_controller.clear_current_step()
```

### 2. Standalone Usage

```python
from src.core.logger_controller import LoggerController

# Context manager (recommended)
with LoggerController("my_test") as logger:
    logger.info("Test started")
    logger.log_action("Performing action")
    logger.step_passed("Action", "Completed successfully")
    
    # Export logs
    logger.export_logs_to_file("my_test_logs.json", "json")

# Manual usage
logger = LoggerController("my_test")
logger.info("Test started")
# ... test code ...
logger.export_logs_to_file("logs.txt", "txt")
```

## Available Methods

### Logging Methods

```python
# Basic logging
logger.debug("Debug message")
logger.info("Info message") 
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Step tracking
logger.step_passed("Step name", "Optional message")
logger.step_failed("Step name", "Error message")
logger.step_skipped("Step name", "Skip reason")

# Action logging
logger.log_action("Click button", {"button_id": "submit"})

# Assertion logging
logger.log_assertion("Button is visible", True, {"selector": "#submit"})

# Performance logging
logger.log_performance("Database query", 0.150, {"query": "SELECT * FROM users"})

# Screenshot logging
logger.log_screenshot("/path/to/screenshot.png", "Error occurred")
```

### Step Management

```python
# Set current step for context
logger.set_current_step("Login Process")

# All subsequent logs will include this step context
logger.info("Entering credentials")  # Will show: [Login Process] Entering credentials

# Clear step context
logger.clear_current_step()
```

### Data Retrieval

```python
# Get logs by level
error_logs = logger.get_logs_by_level(LogLevel.ERROR)
warning_logs = logger.get_logs_by_level(LogLevel.WARNING)

# Get logs by step
setup_logs = logger.get_logs_by_step("Setup")

# Get error logs only
errors = logger.get_error_logs()

# Get test summary
summary = logger.get_test_summary()
print(f"Test duration: {summary['duration_seconds']:.2f}s")
print(f"Error count: {summary['error_count']}")
```

### Export Options

```python
# Export to JSON (includes full metadata)
logger.export_logs_to_file("test_logs.json", "json")

# Export to readable text
logger.export_logs_to_file("test_logs.txt", "txt")

# Export to CSV for analysis
logger.export_logs_to_file("test_logs.csv", "csv")
```

## Integration with Existing Framework

### TestController Integration

The `TestController` is automatically enhanced with logging:

```python
def test_with_integrated_logging(test_controller):
    # TestController now has enhanced logging
    test_controller.add_steps_results("passed", "Step completed")
    # This automatically logs to both TestRail and LoggerController
    
    # Capture screenshot with logging
    test_controller.capture_screenshot_with_log("Success screenshot")
```

### Assertions Integration

The `HomePageAssertions` class now includes logging:

```python
def test_with_assertion_logging(assertions):
    # Assertions now automatically log results
    assertions.verify_that_all_posts_are_displayed(10)
    # This logs the assertion details, results, and timing
```

## Configuration

### Fixture Configuration (in conftest.py)

```python
@pytest.fixture
def logger_controller(request):
    """Enhanced logger fixture with auto-export."""
    test_name = request.node.name
    
    with LoggerController(test_name=test_name) as logger:
        yield logger
        
        # Auto-export logs after test
        logger.export_logs_to_file(f"logs/{test_name}.json", "json")
```

### Custom Logger Setup

```python
# Custom logger with specific settings
logger = LoggerController(
    test_name="custom_test",
    enable_console=True  # Enable/disable console output
)

# Setup file logging
import logging
file_handler = logging.FileHandler("test.log")
logger.logger.addHandler(file_handler)
```

## Log Entry Structure

Each log entry contains:

```python
{
    "timestamp": "2025-08-06T10:30:45.123456",
    "level": "INFO",
    "message": "Test message",
    "test_name": "test_example",
    "step_name": "Setup",  # Optional
    "extra_data": {        # Optional
        "url": "https://example.com",
        "duration": 0.150
    }
}
```

## Best Practices

1. **Use Context Management**: Always use `with` statement or properly clear steps
2. **Structure Your Tests**: Use clear step names for better organization
3. **Log Actions**: Log significant actions for better traceability
4. **Performance Tracking**: Log timing for critical operations
5. **Error Handling**: Always log errors with context data
6. **Export Logs**: Set up automatic log export for analysis

## Example Test Report Structure

After test completion, you'll get detailed reports:

```json
{
  "test_summary": {
    "test_name": "test_verify_posts",
    "duration_seconds": 5.67,
    "total_log_entries": 15,
    "error_count": 0,
    "success_rate": 100
  },
  "log_entries": [
    {
      "timestamp": "2025-08-06T10:30:45.123456",
      "level": "INFO",
      "message": "Starting test",
      "test_name": "test_verify_posts",
      "step_name": "Setup"
    }
  ]
}
```

This comprehensive logging solution will help you track test execution, debug issues, and generate detailed reports for your test automation framework.

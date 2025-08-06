import logging
import datetime
import inspect
import os
import json
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict


class LogLevel(Enum):
    """Enumeration for log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """Data class representing a single log entry."""

    timestamp: str
    level: str
    message: str
    test_name: str
    caller_info: str  # New field for file:line info
    step_name: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert log entry to dictionary."""
        return asdict(self)


class LoggerController:
    """
    Logger controller for test automation framework.

    Features:
    - In-memory log storage for test duration
    - Integration with test steps
    - Multiple output formats (console, file, memory)
    - Test-specific log contexts
    - Performance tracking
    - Screenshot attachment support
    """

    def __init__(self, test_name: str = "", enable_console: bool = True):
        """Initialize the logger controller."""
        self.test_name = test_name
        self.log_entries: List[LogEntry] = []
        self.current_step: Optional[str] = None
        self.test_start_time = datetime.datetime.now()

        # Setup Python logger
        self.logger = logging.getLogger(f"TestLogger.{test_name}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        if enable_console:
            self._setup_console_handler()

    def _get_caller_info(self, skip_frames: int = 2) -> str:
        """
        Get caller file and line number information.

        Args:
            skip_frames: Number of frames to skip (default 2 to skip this method and the calling log method)

        Returns:
            String in format "filename.py:line_number"
        """
        try:
            # Get the current stack
            stack = inspect.stack()

            # Skip internal frames to find the actual caller
            if len(stack) > skip_frames:
                frame = stack[skip_frames]
                filename = os.path.basename(frame.filename)
                line_number = frame.lineno
                return f"{filename}:{line_number}"
        except Exception:
            pass

        return "unknown:0"

    def _setup_console_handler(self) -> None:
        """Setup console logging handler with custom formatter."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Custom formatter that includes caller info
        class CallerFormatter(logging.Formatter):
            def format(self, record):
                # Add caller info to the record if available
                if hasattr(record, "caller_info"):
                    record.name_with_caller = f"{record.name}:{record.caller_info}"
                else:
                    record.name_with_caller = record.name
                return super().format(record)

        formatter = CallerFormatter(
            "%(asctime)s - %(name_with_caller)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _log(
        self,
        level: LogLevel,
        message: str,
        extra_data: Optional[Dict[str, Any]] = None,
        skip_frames: int = 3,  # Skip _log, calling method, and get to actual caller
    ) -> LogEntry:
        """
        Internal logging method with caller tracking.

        Args:
            level: Log level
            message: Log message
            extra_data: Optional extra data
            skip_frames: Number of stack frames to skip to find actual caller
        """
        timestamp = datetime.datetime.now().isoformat()
        caller_info = self._get_caller_info(skip_frames)

        log_entry = LogEntry(
            timestamp=timestamp,
            level=level.value,
            message=message,
            test_name=self.test_name,
            caller_info=caller_info,
            step_name=self.current_step,
            extra_data=extra_data or {},
        )

        self.log_entries.append(log_entry)

        # Log to Python logger with caller info
        log_record = self.logger.makeRecord(
            name=self.logger.name,
            level=getattr(logging, level.value),
            fn="",
            lno=0,
            msg=message,
            args=(),
            exc_info=None,
        )
        log_record.caller_info = caller_info
        self.logger.handle(log_record)

        return log_entry

    def set_current_step(self, step_name: str) -> None:
        """Set the current test step for context."""
        self.current_step = step_name
        self._log(LogLevel.INFO, f"=== Starting Step: {step_name} ===", skip_frames=3)

    def clear_current_step(self) -> None:
        """Clear the current test step."""
        if self.current_step:
            self._log(
                LogLevel.INFO,
                f"=== Completed Step: {self.current_step} ===",
                skip_frames=3,
            )
        self.current_step = None

    def info(
        self, message: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> LogEntry:
        """Log info message."""
        return self._log(LogLevel.INFO, message, extra_data, skip_frames=3)

    def debug(
        self, message: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> LogEntry:
        """Log debug message."""
        return self._log(LogLevel.DEBUG, message, extra_data, skip_frames=3)

    def warning(
        self, message: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> LogEntry:
        """Log warning message."""
        return self._log(LogLevel.WARNING, message, extra_data, skip_frames=3)

    def error(
        self, message: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> LogEntry:
        """Log error message."""
        return self._log(LogLevel.ERROR, message, extra_data, skip_frames=3)

    def critical(
        self, message: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> LogEntry:
        """Log critical message."""
        return self._log(LogLevel.CRITICAL, message, extra_data, skip_frames=3)

    def log_assertion(
        self, message: str, passed: bool, extra_data: Optional[Dict[str, Any]] = None
    ) -> LogEntry:
        """
        Log assertion result with caller information.

        Args:
            message: Assertion description
            passed: Whether assertion passed
            extra_data: Optional additional data
        """
        status = "✅ PASSED" if passed else "❌ FAILED"
        full_message = f"{status} ASSERTION: {message}"

        level = LogLevel.INFO if passed else LogLevel.ERROR
        return self._log(level, full_message, extra_data, skip_frames=3)

    def log_action(
        self, action: str, extra_data: Optional[Dict[str, Any]] = None
    ) -> LogEntry:
        """Log test action with caller info."""
        return self._log(
            LogLevel.INFO, f"🔄 ACTION: {action}", extra_data, skip_frames=3
        )

    def log_screenshot(self, screenshot_path: str, description: str = "") -> LogEntry:
        """Log screenshot capture with caller info."""
        message = f"📸 SCREENSHOT: {description} - {screenshot_path}"
        return self._log(
            LogLevel.INFO, message, {"screenshot_path": screenshot_path}, skip_frames=3
        )

    def log_performance(
        self,
        action: str,
        duration_seconds: float,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> LogEntry:
        """Log performance metrics with caller info."""
        message = f"⏱️ PERFORMANCE: {action} took {duration_seconds:.2f}s"
        perf_data = {"duration_seconds": duration_seconds, "action": action}
        if extra_data:
            perf_data.update(extra_data)
        return self._log(LogLevel.INFO, message, perf_data, skip_frames=3)

    def step_passed(self, step_name: str, message: str) -> LogEntry:
        """Log passed step with caller info."""
        return self._log(
            LogLevel.INFO, f"✅ STEP PASSED: {step_name} - {message}", skip_frames=3
        )

    def step_failed(self, step_name: str, message: str) -> LogEntry:
        """Log failed step with caller info."""
        return self._log(
            LogLevel.ERROR, f"❌ STEP FAILED: {step_name} - {message}", skip_frames=3
        )

    def step_skipped(self, step_name: str, message: str) -> LogEntry:
        """Log skipped step with caller info."""
        return self._log(
            LogLevel.WARNING, f"⏭️ STEP SKIPPED: {step_name} - {message}", skip_frames=3
        )

    def get_logs_by_level(self, level: LogLevel) -> List[LogEntry]:
        """Get all log entries of a specific level."""
        return [entry for entry in self.log_entries if entry.level == level.value]

    def get_logs_by_step(self, step_name: str) -> List[LogEntry]:
        """Get all log entries for a specific step."""
        return [entry for entry in self.log_entries if entry.step_name == step_name]

    def get_error_logs(self) -> List[LogEntry]:
        """Get all error and critical log entries."""
        return [
            entry
            for entry in self.log_entries
            if entry.level in [LogLevel.ERROR.value, LogLevel.CRITICAL.value]
        ]

    def get_test_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the test execution.

        Returns:
            Dictionary containing test summary information
        """
        total_logs = len(self.log_entries)
        logs_by_level = {}

        for level in LogLevel:
            logs_by_level[level.value.lower()] = len(self.get_logs_by_level(level))

        error_count = logs_by_level.get("error", 0) + logs_by_level.get("critical", 0)

        test_duration = (datetime.datetime.now() - self.test_start_time).total_seconds()

        return {
            "test_name": self.test_name,
            "start_time": self.test_start_time.isoformat(),
            "duration_seconds": test_duration,
            "total_log_entries": total_logs,
            "logs_by_level": logs_by_level,
            "has_errors": error_count > 0,
            "error_count": error_count,
            "current_step": self.current_step,
        }

    def export_logs_to_file(self, file_path: str, format_type: str = "json") -> str:
        """
        Export logs to a file.

        Args:
            file_path: Path to export the logs
            format_type: Format type ('json', 'txt', 'csv')

        Returns:
            Path to the exported file
        """
        import os
        import csv

        # Ensure directory exists
        if os.path.dirname(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if format_type.lower() == "json":
            export_data = {
                "test_summary": self.get_test_summary(),
                "log_entries": [entry.to_dict() for entry in self.log_entries],
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

        elif format_type.lower() == "txt":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Test Log Report: {self.test_name}\n")
                f.write("=" * 50 + "\n\n")

                for entry in self.log_entries:
                    step_info = f"[{entry.step_name}] " if entry.step_name else ""
                    caller_info = (
                        f" ({entry.caller_info})"
                        if hasattr(entry, "caller_info") and entry.caller_info
                        else ""
                    )
                    f.write(
                        f"{entry.timestamp} - {entry.level}{caller_info} - {step_info}{entry.message}\n"
                    )

                    if entry.extra_data:
                        f.write(f"    Extra Data: {entry.extra_data}\n")
                    f.write("\n")

        elif format_type.lower() == "csv":
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "Timestamp",
                        "Level",
                        "Test Name",
                        "Caller Info",
                        "Step Name",
                        "Message",
                        "Extra Data",
                    ]
                )

                for entry in self.log_entries:
                    writer.writerow(
                        [
                            entry.timestamp,
                            entry.level,
                            entry.test_name,
                            getattr(entry, "caller_info", ""),
                            entry.step_name or "",
                            entry.message,
                            json.dumps(entry.extra_data) if entry.extra_data else "",
                        ]
                    )

        return file_path

    def clear_logs(self) -> None:
        """Clear all stored log entries."""
        self.log_entries.clear()
        self.current_step = None
        self.test_start_time = datetime.datetime.now()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - log any exceptions."""
        if exc_type:
            self.critical(f"Test failed with exception: {exc_type.__name__}: {exc_val}")

        # Log test completion
        summary = self.get_test_summary()
        self.info(
            f"Test completed. Duration: {summary['duration_seconds']:.2f}s, "
            f"Total logs: {summary['total_log_entries']}, "
            f"Errors: {summary['error_count']}"
        )

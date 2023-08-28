import os
import time
import logging
import argparse
import platform
import subprocess
import shutil
from pathlib import Path
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)
# stream handler for console output
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, binary_path: str) -> None:
        super().__init__()
        self.binary_path: str = os.path.normpath(binary_path)
        self.process: Optional[subprocess.Popen] = None

    def on_created(self, event) -> None:
        if event.is_directory:
            return
        # Extract base filename without extension
        src_path = os.path.splitext(os.path.basename(event.src_path))[0].split(" ")[0]
        bin_path = os.path.splitext(os.path.basename(self.binary_path))[0].split(" ")[0]
        if src_path == bin_path:
            logger.info("Replacement file created. Relaunching...")
            if self.process:
                try:
                    self._terminate_process(self.process)
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning("Old process did not terminate. Forcing termination...")
                    self.process.kill()
            # Launch new process with the updated binary or script file
            self.process = self._create_subprocess(self.binary_path)

    def on_deleted(self, event) -> None:
        """ Handle file deletion event """
        if event.src_path.endswith(os.path.basename(self.binary_path)):
            logger.info("File deleted. Exiting...")
            if self.process:
                try:
                    self._terminate_process(self.process)
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning("Old process did not terminate. Forcing termination...")
                    self.process.kill()
            os._exit(0)

    def on_modified(self, event) -> None:
        """ Handle file modification event """
        if event.is_directory:
            return
        if event.src_path == self.binary_path:
            logger.info("File modified. Relaunching...")
            if self.process:
                try:
                    self._terminate_process(self.process)
                except subprocess.TimeoutExpired:
                    logger.warning("Old process did not terminate. Forcing termination...")
                    self.process.kill()
            self.process = self._create_subprocess(self.binary_path)


    @staticmethod
    def _terminate_process(process: subprocess.Popen) -> None:
        if platform.system() == "Windows":
            try:
                process.terminate()
            except subprocess.TimeoutExpired:
                try:
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)])
                except Exception as e:
                    logger.error(f"Error while terminating process: {e}")
            except Exception as e:
                logger.error(f"Error while terminating process: {e}")
        else:
            try:
                process.terminate()
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                logger.error(f"Error while terminating process: {e}")


    @staticmethod
    def _create_subprocess(binary_path: str) -> subprocess.Popen:
        interpreter = _get_script_interpreter(binary_path)
        # print("script_extension", interpreter)
        if platform.system() == "Windows":
            if interpreter:
                return subprocess.Popen([interpreter, binary_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            elif os.path.isfile(binary_path) and binary_path.lower().endswith(".exe"):
                return subprocess.Popen([binary_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                logger.error(f"Unsupported file type for Windows: {binary_path}")
        else:
            if interpreter:
                return subprocess.Popen([interpreter, binary_path])
            elif os.path.isfile(binary_path) and binary_path.lower().endswith(".exe"):
                return subprocess.Popen([binary_path])
            else:
                logger.error(f"Unsupported file type: {binary_path}")


def count_dir_files(directory: Path) -> int:
    return sum(1 for _ in directory.iterdir() if _.is_file())


def _get_script_interpreter(script_path: str) -> str:
    # script files: map corresponding interpreter based on file extension
    interpreter_mapping = {
        "py": "python",
        "js": "node",
        "rb": "ruby",
        "php": "php",
        "sh": "bash",
        "pl": "perl",
    }
    script_extension = script_path.lower().split(".")[-1]
    if script_extension == "py":
        if shutil.which("python3"):
            return "python3"
        else:
            return "python"
    return interpreter_mapping.get(script_extension, "")


def init_file_monitoring(binary_path: str, monitored_directory: str) -> None:
    """
    Monitor directory for changes and automatically relaunch executable (.exe) or script files.

    Args:
        binary_path (str): Executable or Script file.
        monitored_directory (str): Directory to be monitored.

    Example:
        init_file_monitoring("binary_or_script_file ex: test.exe test.py", "/path/to/directory")
    """
    event_handler = FileChangeHandler(binary_path)
    observer = Observer()

    try:
        observer.schedule(event_handler, str(monitored_directory), recursive=False)
        observer.start()

        file = os.path.basename(binary_path)
        file_count = count_dir_files(monitored_directory)
        logger.info(f"Number of files in the directory: {file_count}")
        logger.info(f"Monitoring directory: {monitored_directory}")
        logger.info(f"File: {file}")
        logger.info("Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file monitoring...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        observer.stop()
        observer.join()


def print_package_version():
    package_version = "0.3.1"
    print(f"binswap {package_version}")


def main():
    parser = argparse.ArgumentParser(description="Monitor directory and automatically relaunch binary or script file.")
    parser.add_argument("--bin", type=Path, required=False, help="Binary or Script file Ex. test.py, test.exe.")
    parser.add_argument(
        "--dir",
        type=Path,
        required=False,
        default=Path.cwd(),
        help="Path to the Directory to be monitored. Defaults to the current working directory.",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Package version.")
    args = parser.parse_args()
    # print(args)
    if args.version:
        print_package_version()
        return
    
    if not args.bin:
        logger.error("File path is required.")
        return
    
    bin_path = args.dir / args.bin  
    if not bin_path.exists():
        logger.error("Binary file does not exist. Please provide a valid path.")
        return

    init_file_monitoring(bin_path, args.dir)

if __name__ == "__main__":
    main()
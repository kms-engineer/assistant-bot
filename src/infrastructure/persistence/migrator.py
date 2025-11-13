import os
import shutil

from ..logging.logger import setup_logger

log = setup_logger()


def migrate_files(src_dir: str, dest_dir: str):
    try:

        if not os.path.isdir(src_dir):
            log.error(f"Source directory '{src_dir}' does not exist.")
            return

        os.makedirs(dest_dir, exist_ok=True)

        count = 0
        src_dir = os.path.abspath(src_dir)
        for filename in os.listdir(src_dir):
            if filename.startswith("."):
                continue

            source_file_path = os.path.join(src_dir, filename)
            if os.path.isfile(source_file_path):
                count += 1
                destination_file_path = os.path.join(dest_dir, filename)
                shutil.move(source_file_path, destination_file_path)

        if count > 0:
            log.info(f"Find {count} files in '{src_dir}'")
            log.info("Migration completed successfully.")

    except Exception as e:
        log.error("Migration failed: %s", e)

from logging import Logger, getLogger


def get_file_path_logger(module: str) -> Logger:
    return getLogger(module.replace(".", "/"))

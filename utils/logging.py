import logging

log_format = '%(asctime)s - %(levelname)s - %(message)s'

# capture info and above
logging.basicConfig(level=logging.INFO, format=log_format, handlers=[logging.StreamHandler()])

# write to files
file_handler = logging.FileHandler('job_errors.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)
logger = logging.getLogger(__name__)
"""Entry point for the project."""


from src.jsonmodipy.arg_parser.parse_args import parse_api_args
from src.jsonmodipy.arg_parser.process_args_apply import process_api_args_gen
from src.jsonmodipy.arg_parser.process_args_checks import (
    process_api_args_check,
)
from src.jsonmodipy.arg_parser.process_args_get import process_api_args_get
from src.jsonmodipy.arg_parser.process_args_store import process_api_args_store
from src.jsonmodipy.file_parsing import split_file_path

api_args = parse_api_args()
process_api_args_check(args=api_args)
# Get filepath and file name.
file_dir: str
filename: str
extension: str
file_dir, filename, extension = split_file_path(file_path=api_args.filepath)
process_api_args_get(
    args=api_args, extension=extension, file_dir=file_dir, filename=filename
)
process_api_args_gen(
    args=api_args, extension=extension, file_dir=file_dir, filename=filename
)
process_api_args_store(
    args=api_args, extension=extension, file_dir=file_dir, filename=filename
)

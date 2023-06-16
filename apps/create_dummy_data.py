'''Simple test'''
import argparse
import logging
from pathlib import Path

def setup_logger():
    '''Setup logger for app'''
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
        format='[%(asctime)s] %(levelname)-9s %(message)s'
    )

def parse_arguments():
    '''Parse input arguments to app'''
    parser = argparse.ArgumentParser(
        prog='Plot Many FRFs',
        description='App to create an overlay plot of all selected FRF signals'
    )
    parser.add_argument('-i', '--input',
                        dest='input',
                        type=Path,
                        required=False,
                        help='Path to folder to create plots from')
    parser.add_argument('-r', '--results_folder_regex',
                        dest='results_folder_regex',
                        type=str,
                        default='ProcDatRev2',
                        help='Regular expression to include in results folder')

    return parser.parse_args()

def evaluate_args():
    '''Evaluate input arguments'''
    args = parse_arguments()

    # Verify that input path is a directory
    if not args.input.is_dir():
        raise ValueError(
            f'Input path {args.input.as_posix()} is not a folder.'
        )

    # Verify that input paths exist
    if not args.input.exists():
        raise ValueError(
            f'Input folder path {args.input.as_posix()} was not found.'
        )

    return args.input, args.results_folder_regex

def main(input: Path, results_folder_regex: str):
    pass

if __name__ == '__main__':
    setup_logger()
    main(*evaluate_args())

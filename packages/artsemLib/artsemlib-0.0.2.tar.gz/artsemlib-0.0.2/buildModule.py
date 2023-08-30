import logging
import os
import sys

__interpreter__ = 'python3' if sys.platform.find('linux') != -1 else 'python.exe'
__build_tools__ = ['twine', 'build']


def parse_args(cmd=None):
    import argparse
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Builds and publish artsemLib package")
    parser.add_argument(
        "-v",
        action="count",
        default=0,
        help="increase logging verbosity [-v, -vv]")
    parser.add_argument(
        "-p", "--publish",
        action="store_true",
        default=False,
        help="If build success, publish the new version of the package to the repository"
    )
    _a = parser.parse_args(cmd)
    if _a.v == 0:
        logging.basicConfig(level='WARN')
    elif _a.v == 1:
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level='DEBUG')
    logging.debug(f"CLI arguments: {_a}")
    return _a


if __name__ == '__main__':
    _args = parse_args()

    # TODO: continue with the build process only if the previous command executed successfully
    logging.info(f"Updating build tools {__build_tools__}...")
    os.system(f'{__interpreter__} -m pip install --upgrade {" ".join(__build_tools__)}')
    os.chdir(os.path.dirname(__file__))
    logging.info(f"Building module...")
    os.system(f'{__interpreter__} -m build')
    logging.info(f"Build completed successfully")
    if _args.publish:
        logging.info(f"Publishing package...")
        os.system(f"{__interpreter__} -m hatch publish")
        logging.info(f"Package published successfully")
    logging.info("Execution completed. Exiting...")

from pathlib import Path
import yaml


def read_yaml(file_yaml):
    BASE_DIR = Path(__file__).parent
    file = BASE_DIR.joinpath(file_yaml)
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data
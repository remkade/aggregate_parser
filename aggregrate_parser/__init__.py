from .gitmodules import GitmodulesFile
from pathlib import Path
import sys

if __name__ == '__main__':
    file = Path(sys.argv[0])
    gm = GitmodulesFile(file)
    print(gm)

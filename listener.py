import sys
from task import worker


if '__main__' == __name__:
    if 2 > len(sys.argv):
        print(f'{__file__} data_file_path', file=sys.stderr)
        sys.exit()
    else:
        with open(str(sys.argv[1]), 'r') as f:
            for line in f:
                worker.send.delay(line)
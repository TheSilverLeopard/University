
# IMPORT MODULES #

import sys

from QRCode import QRCode

# RUNTIME #

if __name__ == "__main__":
    function = sys.argv[1] if len(sys.argv) > 1 else None
    match function:
        case "create":
            args = sys.argv[2] if len(sys.argv) > 2 else None
            QRCode(args)
        case "test":
            #numericalTest = QRCode("8675309")
            alphanumericalTest = QRCode("HELLO WORLD", QRCode.ERROR_CORRECTIONS.M)
            #byteTest = QRCode("Hello, world!")
            #longByteTest = QRCode("Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!")
            #kanjiTest = QRCode("茗荷")
        case "help":
            raise RuntimeError("Needs implementation...")
        case _:
            raise RuntimeError("It's unclear what you want to do. Run the module with argument \"help\" for help.")
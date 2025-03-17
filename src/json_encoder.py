import json
import sys

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return super().default(o)

if __name__ == "__main__":
    print(json.dumps(eval(sys.stdin.read()), cls=CustomEncoder))

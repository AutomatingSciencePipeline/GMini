import sys
import json

def main(experiment_data: str):
    experiment_id = json.loads(experiment_data)['experiment']['id']
    print("Running Experiment: " + experiment_id, file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("Error: Too few arguments")
    elif len(sys.argv) > 2:
        raise ValueError("Error: Too many arguments")
    main(sys.argv[1])

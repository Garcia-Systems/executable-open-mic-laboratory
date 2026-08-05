"""Print the deterministic sample repertoire."""

from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.repertoire_service import describe_repertoire

if __name__ == "__main__":
    for line in describe_repertoire(build_sample_repertoire()):
        print(line)

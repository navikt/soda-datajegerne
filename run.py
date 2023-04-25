import os
from soda.scan import Scan

def run_scan(s: Scan, f: str, dir: str) -> list:
    dataset = f.split(".")[0]
    s.set_data_source_name(dataset)
    s.add_sodacl_yaml_file(f"{dir}/{f}")
    s.execute()
    return s.get_checks_warn_or_fail()


if __name__ == "__main__":
    s = Scan()
    
    config_path = os.environ["SODA_CONFIG"]
    s.add_configuration_yaml_file(file_path=config_path)

    errors = []
    checks_path = os.environ["SODA_CHECKS_FOLDER"]
    for f in os.listdir(checks_path):
        errors_new = run_scan(s, f, checks_path)
        errors += errors_new

    if len(errors) > 0:
        print("errors", errors)

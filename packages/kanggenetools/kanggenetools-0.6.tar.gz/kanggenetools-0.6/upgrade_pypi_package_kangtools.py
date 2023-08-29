import os
import shutil
import subprocess
import argparse
import re

def update_setup_version():
    with open('setup.py', 'r') as f:
        content = f.read()

    version_match = re.search(r"version='(.*)'", content)
    if version_match is None:
        raise Exception("Could not find version in setup.py")

    version_parts = list(map(int, version_match.group(1).split('.')))
    version_parts[-1] += 1

    new_version = '.'.join(map(str, version_parts))
    content = re.sub(r"version='(.*)'", "version='{}'".format(new_version), content)

    with open('setup.py', 'w') as f:
        f.write(content)

    print(f'Updated setup.py to version {new_version}')
    return new_version

def remove_old_distributions():
    print("Removing old distributions...")
    if os.path.exists('./dist'):
        shutil.rmtree('./dist')

def build_and_upload_distribution():
    print("Building new distribution...")
    subprocess.check_call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])
    
    print("Uploading new distribution to PyPI...")
    subprocess.check_call(['twine', 'upload', 'dist/*'])

def main():
    parser = argparse.ArgumentParser(description="""
        This script updates the version number in setup.py, rebuilds the package, 
        and uploads it to PyPI.
    """)
    parser.add_argument('package_name', type=str, help='The name of the package to update and upload')
    args = parser.parse_args()

    if args.package_name is None:
        print("Please provide the name of the package as an argument. Example usage:")
        print("python upgrade_pypi_package_pip_install.py your_package_name")
        return

    new_version = update_setup_version()
    remove_old_distributions()
    build_and_upload_distribution()
    print("All done!")

if __name__ == "__main__":
    main()

import os
import subprocess

class PackageInstaller:
    def __init__(self, requirements_file='requirements.txt'):
        self.requirements_file = requirements_file

    def install_packages(self):
        # Check if the requirements file exists
        try:
            # Run the pip install command
            subprocess.run(['pip', 'install', '-r', self.requirements_file], check=True)
            print(f"Packages from '{self.requirements_file}' installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install packages. Error: {e}")
        except FileNotFoundError:
            print(f"File '{self.requirements_file}' not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# # Example usage
# installer = PackageInstaller()  # You can pass a different requirements file if needed
# installer.install_packages()


def run_python_file(directory, filename):
    # Construct the full path to the Python file
    file_path = os.path.join(directory, filename)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    # Run the Python file
    try:
        subprocess.run(['python', file_path], check=True)
        print(f"Executed '{filename}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute '{filename}'. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

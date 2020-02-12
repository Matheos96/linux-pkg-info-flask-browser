import os
from flask import Flask, render_template, request
import re
app = Flask(__name__)
app.secret_key = os.urandom(24)

FILE_PATH = '/var/lib/dpkg/status'
# FILE_PATH = 'status.real'  # Debug filepath


# Creates a new object out of package lines (as list) 
def create_pkg_object(pkg_list):
    obj = {}
    pattern = re.compile('.: ')
    curr_key = ''
    for entry in pkg_list:
        if pattern.search(entry):
            tmp = entry.split(': ')
            curr_key = tmp[0].strip()
            obj[curr_key] = tmp[1].strip()
        else:
            obj[curr_key] += entry

    return obj


# Finds dependencies within provided object, as well as finds reverse dependencies for current object in installed
def find_create_dependencies(obj, file_lines):

    # Only perform algorithm if there are dependencies
    if 'Depends' in obj:
        dependencies = obj['Depends'].split(',')  # Make list of all dependencies (they are separated by comma)
        dependencies = [x.strip().split()[0] for x in dependencies]  # Remove version numbers where they exist
        final_dep = []
        # Loop over dependencies
        for dep in dependencies:
            # If dependency has pipe character we choose the first one that also is found in the installed pkgs
            if '|' in dep:
                tmp = dep.split('|')  # Temp list of dependency alternatives

                # List of installed packages
                packages = [x.split(':')[1].strip() for x in file_lines if x.startswith('Package: ')]

                # Sort for convenience
                tmp.sort()
                packages.sort()

                # Loop over dependency alternatives
                for alt in tmp:
                    # If alternative is installed packages, add it to our list and break. (First matching only)
                    if alt in packages:
                        final_dep.append(alt)
                        break
            # If dependency has no pipeline character, simply add it to the list
            else:
                if dep not in final_dep:
                    final_dep.append(dep)

        # Set the Depends key to the new list in original object
        obj['Depends'] = final_dep

        # Find reverse dependencies
        reverse_deps = []
        curr_pkg = ''  # Hold value of current package name
        # Loop over all the lines in the file
        for line in file_lines:
            if line.startswith('Package: '):
                curr_pkg = line.split(':')[1].strip()  # Set name of current package
            # If the package has a depends line we check if the package in our object is on that line, if so add it
            elif line.startswith('Depends: ') and len(curr_pkg) > 0:
                # Make sure we dont add current package. as sometime "in" matches with packages that include the name of curr_pkg
                if obj['Package'] in line and obj['Package'] != curr_pkg:
                    reverse_deps.append(curr_pkg)
        # Add the key+value to object if there are reverse dependencies
        if len(reverse_deps) > 0:
            obj['Reverse_Dependencies'] = reverse_deps


@app.route('/', methods=['GET'])
def index():
    # Open file, read in all lines into a list and close the file
    file = open(FILE_PATH, 'r', encoding='UTF-8')
    lines = file.readlines()
    file.close()

    # Filter list of lines to only get the package names. Then strip and remove the leading 'Package: '
    packages = [x.split(':')[1].strip() for x in lines if x.startswith('Package: ')]

    packages.sort()  # Sort the list of package names

    return render_template('index.html', package_names=packages)


@app.route('/package', methods=['GET'])
def package():
    pkg = request.args.get('name')

    # Open file, read in all lines into a list and close the file
    file = open(FILE_PATH, 'r', encoding='UTF-8')
    lines = file.readlines()
    file.close()

    pkg_content = []
    add = False
    # Loop over all lines in file
    for line in lines:
        # If we find the Package: line and if it matches our package, set add=True
        if 'Package: ' in line:
            if line.split(':')[1].strip() == pkg:
                add = True
        # Once add=True and we find a blank row, the package has no more lines, break
        elif line.strip() == '' and add:
            break

        # If package found, append its lines to pkg_content
        if add:
            pkg_content.append(line)

    # Create object out of package lines
    pkg_obj = create_pkg_object(pkg_content)

    # Find reverse dependencies and parse own dependencies on our object
    find_create_dependencies(pkg_obj, lines)

    return render_template('package.html', package=pkg_obj)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

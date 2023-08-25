

def get_library_dependency(meta_data_string:str):
    """Get the required packages by the library, returns a list of package names"""
    package_reqs = []
    for line in meta_data_string.split("\n"):
        if line.startswith("Requires-Dist:"):
            pkg_name : str = line.replace("Requires-Dist:", "")
            pkg_name = pkg_name.replace("Requires-Dist: ", "")

            real_pkg_name = ""
            stillComplete = True
            for i in pkg_name:
                if i != "(" and i != ")" and i != ";" and stillComplete == True:
                    real_pkg_name = real_pkg_name + i
                else:
                    stillComplete = False
            package_reqs.append(real_pkg_name.replace(" ", ""))
    
    return package_reqs

if __name__ == "__main__":
    pass
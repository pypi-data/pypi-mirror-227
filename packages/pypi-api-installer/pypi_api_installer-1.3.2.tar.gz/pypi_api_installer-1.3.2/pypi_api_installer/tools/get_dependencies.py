import requests, json

def get_library_dependency(lib_name:str):
    """Get the required packages by the library, returns a list of package names"""
    package_reqs = []
    get_dpdns = json.loads(requests.get(f"https://pypi.org/pypi/{lib_name}/json").text)['info']['requires_dist']

    for pkn in get_dpdns:
        full_name = ""
        complete_getten_litters = True
        for n in pkn:
            if n != "(" and n != ")" and n != ";" and complete_getten_litters:
                full_name = full_name + n
            else:
                complete_getten_litters = False
        package_reqs.append(full_name.replace(" ", ""))
    
    return package_reqs

if __name__ == "__main__":
    print(get_library_dependency("requests"))
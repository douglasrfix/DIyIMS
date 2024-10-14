def get_url_dict():
    url_dict = {}
    url_dict["add"] = "http://127.0.0.1:5001/api/v0/add"
    url_dict["get"] = "http://127.0.0.1:5001/api/v0/get"
    url_dict["id"] = "http://127.0.0.1:5001/api/v0/id"
    url_dict["dag_import"] = "http://127.0.0.1:5001/api/v0/dag/import"
    url_dict["name_publish"] = "http://127.0.0.1:5001/api/v0/name/publish"
    url_dict["find_providers"] = "http://127.0.0.1:5001/api/v0/routing/findprovs"
    url_dict["pin_list"] = "http://127.0.0.1:5001/api/v0/pin/ls"
    url_dict["pin_remove"] = "http://127.0.0.1:5001/api/v0/pin/rm"
    url_dict["run_gc"] = "http://127.0.0.1:5001/api/v0/repo/gc"
    url_dict["pin_add"] = "http://127.0.0.1:5001/api/v0/pin/add"
    return url_dict

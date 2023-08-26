import webbrowser
import json
import urllib.parse
import time

from nodemapper.server import server


def parse_dict(data: dict):
    parsed_data = {}
    for key, value in data.items():
        if isinstance(value, dict) and len(value.keys()) != 0:
            parsed_data[key] = parse_dict(value)
        elif key == "__desc__":
            parsed_data[key] = value
        else:
            parsed_data[key] = {"__desc__": "No description provided."}
    return parsed_data


def launch(lhs: dict, 
           rhs: dict, 
           lhsTitle: str = "No title provided.", 
           lhsDescription: str = "No description provided.",
           lhsLink: str = "#",
           rhsTitle: str = "No title provided.",
           rhsDescription: str = "No description provided.",
           rhsLink: str = "#",
           host: str = "localhost",
           port: str = "9092"):
    data = {"lhs": parse_dict(lhs), "rhs": parse_dict(rhs), "lhsTitle": lhsTitle, "lhsDescription": lhsDescription, "rhsTitle": rhsTitle, "rhsDescription": rhsDescription, "lhsLink": lhsLink, "rhsLink": rhsLink}
    launched_server = server(host, port)
    launched_server.start()
    webbrowser.open(f"https://nodemapper.freemyip.com/?" + urllib.parse.urlencode({"data": json.dumps(data), "host": host, "port": port}))

    while(launched_server.data == None):
        time.sleep(2)
    return launched_server.data
   
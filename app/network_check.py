import socket
import json
from prettytable import PrettyTable

# variables
host = "example.host.com"
services = {
    "ftp": [1234, "tcp"],
}


class MiloNetworkTool:
    str_table = None

    def __init__(self):
        pass

    def check_service_port(self, ip: str, port: int, protocol="tcp", service_name=None):
        if protocol == "tcp":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return [service_name, "open", "OK"]
            except:
                return [service_name, "close", "not working"]
            finally:
                s.close()
        else:
            raise socket.herror("TCP services only supported!")

    def check_all_services(self, host, services):
        rows = []
        try:
            host_ip = socket.gethostbyaddr(host)
            if "nette" in host_ip[0]:
                rows.append(["internet provider", host_ip[0], "OK"])
            else:
                rows.append(
                    ["internet provider", host_ip[0], "backup internet"])
        except socket.gaierror:
            rows.append(["internet provider", "", "NETTE/PLAY: not working"])

        for k, v in services.items():
            if v[1] == "tcp":
                r = self.check_service_port(
                    host, v[0], protocol=v[1], service_name=k)
                rows.append(r)
            else:
                raise socket.herror("TCP only supported")

        self.table_print(rows)

    def table_print(self, rows_d):
        table = PrettyTable()
        table.field_names = ["SERVICE", "RESULT", "STATUS"]
        table.hrules = 1

        if len(rows_d) == 1:
            table.add_row(rows_d)
        else:
            table.add_rows(rows_d)

        if rows_d[0][2] == "backup internet":
            table.add_row(["vpn", "close", "not working"])
        else:
            table.add_row(["vpn", "open", "OK"])

        self.str_table = table.get_string()

    def create_slack_block(self):
        text = ""
        lines_list = self.str_table.splitlines()
        for line in lines_list:
            text += line + "\n"

        block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{text}```",
                },
            }
        ]
        return block


if __name__ == "__main__":
    mi = MiloNetworkTool()
    mi.check_all_services(host, services)
    mi.create_slack_block()

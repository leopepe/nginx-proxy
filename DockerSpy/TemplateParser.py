__author__ = 'leonardo'

class TemplateParser:

    def __init__(self, template_path='./templates/template'):
        self.template = None
        with open(template_path, 'r') as template_file:
            self.template = template_file.read()

    def replace_node_info(self, container_info):
        data = self.template.replace(
            '<container_vhost>', container_info['vhost']
        ).replace(
            '<container_ip>', container_info['ip']
        ).replace(
            '<container_port>', container_info['port']
        )

        return data


if __name__ == '__main__':
    parser = TemplateParser()
    container_info = {}
    container_info = {
        'name': 'node1',
        'vhost': 'node1.nodomain',
        'ip': '172.0.10.5',
        'port': '8080'
    }
    print(parser.replace_node_info(container_info=container_info))


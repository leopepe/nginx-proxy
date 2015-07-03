__author__ = 'leonardo'

from docker import Client


class DockerSpy(Client):
    """

    """
    def __init__(self, container_name=None, unix_domain='unix://var/run/docker.sock'):
        super(DockerSpy, self).__init__()
        self.client = Client(base_url=unix_domain)
        if container_name:
            self.container_info = self.client.inspect_container(container=container_name)
        else:
            self.container_info = None

    def event_listener(self):
        return self.events(decode=True)

    def env(self, container):
        """

        :rtype: dict
        :return: container's environment variable
        """
        container_info = self.client.inspect_container(container=container)

        def _into_dict():
            """

            :rtype : dict
            :return: container_config
            """
            container_config = {}
            for item in container_info['Config']['Env']:
                k, v = item.split('=', 1)
                container_config[k] = v

            return container_config

        try:
            return _into_dict()
        except:
            raise Exception

    def virtual_port(self, container):
        try:
            container_info = self.client.inspect_container(container=container)
            return container_info['VIRTUAL_PORT']
        except:
            raise Exception

    def ip_address(self, container):
        try:
            container_info = self.client.inspect_container(container=container)
            return container_info['NetworkSettings']['IPAddress']
        except:
            raise Exception

    def list_containers(self):
        try:
            # list live containers names
            # containers = [{'Name': container['Names'][0].replace('/', '')} for container in docker.containers()]
            # containers = {'Name': container['Names'][0].replace('/', '') for container in docker.containers()}
            containers = [container['Names'][0].replace('/', '') for container in self.client.containers()]
            return containers
        except Exception:
            raise

    def live_containers_info(self):
        containers_list = self.list_containers()
        try:
            containers_info = []
            for cont in containers_list:
                if self.env(container=cont).get('VIRTUAL_HOST'):
                    vhost = self.env(container=cont)['VIRTUAL_HOST']
                else:
                    vhost = ''

                if self.env(container=cont).get('VIRTUAL_PORT'):
                    port = self.env(container=cont)['VIRTUAL_PORT']
                else:
                    port = ''

                containers_info.append(
                    {
                        'name': cont,
                        'vhost': vhost,
                        'ip': self.ip_address(container=cont),
                        'port': port
                    }
                )

            return containers_info
        except Exception:
            raise


if __name__ == '__main__':
    from TemplateParser import TemplateParser
    from json import dumps
    docker = DockerSpy()
    parser = TemplateParser()
    #
    # Testing DockerSpy methods
    #
    # print(dumps(docker.env(container='chargeback-sync'), indent=4))
    # print(dumps(docker.virtual_port(container='chargeback-sync'), indent=4))
    # print(dumps(docker.ip_address(container='chargeback-sync'), indent=4))
    # print(dumps(docker.containers(filters={'status': 'running'}), indent=4))
    # print(dumps(docker.list_containers(), indent=4))
    # print(dumps(docker.live_containers_info(), indent=4))
    #
    # Testing TemplateParser()
    #
    # data = ''
    # for node_info in docker.live_containers_info():
    #     if node_info['vhost'] and node_info['port']:
    #         data += parser.replace_node_info(container_info=node_info)
    # print(data)
    #
    #
    # Testing event_listener()
    #

    def generate_confd():
        nginx_conf_path = 'default.conf'  # '/etc/nginx/conf.d/default.conf'
        template_base = open('./template_base', 'r').read()
        confd_data = ''

        def _generate():
            data = ''
            # run through live containers list
            for node_info in docker.live_containers_info():
                # vhost and port exists
                if node_info['vhost'] and node_info['port']:
                    data += parser.replace_node_info(container_info=node_info)
            return data

        def _save(data=_generate()):
            confd = ''
            # Create config for containers at startup
            with open(nginx_conf_path, 'w') as config_file:
                confd = template_base + data
                config_file.write(confd)

        # generate conf.d/default.conf
        _generate()
        _save(data=_generate())

        while True:
            for event in docker.event_listener().__iter__():
                if event['status'] == 'start':
                    print('Container {name} status changed to {status}'.format(name=event['from'], status=event['status']))
                    _save(data=_generate())
                elif event['status'] == 'stop' or event['status'] == 'die':
                    print('Container {name} status changed to {status}'.format(name=event['from'], status=event['status']))
                    _save(data=_generate())

    generate_confd()

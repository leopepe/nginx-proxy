#!/usr/bin/env python
__author__ = 'leonardo'

from DockerSpy import DockerSpy
from TemplateParser import TemplateParser
from subprocess import call
import os

if __name__ == '__main__':
    # constants
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
    TEMPLATE_BASE = os.path.join(TEMPLATE_DIR, 'template_base')
    TEMPLATE = os.path.join(TEMPLATE_DIR, 'template')

    docker = DockerSpy()
    parser = TemplateParser(template_path=TEMPLATE)

    def generate_confd():
        nginx_conf_path = '/etc/nginx/conf.d/default.conf'
        template_base = open(TEMPLATE_BASE, 'r').read()
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
            with open(nginx_conf_path, 'w+') as config_file:
                confd = template_base + data
                config_file.write(confd)

        # generate conf.d/default.conf
        _generate()
        _save(data=_generate())
        call(['/etc/init.d/nginx', 'reload'])

        while True:
            for event in docker.event_listener().__iter__():
                if event['status'] == 'start':
                    print('Container {name} status changed to {status}'.format(name=event['from'], status=event['status']))
                    _save(data=_generate())
                    call(['/etc/init.d/nginx', 'reload'])
                elif event['status'] == 'stop' or event['status'] == 'die':
                    print('Container {name} status changed to {status}'.format(name=event['from'], status=event['status']))
                    _save(data=_generate())
                    call(['/etc/init.d/nginx', 'reload'])

    generate_confd()

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   config.py
@Time    :   2023/08/11 15:44:57
@Author  :   mf.liang
@Version :   1.0
@Contact :   mf.liang@outlook.com
@Desc    :
"""
import yaml
from dhcptool.tools import Tools


def read_yaml_config():
    # 读取YAML文件
    with open('/etc/dhcptool.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data


def merge_args(cmd_args, ip_type):
    """
    合并 config.yaml和  cmd_args的参数
    Args:
        cmd_args:
        ip_type:

    Returns: cmd_args

    """
    # 读取config.yaml中的参数配置
    config_args = read_yaml_config()

    # 根据ip_type 选择 ipv4的参数还是ipv6的参数
    config_args = config_args['v4'] if ip_type == 'ipv4' else config_args['v6']

    # 开始合并 options选项参数
    config_options = config_args.get('options')
    if cmd_args.options:
        # 如果config_options存在参数
        cmd_options = [i.split('=') for i in cmd_args.options.split('&')]
        cmd_options = dict(cmd_options)
        # 将cmd_options参数覆盖config_option参数
        config_options.update(cmd_options)
    if config_options:
        config_options = {str(key): value for key, value in config_options.items()}
        # 将config_options转化为cmd_args格式的options结果
        config_options = list(config_options.items())
        config_options = ['='.join(option) for option in config_options]
        config_options = '&'.join(config_options)
    # 合并常规参数
    if cmd_args.ip_src is None and config_args.get('ip_src'):
        cmd_args.ip_src = config_args.get('ip_src')
    if cmd_args.dhcp_server is None and config_args.get('dhcp_server'):
        cmd_args.dhcp_server = config_args.get('dhcp_server')
    if cmd_args.filter is None and config_args.get('filter'):
        cmd_args.filter = config_args.get('filter')
    if cmd_args.iface is None and config_args.get('iface'):
        cmd_args.iface = config_args.get('iface')
    if cmd_args.relay_forward == Tools.get_local_ipv4() and config_args.get('relay_forward'):
        cmd_args.relay_forward = config_args.get('relay_forward')
    cmd_args.options = config_options
    return cmd_args


if __name__ == '__main__':
    read_yaml_config()

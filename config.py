#! /usr/bin/env python

class HostType(object):
    PHYSICAL_HOST = 0
    VIRTUAL_HOST = 1

# This file need to be updated regularly
class HUT_CONFIG(object):
    WINDOWS_SERVER_CHENGDU = '172.16.64.181'
    WINDOWN_SERVER_SHANGHAI = '192.168.90.142'
    PDU_SERVER_CHENGDU_01 = '172.16.64.180'
    PDU_SERVER_CHENGDU_02 = '172.16.64.200'
    PDU_SERVER_CHENGDU_03 = '172.16.64.199'
    PDU_SERVER_SHANGHAI_01 = '192.168.90.144'

    
    NAME_INFO_MAPPING = {
        'asic01': {
            'ip_address': '172.16.64.201',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_01,
            'pdu_port': 0x1,
            'serial_port': 'com41',
            'hot_plugin_support': True,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic02': {
            'ip_address': '172.16.64.202',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_01,
            'pdu_port': 0x2,
            'serial_port': 'com42',
            'hot_plugin_support': True,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic03': {
            'ip_address': '172.16.64.203',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_01,
            'pdu_port': 0x4,
            'serial_port': 'com43',
            'hot_plugin_support': False,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic04': {
            'ip_address': '172.16.64.204',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_01,
            'pdu_port': 0x8,
            'serial_port': 'com44',
            'hot_plugin_support': False,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic05': {
            'ip_address': '172.16.64.205',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_01,
            'pdu_port': 0x20,
            'serial_port': 'com45',
            'hot_plugin_support': False,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic06': {
            'ip_address': '172.16.64.206',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_01,
            'pdu_port': 0x40,
            'serial_port': 'com46',
            'hot_plugin_support': False,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic07': {
            'ip_address': '172.16.64.207',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_02,
            'pdu_port': 0x8,
            'serial_port': 'com47',
            'hot_plugin_support': False,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic08': {
            'ip_address': '172.16.64.208',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_02,
            'pdu_port': 0x10,
            'serial_port': 'com48',
            'hot_plugin_support': False,
            'for_build': ["local_build"]
        },
        'asic09': {
            'ip_address': '172.16.64.209',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_03,
            'pdu_port': 0x20,
            'serial_port': 'com49',
            'hot_plugin_support': False,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic10': {
            'ip_address': '172.16.64.210',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_02,
            'serial_port': 'com50',
            'pdu_port': 0x40,
            'hot_plugin_support': False,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic17': {
            'ip_address': '172.16.64.211',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_03,
            'serial_port': 'com3',
            'pdu_port': 0x04,
            'hot_plugin_support': True,
            'for_build': ["private_build", "daily_build", "weekly_build"]
        },
        'asic18': {
            'ip_address': '172.16.64.212',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_03,
            'serial_port': 'com50',
            'pdu_port': 0x08,
            'hot_plugin_support': True,
            'for_build': ["local_build"]
        },
        'dirty_powercycle_platform01': {
            'ip_address': '172.16.64.55',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_03,
            'serial_port': 'com14',
            'pdu_port': 0x01,
            'hot_plugin_support': True,
            'for_build': ["local_build"]
        },
        'dirty_powercycle_platform02': {
            'ip_address': '172.16.65.49',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWS_SERVER_CHENGDU,
            'pdu_server': PDU_SERVER_CHENGDU_03,
            'serial_port': 'com16',
            'pdu_port': 0x02,
            'hot_plugin_support': True,
            'for_build': ["local_build"]
        },
        'asic01-SH': {
            'ip_address': '192.168.90.74',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWN_SERVER_SHANGHAI,
            'pdu_server': PDU_SERVER_SHANGHAI_01,
            'pdu_port': 0x01,
            'serial_port': 'com6',
            'hot_plugin_support': True,
            'for_build': ["local_build"]
        },
        'asic02-SH': {
            'ip_address': '192.168.90.49',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWN_SERVER_SHANGHAI,
            'pdu_server': PDU_SERVER_SHANGHAI_01,
            'pdu_port': 0x02,
            'serial_port': 'com7',
            'hot_plugin_support': False,
            'for_build': ["local_build"]
        },
        'asic03-SH': {
            'ip_address': '192.168.90.233',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWN_SERVER_SHANGHAI,
            'pdu_server': PDU_SERVER_SHANGHAI_01,
            'pdu_port': 0x40,
            'serial_port': 'com8',
            'hot_plugin_support': False,
            'for_build': ["local_build"]
        },
        'asic04-SH': {
            'ip_address': '192.168.90.235',
            'username': 'root',
            'password': 'abc-123',
            'ssh_port': 22,
            'type': HostType.PHYSICAL_HOST,
            'windows_server': WINDOWN_SERVER_SHANGHAI,
            'pdu_server': PDU_SERVER_SHANGHAI_01,
            'pdu_port': 0x80,
            'serial_port': 'com9',
            'hot_plugin_support': False,
            'for_build': ["local_build"]
        },
    }

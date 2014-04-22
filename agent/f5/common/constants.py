##############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2014 by F5 Networks and/or its suppliers. All rights reserved.
##############################################################################

# CONSTANTS MODULE
MIN_TMOS_MAJOR_VERSION = 11
MIN_TMOS_MINOR_VERSION = 4
MIN_EXTRA_MB = 500
DEFAULT_HOSTNAME = 'bigip1'
MAX_HOSTNAME_LENGTH = 128
DEFAULT_FOLDER = "/Common"
CONNECTION_TIMEOUT = 30
# DEVICE LOCK PREFIX
DEVICE_LOCK_PREFIX = 'lock_'
# DIR TO CACHE WSDLS.  SET TO NONE TO READ FROM DEVICE
# WSDL_CACHE_DIR = "/data/iControl-11.4.0/sdk/wsdl/"
WSDL_CACHE_DIR = ''
# HA CONSTANTS
HA_VLAN_NAME = "/Common/HA"
HA_SELFIP_NAME = "/Common/HA"
# VIRTUAL SERVER CONSTANTS
VS_PREFIX = 'vs'
# POOL CONSTANTS
POOL_PREFIX = 'pool'
# POOL CONSTANTS
MONITOR_PREFIX = 'monitor'
# VLAN CONSTANTS
VLAN_PREFIX = 'vlan'
# BIG-IP PLATFORM CONSTANTS
BIGIP_VE_PLATFORM_ID = 'Z100'
# DEVICE CONSTANTS
DEVICE_DEFAULT_DOMAIN = ".local"
DEVICE_HEALTH_SCORE_CPU_WEIGHT = 1
DEVICE_HEALTH_SCORE_MEM_WEIGHT = 1
DEVICE_HEALTH_SCORE_CPS_WEIGHT = 1
DEVICE_HEALTH_SCORE_CPS_PERIOD = 5
DEVICE_HEALTH_SCORE_CPS_MAX = 100
# DEVICE GROUP CONSTANTS
PEER_ADD_ATTEMPTS_MAX = 10
PEER_ADD_ATTEMPT_DELAY = 2
DEFAULT_SYNC_MODE = 'autosync'
# MAX RAM SYNC DELAY IS 63 SECONDS
# (3+6+9+12+15+18) = 63
SYNC_DELAY = 3
MAX_SYNC_ATTEMPTS = 6
# SHARED CONFIG CONSTANTS
SHARED_CONFIG_DEFAULT_TRAFFIC_GROUP = '/Common/traffic-group-local-only'
SHARED_CONFIG_DEFAULT_FLOATING_TRAFFIC_GROUP = '/Common/traffic-group-1'
# LOGGING PARAMETERS
import logging
LOG_LEVEL = logging.DEBUG
VXLAN_UDP_PORT = 4789

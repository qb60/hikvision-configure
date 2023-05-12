## Hikvision/HiWatch camera configuring script ##

This script can be used for automatic configuring Hikvision/HiWatch cameras.

All parameters except IP is located in the script.
Uncomment steps you need in **set_cam_options()** function.

```
USAGE:
    ./cam_config.py OLD_IP [NEW_IP/MASK]
    ./cam_config.py OLD_IP [dhcp]

Examples:
    ./cam_config.py 10.10.10.10
    ./cam_config.py 10.10.10.10 10.10.11.10/25
    ./cam_config.py 10.10.10.10 dhcp

```

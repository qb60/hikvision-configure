## Hikvision/HiWatch camera batch auto configuration ##

This script may be used for automatic configure Hikvision/HiWatch cameras including activation.

All parameters except IP is located in the script.
Uncomment steps you need in **set_cam_options()** function.

```
USAGE:
    ./cam_config.py OLD_IP [NEW_IP/MASK]
Example:
    ./cam_config.py 10.145.17.206 10.226.47.130/25
```

#! /usr/bin/python
# coding=utf-8

# ======================= HIKVISION CAM SETUP ======================
# 2020-07-09
# MJPEG stream: /mjpeg/ch1/sub/av_stream
# H264  stream: /h264/ch1/main/av_stream

# pip install --user pycrypto
# pip install --user requests
from __future__ import print_function

new_ntp = '10.10.10.10'
time_zone_gmt_offset = '+5:00:00'

admin_user_name = 'admin'
admin_old_password = 'qwer1234'
# admin_new_password = 'qwer1234'
admin_new_password = admin_old_password

video_user_name = 'video'
video_user_password = 'qwer1234'

# True False
allow_videouser_downloading_records = True

monitoring_user_name = 'monuser'
monitoring_user_password = '1234qwer'

# 320,640,640,704
# 240,360,480,576
# 25,22,20,18,16,15,12,10,8,6,4,2,1
mjpeg_stream_width = 640
mjpeg_stream_height = 480
mjpeg_stream_framerate = 6

# 1280,1920,2560,3072,3840
# 720, 1080,1440,1728,2160
# 15,12,10,8,6,4,2,1
h264_stream_width = 1280
h264_stream_height = 720
h264_stream_framerate = 10

# True False
record_audio = True

primary_dns = '5.5.5.5'
secondary_dns = '8.8.8.8'

sender_email = 'info@example.com'
sender_name_prefix = 'ip-cam-'
smtp_server = 'smtp.example.com'
notification_email1 = 'admin1@example.com'
notification_email2 = 'admin2@example.com'
notification_email3 = ''

refomat_sd_if_it_is_ok = False
photo_capture_interval_minutes = 15
video_ratio_percents = 100

# from params import *

# not less than 15s
DELAY_AFTER_FORMATTING_SECONDS = 20

# ============================= MAIN WORK ===============================


def set_cam_options(auth_type, current_cam_ip, current_password, new_cam_ip):
    # COMMENT UNNEEDED STEPS

    # set_video_user(auth_type, current_cam_ip, current_password)
    # set_ntp(auth_type, current_cam_ip, current_password)
    # set_time(auth_type, current_cam_ip, current_password)
    # set_osd(auth_type, current_cam_ip, current_password)
    # set_off_ip_ban_option(auth_type, current_cam_ip, current_password)
    # set_video_streams(auth_type, current_cam_ip, current_password)
    # set_cloud_parameters(auth_type, current_cam_ip, current_password)

    # =========== for offices - motion detection and so on ===============
    # set_monitoring_user(auth_type, current_cam_ip, current_password)
    # set_basic_auth_method(auth_type, current_cam_ip, current_password)
    # set_no_beep_event_trigger(auth_type, current_cam_ip, current_password)
    # set_device_name(auth_type, current_cam_ip, current_password, new_cam_ip)
    # set_email_notification_addresses(auth_type, current_cam_ip, current_password, new_cam_ip)
    # set_video_photo_ratio(auth_type, current_cam_ip, current_password)
    # set_motion_detector_parameters(auth_type, current_cam_ip, current_password)
    # format_storage(auth_type, current_cam_ip, current_password)
    # set_email_event_triggers(auth_type, current_cam_ip, current_password)
    # set_recording_by_motion_detector_trigger(auth_type, current_cam_ip, current_password)
    # set_recording_schedule(auth_type, current_cam_ip, current_password)
    # set_photo_capturing_parameters(auth_type, current_cam_ip, current_password)
    # ====================================================================
    
    # print_user_list(auth_type, current_cam_ip, current_password)
    # set_ip_and_dns(auth_type, current_cam_ip, new_cam_ip, current_password)
    # set_password(auth_type, current_cam_ip, current_password, admin_new_password)
    # reboot_cam(auth_type, current_cam_ip)
    pass


# ==================================================================

import re
import requests
import base64
import time
import sys
import ipaddress
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from sys import stdout

# ==================================================================
VIDEO_TRACK_ID = '101'
PHOTO_TRACK_ID = '103'
# ============================= URLS ===============================

password_url = '/ISAPI/Security/users/1'
time_url = '/ISAPI/System/time'
ntp_url = '/ISAPI/System/time/ntpServers'
osd_url = '/ISAPI/System/Video/inputs/channels/1/overlays'
video_url = '/ISAPI/Streaming/channels'
video_capabilities_url = '/ISAPI/Streaming/channels/{}/capabilities'
ip_url = '/ISAPI/System/Network/interfaces/1/ipAddress'
reboot_url = '/ISAPI/System/reboot'
ip_ban_option_url = '/ISAPI/Security/illegalLoginLock'
network_capabilities_url = '/ISAPI/System/Network/capabilities'
cloud_url = '/ISAPI/System/Network/EZVIZ'

activation_status_url = '/SDK/activateStatus'
public_key_url = '/ISAPI/Security/challenge'
activation_url = '/ISAPI/System/activate'
users_url = '/ISAPI/Security/users'
permissons_url = '/ISAPI/Security/UserPermission'

device_info_url = '/ISAPI/System/deviceInfo'
email_addresses_url = '/ISAPI/System/Network/mailing/1'
event_diskfull_trigger_url = '/ISAPI/Event/triggers/diskfull/notifications'
event_diskerror_trigger_url = '/ISAPI/Event/triggers/diskerror/notifications'
event_motion_detector_trigger_url = '/ISAPI/Event/triggers/VMD-1/notifications'
motion_detector_parameters_url = '/ISAPI/System/Video/inputs/channels/1/motionDetection'
recording_schedule_url = '/ISAPI/ContentMgmt/record/tracks/'
recording_video_schedule_url = recording_schedule_url + VIDEO_TRACK_ID
recording_photo_schedule_url = recording_schedule_url + PHOTO_TRACK_ID
shapshot_channel_url = '/ISAPI/Snapshot/channels/1'

video_photo_ratio_url = '/ISAPI/ContentMgmt/Storage/quota/1'

storages_status_url = '/ISAPI/ContentMgmt/Storage/hdd'
storage_format_url = '/ISAPI/ContentMgmt/Storage/hdd/1/format'
storage_format_percents_url = '/ISAPI/ContentMgmt/Storage/hdd/1/formatStatus'

security_capabilities_url = '/ISAPI/Security/capabilities'
web_authorization_type_url = '/ISAPI/Security/webCertificate'

# =========================== REQUESTS =============================

user_password_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<User>
    <id>1</id>
    <userName>admin</userName>
    <password>pass</password>
</User>
"""

add_user_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<User>
    <userName>video</userName>
    <userLevel>Viewer</userLevel>
    <password>pass</password>
</User>
"""

time_zone_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<Time>
    <timeMode>NTP</timeMode>
    <timeZone>timezone</timeZone>
</Time>
"""

ntp_server_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<NTPServerList>
    <NTPServer>
        <id>1</id>
        <addressingFormatType>ipaddress</addressingFormatType>
        <ipAddress>1.1.1.1</ipAddress>
        <portNo>123</portNo>
        <synchronizeInterval>60</synchronizeInterval>
    </NTPServer>
</NTPServerList>
"""

ip_address_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<IPAddress>
<ipVersion>dual</ipVersion>
<addressingType>static</addressingType>
<ipAddress>address</ipAddress>
<subnetMask>255.255.255.0</subnetMask>
<ipv6Address>::</ipv6Address>
<bitMask>0</bitMask>
<DefaultGateway>
    <ipAddress>gateway</ipAddress>
    <ipv6Address>::</ipv6Address>
</DefaultGateway>
<PrimaryDNS>
    <ipAddress>8.8.8.8</ipAddress>
</PrimaryDNS>
<SecondaryDNS>
    <ipAddress>0.0.0.0</ipAddress>
</SecondaryDNS>
<Ipv6Mode>
    <ipV6AddressingType>ra</ipV6AddressingType>
    <ipv6AddressList>
        <v6Address>
            <id>1</id>
            <type>manual</type>
            <address>::</address>
            <bitMask>0</bitMask>
        </v6Address>
    </ipv6AddressList>
</Ipv6Mode>
</IPAddress>
"""

cloud_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<EZVIZ>
   <enabled>false</enabled>
</EZVIZ>
"""

osd_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<VideoOverlay>
    <normalizedScreenSize>
        <normalizedScreenWidth>704</normalizedScreenWidth>
        <normalizedScreenHeight>576</normalizedScreenHeight>
    </normalizedScreenSize>
    <attribute>
        <transparent>false</transparent>
        <flashing>false</flashing>
    </attribute>
    <fontSize>adaptive</fontSize>
    <TextOverlayList size="4"></TextOverlayList>
    <DateTimeOverlay>
        <enabled>true</enabled>
        <positionX>0</positionX>
        <positionY>544</positionY>
        <dateStyle>YYYY-MM-DD</dateStyle>
        <timeStyle>24hour</timeStyle>
        <displayWeek>false</displayWeek>
    </DateTimeOverlay>
    <channelNameOverlay>
        <enabled>false</enabled>
        <positionX>512</positionX>
        <positionY>64</positionY>
    </channelNameOverlay>
    <frontColorMode>auto</frontColorMode>
    <frontColor>000000</frontColor>
</VideoOverlay>
"""

video_h254_xml = """\
<Video>
    <enabled>true</enabled>
    <videoInputChannelID>1</videoInputChannelID>
    <videoCodecType>H.264</videoCodecType>
    <videoScanType>progressive</videoScanType>
    <videoResolutionWidth></videoResolutionWidth>
    <videoResolutionHeight></videoResolutionHeight>
    <videoQualityControlType>VBR</videoQualityControlType>
    <constantBitRate>2048</constantBitRate>
    <fixedQuality>60</fixedQuality>
    <vbrUpperCap>2048</vbrUpperCap>
    <vbrLowerCap>32</vbrLowerCap>
    <maxFrameRate></maxFrameRate>
    <keyFrameInterval>5000</keyFrameInterval>
    <snapShotImageType>JPEG</snapShotImageType>
    <H264Profile>Main</H264Profile>
    <GovLength>50</GovLength>
    <PacketType>PS</PacketType>
    <PacketType>RTP</PacketType>
    <smoothing>50</smoothing>
</Video>
"""

video_mjpeg_xml = """\
<Video>
    <enabled>true</enabled>
    <videoInputChannelID>1</videoInputChannelID>
    <videoCodecType>MJPEG</videoCodecType>
    <videoScanType>progressive</videoScanType>
    <videoResolutionWidth></videoResolutionWidth>
    <videoResolutionHeight></videoResolutionHeight>
    <videoQualityControlType>VBR</videoQualityControlType>
    <constantBitRate>256</constantBitRate>
    <fixedQuality>60</fixedQuality>
    <vbrUpperCap>256</vbrUpperCap>
    <vbrLowerCap>32</vbrLowerCap>
    <maxFrameRate></maxFrameRate>
    <keyFrameInterval>8333</keyFrameInterval>
    <snapShotImageType>JPEG</snapShotImageType>
    <GovLength>50</GovLength>
    <PacketType>PS</PacketType>
    <PacketType>RTP</PacketType>
    <smoothing>50</smoothing>
</Video>
"""

ip_ban_option_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<IllegalLoginLock>
    <enabled>false</enabled>
</IllegalLoginLock>
"""

activation_password_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<ActivateInfo>
    <password>pass</password>
</ActivateInfo>
"""

public_key_xml = """\
<PublicKey>
    <key>publickey</key>
</PublicKey>
"""

video_user_permissions_xml = """\
<UserPermission version="2.0">
    <id>id</id>
    <userID>userid</userID>
    <userType>viewer</userType>
    <remotePermission version="2.0">
        <playBack></playBack>
        <preview>true</preview>
        <record>false</record>
        <videoChannelPermissionList>
            <videoChannelPermission>
                <id>1</id>
                <preview>true</preview>
                <playBack></playBack>
                <record>false</record>
            </videoChannelPermission>
        </videoChannelPermissionList>
        <ptzControl>false</ptzControl>
        <upgrade>false</upgrade>
        <parameterConfig>false</parameterConfig>
        <restartOrShutdown>false</restartOrShutdown>
        <logOrStateCheck>false</logOrStateCheck>
        <voiceTalk>false</voiceTalk>
        <transParentChannel>false</transParentChannel>
        <contorlLocalOut>false</contorlLocalOut>
        <alarmOutOrUpload>false</alarmOutOrUpload>
    </remotePermission>
</UserPermission>
"""

device_info_xml = """\
<DeviceInfo version="2.0">
    <deviceName>name</deviceName>
</DeviceInfo>
"""

email_addresses_xml = """\
<mailing version="2.0">
    <id>1</id>
    <sender>
        <emailAddress></emailAddress>
        <name></name>
        <smtp>
            <enableAuthorization>false</enableAuthorization>
            <enableSSL>false</enableSSL>
            <addressingFormatType>hostname</addressingFormatType>
            <hostName></hostName>
            <portNo>25</portNo>
            <accountName></accountName>
            <enableTLS>false</enableTLS>
            <startTLS>false</startTLS>
        </smtp>
    </sender>
    <receiverList>
        <receiver>
            <id>1</id>
            <name></name>
            <emailAddress></emailAddress>
        </receiver>
        <receiver>
            <id>2</id>
            <name></name>
            <emailAddress></emailAddress>
        </receiver>
        <receiver>
            <id>3</id>
            <name></name>
            <emailAddress></emailAddress>
        </receiver>
    </receiverList>
    <attachment>
        <snapshot>
            <enabled>false</enabled>
            <interval>2</interval>
        </snapshot>
    </attachment>
</mailing>
"""

no_beep_event_trigger_xml = """\
<EventTriggerNotificationList version="2.0"></EventTriggerNotificationList>
"""

email_event_trigger_xml = """\
<EventTriggerNotificationList version="2.0">
    <EventTriggerNotification>
        <id>email</id>
        <notificationMethod>email</notificationMethod>
        <notificationRecurrence>beginning</notificationRecurrence>
    </EventTriggerNotification>
</EventTriggerNotificationList>
"""

recording_event_trigger_xml = """\
<EventTriggerNotificationList version="2.0">
    <EventTriggerNotification>
        <id>record-1</id>
        <notificationMethod>record</notificationMethod>
        <videoInputID>1</videoInputID>
        <notificationRecurrence>beginning</notificationRecurrence>
    </EventTriggerNotification>
</EventTriggerNotificationList>
"""

motion_detector_parameters_xml = """\
<MotionDetection version="2.0">
    <enabled>true</enabled>
    <enableHighlight>true</enableHighlight>
    <samplingInterval>2</samplingInterval>
    <startTriggerTime>500</startTriggerTime>
    <endTriggerTime>500</endTriggerTime>
    <regionType>grid</regionType>
    <Grid>
        <rowGranularity>18</rowGranularity>
        <columnGranularity>22</columnGranularity>
    </Grid>
    <MotionDetectionLayout version="2.0"
        xmlns="http://www.std-cgi.com/ver20/XMLSchema">
        <sensitivityLevel>20</sensitivityLevel>
        <layout>
            <gridMap>fffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffcfffffc</gridMap>
        </layout>
    </MotionDetectionLayout>
</MotionDetection>
"""

recording_schedule_time_xml = """\
<ScheduleBlock ScheduleActionSize="8" >
    <ScheduleBlockGUID>{00000000-0000-0000-0000-000000000000}</ScheduleBlockGUID>
    <ScheduleBlockType>www.std-cgi.com/racm/schedule/ver10</ScheduleBlockType>
    <ScheduleAction>
        <id>1</id>
        <ScheduleActionStartTime>
            <DayOfWeek>Monday</DayOfWeek>
            <TimeOfDay>00:00:00</TimeOfDay>
        </ScheduleActionStartTime>
        <ScheduleActionEndTime>
            <DayOfWeek>Monday</DayOfWeek>
            <TimeOfDay>24:00:00</TimeOfDay>
        </ScheduleActionEndTime>
        <ScheduleDSTEnable>false</ScheduleDSTEnable>
        <Description>nothing</Description>
        <Actions>
            <Record>true</Record>
            <ActionRecordingMode>MOTION</ActionRecordingMode>
        </Actions>
    </ScheduleAction>
    <ScheduleAction>
        <id>1</id>
        <ScheduleActionStartTime>
            <DayOfWeek>Tuesday</DayOfWeek>
            <TimeOfDay>00:00:00</TimeOfDay>
        </ScheduleActionStartTime>
        <ScheduleActionEndTime>
            <DayOfWeek>Tuesday</DayOfWeek>
            <TimeOfDay>24:00:00</TimeOfDay>
        </ScheduleActionEndTime>
        <ScheduleDSTEnable>false</ScheduleDSTEnable>
        <Description>nothing</Description>
        <Actions>
            <Record>true</Record>
            <ActionRecordingMode>MOTION</ActionRecordingMode>
        </Actions>
    </ScheduleAction>
    <ScheduleAction>
        <id>1</id>
        <ScheduleActionStartTime>
            <DayOfWeek>Wednesday</DayOfWeek>
            <TimeOfDay>00:00:00</TimeOfDay>
        </ScheduleActionStartTime>
        <ScheduleActionEndTime>
            <DayOfWeek>Wednesday</DayOfWeek>
            <TimeOfDay>24:00:00</TimeOfDay>
        </ScheduleActionEndTime>
        <ScheduleDSTEnable>false</ScheduleDSTEnable>
        <Description>nothing</Description>
        <Actions>
            <Record>true</Record>
            <ActionRecordingMode>MOTION</ActionRecordingMode>
        </Actions>
    </ScheduleAction>
    <ScheduleAction>
        <id>1</id>
        <ScheduleActionStartTime>
            <DayOfWeek>Thursday</DayOfWeek>
            <TimeOfDay>00:00:00</TimeOfDay>
        </ScheduleActionStartTime>
        <ScheduleActionEndTime>
            <DayOfWeek>Thursday</DayOfWeek>
            <TimeOfDay>24:00:00</TimeOfDay>
        </ScheduleActionEndTime>
        <ScheduleDSTEnable>false</ScheduleDSTEnable>
        <Description>nothing</Description>
        <Actions>
            <Record>true</Record>
            <ActionRecordingMode>MOTION</ActionRecordingMode>
        </Actions>
    </ScheduleAction>
    <ScheduleAction>
        <id>1</id>
        <ScheduleActionStartTime>
            <DayOfWeek>Friday</DayOfWeek>
            <TimeOfDay>00:00:00</TimeOfDay>
        </ScheduleActionStartTime>
        <ScheduleActionEndTime>
            <DayOfWeek>Friday</DayOfWeek>
            <TimeOfDay>24:00:00</TimeOfDay>
        </ScheduleActionEndTime>
        <ScheduleDSTEnable>false</ScheduleDSTEnable>
        <Description>nothing</Description>
        <Actions>
            <Record>true</Record>
            <ActionRecordingMode>MOTION</ActionRecordingMode>
        </Actions>
    </ScheduleAction>
    <ScheduleAction>
        <id>1</id>
        <ScheduleActionStartTime>
            <DayOfWeek>Saturday</DayOfWeek>
            <TimeOfDay>00:00:00</TimeOfDay>
        </ScheduleActionStartTime>
        <ScheduleActionEndTime>
            <DayOfWeek>Saturday</DayOfWeek>
            <TimeOfDay>24:00:00</TimeOfDay>
        </ScheduleActionEndTime>
        <ScheduleDSTEnable>false</ScheduleDSTEnable>
        <Description>nothing</Description>
        <Actions>
            <Record>true</Record>
            <ActionRecordingMode>MOTION</ActionRecordingMode>
        </Actions>
    </ScheduleAction>
    <ScheduleAction>
        <id>1</id>
        <ScheduleActionStartTime>
            <DayOfWeek>Sunday</DayOfWeek>
            <TimeOfDay>00:00:00</TimeOfDay>
        </ScheduleActionStartTime>
        <ScheduleActionEndTime>
            <DayOfWeek>Sunday</DayOfWeek>
            <TimeOfDay>24:00:00</TimeOfDay>
        </ScheduleActionEndTime>
        <ScheduleDSTEnable>false</ScheduleDSTEnable>
        <Description>nothing</Description>
        <Actions>
            <Record>true</Record>
            <ActionRecordingMode>MOTION</ActionRecordingMode>
        </Actions>
    </ScheduleAction>
</ScheduleBlock>
"""

recording_schedule_enabling_xml = """\
<CustomExtension>
    <CustomExtensionName>www.std-cgi.com/RaCM/trackExt/ver10</CustomExtensionName>
    <enableSchedule>true</enableSchedule>
    <PreRecordTimeSeconds>5</PreRecordTimeSeconds>
    <PostRecordTimeSeconds>5</PostRecordTimeSeconds>
</CustomExtension>
"""

video_photo_ratio_xml = """\
<diskQuota version="2.0">
    <id>1</id>
    <type>ratio</type>
    <videoQuotaRatio>100</videoQuotaRatio>
    <pictureQuotaRatio>0</pictureQuotaRatio>
</diskQuota>
"""


# ==================================================================


class AuthType:
    BASIC = 1,
    DIGEST = 2,
    UNAUTHORISED = 3


def get_auth_type(cam_ip, password):
    request = requests.get(get_service_url(cam_ip, time_url), auth=HTTPBasicAuth(admin_user_name, password))
    if request.ok:
        return AuthType.BASIC

    request = requests.get(get_service_url(cam_ip, time_url), auth=HTTPDigestAuth(admin_user_name, password))
    if request.ok:
        return AuthType.DIGEST

    return AuthType.UNAUTHORISED


def get_auth(auth_type, name, password):
    if auth_type == AuthType.BASIC:
        return HTTPBasicAuth(name, password)
    elif auth_type == AuthType.DIGEST:
        return HTTPDigestAuth(name, password)
    else:
        return None


def get_service_url(cam_ip, relative_url):
    return 'http://' + cam_ip + relative_url


# =========================================== PASSWORD =================================================

def check_password(password):
    if len(password) >= 8:
        return True
    else:
        print('PASSWORD IS NOT SET, IT\'S TOO SHORT')
        return False


def set_password(auth_type, cam_ip, password, new_password):
    if check_password(new_password):
        request = ElementTree.fromstring(user_password_xml)

        pass_element = request.find('password')
        pass_element.text = new_password

        request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

        process_request(auth_type, cam_ip, password_url, password, request_data, 'Password set')


# =========================================== NTP =================================================


def set_ntp(auth_type, cam_ip, password):
    request = ElementTree.fromstring(ntp_server_xml)

    server_element = request.find('NTPServer')
    ip_element = server_element.find('ipAddress')
    ip_element.text = new_ntp

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    process_request(auth_type, cam_ip, ntp_url, password, request_data, 'NTP set')


# =========================================== IP & DNS =================================================


def set_ip_and_dns(auth_type, cam_ip, new_ip, password):
    if new_ip is not None:
        request = ElementTree.fromstring(ip_address_xml)

        new_ip_address = str(new_ip.ip)
        new_netmask = str(new_ip.netmask)
        new_gateway = str(next(new_ip.network.hosts()))

        ip_element = request.find('ipAddress')
        ip_element.text = new_ip_address

        net_mask_element = request.find('subnetMask')
        net_mask_element.text = new_netmask

        request = write_ip_to_xml(request, 'DefaultGateway', new_gateway)
        request = add_dns_to_xml(request)
        request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

        message = 'IP set to %s, netmask %s, gateway %s, dns1 %s, dns2 %s' % (new_ip_address, new_netmask, new_gateway, primary_dns, secondary_dns)

        process_request(auth_type, cam_ip, ip_url, password, request_data, message, 'Reboot Required')
    else:
        print("New IP is not given, IP won't be changed")
        set_dns(auth_type, cam_ip, password)


def set_dns(auth_type, cam_ip, password):
    request = requests.get(get_service_url(cam_ip, ip_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)
    ip_address_info = ElementTree.fromstring(answer_text)

    addressing_type = ip_address_info.find('addressingType')
    if addressing_type is not None and addressing_type.text == 'static':
        ip_address_info = add_dns_to_xml(ip_address_info)
        request_data = ElementTree.tostring(ip_address_info, encoding='utf8', method='xml')

        process_request(auth_type, cam_ip, ip_url, password, request_data, 'DNS servers set')
    else:
        print("IP address is not static (DHCP, APIPA), DNS won't be set")


def add_dns_to_xml(xml):
    xml = write_ip_to_xml(xml, 'PrimaryDNS', primary_dns)
    xml = write_ip_to_xml(xml, 'SecondaryDNS', secondary_dns)
    return xml


def write_ip_to_xml(xml, tag_name, ip_value):
    parent_element = xml.find(tag_name)
    ip_element = parent_element.find('ipAddress')
    ip_element.text = ip_value
    return xml


# =========================================== VIDEO =================================================


class VideoMode:
    def __init__(self, width, height, framerate):
        self.width = width
        self.height = height
        self.framerate = framerate


class VideoCapabilities:
    def __init__(self, width_list, height_list, framerate_list):
        self.width_list = width_list
        self.height_list = height_list
        self.framerate_list = framerate_list

    def is_mode_supported(self, videomode):
        return self.width_list.count(videomode.width) != 0 \
               and self.height_list.count(videomode.height) != 0 \
               and self.framerate_list.count(videomode.framerate) != 0


class VideoChannel:
    def __init__(self, stream_mode, channel_xml, stream_audio):
        self.stream_mode = stream_mode
        self.channel_xml = channel_xml
        self.stream_audio = stream_audio

    def get_video_element(self):
        video_element = ElementTree.fromstring(self.channel_xml)
        video_element = fill_video_parameters(video_element, self.stream_mode)
        return video_element


def set_video_streams(auth_type, cam_ip, password):
    framerate_multiplier = 100

    request = requests.get(get_service_url(cam_ip, video_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)
    channel_list = ElementTree.fromstring(answer_text)
    channels = channel_list.findall('StreamingChannel')

    h264_stream_mode = VideoMode(h264_stream_width, h264_stream_height, h264_stream_framerate * framerate_multiplier)
    mjpeg_stream_mode = VideoMode(mjpeg_stream_width, mjpeg_stream_height, mjpeg_stream_framerate * framerate_multiplier)
    is_mode_supported = True

    for channel in channels:
        channel_id = channel.find('id').text
        capabilities = get_capabilities(channel_id, auth_type, cam_ip, password)
        if channel_id[-1:] == '1':
            video_channel = VideoChannel(h264_stream_mode, video_h254_xml, record_audio)
        else:
            video_channel = VideoChannel(mjpeg_stream_mode, video_mjpeg_xml, False)

        if video_channel.stream_audio:
            audio_element = channel.find('Audio')
            if audio_element is not None:
                enabled_element = audio_element.find('enabled')
                enabled_element.text = 'true' if record_audio else 'false'

        if capabilities.is_mode_supported(video_channel.stream_mode):
            replace_subelement_with(channel, video_channel.get_video_element())
        else:
            is_mode_supported = False
            break

    if is_mode_supported:
        request_data = ElementTree.tostring(channel_list, encoding='utf8', method='xml')
        process_request(auth_type, cam_ip, video_url, password, request_data, 'Video streams set')
    else:
        print('VIDEO MODE IS NOT SUPPORTED BY CAMERA!')


def get_capabilities(channel_id, auth_type, cam_ip, password):
    request_url = video_capabilities_url.format(channel_id)
    request = requests.get(get_service_url(cam_ip, request_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)
    channel_capabilities = ElementTree.fromstring(answer_text)
    video_capabilities = channel_capabilities.find('Video')
    width_list = get_options_list(video_capabilities, 'videoResolutionWidth')
    height_list = get_options_list(video_capabilities, 'videoResolutionHeight')
    frame_rate_list = get_options_list(video_capabilities, 'maxFrameRate')

    return VideoCapabilities(width_list, height_list, frame_rate_list)


def get_options_list(element, tag):
    inner_element = element.find(tag)
    options_text = inner_element.attrib['opt']
    options = map(int, options_text.split(','))
    return options


def fill_video_parameters(element, videomode):
    width_element = element.find('videoResolutionWidth')
    height_element = element.find('videoResolutionHeight')
    frame_rate_element = element.find('maxFrameRate')
    width_element.text = str(videomode.width)
    height_element.text = str(videomode.height)
    frame_rate_element.text = str(videomode.framerate)
    return element


# =========================================== REBOOT =================================================


def reboot_cam(auth_type, cam_ip):
    request = requests.put(get_service_url(cam_ip, reboot_url), auth=get_auth(auth_type, admin_user_name, admin_new_password), data=[])
    answer_text = request.text

    print_answer_status('Reboot', answer_text, 'OK')


# =========================================== OSD =================================================

def set_osd(auth_type, cam_ip, password):
    process_request(auth_type, cam_ip, osd_url, password, osd_xml, 'OSD set')


# =========================================== IP BAN =================================================


def set_off_ip_ban_option(auth_type, cam_ip, password):
    if is_ip_ban_option_presented(auth_type, cam_ip, password):
        process_request(auth_type, cam_ip, ip_ban_option_url, password, ip_ban_option_xml, 'IP ban option unset')


def is_ip_ban_option_presented(auth_type, cam_ip, password):
    request = requests.get(get_service_url(cam_ip, ip_ban_option_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = request.text

    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    if answer_xml.tag == namespace + 'IllegalLoginLock':
        return True
    else:
        return False

# =========================================== CLOUD =================================================


def set_cloud_parameters(auth_type, cam_ip, password):
    if is_camera_supports_cloud(auth_type, cam_ip, password):
        process_request(auth_type, cam_ip, cloud_url, password, cloud_xml, 'Cloud disabling')


def is_camera_supports_cloud(auth_type, cam_ip, password):
    request = requests.get(get_service_url(cam_ip, network_capabilities_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)

    answer_xml = ElementTree.fromstring(answer_text)
    cloud_element = answer_xml.find('isSupportEZVIZ')

    if cloud_element is not None:
        if cloud_element.text == 'true':
            return True

    return False

# =========================================== TIME =================================================


def set_time(auth_type, cam_ip, password):
    if timezone_has_right_format(time_zone_gmt_offset):
        camera_timezone = convert_gmt_offset_to_internal_timezone(time_zone_gmt_offset)

        request = ElementTree.fromstring(time_zone_xml)

        timezone_element = request.find('timeZone')
        timezone_element.text = camera_timezone

        request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

        process_request(auth_type, cam_ip, time_url, password, request_data, 'Time set')

    else:
        print("Wrong timezone format")


def timezone_has_right_format(gmt_offset):
    format_matched = re.match('[+,-]?\d{1,2}:\d{2}:\d{2}', gmt_offset)
    return format_matched is not None


def convert_gmt_offset_to_internal_timezone(gmt_offset):
    prefix = 'CST'

    sign = gmt_offset[0]
    if sign == '-':
        suffix = '+' + gmt_offset[1:]
    elif sign == '+':
        suffix = '-' + gmt_offset[1:]
    else:
        suffix = '-' + gmt_offset

    return prefix + suffix


# =========================================== ACTIVATION =================================================


def is_activated(cam_ip):
    request = requests.get(get_service_url(cam_ip, activation_status_url))
    answer_text = request.text

    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    answer_status_element = answer_xml.find(namespace + 'Activated')

    if answer_status_element is not None:
        status = answer_status_element.text
        if status == 'false':
            return False

    return True


def set_activation(cam_ip):
    password = admin_old_password

    if not is_activated(cam_ip):
        private_key = RSA.generate(1024, e=65537)

        answer_text = send_public_key(cam_ip, private_key)

        random_key_text, random_key_is_valid = get_random_key_text(answer_text, private_key)

        if random_key_is_valid:
            pass_encrypted_encoded = encrypt_password(random_key_text, admin_new_password)
            process_activation_request(cam_ip, pass_encrypted_encoded)
            password = admin_new_password

        else:
            print("Activation: error")
    else:
        print("Activation: cam is already activated or activation is not supported")

    return password


def get_random_key_text(answer_text, private_key):
    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    random_key_element = answer_xml.find(namespace + 'key')

    if random_key_element is not None:
        random_key_encoded = base64.b64decode(random_key_element.text)
        random_key_bin = base64.b16decode(random_key_encoded.upper())
        random_key_text = private_key.decrypt(random_key_bin)[-32:]

        return random_key_text, True

    else:
        return '', False


def encrypt_password(random_key_text, password):
    random_key = base64.b16decode(random_key_text.upper())

    new_password_to_send = password
    for i in range(len(new_password_to_send), 16):
        new_password_to_send += chr(0)

    aes = AES.new(random_key)
    pass_encrypted = aes.encrypt(random_key_text[:16]) + aes.encrypt(new_password_to_send)
    pass_encrypted_encoded = base64.b64encode(base64.b16encode(pass_encrypted).lower())

    return pass_encrypted_encoded


def send_public_key(cam_ip, private_key):
    public_key = private_key.publickey()
    public_key_bin = bytearray.fromhex('{:0192x}'.format(public_key.n))
    public_key_str = base64.b16encode(public_key_bin).lower()
    public_key_base64_encoded = base64.b64encode(public_key_str)

    request_xml = ElementTree.fromstring(public_key_xml)
    key_element = request_xml.find('key')
    key_element.text = public_key_base64_encoded.decode()

    request_data = ElementTree.tostring(request_xml, encoding='utf8', method='xml')

    request_xml = requests.post(get_service_url(cam_ip, public_key_url), data=request_data)
    answer_text = request_xml.text

    return answer_text


def process_activation_request(cam_ip, pass_encrypted_encoded):
    request = ElementTree.fromstring(activation_password_xml)
    pass_element = request.find('password')
    pass_element.text = pass_encrypted_encoded.decode()

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    process_request(AuthType.UNAUTHORISED, cam_ip, activation_url, admin_old_password, request_data, 'Activation')


# ========================================= USER MANAGEMENT ===========================================================

class User:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.password = ""
        self.is_valid = False


def print_user_list(auth_type, cam_ip, admin_password):
    request = requests.get(get_service_url(cam_ip, users_url), auth=get_auth(auth_type, admin_user_name, admin_password))
    answer_text = request.text

    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    user_elements = answer_xml.findall(namespace + 'User')

    users = []
    for user_element in user_elements:
        username_element = user_element.find(namespace + 'userName')
        if username_element is not None:
            username = username_element.text
            users.append(username)

    print('Users: {}'.format(users))


def set_video_user(auth_type, cam_ip, admin_password):
    user = add_or_update_user(auth_type, cam_ip, admin_password, video_user_name, video_user_password)

    if user.is_valid:
        set_video_user_permissions(auth_type, cam_ip, admin_password, user)


def set_monitoring_user(auth_type, cam_ip, admin_password):
    add_or_update_user(auth_type, cam_ip, admin_password, monitoring_user_name, monitoring_user_password)


def add_or_update_user(auth_type, cam_ip, admin_password, user_name, user_password):
    user = find_user(auth_type, cam_ip, admin_password, user_name)

    if user.is_valid:
        print("User '{}' is presented".format(user_name))
        user.password = user_password
        set_user_password(auth_type, cam_ip, admin_password, user)
        return user
    else:
        add_user(auth_type, cam_ip, admin_password, user_name, user_password)
        return find_user(auth_type, cam_ip, admin_password, user_name)


def set_user_password(auth_type, cam_ip, admin_password, user):
    if check_password(user.password):
        user_element = ElementTree.fromstring(user_password_xml)

        user_id_element = user_element.find('id')
        user_id_element.text = user.id

        user_name_element = user_element.find('userName')
        user_name_element.text = user.name

        password_element = user_element.find('password')
        password_element.text = user.password

        request_text = ElementTree.tostring(user_element, encoding='utf8', method='xml')

        process_request(auth_type, cam_ip, users_url, admin_password, request_text, "'{}' user password updating".format(user.name))


def add_user(auth_type, cam_ip, admin_password, user_name, user_password):
    if check_password(video_user_password):
        user_element = ElementTree.fromstring(add_user_xml)

        user_name_element = user_element.find('userName')
        user_name_element.text = user_name

        password_element = user_element.find('password')
        password_element.text = user_password

        request_text = ElementTree.tostring(user_element, encoding='utf8', method='xml')
        answer = requests.post(get_service_url(cam_ip, users_url), auth=get_auth(auth_type, admin_user_name, admin_password), data=request_text)

        answer_text = answer.text
        print_answer_status("Adding user '{}'".format(user_name), answer_text, 'OK')
    else:
        print('USER ISN\'T ADDED')


def find_user(auth_type, cam_ip, admin_password, user_name):
    request = requests.get(get_service_url(cam_ip, users_url), auth=get_auth(auth_type, admin_user_name, admin_password))
    answer_text = request.text

    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    user_elements = answer_xml.findall(namespace + 'User')

    user = User()

    for user_element in user_elements:
        username_element = user_element.find(namespace + 'userName')

        if username_element is not None:
            username = username_element.text
            if username == user_name:
                user_id_element = user_element.find(namespace + 'id')
                if user_id_element is not None:
                    user.id = user_id_element.text
                    user.name = user_name
                    user.is_valid = True
                    break

    return user


def set_video_user_permissions(auth_type, cam_ip, admin_password, user):
    permissions_id = find_video_permissions_id(auth_type, cam_ip, admin_password, user)

    permissions = ElementTree.fromstring(video_user_permissions_xml)

    id_element = permissions.find('id')
    id_element.text = permissions_id

    user_id_element = permissions.find('userID')
    user_id_element.text = user.id

    remote_permissions_element = permissions.find('remotePermission')

    playback_permission_text = 'true' if allow_videouser_downloading_records else 'false'

    playback_element = remote_permissions_element.find('playBack')
    playback_element.text = playback_permission_text

    videochannel_list_element = remote_permissions_element.find('videoChannelPermissionList')
    videochannel_element = videochannel_list_element.find('videoChannelPermission')
    playback_channel_element = videochannel_element.find('playBack')
    playback_channel_element.text = playback_permission_text

    request_text = ElementTree.tostring(permissions, encoding='utf8', method='xml')

    process_request(auth_type, cam_ip, permissons_url + '/' + user.id, admin_password, request_text, 'Video user permissions')


def find_video_permissions_id(auth_type, cam_ip, admin_password, user):
    request = requests.get(get_service_url(cam_ip, permissons_url), auth=get_auth(auth_type, admin_user_name, admin_password))
    answer_text = request.text

    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    permissions_elements = answer_xml.findall(namespace + 'UserPermission')

    permissions_id = 0

    for permission_element in permissions_elements:
        user_id_element = permission_element.find(namespace + 'userID')

        if user_id_element is not None:
            user_id = user_id_element.text
            if user_id == user.id:
                permissions_id_element = permission_element.find(namespace + 'id')
                if permissions_id_element is not None:
                    permissions_id = permissions_id_element.text
                    break

    return permissions_id

# =========================================== AUTHORIZATION =================================================


def set_basic_auth_method(auth_type, cam_ip, password):
    print('Enabling Basic authorization', end = '')

    if auth_type != AuthType.BASIC:
        request = requests.get(get_service_url(cam_ip, security_capabilities_url), auth=get_auth(auth_type, admin_user_name, password))
        answer_text = clear_xml_from_namespaces(request.text)

        answer_xml = ElementTree.fromstring(answer_text)
        web_auth_types_capabilities_element = answer_xml.find('WebCertificateCap')

        if web_auth_types_capabilities_element is not None:
            auth_types = web_auth_types_capabilities_element.find('CertificateType').attrib['opt']

            if 'basic' in auth_types:
                enable_basic_auth(auth_type, cam_ip, password)
            else:
                print(': Basic authorization is not supported')
        else:
            print(': changing authorization is not supported')
    else:
        print(': authorization is already Basic')


def enable_basic_auth(auth_type, cam_ip, password):
    web_authorization_type_request = requests.get(get_service_url(cam_ip, web_authorization_type_url), auth=get_auth(auth_type, admin_user_name, password))
    web_authorization_type_text = clear_xml_from_namespaces(web_authorization_type_request.text)

    web_authorization_type_xml = ElementTree.fromstring(web_authorization_type_text)
    web_authorization_type_element = web_authorization_type_xml.find('CertificateType')
    web_authorization_type_element.text = 'digest/basic'

    request_text = ElementTree.tostring(web_authorization_type_xml, encoding='utf8', method='xml')
    process_request(auth_type, cam_ip, web_authorization_type_url, password, request_text, '')


# =========================================== DEVICE NAME =================================================


def set_device_name(auth_type, cam_ip, password, new_cam_ip):
    request = ElementTree.fromstring(device_info_xml)

    device_name_element = request.find('deviceName')
    device_name_element.text = choose_ip_for_information(cam_ip, new_cam_ip)

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    process_request(auth_type, cam_ip, device_info_url, password, request_data, 'Device name set')


# =========================================== EMAIL NOTIFICATIONS ADDRESSES =================================================


def set_email_notification_addresses(auth_type, cam_ip, password, new_cam_ip):
    request = ElementTree.fromstring(email_addresses_xml)

    sender_element = request.find('sender')
    sender_element = set_email(sender_element, sender_email)

    sender_name_element = sender_element.find('name')
    sender_name_element.text = sender_name_prefix + choose_ip_for_information(cam_ip, new_cam_ip)

    set_smtp(sender_element)

    request = fill_receivers_email(request)

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')
    process_request(auth_type, cam_ip, email_addresses_url, password, request_data, 'Email notification addresses set')


def fill_receivers_email(parent_element):
    receiver_list_element = parent_element.find('receiverList')
    receiver_elements = receiver_list_element.findall('receiver')
    emails = [notification_email1, notification_email2, notification_email3]
    for receiver_element in receiver_elements:
        email_id_element = receiver_element.find('id')
        email_id = int(email_id_element.text) - 1
        email = emails[email_id]

        name_element = receiver_element.find('name')
        name_element.text = email

        set_email(receiver_element, email)
    return parent_element


def set_email(parent_element, email_value):
    sender_email_element = parent_element.find('emailAddress')
    sender_email_element.text = email_value
    return parent_element


def set_smtp(parent_element):
    smtp_element = parent_element.find('smtp')
    server_element = smtp_element.find('hostName')
    server_element.text = smtp_server
    return parent_element


# =========================================== EVENT TRIGGERS =================================================


def set_no_beep_event_trigger(auth_type, cam_ip, password):
    process_request(auth_type, cam_ip, event_diskerror_trigger_url, password, no_beep_event_trigger_xml, 'No beep trigger for diskerror event set')


def set_email_event_triggers(auth_type, cam_ip, password):
    process_request(auth_type, cam_ip, event_diskfull_trigger_url, password, email_event_trigger_xml, 'Email trigger for diskfull event set')
    process_request(auth_type, cam_ip, event_diskerror_trigger_url, password, email_event_trigger_xml, 'Email trigger for diskerror event set')


def set_recording_by_motion_detector_trigger(auth_type, cam_ip, password):
    process_request(auth_type, cam_ip, event_motion_detector_trigger_url, password, recording_event_trigger_xml, 'Recording by motion detector trigger set')


# =========================================== MOTION DETECTOR =================================================


def set_motion_detector_parameters(auth_type, cam_ip, password):
    process_request(auth_type, cam_ip, motion_detector_parameters_url, password, motion_detector_parameters_xml, 'Motion detector parameters set')


# =========================================== RECORDING SCHEDULE =================================================


def set_recording_schedule(auth_type, cam_ip, password):
    request = requests.get(get_service_url(cam_ip, recording_video_schedule_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)
    track_element = ElementTree.fromstring(answer_text)
    track_element = replace_subelement_body_with_text(track_element, 'TrackSchedule', recording_schedule_time_xml)
    track_element = replace_subelement_body_with_text(track_element, 'CustomExtensionList', recording_schedule_enabling_xml)

    loop_enable_element = track_element.find('LoopEnable')
    loop_enable_element.text = "true"

    request_data = ElementTree.tostring(track_element, encoding='utf8', method='xml')
    process_request(auth_type, cam_ip, recording_video_schedule_url, password, request_data, 'Recording schedule set')


# ======================================= CAPTURING PHOTOS =================================================


def set_photo_capturing_parameters(auth_type, cam_ip, password):
    set_photo_schedule(auth_type, cam_ip, password)
    set_shapshot_settings(auth_type, cam_ip, password)


def set_photo_schedule(auth_type, cam_ip, password):
    request = requests.get(get_service_url(cam_ip, recording_photo_schedule_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)
    track_element = ElementTree.fromstring(answer_text)

    schedule_element = ElementTree.fromstring(recording_schedule_time_xml)
    actions = schedule_element.findall('ScheduleAction')

    for action in actions:
        recording_mode = action.find('Actions').find('ActionRecordingMode')
        recording_mode.text = 'CMR'

    recording_schedule_enabling_element = ElementTree.fromstring(recording_schedule_enabling_xml)

    pre_record_time_element = recording_schedule_enabling_element.find('PreRecordTimeSeconds')
    pre_record_time_element.text = '0'

    post_record_time_element = recording_schedule_enabling_element.find('PostRecordTimeSeconds')
    post_record_time_element.text = '0'

    track_element = replace_subelement_body_with(track_element, 'TrackSchedule', schedule_element)
    track_element = replace_subelement_body_with(track_element, 'CustomExtensionList', recording_schedule_enabling_element)

    loop_enable_element = track_element.find('LoopEnable')
    loop_enable_element.text = "false"

    request_data = ElementTree.tostring(track_element, encoding='utf8', method='xml')
    process_request(auth_type, cam_ip, recording_photo_schedule_url, password, request_data, 'Photo capture schedule set')


def set_shapshot_settings(auth_type, cam_ip, password):
    request = requests.get(get_service_url(cam_ip, shapshot_channel_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)
    shapshot_channel_element = ElementTree.fromstring(answer_text)

    timing_capture_element = shapshot_channel_element.find('timingCapture')
    timing_capture_element.find('enabled').text = 'true'

    compress_element = timing_capture_element.find('compress')
    compress_element.find('quality').text = '80'
    compress_element.find('captureInterval').text = str(photo_capture_interval_minutes * 60000)
    compress_element.find('captureNumber').text = '0'

    request_data = ElementTree.tostring(shapshot_channel_element, encoding='utf8', method='xml')
    process_request(auth_type, cam_ip, shapshot_channel_url, password, request_data, 'Photo capture enabling')


# =========================================== STORAGE =================================================

class StorageStatus:
    OK = 'ok'
    UNFORMATTED = 'unformatted'
    FORMATTING = 'formatting'
    NOT_FOUND = 'not found'
    UNKNOWN = 'unknown'


class FormattingStatus:
    FORMATTING = 0,
    NOT_FORMATTING = 1,
    ERROR = 2


def set_video_photo_ratio(auth_type, cam_ip, password):
    ratio_elements = ElementTree.fromstring(video_photo_ratio_xml)
    ratio_elements.find('videoQuotaRatio').text = str(video_ratio_percents)
    ratio_elements.find('pictureQuotaRatio').text = str(100-video_ratio_percents)

    request_data = ElementTree.tostring(ratio_elements, encoding='utf8', method='xml')
    process_request(auth_type, cam_ip, video_photo_ratio_url, password, request_data, 'Video-photo ratio set')


def format_storage(auth_type, cam_ip, password):
    print("Format storage")
    authenticator = get_auth(auth_type, admin_user_name, password)
    storage_status = get_storage_status(authenticator, cam_ip)
    print_storage_status(storage_status)

    if storage_status == StorageStatus.NOT_FOUND:
        print("THERE'S NO STORAGE FOR FORMATTING!")
        return

    if storage_status == StorageStatus.OK:
        print("Storage is already formatted{}".format(": reformatting" if refomat_sd_if_it_is_ok else ""))

    if storage_status != StorageStatus.OK or refomat_sd_if_it_is_ok:
        do_format_storage(authenticator, cam_ip)


def is_storage_presented(authenticator, cam_ip):
    return get_storage_status(authenticator, cam_ip) != StorageStatus.NOT_FOUND


def get_storage_status(authenticator, cam_ip):
    storages_list = requests.get(get_service_url(cam_ip, storages_status_url), auth=authenticator)
    storages_list_text = clear_xml_from_namespaces(storages_list.text)

    storages_list_element = ElementTree.fromstring(storages_list_text)
    hdd_element = storages_list_element.find('hdd')

    if hdd_element is None:
        return StorageStatus.NOT_FOUND
    else:
        status_element = hdd_element.find('status')

        status_table = {
            'ok': StorageStatus.OK,
            'unformatted': StorageStatus.UNFORMATTED,
            'formating': StorageStatus.FORMATTING
        }

        return status_table.get(status_element.text, StorageStatus.UNKNOWN)


def print_storage_status(status_text):
    print('Storage status: {}'.format(status_text))


def do_format_storage(authenticator, cam_ip):
    # unformatted
    # formatting 0%
    # ...
    # formatting 88%
    # ok
    # not found
    # ... 15 seconds
    # ok

    start_formatting(authenticator, cam_ip)
    time.sleep(1)

    display_formatting_process(authenticator, cam_ip)
    time.sleep(DELAY_AFTER_FORMATTING_SECONDS)

    percentage = get_formatting_percentage(authenticator, cam_ip)
    storage_status = get_storage_status(authenticator, cam_ip)

    if storage_status == StorageStatus.OK:
        print('\rFormatting: {}%         Status: {}                 '.format(percentage, storage_status))
        print('Formatting: success')
    else:
        print('')
        raise RuntimeError('ERROR during formatting, storage status: {}'.format(storage_status))


def start_formatting(authenticator, cam_ip):
    try:
        requests.put(get_service_url(cam_ip, storage_format_url), auth=authenticator, timeout=1)
    except requests.exceptions.RequestException:
        pass


def display_formatting_process(authenticator, cam_ip):
    prev_percentage = 0

    while True:
        percentage = get_formatting_percentage(authenticator, cam_ip)
        storage_status = get_storage_status(authenticator, cam_ip)

        if storage_status != StorageStatus.FORMATTING:
            break

        if percentage != prev_percentage:
            stdout.write('\rFormatting: {}%         Status: {}                 '.format(percentage, storage_status))
            stdout.flush()
        prev_percentage = percentage

        time.sleep(1)


def get_formatting_percentage(authenticator, cam_ip):
    percents_answer = requests.get(get_service_url(cam_ip, storage_format_percents_url), auth=authenticator)

    if percents_answer:
        percents_answer_text = clear_xml_from_namespaces(percents_answer.text)
        percents_element = ElementTree.fromstring(percents_answer_text)

        percentage = percents_element.find('percent')
        return percentage.text
    else:
        return 0


# =========================================== VARIOUS STUFF =================================================

def print_device_info(auth_type, cam_ip, password):
    request = requests.get(get_service_url(cam_ip, device_info_url), auth=get_auth(auth_type, admin_user_name, password))
    answer_text = clear_xml_from_namespaces(request.text)
    device_info = ElementTree.fromstring(answer_text.encode('utf-8'))

    model = device_info.find('model').text
    mac = device_info.find('macAddress').text
    fw_version = device_info.find('firmwareVersion').text

    print('MAC: {}, Model: {}, Firmware {}'.format(mac.upper(), model, fw_version))


def choose_ip_for_information(current_ip, new_cam_ip):
    if new_cam_ip is not None:
        return str(new_cam_ip.ip)
    else:
        return current_ip


def parse_ip(ip_with_mask):
    if ip_with_mask.count('/') == 0:
        ip_with_mask += '/24'

    addr = ipaddress.ip_interface(unicode(ip_with_mask))
    return addr


def process_request(auth_type, cam_ip, request_url, password, request_data, operation, expected_status_text='OK'):
    request = requests.put(get_service_url(cam_ip, request_url), auth=get_auth(auth_type, admin_user_name, password), data=request_data)
    answer_text = request.text

    print_answer_status(operation, answer_text, expected_status_text)


def print_answer_status(operation_text, answer_text, status_text):
    default_status_text = 'OK'
    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    answer_status_element = answer_xml.find(namespace + 'statusString')

    result_status = False
    if answer_status_element is not None:
        status = answer_status_element.text
        if (status == status_text) or (status == default_status_text):
            result_status = True

    if result_status:
        print(operation_text + ': success')
    else:
        error_answer = parse_error_xml(answer_text)
        error_message = operation_text + ' error, answer is:\n' + error_answer
        print(answer_text)
        raise RuntimeError(error_message)


def parse_error_xml(answer_text):
    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    answer_status_element = answer_xml.find(namespace + 'statusString')
    answer_substatus_element = answer_xml.find(namespace + 'subStatusCode')

    if answer_status_element is not None and answer_substatus_element is not None:
        status = answer_status_element.text
        substatus = answer_substatus_element.text

        message = "%s: %s" % (status, substatus)

    else:
        message = answer_text

    return message


def get_namespace(element):
    m = re.match("\{.*\}", element.tag)
    return m.group(0) if m else ''


def clear_xml_from_namespaces(xml_text):
    return re.sub(' xmlns="[^"]+"', '', xml_text, count=0)


def replace_subelement_with(parent, new_subelement):
    subelement_tag = new_subelement.tag
    subelement = parent.find(subelement_tag)
    parent.remove(subelement)

    parent.append(new_subelement)
    return parent


def replace_subelement_body_with_text(parent, subelement_tag, new_body_text):
    new_body = ElementTree.fromstring(new_body_text)
    return replace_subelement_body_with(parent, subelement_tag, new_body)


def replace_subelement_body_with(parent, subelement_tag, new_body):
    subelement = parent.find(subelement_tag)
    subelement.clear()
    subelement.append(new_body)
    return parent


def main():
    if len(sys.argv) > 1:
        current_cam_ip = sys.argv[1]
        if len(sys.argv) == 3:
            new_cam_ip = parse_ip(sys.argv[2])
        else:
            new_cam_ip = None

        print('Processing cam %s:' % current_cam_ip)

        try:
            current_password = set_activation(current_cam_ip)
            auth_type = get_auth_type(current_cam_ip, current_password)
            if auth_type == AuthType.UNAUTHORISED:
                raise RuntimeError("Unauthorised! Check login and password")

            print_device_info(auth_type, current_cam_ip, current_password)
            set_cam_options(auth_type, current_cam_ip, current_password, new_cam_ip)

        except RuntimeError as e:
            print(str(e))
        
        except requests.exceptions.ConnectionError as e:
            print('Connection error: %s' % str(e))

        except KeyboardInterrupt:
            pass
    else:
        print("USAGE:")
        print("    {} OLD_IP [NEW_IP/MASK]".format(sys.argv[0]))
        print("Example:")
        print("    {} 10.145.17.206 10.226.47.130/25".format(sys.argv[0]))

    print("")


if __name__ == "__main__":
    main()

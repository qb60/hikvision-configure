#! /usr/bin/python

# ======================= HIKVISION CAM SETUP ======================
# MJPEG stream: /mjpeg/ch1/sub/av_stream
# H264  stream: /h264/ch1/main/av_stream

import re
import requests
import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from xml.etree import ElementTree

cam_ips = [
    # (      OLD     ,        NEW      )
    ('192.168.1.64', '10.0.0.10'),
]

user_name = 'admin'
old_password = '12345'

new_password = 'qwerty123'
new_gateway = '10.0.0.1'
new_ntp = '10.0.0.1'

h264_stream_width = 1280
h264_stream_height = 720
h264_stream_framerate = 10

mjpeg_stream_width = 640
mjpeg_stream_height = 480
mjpeg_stream_framerate = 6

# =========================== REQUESTS =============================

password_set_request = """\
<?xml version="1.0" encoding="UTF-8"?>
<User>
    <id>1</id>
    <userName>admin</userName>
    <userLevel>Administrator</userLevel>
    <password>pass</password>
</User>
"""

time_set_request = """\
<?xml version="1.0" encoding="UTF-8"?>
<Time>
    <timeMode>NTP</timeMode>
    <timeZone>CST-5:00:00</timeZone>
</Time>
"""

ntp_set_request = """\
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

ip_set_request = """\
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

osd_set_request = """\
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

video_set_request = """\
<?xml version="1.0" encoding="UTF-8"?>
<StreamingChannelList>
    <StreamingChannel>
        <id>1</id>
        <channelName>Camera 01</channelName>
        <enabled>true</enabled>
        <Transport>
            <maxPacketSize>1000</maxPacketSize>
            <ControlProtocolList>
                <ControlProtocol>
                    <streamingTransport>RTSP</streamingTransport>
                </ControlProtocol>
                <ControlProtocol>
                    <streamingTransport>HTTP</streamingTransport>
                </ControlProtocol>
                <ControlProtocol>
                    <streamingTransport>SHTTP</streamingTransport>
                </ControlProtocol>
            </ControlProtocolList>
            <Unicast>
                <enabled>true</enabled>
                <rtpTransportType>RTP/TCP</rtpTransportType>
            </Unicast>
            <Multicast>
                <enabled>true</enabled>
                <destIPAddress>0.0.0.0</destIPAddress>
                <videoDestPortNo>8600</videoDestPortNo>
                <audioDestPortNo>8600</audioDestPortNo>
            </Multicast>
            <Security>
                <enabled>true</enabled>
            </Security>
        </Transport>
        <Video>
            <enabled>true</enabled>
            <videoInputChannelID>1</videoInputChannelID>
            <videoCodecType>H.264</videoCodecType>
            <videoScanType>progressive</videoScanType>
            <videoResolutionWidth>1280</videoResolutionWidth>
            <videoResolutionHeight>720</videoResolutionHeight>
            <videoQualityControlType>VBR</videoQualityControlType>
            <constantBitRate>1024</constantBitRate>
            <fixedQuality>60</fixedQuality>
            <vbrUpperCap>1024</vbrUpperCap>
            <vbrLowerCap>32</vbrLowerCap>
            <maxFrameRate>1000</maxFrameRate>
            <keyFrameInterval>5000</keyFrameInterval>
            <snapShotImageType>JPEG</snapShotImageType>
            <H264Profile>Main</H264Profile>
            <GovLength>50</GovLength>
            <PacketType>PS</PacketType>
            <PacketType>RTP</PacketType>
        </Video>
        <Audio>
            <enabled>false</enabled>
            <audioInputChannelID>1</audioInputChannelID>
            <audioCompressionType>G.711ulaw</audioCompressionType>
        </Audio>
    </StreamingChannel>
    <StreamingChannel>
        <id>2</id>
        <channelName>Camera 01</channelName>
        <enabled>true</enabled>
        <Transport>
            <maxPacketSize>1000</maxPacketSize>
            <ControlProtocolList>
                <ControlProtocol>
                    <streamingTransport>RTSP</streamingTransport>
                </ControlProtocol>
                <ControlProtocol>
                    <streamingTransport>HTTP</streamingTransport>
                </ControlProtocol>
                <ControlProtocol>
                    <streamingTransport>SHTTP</streamingTransport>
                </ControlProtocol>
            </ControlProtocolList>
            <Unicast>
                <enabled>true</enabled>
                <rtpTransportType>RTP/TCP</rtpTransportType>
            </Unicast>
            <Multicast>
                <enabled>true</enabled>
                <destIPAddress>0.0.0.0</destIPAddress>
                <videoDestPortNo>8600</videoDestPortNo>
                <audioDestPortNo>8600</audioDestPortNo>
            </Multicast>
            <Security>
                <enabled>true</enabled>
            </Security>
        </Transport>
        <Video>
            <enabled>true</enabled>
            <videoInputChannelID>1</videoInputChannelID>
            <videoCodecType>MJPEG</videoCodecType>
            <videoScanType>progressive</videoScanType>
            <videoResolutionWidth>640</videoResolutionWidth>
            <videoResolutionHeight>480</videoResolutionHeight>
            <videoQualityControlType>VBR</videoQualityControlType>
            <constantBitRate>256</constantBitRate>
            <fixedQuality>60</fixedQuality>
            <vbrUpperCap>256</vbrUpperCap>
            <vbrLowerCap>32</vbrLowerCap>
            <maxFrameRate>600</maxFrameRate>
            <keyFrameInterval>8333</keyFrameInterval>
            <snapShotImageType>JPEG</snapShotImageType>
            <H264Profile>Main</H264Profile>
            <GovLength>50</GovLength>
            <PacketType>PS</PacketType>
            <PacketType>RTP</PacketType>
        </Video>
        <Audio>
            <enabled>false</enabled>
            <audioInputChannelID>1</audioInputChannelID>
            <audioCompressionType>G.711ulaw</audioCompressionType>
        </Audio>
    </StreamingChannel>
</StreamingChannelList>
"""

illegal_login_set_request = """\ 
<?xml version="1.0" encoding="UTF-8"?>
<IllegalLoginLock>
    <enabled>false</enabled>
</IllegalLoginLock>
"""

activation_set_request = """\
<?xml version="1.0" encoding="UTF-8"?>
<ActivateInfo>
    <password>pass</password>
</ActivateInfo>
"""

public_key_set_request = """\
<PublicKey>
    <key>publickey</key>
</PublicKey>
"""

# ============================= URLS ===============================

password_url = '/ISAPI/Security/users/1'
time_url = '/ISAPI/System/time'
ntp_url = '/ISAPI/System/time/ntpServers'
osd_url = '/ISAPI/System/Video/inputs/channels/1/overlays'
video_url = '/ISAPI/Streaming/channels'
ip_url = '/ISAPI/System/Network/interfaces/1/ipAddress'
reboot_url = '/ISAPI/System/reboot'
illegal_login_url = "/ISAPI/Security/illegalLoginLock"

activation_status_url = "/SDK/activateStatus"
public_key_url = "/ISAPI/Security/challenge"
activation_url = "/ISAPI/System/activate"

# ==================================================================


def get_service_url(cam_ip, relative_url):
    return 'http://' + cam_ip + relative_url


def set_password(cam_ip, password):
    request = ElementTree.fromstring(password_set_request)

    pass_element = request.find('password')
    pass_element.text = new_password

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    process_request(cam_ip, password_url, password, request_data, 'Password set')


def set_ntp(cam_ip, password):
    request = ElementTree.fromstring(ntp_set_request)

    server_element = request.find('NTPServer')
    ip_element = server_element.find('ipAddress')
    ip_element.text = new_ntp

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    process_request(cam_ip, ntp_url, password, request_data, 'NTP set')


def set_ip(cam_ip, new_ip, password):
    request = ElementTree.fromstring(ip_set_request)

    ip_element = request.find('ipAddress')
    ip_element.text = new_ip

    gateway_element = request.find('DefaultGateway')
    gateway_ip_element = gateway_element.find('ipAddress')
    gateway_ip_element.text = new_gateway

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    message = 'IP set to %s, gateway %s' % (new_ip, new_gateway)

    process_request(cam_ip, ip_url, password, request_data, message, 'Reboot Required')


def set_video(cam_ip, password):
    request = ElementTree.fromstring(video_set_request)

    channels = request.findall('StreamingChannel')
    for channel_element in channels:
        id_text = channel_element.find('id').text
        video_element = channel_element.find('Video')
        width_element = video_element.find('videoResolutionWidth')
        height_element = video_element.find('videoResolutionHeight')
        frame_rate_element = video_element.find('maxFrameRate')

        if id_text == '1':
            width_element.text = str(h264_stream_width)
            height_element.text = str(h264_stream_height)
            frame_rate_element.text = str(h264_stream_framerate * 100)

        if id_text == '2':
            width_element.text = str(mjpeg_stream_width)
            height_element.text = str(mjpeg_stream_height)
            frame_rate_element.text = str(mjpeg_stream_framerate * 100)

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    process_request(cam_ip, video_url, password, request_data, 'Video streams set')


def reboot_cam(cam_ip):
    request = requests.put(get_service_url(cam_ip, reboot_url), auth=(user_name, new_password), data=[])
    answer_text = request.text

    print_answer_status('Reboot', answer_text, 'OK')


def set_time(cam_ip, password):
    process_request(cam_ip, time_url, password, time_set_request, 'Time set')


def set_osd(cam_ip, password):
    process_request(cam_ip, osd_url, password, osd_set_request, 'OSD set')


def set_illegal_password(cam_ip, password):
    if is_illegal_password_presented(cam_ip, password):
        process_request(cam_ip, illegal_login_url, password, illegal_login_set_request, 'Illegal password check unset')


def is_illegal_password_presented(cam_ip, password):
    request = requests.get(get_service_url(cam_ip, illegal_login_url), auth=(user_name, password))
    answer_text = request.text

    answer_xml = ElementTree.fromstring(answer_text)
    namespace = get_namespace(answer_xml)

    if answer_xml.tag == namespace + 'IllegalLoginLock':
        return True
    else:
        return False

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
    password = old_password

    if not is_activated(cam_ip):
        private_key = RSA.generate(1024, e=65537)

        answer_text = send_public_key(cam_ip, private_key)

        random_key_text, random_key_is_valid = get_random_key_text(answer_text, private_key)

        if random_key_is_valid:
            pass_encrypted_encoded = encrypt_password(random_key_text, new_password)
            process_activation_request(cam_ip, pass_encrypted_encoded)
            password = new_password

        else:
            print "Activation: error"
    else:
        print "Activation: cam is already activated or activation is not supported"

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

    request_xml = ElementTree.fromstring(public_key_set_request)
    key_element = request_xml.find('key')
    key_element.text = public_key_base64_encoded

    request_data = ElementTree.tostring(request_xml, encoding='utf8', method='xml')

    request_xml = requests.post(get_service_url(cam_ip, public_key_url), auth=(user_name, old_password), data=request_data)
    answer_text = request_xml.text

    return answer_text


def process_activation_request(cam_ip, pass_encrypted_encoded):
    request = ElementTree.fromstring(activation_set_request)
    pass_element = request.find('password')
    pass_element.text = pass_encrypted_encoded

    request_data = ElementTree.tostring(request, encoding='utf8', method='xml')

    process_request(cam_ip, activation_url, old_password, request_data, 'Activation')


# ================================================================================================================


def process_request(cam_ip, request_url, password, request_data, operation, expected_status_text='OK'):
    request = requests.put(get_service_url(cam_ip, request_url), auth=(user_name, password), data=request_data)
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
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''


try:
    for current_cam_pair_ip in cam_ips:
        (current_cam_ip, new_cam_ip) = current_cam_pair_ip

        print('Processing cam %s:' % current_cam_ip)

        try:
            current_password = set_activation(current_cam_ip)
            set_time(current_cam_ip, current_password)
            set_ntp(current_cam_ip, current_password)
            set_osd(current_cam_ip, current_password)
            set_illegal_password(current_cam_ip, current_password)
            set_video(current_cam_ip, current_password)
            set_ip(current_cam_ip, new_cam_ip, current_password)
            set_password(current_cam_ip, current_password)
            reboot_cam(current_cam_ip)

        except RuntimeError as e:
            print(e.message)

        print

except requests.exceptions.ConnectionError as e:
    print('Connection error: %s' % e.message)

except KeyboardInterrupt:
    pass

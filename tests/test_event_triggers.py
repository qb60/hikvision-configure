import unittest

from cam_config import mute_possible_events

xml_event_triggers_text = '''<?xml version="1.0" encoding="UTF-8"?>
<EventNotification version="2.0">
    <EventTriggerList version="2.0">
        <EventTrigger>
            <id>VMD-1</id>
            <eventType>VMD</eventType>
            <eventDescription>VMD Event trigger Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
                <EventTriggerNotification>
                    <id>record-1</id>
                    <notificationMethod>record</notificationMethod>
                    <videoInputID>1</videoInputID>
                    <notificationRecurrence>beginning</notificationRecurrence>
                </EventTriggerNotification>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>tamper-1</id>
            <eventType>tamperdetection</eventType>
            <eventDescription>shelteralarm Event trigger Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>diskfull</id>
            <eventType>diskfull</eventType>
            <eventDescription>exception Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
                <EventTriggerNotification>
                    <id>email</id>
                    <notificationMethod>email</notificationMethod>
                    <notificationRecurrence>beginning</notificationRecurrence>
                </EventTriggerNotification>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>diskerror</id>
            <eventType>diskerror</eventType>
            <eventDescription>exception Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
                <EventTriggerNotification>
                    <id>email</id>
                    <notificationMethod>email</notificationMethod>
                    <notificationRecurrence>beginning</notificationRecurrence>
                </EventTriggerNotification>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>nicbroken</id>
            <eventType>nicbroken</eventType>
            <eventDescription>exception Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>ipconflict</id>
            <eventType>ipconflict</eventType>
            <eventDescription>exception Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>illaccess</id>
            <eventType>illaccess</eventType>
            <eventDescription>exception Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>linedetection-1</id>
            <eventType>linedetection</eventType>
            <eventDescription>Linedetection Event trigger Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>fielddetection-1</id>
            <eventType>fielddetection</eventType>
            <eventDescription>fielddetection Event trigger Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>videomismatch</id>
            <eventType>videomismatch</eventType>
            <eventDescription>exception Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
                <EventTriggerNotification>
                    <id>beep</id>
                    <notificationMethod>beep</notificationMethod>
                    <notificationRecurrence>beginning</notificationRecurrence>
                </EventTriggerNotification>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>badvideo</id>
            <eventType>badvideo</eventType>
            <eventDescription>exception Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>PIR</id>
            <eventType>PIR</eventType>
            <eventDescription>PIR Event trigger Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
                <EventTriggerNotification>
                    <id>record-1</id>
                    <notificationMethod>record</notificationMethod>
                    <videoInputID>1</videoInputID>
                    <notificationRecurrence>beginning</notificationRecurrence>
                </EventTriggerNotification>
                <EventTriggerNotification>
                    <id>beep</id>
                    <notificationMethod>beep</notificationMethod>
                    <notificationRecurrence>beginning</notificationRecurrence>
                </EventTriggerNotification>
                <EventTriggerNotification>
                    <id>center</id>
                    <notificationMethod>center</notificationMethod>
                    <notificationRecurrence>beginning</notificationRecurrence>
                </EventTriggerNotification>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>facedetection-1</id>
            <eventType>facedetection</eventType>
            <eventDescription>facedetection Event trigger Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
        <EventTrigger>
            <id>storageDetection-1</id>
            <eventType>storageDetection</eventType>
            <eventDescription>storageDetection Event trigger Information</eventDescription>
            <videoInputChannelID>1</videoInputChannelID>
            <dynVideoInputChannelID>1</dynVideoInputChannelID>
            <EventTriggerNotificationList>
            </EventTriggerNotificationList>
        </EventTrigger>
    </EventTriggerList>
</EventNotification>
'''


class TestEventTriggers(unittest.TestCase):
    def test_mute_all_possible_events(self):
        events = mute_possible_events(xml_event_triggers_text)
        expected_events = [
            'VMD-1',
            'tamper-1',
            'diskfull',
            'diskerror',
            'nicbroken',
            'ipconflict',
            'illaccess',
            'linedetection-1',
            'fielddetection-1',
            'videomismatch',
            'badvideo',
            'PIR',
            'facedetection-1',
            'storageDetection-1'
        ]

        self.assertEqual(expected_events, events)


if __name__ == '__main__':
    unittest.main()

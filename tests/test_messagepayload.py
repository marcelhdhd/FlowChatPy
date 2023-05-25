import unittest
from datetime import datetime
import json

from net import messagepayload


class TestMessagePayload(unittest.TestCase):

    def test_usermessage(self):
        system_date = datetime.now().strftime("[%H:%M:%S] ")

        user_payload = messagepayload.UserMessage()
        user_payload.message = "unittest FlowChatMessage"
        user_payload.date = system_date
        user_payload.ip = "192.168.42.42"
        user_payload.name = "test U Name"

        test_json = json.loads(user_payload.toJson())
        test_json_type = test_json["type"]
        test_json_message = test_json["message"]
        test_json_date = test_json["date"]
        test_json_ip = test_json["ip"]
        test_json_name = test_json["name"]

        self.assertEqual(test_json_type, "userMessage", "Should be of type \"userMessage\"")
        self.assertEqual(test_json_message, "unittest FlowChatMessage", "Should be \"unittest FlowChatMessage\"")
        self.assertEqual(test_json_date, system_date, "Should be " + system_date)
        self.assertEqual(test_json_ip, "192.168.42.42", "Should be 192.168.42.42")
        self.assertEqual(test_json_name, "test U Name", "Should be \"test U Name\"")

    def test_custommessage(self):
        custom_payload = messagepayload.CustomMessage()
        custom_payload.message = "unittest custom FlowChatMessage"

        test_json = json.loads(custom_payload.toJson())
        test_json_type = test_json["type"]
        test_json_message = test_json["message"]

        self.assertEqual(test_json_type, "customMessage", "Should be of type \"customMessage\"")
        self.assertEqual(test_json_message, "unittest custom FlowChatMessage", "Should be \"unittest custom "
                                                                               "FlowChatMessage\"")

    def test_command(self):
        system_date = datetime.now().strftime("[%H:%M:%S] ")

        command_payload = messagepayload.Command()
        command_payload.command = "unittest_check"
        command_payload.date = system_date
        command_payload.ip = "192.168.42.42"

        test_json = json.loads(command_payload.toJson())
        test_json_type = test_json["type"]
        test_json_command = test_json["command"]
        test_json_date = test_json["date"]
        test_json_ip = test_json["ip"]

        self.assertEqual(test_json_type, "command", "Should be of type \"command\"")
        self.assertEqual(test_json_command, "unittest_check", "Should be \"unittest_check\"")
        self.assertEqual(test_json_date, system_date, "Should be " + system_date)
        self.assertEqual(test_json_ip, "192.168.42.42", "Should be 192.168.42.42")


if __name__ == '__main__':
    unittest.main()

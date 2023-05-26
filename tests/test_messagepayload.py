import unittest
from datetime import datetime
import json

import net.messagepayload
from net import messagepayload

messages = ["python unittest", "o92837rzfcmqo9rzxcLMCL qhwidf7fd§NEC / ", "CCWVz54g(fXMhdgU-=3#/Xe(Vr[%}?",
                   "cSE?U:@%DXzht:G9VH!K8x8wGVi*S+", "#{/[PD&BT*Epr]4J7VwjB@$Q.U?.dX", "!q4{MzKuWta,C2wPT{j8:imA}b6B.$",
                   "LH&}t_,W@Pg{P*bQq,;U&GEP7UU*];", "]GJ,,2xaA%4y8d?+8amVrQ=FV,=X*}"]
dates = ["[14:34:30]", "[04:54:10]", "[18:25:00]"]
ips = ["192.168.1.1", "10.10.10.10", "0.0.0.0"]
names = ["marcelhdhd", "julian", "jonas", "max", "pascal"]

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

    def test_json_to_messagepayload_usermessage(self):
        jsons = []
        for message in messages:
            for date in dates:
                for ip in ips:
                    for name in names:
                        jsons.append("{\"type\": \"userMessage\", \"message\": \"" + message + "\", \"date\": \""
                                     + date + " \", \"ip\": \"" + ip + "\", \"name\": \"" + name + "\"}")
        for jsonn in jsons:
            self.assertTrue(isinstance(net.messagepayload.Incoming(jsonn).json_to_messagepayload(), net.messagepayload.UserMessage))
            self.assertFalse(isinstance(net.messagepayload.Incoming(jsonn).json_to_messagepayload(),
                                        (net.messagepayload.CustomMessage, net.messagepayload.Command)))

    def test_json_to_messagepayload_custommessage(self):
        jsons = []
        for message in messages:
            jsons.append("{\"type\": \"customMessage\", \"message\": \"" + message + "\"}")
        for jsonn in jsons:
            self.assertTrue(isinstance(net.messagepayload.Incoming(jsonn).json_to_messagepayload(), net.messagepayload.CustomMessage))
            self.assertFalse(isinstance(net.messagepayload.Incoming(jsonn).json_to_messagepayload(),
                                        (net.messagepayload.UserMessage, net.messagepayload.Command)))

    def test_json_to_messagepayload_command(self):
        jsons = []
        for command in messages:
            for date in dates:
                for ip in ips:
                    jsons.append("{\"type\": \"command\", \"command\": \"" + command + "\", \"date\": \""
                                 + date + " \", \"ip\": \"" + ip + "\"}")
        for jsonn in jsons:
            self.assertTrue(isinstance(net.messagepayload.Incoming(jsonn).json_to_messagepayload(), net.messagepayload.Command))
            self.assertFalse(isinstance(net.messagepayload.Incoming(jsonn).json_to_messagepayload(),
                                        (net.messagepayload.UserMessage, net.messagepayload.CustomMessage)))

    def test_json_to_messagepayload_typeerror(self):
        jsonn = "{\"type\": \"illegal\"}"
        illegal = net.messagepayload.Incoming(jsonn)
        self.assertRaises(TypeError, illegal.json_to_messagepayload)

if __name__ == '__main__':
    unittest.main()

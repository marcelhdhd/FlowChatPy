import json
import threading
import time
import unittest
import ipaddress
import tracemalloc

from net import networkmanager

# more debug information
tracemalloc.start()
messagesEmojiStr = ["python unittest", "python unittest smile:smile:", "python unittest crylaugh:crylaugh:",
                    "python unittest cool:cool:", "python unittest think:think:", "python unittest smirk:smirk:",
                    "python unittest sad:sad:", "python unittest yawn:yawn:", "python unittest cry:cry:",
                    "python unittest fear:fear:", "python unittest clown:clown:"]
messagesEmoji = ["python unittest", "python unittest smile😊", "python unittest crylaugh😂", "python unittest cool😎",
                 "python unittest think🤔", "python unittest smirk😏", "python unittest sad🙁",
                 "python unittest yawn🥱", "python unittest cry😭", "python unittest fear😱", "python unittest clown🤡"]
messagesNoEmoji = ["python unittest", "o92837rzfcmqo9rzxcLMCL qhwidf7fd§NEC / ", "CCWVz54g(fXMhdgU-=3#/Xe(Vr[%}?",
                   "cSE?U:@%DXzht:G9VH!K8x8wGVi*S+", "#{/[PD&BT*Epr]4J7VwjB@$Q.U?.dX", "!q4{MzKuWta,C2wPT{j8:imA}b6B.$",
                   "LH&}t_,W@Pg{P*bQq,;U&GEP7UU*];", "]GJ,,2xaA%4y8d?+8amVrQ=FV,=X*}"]
emotestrings = [":smile:", ":crylaugh:", ":cool:", ":think:", ":smirk:", ":sad:", ":yawn:", ":cry:", ":fear:",
                ":clown:"]
emotesymbols = ["😊", "😂", "😎", "🤔", "😏", "🙁", "🥱", "😭", "😱", "🤡"]


class TestNetwork(unittest.TestCase):

    def test_ip_finder(self):
        # Assert that ip_finder() returns a valid ipv4 Address
        ip = networkmanager.ip_finder()
        self.assertTrue(ipaddress.ip_address(ip))

    def test_send_message(self):
        # Start networkmanager's listen_loop method in new thread
        listener_daemon = threading.Thread(target=networkmanager.listen_loop, daemon=True)
        listener_daemon.start()
        networkmanager.message_queue.clear()
        # Send all messages
        for message in messagesNoEmoji:
            networkmanager.send_message(message)
        # Stop networkmanager.listen_loop
        networkmanager.on_closing()
        i = 0
        for recv_message in networkmanager.message_queue:
            payload = json.loads(recv_message)
            self.assertEqual(payload["message"], messagesNoEmoji[i], "retrieved messages missmatch!")
            self.assertEqual(payload["type"], "userMessage", "should be userMessage")
            i += 1
        networkmanager.message_queue.clear()
        # todo längere Nachrichten

    def test_check_emote(self):
        i = 0
        for messageEmojiStr in messagesEmojiStr:
            self.assertEqual(networkmanager.check_emote(messageEmojiStr), messagesEmoji[i],
                             "retrieved Emoji missmatch!")
            i += 1

    def test_check_which_emote(self):
        i = 0
        for emotestring in emotestrings:
            self.assertEqual(networkmanager.check_which_emote(emotestring), emotesymbols[i], "emote missmatch!")
            i += 1

    def test_send_custom_message(self):
        # Start networkmanager's listen_loop method in new thread
        listener_daemon = threading.Thread(target=networkmanager.listen_loop, daemon=True)
        listener_daemon.start()
        networkmanager.message_queue.clear()
        for message in messagesNoEmoji:
            networkmanager.send_custom_message(message)
        # Stop listen_loop
        networkmanager.on_closing()
        i = 0
        for recv_message in networkmanager.message_queue:
            payload = json.loads(recv_message)
            self.assertEqual(payload["message"], messagesNoEmoji[i], "retrieved messages missmatch!")
            self.assertEqual(payload["type"], "customMessage", "should be customMessage")
            i += 1
        networkmanager.message_queue.clear()

    def test_on_closing(self):
        networkmanager.running = True
        networkmanager.on_closing()
        self.assertFalse(networkmanager.running, "Should be False")

    def test_networkmanager(self):
        # Integrationstest???
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

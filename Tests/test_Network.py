import unittest
import ipaddress
import networkmanager
import tracemalloc

# more debug information
tracemalloc.start()

class TestNetwork(unittest.TestCase):

    def test_ip_finder(self):
        ip = networkmanager.ip_finder()
        self.assertTrue(ipaddress.ip_address(ip))

    def test_ready_listen_socket(self):
        networkmanager.ready_listen_socket().close()
        self.assertTrue(True) ## Wie testet man einen Socket?

    def test_ready_send_socket(self):
        # ready_send_socket() ist auf Variabeln angewiesen, die im networkmanager vorher gesetzt werden
        # mocking?
        #sock = networkmanager.ready_send_socket()
        self.assertTrue(True)

    def test_listen_handle_messages(self):
        # starte loop
        # sende ein udp packet an diese loop
        # assertEquals content von empfangenem packet
        # schließe loop
        self.assertTrue(True)

    def test_send_message(self):
        message = "python unittest"
        # längere Nachrichten
        # lausche auf recv port
        # nutze networkmanager.send_message(message)
        # assertEquals content
        self.assertTrue(True)

    def test_check_emote(self):
        # Julian fragen was die check_emote(message) Funktion macht
        message0 = "python unittest"
        message1 = "python unittest smile😊"
        message2 = "python unittest crylaugh😂"
        message3 = "python unittest cool😎"
        message4 = "python unittest think🤔"
        message5 = "python unittest smirk😏"
        message6 = "python unittest sad🙁"
        message7 = "python unittest yawn🥱"
        message8 = "python unittest cry😭"
        message9 = "python unittest fear😱"
        message10 = "python unittest clown🤡"
        self.assertTrue(True)

    def test_check_which_emote(self):
        emotestrings = [":smile:", ":crylaugh:", ":cool:", ":think:", ":smirk:", ":sad:", ":yawn:", ":cry:", ":fear:", ":clown:"]
        emotesymbols = ["😊", "😂", "😎", "🤔", "😏", "🙁", "🥱", "😭", "😱", "🤡"]
        # Mit Julian abchecken
        self.assertTrue(True)

    def test_send_custom_message(self):
        # Mit Jonas abchecken was wofür diese methode gebraucht wird im Gegensatz zu send_message
        self.assertTrue(True)

    def test_on_closing(self):
        # Networkmanager starten
        # Networkmanager stoppen
        # assert dass thread wirklich gestoppt ist
        self.assertTrue(True)

    def test_networkmanager(self):
        # Integrationstest???
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

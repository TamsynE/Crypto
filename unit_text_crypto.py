import unittest
from crypto import RailFence, Substitution, Playfair

class CryptoTest(unittest.TestCase):

    def test_rail_fence_encrypt_decrypt(self):
        rf = RailFence()
        plaintext = "This is a secret message"
        
        ciphertext = rf.encrypt(plaintext)
        decrypted_text = rf.decrypt(ciphertext)
        
        self.assertEqual(decrypted_text, plaintext)

    def test_substitution_encrypt_decrypt(self):
        password = "my password"
        sub = Substitution(password)
        plaintext = "this is a secret message"
        
        ciphertext = sub.encrypt(plaintext)
        decrypted_text = sub.decrypt(ciphertext)
        
        self.assertEqual(decrypted_text, plaintext)

    def test_playfair_encrypt_decrypt(self):
        keyword = "KEYWORD"
        play = Playfair(keyword)
        plaintext = "This is a secret message"
        
        ciphertext = play.encrypt(plaintext)
        decrypted_text = play.decrypt(ciphertext)
        plaintext = plaintext.replace(' ', '').upper()
        self.assertEqual(decrypted_text, plaintext)

if __name__ == '__main__':
    unittest.main()
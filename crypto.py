""" Collection of simple, historic, text-based cryptographic algorithms. """
import argparse

class RailFence:
    """ Encrypts and decrypts text messages using the Rail Fence algorithm. """
    
    def __init__(self):
        self.evenChars = ''
        self.oddChars = ''
        
    def encrypt(self, plaintext):
        """ Encrypts a message with the Rail Fence cipher. """
        
        msgLength = len(plaintext)

        for i in range(msgLength):
            if i % 2 == 0:
                self.evenChars = self.evenChars + plaintext[i]
            else:
                self.oddChars = self.oddChars + plaintext[i]
        ciphertext = self.oddChars + self.evenChars
        return ciphertext

    def decrypt(self, ciphertext):
        """ Decrypts a message with the Rail Fence cipher. """  

        halfLength = len(ciphertext) // 2
        oddText = ciphertext[:halfLength]  # from the beginning, up to the halfway point
        evenText = ciphertext[halfLength:] # from the halfway point, all the way to the end

        plaintext = ''
        for i in range(halfLength):
            plaintext = plaintext + evenText[i]
            plaintext = plaintext + oddText[i]

        if len(evenText) > len(oddText):
            plaintext = plaintext + evenText[-1]

        return plaintext

class Password:
    """""Converts the password given for a substitution cipher to a key"""
    
    def password_to_key(keyword):
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        keyword = keyword.lower()
                
        newKey = ''
        for ch in keyword:
            if ch not in newKey:
                newKey = newKey + ch

        splitChr = newKey[-1]
        splitIdx = alphabet.find(splitChr)
     
        afterStr = ''
        for ch in alphabet[splitIdx+1:]:
            if ch not in newKey:
                afterStr = afterStr + ch
        beforeStr = ''
        for ch in alphabet[:splitIdx]:
            if ch not in newKey:
                beforeStr = beforeStr + ch

        grid = newKey + afterStr + beforeStr

        return grid


class Substitution:
    """ Encrypts and decrypts text messages using the Substitution algorithm. """

    def __init__(self, password):
        key = Password.password_to_key(password)
        self.key = key

    def encrypt(self, plaintext):
        """ Encrypts a message with the Substitution cipher. """

        alphabet = "abcdefghijklmnopqrstuvwxyz "
        ciphertext = ""
        for ch in plaintext:
            idx = alphabet.find(ch)
            if idx != -1:
                ciphertext = ciphertext + self.key[idx]
        return ciphertext
    
    def decrypt(self, ciphertext):
        """ Decrypts a message with the Substitution cipher. """
        
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        plaintext = ""
        for ch in ciphertext:
            idx = self.key.find(ch)
            plaintext = plaintext + alphabet[idx]
        return plaintext


class Playfair:
    """ Encrypts and decrypts text messages using the WWI British Playfair algorithm. """
    
    def __init__(self, keyword):
        self.keyword = keyword.upper()

    def create_playfair_grid(self, keyword):
        """""Creates the 25 letter-long key from a keyword/password with no repeated letters for Playfair encryption/decryption"""
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        
        newKey = ''
        keyword = keyword.replace(' ', '')
        for ch in keyword:
            if ch not in newKey:
                newKey = newKey + ch
        
        afterStr = ''
        for ch in alphabet[0:]:
            if ch not in newKey:
                afterStr = afterStr + ch
        grid = newKey + afterStr

        return grid 
    
    def create_playfair_digrams(self, text):
        """Arranges the plaintext into digrams and inserts Q's between matching-letter-digrams"""
        # Initialize an empty list to store the digrams
        digrams = []
        i = 0
        text = text.replace(' ', '')

        while i < len(text):
            ch = text[i]
            x_notx = 'Q'

            # check if there is a next character and if it matches the previous character
            if i +1 < len(text) and text[i+1] == ch:
                i-=1 # for when we add X

            else:
                if i+1 < len(text):
                    x_notx = text[i +1] 
                else:
                    x_notx = 'Q'
            
            digrams.append(ch + x_notx)
            i+=2

            # if last character is by itself
            if len(digrams[-1]) == 1:
                digrams[-0] == 'Q'

        # Join the digrams and return the result
        return digrams

    def encrypt(self, plaintext, debug=False):
        """ Encrypts a message with the Playfair cipher. """
        grid = self.create_playfair_grid(self.keyword)
        digrams = self.create_playfair_digrams(plaintext)

        row1 = grid[0:5]
        row2 = grid[5:10]
        row3 = grid[10:15]
        row4 = grid[15:20]
        row5 = grid[20:25]

        i = 0
        text = ''
        
        # put digrams together in string
        while i < len(digrams):
            text += digrams[i]
            i +=1
        i = 0
        new_text = ''

        while i < len(text):
            # remove punctuation
            if text[i] in ' !:@#$%^&*()1234567890,.;"/':
                i+=1
                continue
            # replace 'j' with 'i'
            if text[i].lower() == 'j':
                new_text += 'i'
                i+=1
                continue
            
            new_text += text[i]
            i+=1
        
        i = 0
        encrypted_text = ''
        new_text = new_text.upper()
        
        # 5 cases for the digrams placement
        while i < len(new_text)-1:
            char1 = new_text[i]
            char2 = new_text[i + 1]

            column_of_1 = (grid.index(char1) % 5) 
            column_of_2 = (grid.index(char2) % 5) 
            row_of_1 = (grid.index(char1) // 5) 
            row_of_2 = (grid.index(char2) // 5) 

            if row_of_1 == row_of_2 and column_of_1 == column_of_2:
                new_char1 = new_char2 = char1 = char2
                encrypted_text += new_char1 + new_char2
            
            else:
                # 1. Same Row
                if row_of_1 == row_of_2 and column_of_1 != column_of_2:
                    if char1 in row1 and char2 in row1: 
                        # Case 1: Same Row (for row1)
                        col1 = row1.index(char1)
                        col2 = row1.index(char2)
                        new_char1 = row1[(col1 + 1) % 5]
                        new_char2 = row1[(col2 + 1) % 5]
                        encrypted_text += new_char1 + new_char2
                        
                    elif char1 in row2 and char2 in row2:
                        # Case 2: Same Row (for row2)
                        col1 = row2.index(char1)
                        col2 = row2.index(char2)
                        new_char1 = row2[(col1 + 1) % 5]
                        new_char2 = row2[(col2 + 1) % 5]
                        encrypted_text += new_char1 + new_char2

                    elif char1 in row3 and char2 in row3:
                        # Case 3: Same Row (for row3)
                        col1 = row3.index(char1)
                        col2 = row3.index(char2)
                        new_char1 = row3[(col1 + 1) % 5]
                        new_char2 = row3[(col2 + 1) % 5]
                        encrypted_text += new_char1 + new_char2

                    elif char1 in row4 and char2 in row4:
                        # Case 4: Same Row (for row4)
                        col1 = row4.index(char1)
                        col2 = row4.index(char2)
                        new_char1 = row4[(col1 + 1) % 5]
                        new_char2 = row4[(col2 + 1) % 5]
                        encrypted_text += new_char1 + new_char2

                    elif char1 in row5 and char2 in row5:
                        # Case 5: Same Row (for row5)
                        col1 = row5.index(char1)
                        col2 = row5.index(char2)
                        new_char1 = row5[(col1 + 1) % 5]
                        new_char2 = row5[(col2 + 1) % 5]
                        encrypted_text += new_char1 + new_char2
            
                # 2. Same Column
                if column_of_1 == column_of_2 and row_of_1 != row_of_2:
                    # if first letter in last row - needs to move to top row
                    if (row_of_1+1) == 5:
                        new_char1 = grid[(5 * (row_of_1+1)%5) + column_of_1]
                        new_char2 = grid[(5 * (row_of_2+1))+ column_of_1]
                    # if second letter in last row - ''
                    elif (row_of_2+1) == 5:
                        new_char1 = grid[(5 * (row_of_1+1)) + column_of_1]
                        new_char2 = grid[(5 * (row_of_2+1)%5)+ column_of_1]
                    # in the middle
                    else:
                        new_char1 = grid[(5 * (row_of_1+1)) + column_of_1]
                        new_char2 = grid[(5 * (row_of_2+1))+ column_of_1]
                    encrypted_text += new_char1 + new_char2

            # 3. Rectangle
                if column_of_1 != column_of_2 and row_of_1 != row_of_2:

                    new_char1 = grid[(row_of_1) * 5 + column_of_2]
                    new_char2 = grid[(row_of_2) * 5 + column_of_1] 

                    encrypted_text += new_char1 + new_char2

            i+=2
        return encrypted_text

    def decode_playfair_cipher(self, text):
        text_orig = text.lower()
        text_new = ""

        i = 0
        while i < len(text_orig):
            if text_orig[i] == 'q' and i > 0 and i < len(text_orig) - 1 and text_orig[i - 1] == text_orig[i + 1]:
                # If 'q' is surrounded by the same letter, skip it.
                i += 1
            else:
                text_new += text_orig[i]
                i += 1

            if i == len(text_orig)-1 and text_orig[i] == 'q':
                text_new += ''
                i+=1
                continue

        return text_new
        
    def decrypt(self, ciphertext):
        """ Decrypts a message with the Playfair cipher. """
        
        grid = self.create_playfair_grid(self.keyword)
        row1 = grid[0:5]
        row2 = grid[5:10]
        row3 = grid[10:15]
        row4 = grid[15:20]
        row5 = grid[20:25]

        i = 0
        decrypted_text = ''
        ciphertext = ciphertext.upper()
        # 5 cases for the digrams placement
        
        while i < len(ciphertext):
            char1 = ciphertext[i]
            char2 = ciphertext[i + 1]

            column_of_1 = (grid.index(char1) % 5) 
            column_of_2 = (grid.index(char2) % 5) 
            row_of_1 = (grid.index(char1) // 5)
            row_of_2 = (grid.index(char2) // 5) 

            if row_of_1 == row_of_2 and column_of_1 == column_of_2:
                new_char1 = new_char2 = char1 = char2
                decrypted_text += new_char1 + new_char2
                
            else:
            # 1. Same Row
                if char1 in row1 and char2 in row1:
                    col1 = row1.index(char1)
                    col2 = row1.index(char2)
                    new_char1 = row1[(col1 - 1) % 5]
                    new_char2 = row1[(col2 - 1) % 5]
                    decrypted_text += new_char1 + new_char2

                elif char1 in row2 and char2 in row2:
                    # Case 2: Same Row (for row2)
                    col1 = row2.index(char1)
                    col2 = row2.index(char2)
                    new_char1 = row2[(col1 - 1) % 5]
                    new_char2 = row2[(col2 - 1) % 5]
                    decrypted_text += new_char1 + new_char2

                elif char1 in row3 and char2 in row3:
                    # Case 3: Same Row (for row3)
                    col1 = row3.index(char1)
                    col2 = row3.index(char2)
                    new_char1 = row3[(col1 - 1) % 5]
                    new_char2 = row3[(col2 - 1) % 5]
                    decrypted_text += new_char1 + new_char2

                elif char1 in row4 and char2 in row4:
                    # Case 4: Same Row (for row4)
                    col1 = row4.index(char1)
                    col2 = row4.index(char2)
                    new_char1 = row4[(col1 - 1) % 5]
                    new_char2 = row4[(col2 - 1) % 5]
                    decrypted_text += new_char1 + new_char2

                elif char1 in row5 and char2 in row5:
                    # Case 5: Same Row (for row5)
                    col1 = row5.index(char1)
                    col2 = row5.index(char2)
                    new_char1 = row5[(col1 - 1) % 5]
                    new_char2 = row5[(col2 - 1) % 5]
                    decrypted_text += new_char1 + new_char2

                # 2. Same Column
                if column_of_1 == column_of_2 and row_of_1 != row_of_2:

                    if (row_of_1+1) == 1: # first one goes to the bottom
                        new_char1 = grid[(5 * (row_of_1+4)) + column_of_1]
                        new_char2 = grid[(5 * (row_of_2-1))+ column_of_1]

                    elif (row_of_2+1) == 1: # second one goes to bottom
                        new_char1 = grid[(5 * (row_of_1-1)) + column_of_1]
                        new_char2 = grid[(5 * (row_of_2+4)) + column_of_1] 

                    else:
                        new_char1 = grid[(5 * (row_of_1-1)) + column_of_1]
                        new_char2 = grid[(5 * (row_of_2-1)) + column_of_1]
                    decrypted_text += new_char1 + new_char2

                # 3. Rectangle -- so this is our focus
                if column_of_1 != column_of_2 and row_of_1 != row_of_2:
                    new_char1 = grid[(row_of_1) * 5 + column_of_2]
                    new_char2 = grid[(row_of_2) * 5 + column_of_1]

                    decrypted_text += new_char1 + new_char2
            i+=2
        decrypted_text2 = self.decode_playfair_cipher(decrypted_text)
            
        return decrypted_text2.upper()

def main():
        parser = argparse.ArgumentParser(description='Encrypt or decrypt text.')
        # 1. --algorithm
        parser.add_argument('-a', '--algorithm', choices=['substitution', 'rail_fence', 'playfair'], help='Choose algorithm: substitution/rail_fence/playfair')
        # 2. --mode (operation)
        parser.add_argument('-m', '--mode', choices=['encrypt', 'decrypt'], help='Choose mode: encrypt/decrypt')
        # 3. --key
        parser.add_argument('-k', '--key', type=str, help='key/password string from encryption/decryption', required=False)
        # 4. --text (message)
        parser.add_argument('-t', '--text', type=str, help='Text to be encrypted or decrypted')
        
        args = parser.parse_args()
        
        # Rail Fence
        if args.algorithm == "rail_fence":
            rail_fence = RailFence()

            if args.mode == "encrypt":
                ciphertext = rail_fence.encrypt(args.text)
                print("Encrypted Message: ", ciphertext)

            elif args.mode == "decrypt":
                plaintext = rail_fence.decrypt(args.text)
                print("Decrypted Message:", plaintext)

        # Substitution
        elif args.algorithm == "substitution":
            if args.key is None:
                print("Please enter valid key")
                return

            sub = Substitution(args.key)
            if args.mode == "encrypt":
                ciphertext = sub.encrypt(args.text)
                print("Encrypted Message:", ciphertext)

            elif args.mode == "decrypt":
                plaintext = sub.decrypt(args.text)
                print("Decrypted Message:", plaintext)

        # Playfair
        elif args.algorithm == "playfair":
            if args.key is None:
                print("Please enter valid key")
                return

            play = Playfair(args.key)
            if args.mode == "encrypt":
                ciphertext = play.encrypt(args.text)
                print("Encrypted Message:", ciphertext)

            elif args.mode == "decrypt":
                plaintext = play.decrypt(args.text)
                print("Decrypted Message:", plaintext)

if __name__ == "__main__":
    main()


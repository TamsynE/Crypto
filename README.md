# Crypto

# Purpose 
Encrypt and decrypt secret messages using the Playfair Cipher.  The Playfair Cipher was invented in the mid-1800s and went unbroken for almost 75 years.  It was a British Cipher that was used in World War I and was similar to another cipher used by the Germans in WWI called the ADFGVX cipher.
Files
The main program file for this program is crypto.py which lets the user select from 3 different cipher methods: rail fence, substitution, or playfair cipher.  They are then prompted to choose a key and text to either encrypt or decrypt with.
Version
Requires python3 and the argparse module.
Usage
python crypto.py -a playfair -m encrypt -k "playfair example" -t "Hide the gold in the tree stump"

python crypto.py -a playfair -m decrypt -k "playfair example" -t "BMODZBXDNABEKUDMUIXMMOUVIF" 

Playfair Rules
Converting from plaintext to ciphertext
Generate key table (5x5), remove duplicate letters from key, replace all “j” with “i” and remove any non-alphabet characters, continue alphabet from the last letter of the keyword.
Split plaintext into groups of 2 letters, if both letters are the same (or only one letter is left), add "X" after the first letter.  Encrypt the new pair and continue.
If the pair of letters are on the same row of your key table, replace them with the letters to their immediate right and wrap around to the beginning of the row if needed.
If the pair of letters are on the same column of your key table, replace them with the letters immediately below and wrap around to the top of the column if needed.
If the letters are not on the same row or column, create a rectangle with the two letters and replace the letters with the corresponding letter in the same row.
Converting from ciphertext to plaintext
Generate key table (5x5), remove duplicate letters from key, replace all “j” with “i” and remove any non-alphabet characters, continue alphabet from the last letter of the keyword.
Split ciphertext into groups of 2 letters, if the pair of letters are in the same row of your key table, replace them with the letters to their immediate left and wrap around to the end of the row if needed.
If the pair of letters are on the same column of your key table, replace them with the letters immediately above and wrap around to the bottom of the column if needed.
If the letters are not on the same row or column, create a rectangle with the two letters and replace the letters with the corresponding letter in the same row.
(last step) Locate all “X”s in plaintext.  Check letters to the immediate right and left and if they are the same or if “X” is the last letter, remove “X”
Testing
The playfair module contains a short unit test that verifies the object translates from plaintext to ciphertext correctly and vice-versa.
Plaintext: "Hide the gold in the tree stump"
Key: "playfair example"
Ciphertext: "BMODZBXDNABEKUDMUIXMMOUVIF”

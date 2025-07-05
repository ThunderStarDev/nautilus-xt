# NAUTILUS XT v.07.25 manual

**Nautilus XT** is a password generation utility that allows you to create and retrieve complex passwords without the need to store them locally. 
Simply think of a passphrase, specify the account name and password length (default is 12 characters or 5 mnemonic words), and the program will generate a unique password each time based on this information.

If you wish, you can create an **additional layer of protection**. There is a **SEED.txt** file in the folder with the installed program, (it is empty by default). If you wish, you can change the word to your own. However, remember that if you reinstall the software, you will need to re-write the word specified inside the file.

**Password** = Passphrase + Account + SEED.txt

## Key Features
- **Unlimited** password length
- Generation of **hard**, but easily retrieveable passwords
- Ability to generate mnemonic phrases
- Simple, but functional UI
- **No** internet connection
- Minimalism

You only need to remember one passphrase. It's recommended to store other information (such as account names and password lengths) on paper, in a text file or password manager.
A difference of one character is enough to create two unique passwords. The password generation algorithm is NOT case sensitive.

## Guide
1. Create a passphrase that you can easily remember. For convenience, write it down on paper. 

    NOTE: You **can** create passwords without a passphrase and seedphrase. However, I recommend filling in all fields, as this makes it much more difficult to guess the password.

2. Enter passphrase into the program, specify the desired password length, and provide the name of the account. This could be a website name, email address, username, etc.
3. Remember (or better yet, write down) the account name and password length. DO NOT WRITE DOWN THE PASSPHRASE AND ACCOUNT NAMES ON THE SAME PAPER.
4. Double check that you've written everything down correctly.
5. Select the mode. "Password" is suitable for standard use, but "Mnemonic" makes easier to remember passwords.
	
   In "Mnemonic" mode, the "Length" field determines not the number of characters, but the number of words. Each word is taken from the BIP39 dictionary, the full list of words is in the folder with the installed program.
 
6. Press "Generate" button. The program will generate a unique password based on the entered information. 
	If the generated password exceeds the output window length, use Ctrl + A to select the entire password, then Ctrl + C to copy it.
7. Store the paper with your passphrase in a safe place. This could be a safe, a bank deposit box, or a personal hiding spot.

### Example: 
- I wrote the word "Thunder" in the SEED.txt file right after installation.
- After that, I came up with the Passphrase "Star" and wrote it down in a notepad so I wouldn't forget.
- Then, I entered the Passphrase in the corresponding window, entered the account name "Dev" and the length of the characters "20"

	  Generated password: R#R?pSM!g+eH$*eO$Qag

## Important
Your passphrase should be simple and easy for you to remember but not obvious to others.
**Do not** store your passphrase electronically (e.g., in a text file), as this could compromise security.
If you change even one letter, the resulting password will be completely **different**.

Choose a simple but **non-obvious** word that you can easily remember.

## Usage Recommendations
Avoid using personal information as your passphrase, such as:
- Birthdates
- **Names** of relatives or pets
- Information that can be **directly** associated with you

**A password length of at least 12 characters /  5 mnemonic words is recommended for optimal security.**

## Disclaimer
The developer **is not** responsible for any loss of access to your accounts. Ensure that your passphrase is secure and easy to remember.
The program version is designed for use on Linux and Windows operating systems. No specific hardware requirements are necessary. Tested on Debian 12, Debian 13, Windows 10, Windows 11.

## License
This project is licensed under the Apache License, Version 2.0. See LICENSE.txt for more details.

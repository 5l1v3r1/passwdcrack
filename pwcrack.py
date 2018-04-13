import crypt
import sys
import time

class bcolours:
    GREEN = '\033[92m'
    TURQ = '\033[96m'
    ENDC = '\033[0m'

def testPass(user, cryptPass):
    salt = cryptPass[0:2]
    if not salt in ('HX','$6','$s'):
         print ('[*] Sorry, hash not recognised, moving onto next hash')
         return
    shasalt = cryptPass[3:11].strip()
    insalt = '$6$' + shasalt
    dictFile = open(sys.argv[2],'r')
    dictLen = 0
    for line in dictFile.readlines():
        dictLen += 1
    fileLen = dictLen
    dictFile = open(sys.argv[2],'r')
    currLine = 0
    for word in dictFile.readlines():
        currLine += 1
        word = word.strip('\n')
        cryptWord = crypt.crypt(word,salt)
        cryptSHA = crypt.crypt(word, insalt)
        if (cryptWord == cryptPass or cryptSHA.rstrip() == cryptPass.rstrip()):
            print (bcolours.GREEN + '\n' + '[+] ' + bcolours.ENDC + 'Successful Brute Force: ' + user + ':' + word + "\n")
            with open('cracked.txt', 'a') as file:
                print >> file, (user + ':' + word)
            time.sleep(2)
            break
        if (cryptWord != cryptPass or cryptSHA != cryptPass):
            print ('[-] Trying: ' + word  + " " + str(currLine) + "/" + str(fileLen))
            continue
    return

def main():
    if len(sys.argv) != 3:
        print ('usage: pwcrack.py <hashes file> <wordlist file>')
        exit(0)
    count = 0
    passFile = open(sys.argv[1],'r')
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptPass = line.split(":")[1].strip(' ')
            print ('\n' + '[*] Cracking Password for username: ' + user + '\n')
            time.sleep(2)
            testPass(user, cryptPass)

if __name__ == "__main__":
    main()

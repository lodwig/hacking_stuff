from cmd import Cmd

# skeleton untuk looping command  
class Terminal(Cmd):
    prompt = "Command: "


    def __init__(self):
        self.kerjakan()
        super().__init__()

    # Di Panggil Pada Saat Initialisasi skeleton
    def kerjakan(self):
        # modif function ini untuk kepentingan
        print("Modify di sinis untuk LFI atau SQLI atau Command Injection") 

    def default(self, args):
        print(args)

    def do_exit(self, args):
        print(f"[+] Terminal di tutup ~ aka : Lodwig")
        return True

console = Terminal()
console.cmdloop()
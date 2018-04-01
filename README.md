# PyBotnet

This is an `HTTPs Pull Botnet` :
The victims are always active and every 30 seconds (you can change the time for request), send a request to the C&C Panel for check if there are commands to execute.

The botnet is very useful for passive control, like credentials harvesting or malware spamming, but not for commands execution in-live because the host doesn't contact the victim (however, there is a reverse shell option).

### Requirements

- Requests library (for all the requests realized)
- PyCrypto (for crypting and hashing)
- CherryPy (for the http server)
- Jinja2 (for the templates)

### Utility

Aside from the `Server`, `Core` (the agent) and the `HTML Web Pages`, there is a simple script, named `db.py` that you can use for initialize, delete and view the dbs.
Here you can see the help message: 

![Db.py Help Message](https://github.com/Mik317/PyBotnet/blob/master/doc/dbhelp.png)
, while here youcan see the various usages:

![Db.py Usages](https://github.com/Mik317/PyBotnet/blob/master/doc/dbopt.png).

### Something More

The botnet is very simple: as soon as the bot is infected, it will send to the Server Web API* a request to the `/welcome/`, and trough JSON, it will send the `Key` (that's the pc-user encoded with SHA512 and MD5), the username, the IP, the location, a simple uname and other infos that will be memorized in the `Bots` table of the DB `bots.db` (created with sqlite using `py db.py init`).

* API = the API are the pages that contains only the things that the bots must see.

Immediately after, the bot begin to send every 5 minutes (default time) some requests to the API at the page `/check_cmd/<their key>`, and if there is commands in queque in the table `CmdsIn` of the DB `cmds.db`, they will be returned, vested from the bots and executed for send the output at the `/cmd_out/` throug JSON, that will be stored in the table `CmdsOut` on the DB `cmds.db`.

As you will have guessed, all is based on the `Keys` of the bots, that identify all of them and are used for get infos, give commands and read outputs.

The authentication, is based on the session of CherryPy, and will be enforced by a simple header (`LoggedIn`), that verify if the key of the BotMaster is `OK`. The auth happens when BotMaster Key, and User+Pass are OK.
All the things, such as login,requests from the bot, etc .... are logged using the logging function of CherryPy, that grab IP, date and some infos onthe request.

This botnet provide a very beautiful web panel, written in `HTML`+`Bootstrap`+`Chart.js`,and allow you to:
- Control and manage all the bots 
- Send commands to bots
- Have a nice view of the data

### Get Started

This botnet is composed by 2 main files: `Server.py` (that's the HTTP Server that contains API, C&C Panel, the DBs of sqlite and the session), and the `Core.py` file, that is the agent with which infect the bots.

1. Execute the `Server` using the following command on the server machine: `py Server.py`
2. Go to `localhost:8080`
3. Login using the user, the pass* and the key of the botmaster
4. Execute the `Core.py` on the victim machina, using the command like this: `py Core.py`
5. Wait some seconds that the Agent send us all the infos
6. Explore the C&C Panel !!!

* Pass = The password will be generated automatically using AES and base64 encoding, therefore you must copy it every time that you execute the server.

The credentials can be obtained only from Chrome, and will be memorized in the `Creds` table of the `creds.db` DB; After, you can see they for every single bot. If you want the credentias, you will insert as command to execute, the special keyword `cred`, that execute the `cred` module in the Agent.

Some photos here:

![Server Started](https://github.com/Mik317/PyBotnet/blob/master/doc/startserver.png)
![Login Botnet](https://github.com/Mik317/PyBotnet/blob/master/doc/login.png)
![DashBoard](https://github.com/Mik317/PyBotnet/blob/master/doc/dashboard.png)
![View Bot From Key](https://github.com/Mik317/PyBotnet/blob/master/doc/view.png)
![Bots Requests](https://github.com/Mik317/PyBotnet/blob/master/doc/botrequests.png)
![CMD In](https://github.com/Mik317/PyBotnet/blob/master/doc/cmdin.png)
![CMD Out](https://github.com/Mik317/PyBotnet/blob/master/doc/cdmout.png)

And, if you give the `cred` command ...... you can obtain all the credentials stealed from the Chrome Credentials DB, that will be reported on the Web Panel like this:
![Cred Page](https://github.com/Mik317/PyBotnet/blob/master/doc/cred.png)

### Commands

| Command       | Description   |     
| ------------- |:-------------:|
| $simple_command_to_execute_directly_(like_`ls`)      | Simply executed as a normal command |
| cred      | Obtain all the credentials stored in the Chrome DB      |
| ddos | Launch a DDOS Attack      |

### Todo
- [x] Add some graphs on the DashBoard page
- [x] Add the Credential Grabber Module
- [x] Add the web page for managing of the credentials
- [ ] Add persistence
- [ ] Add the DDOS Module
- [ ] Add the DDOS Map (using )

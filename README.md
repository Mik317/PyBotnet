# PyBotnet

This is an `HTTPs Pull Botnet` :
The victims are always active and every 5 minutes, send a request to the C&C Panel for check if there are commands to execute.

The botnet is very useful for passive control, like credentials harvesting or malware spamming, but not for commands execution in-live because the host doesn't contact the victim (however, there is a reverse shell option).

The project have been realized in only 5 days, and it's a simple botnet that permit to monitor all the infected bots.

### Requirements

- Requests library (for all the requests realized)
- PyCrypto (for crypting and hashing)
- CherryPy (for the http server)
- Jinja2 (for the templates)

### Utility

Aside from the `Server`, `Core` (the agent) and the `HTML Web Pages`, there is a simple script, named `db.py` that you can use for initialize, delete and view the dbs.
Here you can see the help message: 

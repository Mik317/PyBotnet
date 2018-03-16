# PyBotnet

This is an `HTTPs Pull Botnet` that works under TOR:
The victims are always active and every 5 minutes, send a request to the C&C Panel (under TOR) for check if there are commands to execute.

The botnet is very useful for passive control, like credentials harvesting or malware spamming, but not for commands execution in-live because the host doesn't contact the victim.


Install your public key in the remote machine's authorized_keys

Run the following command in a shell on the remote system:
```
mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo "ssh-rsa KEYGOESHERE user@remotehost or note" >> ~/.ssh/authorized_keys
```

If you do not already have a public key on your local system:
```
ssh-keygen -t rsa
```

Copy public key to remote authorized_keys file
```
local> scp .ssh/id_dsa.pub remote.com:
local> ssh remote.com
remote> cat id_dsa.pub >> .ssh/authorized_keys
remote> rm id_dsa.pub
remote> exit
```

-fin-

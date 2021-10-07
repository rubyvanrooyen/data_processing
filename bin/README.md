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

Data location on bruce:
```
ssh -XY bruce

quota -s
Disk quotas for user ruby (uid 1582):
     Filesystem   space   quota   limit   grace   files   quota   limit   grace
/dev/mapper/ubuntu--vg-root
                     4K   2048M   5120M               2       0       0
/dev/mapper/ubuntu--vg-home
                  1384K  20480G  20480G             346       0       0
    com08:/home    939M  10240M  15360M           30372       0       0

df -h
Filesystem                   Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-root 1007G   28G  929G   3% /
/dev/mapper/ubuntu--vg-home   85T  7.7T   74T  10% /home
com08:/home                  458G  254G  181G  59% /net/com08/home
```

-fin-

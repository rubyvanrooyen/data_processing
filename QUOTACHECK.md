## Check if you have exceeded you quota
```
> quota -s
Disk quotas for user ruby (uid 1582):
     Filesystem   space   quota   limit   grace   files   quota   limit   grace
      /dev/sda1   2660M*  2048M   5120M    none   48282       0       0
      /dev/sdb1   2062G  15360G  15360G           29430       0       0
```
```
> quota -q
Disk quotas for user ruby (uid 1582):
	Over block quota on /dev/sda1
```
```
> df -h .
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       458G   33G  402G   8% /
```
```
> du -hcs .
2.6G	.
2.6G	totalgg
```
Exceeded home directory limit of 2G
```
Filesystem   space   quota
 /dev/sda1   2660M*  2048M
```

## Find the large files
Include hidden files and directories
`du -sch .[!.]* * | sort -h`

Often it is the pip cache. Try using `--no-cache-dir` when using pip install
* `pip cache purge` removes all the wheel files in the cache
* `pip install --no-cache-dir <package>` install a package without using the cache, for just this run

## Clean/remove RadioPadre
Can become to large and cause quota issues   
Use Makefile to clean up remote installation   
`make cleanpadre`

## Inspecting large files in root
Find files owned by your user in / directory   
```
find / -group ruby 2> /dev/null | grep -v /home/ruby > /home/ruby/ownership.txt
grep -v '^/net\|^/sys\|^/proc' /home/ruby/ownership.txt
```
Check size of suspected large crash files and removed large files belonging to you
```
cd /var/crash
ls -alh
```
```
-rw-r-----  1 ruby   ruby   2.1G Feb 15 15:33 _opt_casalite_lib_casa_bin_casaviewer.1582.crash
-rw-r-----  1 ruby   ruby    65M Feb 16 17:35 _opt_casalite_lib_casa_bin_python.1582.crash
-rw-r-----  1 ruby   ruby   1.4G Feb 18 18:01 _usr_bin_wsclean.1582.crash
```

## Adding auto flake8 checks to vim
Install flake8 for python
`pip install flake8 --no-cache-dir`

Add config to .vim directory
```
mkdir -p ~/.vim/ftplugin
cd ~/.vim/ftplugin
```
Add the python config `python.vim` file
```
> cat python.vim
setlocal autoindent        " align the new line indent with the previous line
setlocal expandtab         " insert spaces when hitting TABs
" setlocal shiftround        " round indent to multiple of 'shiftwidth'
setlocal shiftwidth=4      " operation >> indents 4 columns; << unindents 4 columns
setlocal softtabstop=4     " insert/delete 4 spaces when hitting a TAB/BACKSPACE
setlocal tabstop=8         " a hard TAB displays as 8 columns
setlocal textwidth=79      " lines longer than 79 columns will be broken
" setlocal foldmethod=indent " folding based on indentation

" Use the below highlight group when displaying bad whitespace is desired.
highlight BadWhitespace ctermbg=red guibg=red

" Display tabs at the beginning of a line in Python mode as bad.
" Make trailing whitespace be flagged as bad.
autocmd! BufEnter <buffer> match BadWhitespace /^\t\+\|\s\+$/

" run the Flake8 check every time a Python file is written
autocmd BufWritePost *.py call Flake8()
```

VIM config
```
# https://github.com/nvie/vim-flake8
mkdir -p ~/.vim/pack/flake8/start/
cd ~/.vim/pack/flake8/start/
git clone https://github.com/nvie/vim-flake8.git
```
This will make sure flake8 checks are run when file is written

To run flake8 independently
```
flake8 <file>
flake8 <project_dir>
flake8 *.py
flake8 .
```

## 10Ge network not connected
Getting data from archive times out
```
> ping archive-gw-1.kat.ac.za
PING archive-gw-1.kat.ac.za (10.98.56.16) 56(84) bytes of data.
```

Check network mapping
```
> netstat -r
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         10.8.76.254     0.0.0.0         UG        0 0          0 em3
10.8.76.0       0.0.0.0         255.255.255.0   U         0 0          0 em3
10.98.6.0       10.98.32.254    255.255.255.0   UG        0 0          0 em1
10.98.32.0      0.0.0.0         255.255.255.0   U         0 0          0 em1
10.98.56.0      10.98.32.254    255.255.255.0   UG        0 0          0 em1
172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 docker0
225.100.0.0     0.0.0.0         255.255.0.0     U         0 0          0 em1
```
```
> ping 10.98.32.254
PING 10.98.32.254 (10.98.32.254) 56(84) bytes of data.
From 10.98.32.18 icmp_seq=1 Destination Host Unreachable
From 10.98.32.18 icmp_seq=2 Destination Host Unreachable
From 10.98.32.18 icmp_seq=3 Destination Host Unreachable
```

Check IPs
```
ifconfig -a

em1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 8900
        inet 10.98.32.18  netmask 255.255.255.0  broadcast 10.98.32.255
        inet6 fe80::1618:77ff:fe5c:93db  prefixlen 64  scopeid 0x20<link>
        ether 14:18:77:5c:93:db  txqueuelen 1000  (Ethernet)
        RX packets 1600398  bytes 109478804 (109.4 MB)
        RX errors 0  dropped 3  overruns 0  frame 0
        TX packets 17277  bytes 4021730 (4.0 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 46  memory 0x95000000-957fffff
```

See if you can ping the ip
```
ruby@com08:~/comet67p$ ping 10.98.32.18
PING 10.98.32.18 (10.98.32.18) 56(84) bytes of data.
From 10.98.32.32 icmp_seq=1 Destination Host Unreachable
From 10.98.32.32 icmp_seq=2 Destination Host Unreachable
From 10.98.32.32 icmp_seq=3 Destination Host Unreachable
```


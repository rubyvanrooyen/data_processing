## Set up development environment
```
python3 -m venv venv
source venv/bin/activate

pip install -U pip setuptools wheel

# install newest master to correct the setjy model error
pip install --no-cache-dir git+https://github.com/caracal-pipeline/caracal.git

# check installation
caracal -h

# clean up unneccessay installation files
pip cache purge
deactivate
```

## Caracal data processing
Data processing takes a long time, if working on a remote server is it suggested that you use tmux or screen sessions

Create symbolic link to raw data files
```
ln -s <path/to/rawdata> ms-orig
```

Execute CARACal pipeline
```
caracal -c run-g330-32k.yml

# sw : start-worker
# ew : end-worker
caracal -c run-g330-32k.yml -sw general -ew transform__calibrators
```

-fin-

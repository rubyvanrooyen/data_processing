list all the minor cycle images created by wsclean
ls comet67p.*.wsclean-000?-*.fits

move them out of the way for easy removal later
mkdir wipeme
mv comet67p.*.wsclean-000?-*.fits wipeme/

move images into their own directory
mdir fitsims
mv comet67p.*.wsclean-MFS-*.fits fitsims/


given the sizes of the files, always issue commands inside a tmux so that if the network disconnects the command still finishes
for inspection you may need casa
tmux new -s casa (tmux a -t casa)
since this exports your display settings, you may need to kill and restart this tmux from time to time



clean:
	rm -f .last*
	rm -rf .stimela_workdir*
	rm -rf .radiopadre*
	rm -rf .ipynb_checkpoints

clobber: clean
	rm -rf  input
	rm -rf  msdir
	rm -rf  output*
	rm -rf *.ipynb

cleanpadre:
	rm -f radiopadre-default.ipynb
	rm -rf .radiopadre*
	rm -rf radiopadre
	rm -rf radiopadre-client

clobberpadre: cleanpadre
	rm -rf  .jupyter
	rm -rf  .carta

# -fin-

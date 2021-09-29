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

# -fin-

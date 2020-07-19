python node_program.py 1 100 3 "This is the big message sending to the node 3 through node 5 to test rerouting in case of node failure in between:" 15 2 5 4 &
python node_program.py 2 100 2 1 3 &
python node_program.py 3 100 3 2 5 4 &
python node_program.py 4 100 4 1 3 &
python node_program.py 5 25 5 1 3 &

python node_program.py 1 80 6 "Sending this message to the node 6 to test the rerouting in case of node failure. This is the test for node failure detection testing testing testing:" 15 2 7 3 &
python node_program.py 2 80 2 1 4 &
python node_program.py 3 80 3 1 5 &
python node_program.py 4 80 1 "Simple message for testing:" 10 2 6 &
python node_program.py 5 80 5 3 6 &
python node_program.py 6 80 6 4 5 7 &
python node_program.py 7 20 7 1 6 &

python node_program.py 0 100 0 1 4 &
python node_program.py 1 100 3 "This is the reroute testing when the destination is killed and the message is from node 1 to node 3. The up time of the node 2 is big so need bigger message to test the rerouting protocol. Hence the bigger sentence. Thank you!:" 5 0 2 &
python node_program.py 2 10 2 1 3 &
python node_program.py 3 100 3 4 2 &
python node_program.py 4 100 4 0 3 &

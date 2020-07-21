###### Python Version

       $ Python 2.7

#### DESCRIPTION

The Project aims at designing and implementing various layers of OSI
layer model. A python process representing a node constructs a network 
of nodes which can be controlled through the input arguments to the 
process. The process simulates various layers of OSI model, _Layer 5
(Application Layer), Layer 4 (creates datagram segments), Layer 3 
(IP packets; uses node ids to reach destination), Layer 2 (forms frames 
from IP packets; uses node ids for next hop), and Layer 1 (uses text 
files to communicate)._ Other functionalities of the node include, 
1) _byte stuffing_ to determine start and end bytes,
2) _forward error correction_ for error correction at the destination,
3) _shortest path detection_ to the destination,and
4) _node failure detection_; rerouting the message, in case of node failure.

#### Physical Layer:

The process communicates with other processes through _text files_ which
represents communication channels. **_Concurrent channel protocol_** is used 
to send messages to the other nodes.

The text file _file0to1.txt_ is the channel used by the source node **_0_** to 
send bytes to the destination node **_1_** and the _file1to0.txt_ is the channel
used by the source node **_1_** to send bytes to the destination **_0_**.

#### Datalink Layer:

The layer uses byte-stuffing(a.k.a byte insertion) to determine begin and end of
the frame. The beginning is indicated with letter _F_, the end with _E_. The 
datalink layer also makes sure that the messages are sent reliably to the next
hop. Thus, there are two types of datalink frames: _data_ messages and _ack_ messages. 
In addition, the layer use concurrent logical channels protocol to send frames.
It uses two logical channels. 

The data messages are sent as 

_F data x y \<netw layer message> E_

where _x_ is the channel number and _y_ is the sequence number.

#### Network Layer:

There are two types of network layer messages, _data_ messages and _routing_ messages. 
Data messages carry transport layer messages and are varying length. Routing messages 
are sent between neighbors to find the path between nodes which are of fixed length: 12 
bytes.

The messages follow the format:

_Routing_

_R 2 3 4 5 9 X X X X X X_

indicates that the path to reach 9 from 2 is 3 4 5 9

_Data message_

_D d \<trans layer message>_

_'d'_ is the destination id

#### Transport Layer:

Transport layer messages are limited in size, and hence, if the string is bigger, then the
string is divided into multiple transport messages.

The transport implements forward error correction protocol, i.e. for every pair of data messages
sent, we include XOR of the previous two data messages.

Data messages have the following format
1) 1 byte for message type: "D" for data
2) 1 byte source id (from "0" up to "9")
3) 1 byte destination id (from "0" up to "9")
4) 2 byte sequence number (from "00" to "99")
5) up to five bytes of data (i.e. up to five bytes of the string to be transported)

XOR messages have the following format
1) 1 byte message type, whose value is "X" for XOR
2) 1 byte source id (from "0" up to "9")
3) 1 byte destination id (from "0" up to "9")
4) 2 byte sequence number (it contains the sequence number of the even message in the pair)
5) up to five numbers (separated by a blank) in the range 0 .. 255, these correspond to the XOR of the
corresponding data bytes

The transport layer cannot send its messages until enough time has elapsed, which is indicated in
the arguments of the program.


#### INSTRUCTIONS
Python2 is used to develop the script. The instructions to run the script is as follows:

The python process acts as a router and a node or both depending on the running instructions.
The shell script _run.sh_ contains instructions that runs the program as a background process.

```python
   $ python node_program.py 1 80 6 "Message to send to destination" 15 2 7 3 &
```

The above instruction run python process as a node. 
1) the first argument _1_ defines its _node-id_ and the third argument _6_ defines the _destination
   node-id_ that the source _1_ is trying to send the message _""Message to send to destination"_.
2) the second argument _80_ describes the _up-time_ (alive time or running time of the node).
3) the _4 th_ argument or the string is the message to the destination.
4) the _5 th_ argument _15_ is the time after which the node or process starts sending the message to
the destination.
5) the remaining arguments instructs the neighboring nodes.

the instruction:

```python
   $ python node_program.py 2 80 2 1 4 &
```

creates the process with the node_id _2_ and neighbors _1,4_ that runs as a _router_ that forwards 
link layer messages to the neighbouring nodes. It also helps determine shortest path.

Running these instructions multiple times with different node_ids, creates a network with nodes and 
routers. 


#### IMPLEMENTATION

The script initially process the input arguments and creates a class object with all the variables and
then the _main()_ function is then executed. The main function performs the following tasks:

1) initializes the routing table with neighbor nodes. 
2) executes _network_send()_ function which executes the **RIP** protocol. 
3) inside the while loop, the main methods checks all the interface channels (text files) for incoming 
messages which is performed by the method _datalink_receive_from_channel()_. This method receives two types
of data, 
    1) _'data'_ messages which are sent to the network layer, if the message is intended for the same node.
     The method then responds with _ack_ message.```` 
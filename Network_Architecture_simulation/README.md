#### Python Version

    --- Python 2.7

#### Description:

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

##### Datalink Layer:

The layer uses byte-stuffing(a.k.a byte insertion) to determine begin and end of
the frame. The beginning is indicated with letter _F_, the end with _E_. The 
datalink layer also makes sure that the messages are sent reliably to the next
hop. Thus, there are two types of datalink frames: _data_ messages and _ack_ messages. 
In addition, the layer use concurrent logical channels protocol to send frames.
It uses two logical channels. 

The data messages are sent as 

_F data x y \<netw layer message> E_

where _x_ is the channel number and _y_ is the sequence number.

##### Network Layer:

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

##### Transport Layer:

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



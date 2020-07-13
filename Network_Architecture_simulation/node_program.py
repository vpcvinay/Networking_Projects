#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:38:57 2019

@author: vinay
"""

import time
import sys
import os
from numpy import array

class variables:
    def __init__(self):
        self.self_id = 0
        self.dest_id = 0
        self.timeout = 0
        self.message = 0
        self.sendtme = 0
        self.nghnode = 0
        self.position = dict()
        self.seq_no = 0
        self.channel = [False,False,False,False,False,False,False]
        self.output_buffer = []
        self.input_buffer  = []
        self.sent_message = dict()
        self.channel_buffer = dict()
        self.data_link_sq_num = 0
        self.ack_timeout = [0]*7
        self.transmit_rec_buffer = dict()
        self.transmit_rec_XOR_buffer = dict()
        self.route_table = dict()
        self.Time  =  time.time()
        
        
    def create_route(self):
        for node in self.nghnode:
            self.route_table.update({node:['X']})
            
        
def byte_stuff(msg):
    message = ''
    for char in msg:
        if char=='E' or char=='F':
            message+='X'+char
            
        elif char=='X':
            message+='X'+char
            
        else:
            message+=char
            
    return message

def remove_byte_stuff(msg):
    message=''
    prev = ''
    for char in msg:
        if char=='X' and prev=='X':
            message+=char
            prev = ''
            
        elif char=='X' and prev!='X':
            prev = char
            
        else:
            message+=char
            continue
        
    return message

def append_message(temp_msg,msg_type,msg):
    temp_msg.append(msg_type)
    temp_msg.append(var_obj.self_id)
    temp_msg.append(var_obj.dest_id)
    seq_no = "%02d" %var_obj.seq_no
    temp_msg.append(seq_no)
    transmit_msg = msg    
    temp_msg.append(transmit_msg)
    return temp_msg

def transport_send_string():
    size_of_msg = 5
    msg_type = ["D","X"]
    transmit_msg = ''
    packet_list = []
    count = 0
    even = True
    for char in var_obj.message:
        transmit_msg+=char
        count+=1
        temp_msg = []
        if count==size_of_msg:
            temp_msg = append_message(temp_msg,msg_type[0],transmit_msg)
            transmit_msg = ''
            count=0
            even = not even
            if even:
                prev_msg = packet_list[-1][-1]
                pres_msg = temp_msg[-1]
                XOR = []
                for prv,prs in zip(prev_msg,pres_msg):
                    xor = "%03d" % (ord(prv)^ord(prs))
                    XOR.append(xor)
                    
                temp_msg = append_message(temp_msg,msg_type[1],XOR)
                
            var_obj.seq_no+=1
            packet_list.append(temp_msg)
            
    else:
        yield False
        
    if transmit_msg:
        temp_msg = append_message(temp_msg, msg_type[0], transmit_msg)
        packet_list.append(temp_msg)
        
        
    while packet_list:
        trans_msg = packet_list.pop(0)
        network_receive_from_transport(trans_msg)
        yield True
        
    

# recieves data from the transport layer and sends to the datalink
def network_receive_from_transport(trans_msg):
    ntw_msg = []
    ntw_msg.append('D')
    ntw_msg.append(str(var_obj.dest_id))
    for data in trans_msg:
        if type(data)==list:
            for i in data:
                ntw_msg.append(str(i))
                
        else:
            ntw_msg.append(str(data))
            
    #print ntw_msg
    var_obj.output_buffer.append(ntw_msg)
    
def send_ack_msg(channel,seq_no,src,dest):
    message = ['F','ack',str(channel),seq_no,'E']
    #print "the ack message is ",message
    #filename = "file"+str(src)+"to"+str(dest)+".txt"
    #print "writing to file ",filename
    data_link_writer(src,dest,message)
    
    
def recover_message():
    for node in var_obj.transmit_rec_XOR_buffer:
        seq_xor_mes = var_obj.transmit_rec_XOR_buffer[node]
        seq_mes = var_obj.transmit_rec_buffer[node]
        for seq in sorted(seq_xor_mes):
            xor_bytes = seq_xor_mes[seq]
            msg_bytes = seq_mes[seq]
            prev_msg = ''
            for xor,pres_msg in zip(xor_bytes,msg_bytes):
                chk_msg = ord(pres_msg)^int(xor)
                chk_msg = chr(chk_msg)
                prev_msg+=chk_msg
                
            seq_mes.update({int(seq)-1:prev_msg})
            
        

def transport_output_all_received():
    recover_message()
    for node in var_obj.transmit_rec_buffer:
        seq_mes = var_obj.transmit_rec_buffer[node]
        filename = "node"+str(var_obj.self_id)+"received.txt"
        f_desc = open(filename,"a+")
        f_desc.write("From "+str(node)+" received: ")
        for seq in sorted(seq_mes):
            f_desc.write(seq_mes[seq])
            
        f_desc.write("\n")
        f_desc.close()
        
    #print "The transmit reciever buffer is and XOR buffer ",var_obj.transmit_rec_buffer,var_obj.transmit_rec_XOR_buffer

def transport_output_all_received_bk():
    for node in var_obj.transmit_rec_buffer:
        seq_mes = var_obj.transmit_rec_buffer[node]
        filename = "node"+str(var_obj.self_id)+"received.txt"
        f_desc = open(filename,"a+")
        f_desc.write("From "+str(node)+" received: ")
        for seq in sorted(seq_mes):
            f_desc.write(seq_mes[seq])
            
        f_desc.write("\n")
        f_desc.close()
        
    #print "The transmit reciever buffer is and XOR buffer ",var_obj.transmit_rec_buffer,var_obj.transmit_rec_XOR_buffer

    
def transport_receive_from_network(message):
    #msg = message
    source = message[1]
    seq_no = message[3:5]
    trans_msg = remove_byte_stuff(message[5:10])
    #print " the source {} seq_no is {} and the message at the transport layer is {}".format(source,seq_no,message)
    if(source not in var_obj.transmit_rec_buffer):
        var_obj.transmit_rec_buffer[source] = {}
        var_obj.transmit_rec_XOR_buffer[source] = {}
        
    var_obj.transmit_rec_buffer[source][int(seq_no)] = trans_msg
    if len(message)>11:
        XOR_msg = 'X'+message[10:]
        XOR_src = XOR_msg[1]
        XOR_seq_no = XOR_msg[3:5]
        XOR_Bytes = [int(''.join(k)) for k in array(list(XOR_msg[5:])).reshape(-1,3)]
        var_obj.transmit_rec_XOR_buffer[XOR_src][int(XOR_seq_no)] = XOR_Bytes
        
        #print " the XOR_source {} seq_no {} and the XOR_message is {} ".format(XOR_src,XOR_seq_no,XOR_Bytes)
        
    #print "The message dict is ",var_obj.transmit_rec_buffer
    

# Network layer which Recieves data from the datalink layer
def network_receive_from_datalink(message):
    cnt = 0
    #print "data reached the network layer from the data link ", message
    if message[cnt]=='D':
        cnt+=1
        if int(message[cnt])==var_obj.self_id:
            cnt+=1
            message = message[cnt:]
            #print "sending message to transport is ",message
            transport_receive_from_network(message)
            
        else:
            msg = list(message[0:5])+[message[5:7]]+[message[7:]]
            var_obj.output_buffer.append(msg)
            
def network_route(snd_rcv,msg=0,dest=0,node_path_for=0):
    if snd_rcv=="send":
        route_msg = []
        for dest_node in var_obj.nghnode:
            count = 0
            for node in var_obj.route_table:
                count+=1
                path = var_obj.route_table[node]
                if path[0]=='X':
                    route_msg = ['R',str(var_obj.self_id),str(node)]
                else:
                    path = list(map(str,path))
                    route_msg = ['R',str(var_obj.self_id)]+path+[str(node)]
                for _ in range(12-len(route_msg)):
                    route_msg.append('X')
                    
                route_msg.append(dest_node)
                var_obj.output_buffer.append(route_msg)
                
        #print "original route table is {} and number of route messages is {}".format(var_obj.route_table,count)
    elif snd_rcv=="recieve":
        route_msg = msg
        path = []
        for ch in route_msg:
            if ch=='R':
                continue
            
            if ch=='X':
                break
            
            else:
                path.append(int(ch))
                
        #route_src = path[0]
        route_dst = path.pop(-1)
        if route_dst == var_obj.self_id or (route_dst in var_obj.nghnode):
            pass
        
        else:
            if route_dst not in var_obj.route_table.keys():
                var_obj.route_table.update({route_dst:path})
                
            else:
                if var_obj.route_table[route_dst]==None:
                    var_obj.route_table[route_dst]=path
                    
                else:
                    prs_hops = len(var_obj.route_table[route_dst])
                    new_hops = len(path)
                    if new_hops<prs_hops:
                        var_obj.route_table[route_dst] = path
                        
    #print var_obj.temp
    #print "output buffer ",var_obj.output_buffer            


def datalink_receive_from_network(pck,ch_count,retransmit = False):
    src_id = str(var_obj.self_id)
    if len(pck)==2:
        dest_id = pck[0][1]
    else:
        dest_id = pck[1]
        
    if var_obj.route_table.get(int(dest_id)):
        if var_obj.route_table.get(int(dest_id)) == ['X']:
            if retransmit:
                seq_no = pck[-1]
                pck = pck[0]
            else:
                seq_no = "%02d" % var_obj.data_link_sq_num
                var_obj.data_link_sq_num+=1
                
            pck[6] = byte_stuff(pck[6])
            send_msg = ['F','data',str(ch_count),seq_no]+pck+['E']
            var_obj.channel[ch_count] = True
            var_obj.ack_timeout[int(ch_count)] = time.time()
            var_obj.channel_buffer.update({ch_count:[pck,seq_no]})
            #print send_msg
            data_link_writer(src_id,dest_id,send_msg)
            
        else:
            if retransmit:
                seq_no = pck[-1]
                pck = pck[0]
            else:
                seq_no = "%02d" % var_obj.data_link_sq_num
                var_obj.data_link_sq_num+=1
            
            var_obj.ack_timeout[int(ch_count)] = time.time()
            var_obj.channel_buffer.update({ch_count:[pck,seq_no]})
            dest_id = var_obj.route_table.get(int(dest_id))[0]
            send_msg = ['F','data',str(ch_count),seq_no]+pck+['E']
            var_obj.channel[ch_count] = True
            
            #print send_msg
            data_link_writer(src_id,dest_id,send_msg)
            
        success = True
    else:
        success = False
        
    return success


# Reads messages from the channel
def datalink_receive_from_channel(src_node,dest_node):
    pos = var_obj.position[src_node]
    #print "position is ",pos
    recieve_message = data_link_reader(src_node,dest_node,pos)
    if recieve_message:
        for packet in recieve_message:
            if packet=='\n':
                break
            if packet[0]=='R':
                network_route("recieve",msg=packet)
                continue
            
            msg = ''
            start_byte = 0
            end_byte = 3
            #print "recieved packet ",packet
            char = packet[start_byte:end_byte]
            msg+=char
            if msg=='ack':
                char = packet[end_byte]
                var_obj.channel[int(char)] = False
                var_obj.ack_timeout[int(char)] = 0
                if var_obj.channel_buffer.get(int(char)):
                    del var_obj.channel_buffer[int(char)]
                end_byte+=1
                char1,char2 = packet[end_byte],packet[end_byte+1]
                var_obj.ack_sq_num = int(char1+char2)
                #print "ack message recieved for channel ",int(char)
                continue
            
            msg+=packet[end_byte]
            if msg=='data':
                end_byte+=1
                channel = int(packet[end_byte])
                end_byte+=1
                seq_no = "%02d" % int(packet[end_byte]+packet[end_byte+1])
                end_byte+=2
                send_ack_msg(channel,seq_no,dest_node,src_node)
                network_msg = packet[end_byte:]
                network_receive_from_datalink(network_msg)
                #print "sending ack for channel {}, seq_no {} ".format(channel,seq_no)
                continue
                

def data_link_reader(src_node,dest_node,position):
    filename = "file"+str(src_node)+"to"+str(dest_node)+".txt"
    recieve_packets = []
    if os.path.isfile(filename):
        f_desc = file(filename,'r+')
        #print "reading file ",filename
        f_desc.seek(position)
        msg = ''
        prev_chr = ''
        while True:
            ch = f_desc.read(1)
            if (ch=='' or (ch=='E' and prev_chr!='X') or (ch=='F' and msg=='')):
                if ch=='E':
                    recieve_packets.append(msg)
                    msg = ''
                    prev_chr = ''
                    continue
                elif ch=='F':
                    continue
                
                elif ch=='' and msg:
                    recieve_packets.append(msg)
                    break
                else:
                    break
            
            elif ch=='X' and prev_chr!='X':
                prev_chr = ch
                continue
            
            elif ch=='R' and not msg:
                msg+=ch
                for _ in range(11):
                    ch = f_desc.read(1)
                    msg+=ch
                    
                recieve_packets.append(msg)
                msg = ''
                continue
            
            msg+=ch
            
            if ch=='X' and prev_chr=='X':
                prev_chr = ''
              
            else:
                prev_chr = ch
        
        var_obj.position.update({src_node:f_desc.tell()})
        f_desc.close()
        
    else:
        #print "Error opening file ",filename
        pass
    
    return recieve_packets


def data_link_writer(src_id,dest_id,message):
    filename = "file"+str(src_id)+"to"+str(dest_id)+".txt"
    f_desc = file(filename,"a+")
    for ch in message:
        f_desc.write(ch)
    f_desc.close()
    

def main(var_obj):
    var_obj.create_route()
    trans_gen = transport_send_string()
    str_time = time.time()
    ch_count = 0
    no_of_times_rt_sent = 0
    rTime = time.time()
    network_route("send")
    var_obj.output_buffer = []
    failed_pcks = []
    #print "in main function ",var_obj.position
    while (time.time()-str_time)<=var_obj.timeout:
        #time_count = time.time()
        for node in var_obj.nghnode:
            #print "Neighbour Nodes ",node
            datalink_receive_from_channel(node,var_obj.self_id)
            
        if failed_pcks:
            var_obj.output_buffer.append(failed_pcks)
            failed_pcks = []
            
        #print "temp dict ",var_obj.temp
        if var_obj.output_buffer: # the message in output buffer comesa as list
            #print "The output Buffer is {} at time {} ".format(var_obj.output_buffer,time.time()-str_time)
            while var_obj.output_buffer:
                if not var_obj.channel[ch_count]:
                    pck = var_obj.output_buffer.pop(0)
                    #print "sending packet {} from the node is".format(pck,var_obj.self_id)
                    if pck[0]=='D':
                        success = datalink_receive_from_network(pck,ch_count)
                        if not success:
                            failed_pcks.append(pck)
                            ch_count-=1
                        try:
                            if (time.time()-var_obj.Time)>=float(var_obj.sendtme):
                                sc = next(trans_gen)
                            
                        except StopIteration:
                            pass
                        
                    elif pck[0]=='R':
                        #print "sending the routing packet to the channel "
                        src_id = var_obj.self_id
                        node = pck.pop()
                        data_link_writer(src_id,node,pck)
                
                ch_count+=1
                if ch_count>=7:
                    ch_count = 0
                    break
                   
        while True:
            count = 0
            try:
                if (time.time()-var_obj.Time)>=float(var_obj.sendtme):
                    sc = next(trans_gen)
                    count+=1
                    if count==6 or not sc:
                        break
                    
                else:
                    break
                
            except StopIteration:
                break
            
            
        if (time.time()-rTime)>=5:
            #print "rTime is {} and time.time()-rTime is {} ".format(rTime,time.time()-rTime)
            #print "sending route message at ",time.strftime("%H:%M:%S",time.gmtime())
            rTime = time.time()
            #print "rTime is {} and time.time()-rTime is {} after update ".format(rTime,time.time()-rTime)
            no_of_times_rt_sent += 1
            network_route("send")
            
        for chn_no in range(7):
            if (time.time()-var_obj.ack_timeout[chn_no])>=5 and var_obj.channel and var_obj.ack_timeout[chn_no]!=0:
                #print "output_buffer before timeoout is ",var_obj.output_buffer
                pck = var_obj.channel_buffer[chn_no]
                success = datalink_receive_from_network(pck,chn_no,retransmit=True)
                if not success:
                    failed_pcks.append(pck)
                
                #print "output_buffer after timeoout is ",var_obj.output_buffer
                var_obj.ack_timeout[chn_no] = time.time()
                
            else:
                continue
                
        #print "spent Time is ",time.time()-str_time
        #print "The routing table at {} is {}".format(var_obj.self_id,var_obj.route_table)
        time.sleep(1)
    transport_output_all_received()
    #print "number of times routes sent ",no_of_times_rt_sent
    #print "output buffer is {} ",var_obj.output_buffer

if __name__=="__main__":
    var_obj = variables()
    if sys.argv[1]!=sys.argv[3]:
        var_obj.self_id = int(sys.argv[1])
        var_obj.dest_id = int(sys.argv[3])
        var_obj.timeout = float(sys.argv[2])
        var_obj.message = str(sys.argv[4])
        var_obj.sendtme = float(sys.argv[5])
        var_obj.nghnode = list(map(int,sys.argv[6:]))
        for node in var_obj.nghnode:
            var_obj.position.update({node:0})
            
    else:
        var_obj.self_id = int(sys.argv[1])
        var_obj.dest_id = int(sys.argv[3])
        var_obj.timeout = float(sys.argv[2])
        var_obj.message = ''
        var_obj.sendtme = 0
        var_obj.nghnode = list(map(int,sys.argv[4:]))
        for node in var_obj.nghnode:
            var_obj.position.update({node:0})
            
    main(var_obj)
    
    

#! /bin/bash

function local_port(){
    # port local port 14007 to remote machine localhost:2002
    ssh -i ~/.ssh/key.pem -L 14007:localhost:2002 -N user@ip
    # nohup ssh -i ~/.ssh/key.pem -L 14007:localhost:2002 -N user@ip 2>&1 &
}

#! /bin/bash
# http://297020555.blog.51cto.com/1396304/494315
function pb1() {
    b='' 
    for ((i=0;$i<=100;i+=2))  
    do  
        # width of b is half of 100
        printf "progress:[%-50s]%d%%\r" $b $i  
        sleep 0.1  
        b=#$b  
    done  
    echo
}

pb2() {
    i=0 
    while [ $i -lt 20 ]  
    do  
       ((i++))  
       echo -ne "=>\033[s"  
       echo -ne "\033[40;50H"$((i*5*100/100))%"\033[u\033[1D"  
       sleep 5
    done  
    echo 
}

pb1

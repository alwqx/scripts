#! /bin/bash
# ./sslocal.sh ss_pass

ss_port=443
#ss_pass=
ss_methon=rc4-md5
sudo sslocal -s sdzx -p $ss_port -k $1 -m $ss_methon -d start

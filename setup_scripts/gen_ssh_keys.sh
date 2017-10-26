!#/bin/bash
echo "[Hint] Empty passphrase!"


ssh-keygen -t rsa -C "ddatta@vt.edu"
cd ~/.ssh
echo "--------------------"
echo " Please copy the output (next line) , and place it in the SSh keys box . Got it Einstien ?"
echo "--"
cat ~/.ssh/id_rsa.pub
echo "--"
echo "Set up done. Lets wreak havoc!" 

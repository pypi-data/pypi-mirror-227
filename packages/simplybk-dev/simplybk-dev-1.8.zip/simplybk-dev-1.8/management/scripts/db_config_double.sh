sudo fdbcli --exec "configure FORCE double" --timeout 100
sleep 10
sudo fdbcli --exec "coordinators auto" --timeout 100
sleep 5
sudo fdbcli --exec "coordinators auto" --timeout 100
sleep 2
docker exec -it powerbarcoder bash
cd main/
bash powerBarcode.sh 202412251551


bash fileLister.sh 202412171609
bash fileLister_raw.sh 202412171609


sudo apt-get -y install util-linux

docker stop powerbarcoder
docker rm -f powerbarcoder
docker rmi powerbarcoder
docker build -t powerbarcoder .
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder powerbarcoder
docker exec -it powerbarcoder bash

#if WSL ext4.vhdx too large, run this command to shrink it
docker builder prune
wsl --shutdown
diskpart
select vdisk file="C:\Users\kwz50\AppData\Local\Docker\wsl\data\ext4.vhdx"
select vdisk file="C:\Users\kwz50\AppData\Local\Docker\wsl\disk\docker_data.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
wsl


git pull origin feature-gbifDataPaper_20240202

docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder --cpus=8 powerbarcoder
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder --restart=unless-stopped --cpus=8 powerbarcoder

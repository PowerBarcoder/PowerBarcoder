cd /home/lykuo/lab_data2/miseq/PowerBarcoder
git pull origin feature-gbifDataPaper_20240202
docker stop powerbarcoder
docker rm -f powerbarcoder
docker rmi powerbarcoder
docker build -t powerbarcoder .
docker run -d -p 5000:5000 -v ${PWD}:/PowerBarcoder --name powerbarcoder powerbarcoder
docker exec -it powerbarcoder bash

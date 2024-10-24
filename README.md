# Kawaii-donis

A simple web app to make Adonis a cute kawaii, by giving him a pretty blush, 2 cute little hearts and of course the mandatory bunny ears. 
Access it directly on the link, or deploy it on your own. 


The online application is going to be slower compared when deployed locally. The VM has only 2GB of RAM so it could take some time to process the image. 
The larger the photo and more the faces it would take longer to load. 


## Training

The training can be found under the `/training` folder.  It contains the code `trainer.py`, the final model is in the `model` directory and there are 3 test images inside the `media` folder. The training data is not there for an obvious reason, starting from copy and ending in rights. Just place your model images inside the model folder, run the script, and the pickle file will be ready to use. 


## Web Application

The whole thing is made into a web app inside the `/server` fodler, and can be easily build and run using `docker-compose`. The whole setup is composed of 3 parts, which they work togather.

#### nginx
The server runs as a reverse proxy, and sends the reqeusts where its needed per case


#### Web
The react front-end of the application, all the cute nice animations, where your little eyes can indulge. 

#### App
The fast-api backend of the application, where all the logic happens. It does the processing and send the modified image back to the front-end.


### Build

`sudo docker compose up --build`

This will take some time, mainly because of the python libraries, but after running it, you can access the web app on localhost, port 80. It currently offers no SSL, if you want ssl, you can either modify nginx to have a ceritifcate, or deploy it behind Cloudflare. 
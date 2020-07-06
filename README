# A minimal web application that supports both a simple REST API and web forms for finding photos.

## Features
 - search photo using `GET`: endpoint api/v1/search
 - filter photo using search params (color, orientation), e.g. api/v1/search?color=red
 - supported color values are black_and_white, black, white, yellow, orange, red, purple, magenta, green, teal, and blue.
 - supported orientation values are landscape, portrait, squarish
 - use a web search-form to find a photo. (from your browser go to http://127.0.0.1:8000/)


## Install

### Get the app

 - $ `git clone https://github.com/nmakro/unsplash-api.git`

### Create a free account in unsplash.com to use the access and secret keys provided. Edit the docker-compose.yml with your keys.

### Run the application
$ `docker-compose up`

## Use

#### Fetch Single Product
$ `http://127.0.0.1:5000/api/v1/search?orientation=landscape`

```json
{
    "message": "Click on the link provided to view a thumbnail of the photo",
    "thumb_url": "http://localhost:5000/static/ojLZ1Zfghlg.jpeg"
}
```
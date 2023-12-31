## Content Publisher

This project cross social media platform, highly configurable,generic publisher system, which take media from one social media to anthor, i.e  upload reels to instagram from youtube

### Prerequisites

- Social media creds


### Installation

1. Clone the repository:

```bash
git clone https://github.com/RaviBalas/contentpublisher.git
```

2. Set your environment variable

```bash
REDIS_HOST
REDIS_PORT
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DJ_DB
BACKEND_PUBLIC_URL="www.abc.com" # backend hosted  url or ngrok url
```
3. Build docker image

```bash
docker compose build .
```
4. Run  code in docker container
```bash
docker compose up
```

### Initial Configuration
To set up your initial configuration:

### Generate a YouTube API Key

1. Set up a Google Developers Console project and enable the YouTube Data API:

   a. Go to the [Google Developers Console](https://console.developers.google.com/).
   
   b. Create a new project by clicking the project drop-down menu, then click "New Project" and fill in the required fields, or select an existing project from the list.
   
   c. In the Dashboard, click on "Enable APIs and Services" and search for the "YouTube Data API v3". Click on it and then click the "Enable" button.
   
   d. Create an API key by going to "Credentials" in the left-hand menu, then click on "Create credentials" > "API key".

2. During the initial configuration process, you'll be prompted to input your YouTube API key. Enter the key when prompted.

## Usage

###  



```bash
docker compose build
```

```bash
docker compose up 
```

Depending on the selected configuration options, this will scrape reels and shorts, store them in the `downloads` folder, and post them to your Instagram account at the specified interval.


## Contributing

To contribute to this project, submit pull requests or open issues with your suggestions and ideas.

## License

Content publisher is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to all developers who contributed to the libraries used in this project.

## Additional Features

1. Reels and shorts scheduling: Schedule specific reels and shorts to be posted at certain times or dates.
2. Custom captions: Add custom captions to each reel or short when posting.
3. Multiple social platform Support for posting reels and shorts to multiple social accounts. 

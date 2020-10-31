# imgur2pdf
Download an Imgur album to a PDF file

## Set up

1. Install `imgur2pdf`
    ```sh
    pip install imgur2pdf
    ```
1. Create your Imgur API credentials: https://api.imgur.com/oauth2/addclient
1. Save the crendentials in `~/.imgur/config.ini`
    ```ini
    [imgur2pdf]
    client_id = xxxxxxxxxxxxxxx
    client_secret = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

## Usage

```sh
imgur2pdf ALBUM_ID
```

Find the `ALBUM_ID` in the URL: https://imgur.com/gallery/ALBUM_ID

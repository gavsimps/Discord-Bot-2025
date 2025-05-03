# GardenBot - Testing Capabilities of a Discord Bot

## Initial Setup
- clone this repository into whatever directory you choose
- pip install -r 'requirements.txt'
- Then ffmpeg is needed:
-   Windows OS: Download latest stable release and put `ffmpeg.exe` into C:\Users\{user}\AppData\Local\Programs\Python\Python313\Scripts
-   Linux OS: `sudo apt install ffmpeg`


Check this later for no downloads: https://stackoverflow.com/questions/57688808/playing-music-with-a-bot-from-youtube-without-downloading-the-file

## Functions and Feature
 - Bot returns a random message when mentioned in ANY text channel
 - Has a 1 in 5 chance to delete the message of a unique individual whenever they post
 - A refresh command to restart the bot from discord (admin only)
 - Disconnect a random user from any voice channel
 - Time users out
 - When a unique individual joins a voice call, bot messages main text channel for announcement
 - Shows a user's Discord statistics with properties for more in depth viewing
 - Shows the host server stats
 - Rudimentary youtube video downloading and playing 

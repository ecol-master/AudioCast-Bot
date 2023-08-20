start-text = 
    Hello!.

    This is a bot that will help you turn a YouTube video into a full-fledged podcast for background listening.

    Use the /help command to get help on using the bot.

help-text = 
    Help for using the bot:
        /menu - get my action menu
        /cancel - cancel the last command

    Send a video link and get the extracted audio track to listen in the background.

    Due to the large number of spam bots, restrictions have been set:
         - you can download podcasts every 3 minutes
         - maximum podcast duration 2 hours and 30 minutes.

cancel-text = 
    The last action is undone.

admin-statistic-text = 
    Information on using the bot:

     Number of registered users: <b>{ $all_users }</b>
     Number of active users in the past day: <b>{ $last_day_users }</b>
     Weekly Active Users: <b>{ $last_week_users }</b>
     Monthly Active Users: <b>{ $last_month_users }</b>

     Total number of downloaded podcasts: <b>{ $all_podcasts }</b>

no_url_in_message-text = 
    There is no video link in your message.

dowload_podcast_is_no_ability-text =
    You can download podcasts once every 3 minutes.

load_message-text = 
    Downloading...🕔

download_audio_error-text = 
    Check your video url!

duration_limit_error-text = 
    This podcast is too long.
    Max podcast duration 2 hours and 30 minutes


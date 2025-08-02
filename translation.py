class Translation(object):
    START_TEXT = """<u>Hello there 👋</u>
    
<b>I am a very-special URL Uploader Bot!</b>

<i>I can specially upload various kind of direct link formats such as,</i>
    1. m3u8(Many m3u8 format support has been specially added!)
    2. mp4
    3. Google drive links (If link is public)
    4. Youtube links
    5. Seedr links
    6. Zoom recording links (Even the recording is password protected!)
    7. Mediafire links
    8. Mega links.
    and many other direct links!...🥳

<b>I can download links which are bigger than 2GB too! 😍</b>

<i>You have the ability to set custom captions and custom thumbnails for your uploads too!</i>

<b>So what are you waiting for!...</b>

<b>Send me a direct link and I will upload it to telegram as a file/video.</b>

⭕️ Press /help for detailed instructions...
    <b>Created with ❤️ by @xmysteriousx</b>
"""
    RENAME_403_ERR = "Sorry. You are not permitted to rename this file."
    ABS_TEXT = " Please don't be selfish."
    UPGRADE_TEXT = "<b>Plan:</b> Free User!. \n<b>Unlimited Plan</b>"
    FORMAT_SELECTION = "<b>If you haven't set a thumbnail before you can send a photo now. If you don't want to don't worry - You will get an auto genarated thumnail from the video to your upload.😇</b>"
    SET_CUSTOM_USERNAME_PASSWORD = """\n📭 𝗦𝗲𝗹𝗲𝗰𝘁 𝗔𝗻𝗱 𝗖𝗵𝗼𝘀𝗲 𝗬𝗼𝘂𝗿 𝗙𝗼𝗿𝗺𝗮𝘁👇\n(If your link is a video and if you want it as a streamable video select a video option. If you want your upload in document format select a file option)\n\n<b>Don't select other format options if it shows any!</b>"""
    NOYES_URL = "@robot URL detected. Please use https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
    DOWNLOAD_START = "<b>Downloading to my server now 📥</b> \n\n<code>Please wait uploading will start as soon as possible😇...</code>"
    UPLOAD_START = "<b>Uploading to Telegram now 📤...</b>"
    RCHD_BOT_API_LIMIT = "size greater than maximum allowed size (50MB). Neverthless, trying to upload."
    RCHD_TG_API_LIMIT = "<b>Downloaded in {} seconds.</b>\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 2GB due to Telegram API limitations."
    AFTER_SUCCESSFUL_UPLOAD_MSG = "<b>𝗧𝗵𝗮𝗻𝗸𝘀 𝗙𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗧𝗵𝗶𝘀 𝗦𝗲𝗿𝘃𝗶𝗰𝗲, 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗧𝗼 @botzupdate 𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗔𝗺𝗮𝘇𝗶𝗻𝗴 𝗕𝗼𝘁𝘀</b>"
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "Downloaded in <b>{}</b> seconds.\n\nUploaded in <b>{}</b> seconds.\n\n<b>Thanks For Using This Free Service, Subscribe To @botzupdate For More Amazing Bots</b>"
    NOT_AUTH_USER_TEXT = "Please /upgrade your subscription."
    NOT_AUTH_USER_TEXT_FILE_SIZE = "Detected File Size: {}. Free Users can only upload: {}\nPlease /upgrade your subscription."
    SAVED_CUSTOM_THUMB_NAIL = "𝗖𝘂𝘀𝘁𝗼𝗺 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗜𝘀 𝗦𝗮𝘃𝗲𝗱. 𝗧𝗵𝗶𝘀 𝗜𝗺𝗮𝗴𝗲 𝗪𝗶𝗹𝗹 𝗕𝗲 𝗨𝘀𝗲𝗱 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗡𝗲𝘅𝘁 𝗨𝗽𝗹𝗼𝗮𝗱𝘀 📁.\n\nIf you want to delete it send\n /deletethumbnail anytime!"
    DEL_ETED_CUSTOM_THUMB_NAIL = "𝗖𝘂𝘀𝘁𝗼𝗺 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗖𝗹𝗲𝗮𝗿𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ❌.\nYou will now get an auto generated thumbnail for your video uploads!"
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "Media Cleared Succesfully ❌."
    SAVED_RECVD_DOC_FILE = "𝗗𝗼𝗰𝘂𝗺𝗲𝗻𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 📁."
    CUSTOM_CAPTION_UL_FILE = " "
    NO_CUSTOM_THUMB_NAIL_FOUND = "No Custom ThumbNail found."
    NO_VOID_FORMAT_FOUND = "<b>I think you have entered an unaccessible url or a private url.</b>\n<i>Go check if you can access the content in the url from your browser first!</i>\n\nIf you have any problem contact @botzupdate\n<b>YouTubeDL</b> said: {}"
    USER_ADDED_TO_DB = "User <a href='tg://user?id={}'>{}</a> added to {} till {}."
    CURENT_PLAN_DETAILS = """Current plan details
--------
Telegram ID: <code>{}</code>
Plan name: <a href='tg://user?id={}'>{}</a>
Expires on: {}"""
    
    HELP_USER = """💫 <u>I am X-Uploader Robot</u> ✨
 
<b>A detailed (simple) guide for using me:-</b>
 
<b>1. Send url</b>

If you want a custom caption on your video/file send the name/text you want to set on the video/file in the following format. 👇

<b>Link * caption without Extension.</b> 
[Separate the link and the caption name with "*" mark.]

Example:- 𝚑𝚝𝚝𝚙𝚜://𝚠𝚠𝚠.𝚠𝚎𝚋𝚜𝚒𝚝𝚎.𝚌𝚘𝚖/𝚟𝚒𝚍𝚎𝚘.𝚖𝚙𝟺 * 𝚌𝚊𝚙𝚝𝚒𝚘𝚗 𝚝𝚎𝚡𝚝

☣️ Tʜᴇ ᴄᴀᴘᴛɪᴏɴ/ᴛᴇxᴛ ʏᴏᴜ ᴛʏᴘᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ sᴇᴛ ᴀs ᴛʜᴇ ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ ᴏғ ᴛʜᴇ ᴜᴘʟᴏᴀᴅᴇᴅ ғɪʟᴇ.😇

<i>Note:- You can change/add any caption later if you want as explained in the end. 🥰</i>

<b>2. Then send Custom Thumbnail when asked while uploading the url.</b> <i>(This step is Optional)</i> 

💠 It means it is not necessary to send an image to include as an thumbnail.
If you don't send a thumbnail the video/file will be uploaded with an auto genarated thumbnail from the video.
The thumbnail you send will be used for your next uploads!

press /deletethumbnail if you want to delete the previously saved thumbnail.
(Then the video will be uploaded with an auto-genarated thumbnail!)

<b>3. Select the button.</b>
   Video-option :- Give Video/file in video format
   File-option :- Give video/file in file format
   
<b>Special feature:- Set caption to any file you want!</b>

☣️ Select an uploaded file/video or forward me <b>Any Telegram File</b> and Just write the text you want to be on the file as a reply to the File by selecting it (as replying to a message😅) and the text you wrote will be attached as caption!😍

Ex:- <a href="https://telegra.ph/file/2177d8611f68d63a34c88.jpg">Send Like This! It's Easy🥳</a>

<b>Note</b> :- You can download links which are bigger than 2GB from me too! Due to telegram API limits I can't upload files which are bigger than 2GB so I will split such files and upload them to you!

<b><u>Method to upload zoom normal and password protected links:-</u></b>

- If your zoom recording url is not password protected just send the normal zoom recording share link to the bot - (Do not send the 'ssrweb' url. Just send the normal recording share link.)

- If your zoom recording link is password protected send the link in the following way👇

<b>zoom link | passcode</b>
[Separate the link and the passcode with "|" mark.]

<b>Notes:-</b>

❇️ The zoom link should be the normal recording share url (not a 'ssrweb' url)

❇️ This 👉 '|' is a symbol which you can find in a mobile keyboard. (Not Capital I letter or simple l letter😅)
You will not be able to find it in a pc keyboard😕
But do not worry 😇 If you want to copy it tap on this symbol
👇
<code>|  (Tap on it to copy)</code>

<i>⚠️ If your zoom recording link requires a registration before watching you will need to send a cookie link to the bot. 
The feature is already added to the bot but it is little hard and takes time to explain you about exporting cookies🥵

(In short install cookies txt chrome extension, go to your recording link, enter the registration details that are asked before watching the recording, enter the passcode if it requires, click on the extension icon, export the cookies.txt file, send it to a direct file link bot, get the direct link of the cookie file.

After that send the links to the bot in this format👉 zoom link*cookie link )</i>

<b>Created with ❤️ by</b> <b><i>@xmysteriousx</i></b>
"""
    BANNED_USER_TEXT = """Hi **{}!!!**, Congratulations 😂 You Are Now Banned"""
    ABOUT_USER = """<b>○ My Name : 𝗠𝘆𝘀𝘁𝗲𝗿𝗶𝗼𝘂𝘀 𝗨𝗽𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁</b>
<b>○ Creator :</b> <a href='https://t.me/xmysteriousx/'>xmysteriousx</a>
<b>○ Credits :</b> <code>Everyone in this journey</code>
<b>○ Language :</b> <a href='https://docs.pyrogram.org/'>Python3</a>
<b>○ Library :</b> <code>Pyrogram asyncio 0.16.1</code>
<b>○ Source Code :</b> <a href='https://t.me/botzupdate/'>👉 CLICK HERE 👈</a>
<b>○ Server :</b> <code>Heroku</code>
<b>○ Build Status :</b> <code>V5 [+0.4]</code>"""

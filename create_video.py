from moviepy.video import *
from moviepy.editor import *
import moviepy.editor as mp
import subprocess
##################################################################################################

#ABSOLUTE_PATH = ""
ABSOLUTE_PATH = "/home/hazdev/quote_creator_website_live/"

##################################################################################################
def render_video_finesstv(linkurl, trim_start, trim_end):
    clip_start = int(trim_start)
    #IMPORT VIDEO

    #subprocess.check_call(["python3.6", "/home/hazdev/quote_creator_website_live/twitter2mp4.py", linkurl, "-fn", "finesstv"])

    tweet_url = str(linkurl)
    cmd = "python3.6 /home/hazdev/quote_creator_website_live/twitter2mp4.py " + tweet_url + " -fn finesstv"
    p = subprocess.Popen(["python3.6", "/home/hazdev/quote_creator_website_live/twitter2mp4.py", linkurl, "-fn", "finesstv"])
    p.kill()

    original_clip = mp.VideoFileClip(ABSOLUTE_PATH + "videos/finesstv.mp4").margin(20, color=(255,255,255))
    if trim_end != "":
        clip_end = int(trim_end)
        if clip_end > clip_start:
            original_clip = original_clip.subclip(clip_start, trim_end)
    elif trim_end == "":
        original_clip = original_clip.subclip(clip_start, original_clip.duration)

    (oc_width, oc_height) = original_clip.size

    #BLANK VIDEO
    blank_clip = mp.VideoFileClip(ABSOLUTE_PATH + "static/blank.mp4").set_duration(original_clip.duration)

    #CHANGE SIZE OF VIDEO
    if oc_width > oc_height:
        resized_clip = original_clip.resize(width=720)
    elif oc_width < oc_height:
        resized_clip = original_clip.resize(height=720)
    else:
        resized_clip = original_clip.resize(width=720)
    #NEW HEIGHT
    r_weight, r_height = resized_clip.size

    #BAD WAY TO GET CAPTION HEIGHT (LOAD IT IN TWICE)
    caption_temp = (mp.ImageClip(ABSOLUTE_PATH + "static/captions/finesstv.jpg").set_duration(original_clip.duration).resize(width=700))
    c_height = caption_temp.h

    #RESIZE IF STUFFS TOO BIG!
    if c_height + r_height > 720:
        blank_clip = blank_clip.resize((720, 864))
        #RESIZE VIDEO CLIP
        resize_video_size = blank_clip.h - c_height
        resized_clip = resized_clip.resize(height=resize_video_size)
        #NEW HEIGHT
        r_weight, r_height = resized_clip.size

    #WHAT Y FOR CAPTION
    def calculate_caption_pos():
        if c_height + r_height < 720 or c_height + r_height == 720:
            content_height = c_height + r_height
            top_content = (720 - content_height)/2
            return top_content
        elif c_height + r_height > 720:
                top_content = 0
                return top_content

    #CAPTION
    caption = (mp.ImageClip(ABSOLUTE_PATH + "static/captions/finesstv.jpg")
        .set_duration(original_clip.duration)
        .resize(width=700)
        .set_pos((0,calculate_caption_pos())))
    #WATERMARK
    watermark = (mp.ImageClip(ABSOLUTE_PATH + "static/watermarks/finesstv_big.png")
        .set_duration(original_clip.duration)
        .resize(height=115))

    #VIDEO Y POSITION
    def calculate_video_pos():
        return calculate_caption_pos() + c_height

    #STUFF
    watermark_y = calculate_video_pos() + (r_height*0.75)
    watermark_w = watermark.w
    final_duration = original_clip.duration

    #RENDER
    render = CompositeVideoClip([
        blank_clip,
        resized_clip.set_position(("center",calculate_video_pos())),
        caption,
        watermark.set_pos(lambda t: (720-((t/final_duration)*720 + watermark_w), watermark_y))
        ]).set_duration(original_clip.duration)
    render.write_videofile(ABSOLUTE_PATH + "static/renders/finesstv.mov", codec="libx264", fps=30)

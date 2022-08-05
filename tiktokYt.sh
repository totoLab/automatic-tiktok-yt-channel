#!/bin/bash

BUILD_DIR="build"
BLUR_DIR="build/blur"
DOWNLOAD_DIR="build/raw_videos"
: <<'END_COMMENT'
END_COMMENT

if [[ ! -d "$DOWNLOAD_DIR" ]]; then
    mkdir -p "$DOWNLOAD_DIR"
fi

youtube-dl $(curl -s -H "User-agent: 'your bot 0.1'" "https://www.reddit.com/r/TikTokCringe/hot.json?limit=12" | jq '.' | grep url_overridden_by_dest | grep -Eoh "https:\/\/v\.redd\.it\/\w{4}") --output $DOWNLOAD_DIR/"%(title)s.%(ext)s" &&

if [[ ! -d "$BLUR_DIR" ]]; then
    mkdir -p "$BLUR_DIR"
fi

for f in $DOWNLOAD_DIR/*.mp4;
do
    new_name="${f##*/}"
    ffmpeg -i $f -lavfi '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16' -vb 800K $BLUR_DIR/$new_name ;
done

file_list_loc="$BUILD_DIR/file_list.txt"
if [ -f $file_list_loc ]; then
    > $file_list_loc 
else
    touch $file_list_loc
fi

for f in $BLUR_DIR/*.mp4;
do
    new_name="${f##*/}"
    echo "file 'blur/$new_name'" >> $file_list_loc 
done


ffmpeg -y -f concat -i $file_list_loc -vcodec copy -acodec copy final.mp4

./command.sh "final.mp4" "Complete test run 1"
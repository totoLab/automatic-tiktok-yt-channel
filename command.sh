titleDescr="Tiktok video compilation #$2"
python3 upload_video.py --file="$1" \
                        --title="$titleDescr" \
                        --description="$titleDescr" \
                        --keywords="tiktok,reddit,videos,funny" \
                        --category="24" \ # 24: entertainment
                        --privacyStatus="public"
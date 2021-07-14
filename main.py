import os
import discord
from datetime import datetime, timedelta

client = discord.Client()

# メンバーのボイスチャンネル出入り時に実行される処理
@client.event
async def on_voice_state_update( member, before, after ):
    # サーバーIDによる分岐
    if member.guild.id == os.environ.get('SERVER_ID') and ( before.channel != after.channel ):

        # 日本時間に合わせた状態の時刻を取得
        now = datetime.utcnow() + timedelta( hours = 9 )

        # 投稿するチャンネルIDを指定
        alert_ch = client.get_channel( os.environ.get('CHANNEL_ID') )

        # 入室通知
        if before.channel is None:
            msg = f':arrow_forward: [{now:%m/%d %H:%M}] {member.name}がチャンネル[{after.channel.name}]に入室'
            await alert_ch.send( msg )

        # 退出通知
        elif after.channel is None:
            msg = f':arrow_backward: [{now:%m/%d %H:%M}] {member.name}がチャンネル[{before.channel.name}]から退出'
            await alert_ch.send( msg )

client.run( os.environ.get('DISCORD_BOT_TOKEN') )
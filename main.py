import os
import discord
from datetime import datetime, timedelta
from os.path import join, dirname
from dotenv import load_dotenv

# 環境変数を取得
dotenv_path = join( dirname( __file__ ), '.env')
load_dotenv( dotenv_path )

SERVER_ID = os.environ.get('SERVER_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

client = discord.Client()

# メンバーのボイスチャンネル出入り時に実行される処理
@client.event
async def on_voice_state_update( member, before, after ):
    # サーバーIDによる分岐
    if member.guild.id == SERVER_ID and ( before.channel != after.channel ):

        # 日本時間に合わせた状態の時刻を取得
        now = datetime.utcnow() + timedelta( hours = 9 )

        # 投稿するチャンネルIDを指定
        alert_ch = client.get_channel( CHANNEL_ID )

        # 入室通知
        if before.channel is None:
            msg = f':arrow_forward: [{now:%m/%d %H:%M}] {member.name}がチャンネル[{after.channel.name}]に入室'
            await alert_ch.send( msg )

        # 退出通知
        elif after.channel is None:
            msg = f':arrow_backward: [{now:%m/%d %H:%M}] {member.name}がチャンネル[{before.channel.name}]から退出'
            await alert_ch.send( msg )

client.run( DISCORD_BOT_TOKEN )
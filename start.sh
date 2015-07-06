#! /bin/bash
echo "Starting HelpBot..."

if [ -n "$ADMINCHANNEL" ]; then
  sed -i "s,ADMINCHANNEL,$ADMINCHANNEL,g" /helpbot/rtmbot.conf
fi
if [ -n "$SLACKTOKEN" ]; then
  sed -i "s,SLACKTOKEN,$SLACKTOKEN,g" /helpbot/rtmbot.conf
fi
if [ -n "$ICONEMOJI" ]; then
  sed -i "s,ICONEMOJI,$ICONEMOJI,g" /helpbot/rtmbot.conf
fi
if [ -n "$SLACKBOTNAME" ]; then
  sed -i "s,SLACKBOTNAME,$SLACKBOTNAME,g" /helpbot/rtmbot.conf
fi
if [ -n "$REDISHOST" ]; then
  sed -i "s,REDISHOST,$REDISHOST,g" /helpbot/rtmbot.conf
else
  sed -i "s,REDISHOST,localhost,g" /helpbot/rtmbot.conf
fi
if [ -n "$REDISPORT" ]; then
  sed -i "s,REDISPORT,$REDISPORT,g" /helpbot/rtmbot.conf
else
  sed -i "s,REDISPORT,6379,g" /helpbot/rtmbot.conf
fi
if [ -n "$REDISKEY" ]; then
  sed -i "s,REDISKEY,$REDISKEY,g" /helpbot/rtmbot.conf
else
  sed -i "s,REDISKEY,halpchats,g" /helpbot/rtmbot.conf
fi
if [ -n "$REDISDB" ]; then
  sed -i "s,REDISDB,$REDISDB,g" /helpbot/rtmbot.conf
else
  sed -i "s,REDISDB,0,g" /helpbot/rtmbot.conf
fi
if [ -n "$REDISPASSWORD" ]; then
  sed -i "s,REDISPASSWORD,$REDISPASSWORD,g" /helpbot/rtmbot.conf
else
  sed -i "/REDISPASSWORD/d" /helpbot/rtmbot.conf
fi

exec python rtmbot.py

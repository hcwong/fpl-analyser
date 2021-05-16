require 'httparty'
require 'telegram/bot'
require 'time'
require 'dotenv'
Dotenv.load('../.env')

response = HTTParty.get('https://fantasy.premierleague.com/api/bootstrap-static/')
response_hash = JSON.parse(response.body)

next_gameweek_date_str = ''
response_hash['events'].each do |event|
  next_gameweek_date_str = event['deadline_time'] if event['is_next']
end

exit! if next_gameweek_date_str.empty?

next_gameweek_date = Time.parse(next_gameweek_date_str)
current_date = Time.now.utc
diff = (next_gameweek_date - current_date) / 3600

Telegram::Bot::Client.run(ENV['BOT_TOKEN']) do |bot|
  message = "Less than #{diff.ceil} hours to Gameweek deadline"
  if [23, 5, 2].include?(diff.floor)
    bot.api.send_message(chat_id: ENV['CHAT_ID'], text: message)
  end
end

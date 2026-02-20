require 'octokit'

client = Octokit::Client.new(access_token: ENV['GH_TOKEN'])

# Create the new branch
client.create_ref(
"andrew-wc-brown/Github-Examples", 
"heads/sdks", 
"3a652b86905ca4e7888f4898e1b6f5d957b2c926"
)
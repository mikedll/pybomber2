
net = require 'net'

turn_queue = []


server = net.createServer (socket) ->
  socket.write "Welcome to Mike's Server!\n\n"
  socket.on('data', (data) ->
    socket.write "Received...\n"
    console.log("Adding to queue.")
    player_input[player_input.length] = data
  )
  socket.on('end', () ->
    console.log "End of time"
    console.log( player_input.join(",") )
  )


server.listen( 1337, "127.0.0.1" )

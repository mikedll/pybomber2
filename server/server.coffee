
require.paths.unshift __dirname

_ = require 'underscore'
net = require 'net'
{ ServerState } = require 'server_state'

serverState = new ServerState() # new ServerState()

server = net.createServer (socket) ->

  socket.setEncoding('utf8')

  playerId = null

  socket.on('connect', () ->
    socket.write "You have started a PyBomber session.\n"
    playerId = serverState.addPlayer( socket )
    socket.write "Your ID is #{playerId}\n\n"
  )
  socket.on('data', (data) ->
    msg = data.replace(/\s+/, '')
    if serverState.isMove( msg )
      serverState.move(playerId, data)
    else
      switch msg
        when "start"
          serverState.start()
          console.log("Starting game")
        when "fin"
          serverState.finishGame()
          server.close()
        else
          error = "Unrecognized: #{data}"
          socket.write error
          console.log error

  )
  socket.on('end', () ->
  )


server.on('close', () ->
  console.log("Ending game")
)

server.listen( 1337, "127.0.0.1" )

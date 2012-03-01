
_ = require 'underscore'

class ServerState
  constructor: () ->
    @playerCount = 0
    @latestMove = {}
    @disabledAdds = false
    @connections = {}

  addPlayer: (socketConnection) ->
    return if @disabledAdds
    id = @playerCount
    @connections[ id ] = socketConnection
    @playerCount += 1

    console.log( "Added player #{id}" )
    id

  lockPlayers: () ->
    @disabledAdds = true

  isMove: (s) ->
    s in ["L", "R", "M", "A"]

  move: (id, move) ->
    throw "Illegal state: player tried to move despite player list not being locked" if !@disabledAdds
    throw "Illegal state: player sent move despite already having moved." if @latestMove[ id ]?
    @latestMove[ id ] = move

    @finishTurn() if _.values( @latestMove ).length == @playerCount

  finishTurn: () ->
    conn.write (JSON.stringify( @allMoves() )  + "\n" )for conn in _.values( @connections )
    @latestMove = {}

  finishGame: () ->
    conn.end("finnish\n") for conn in _.values( @connections )
    @connections = {}
    @latestMove = {}

  allMoves: () ->
    @latestMove[i] for i in [0...@playerCount]

  start: () ->
    @lockPlayers()
    conn.write "start\n" for conn in _.values( @connections )


  # s = new ServerState()
  # s.addPlayer()
  # s.addPlayer()
  # s.addPlayer()
  # s.addPlayer()

  # s.move( 3, "A" )
  # s.move( 0, "L" )
  # s.move( 2, "M" )
  # s.move( 1, "R" )

  # console.log( JSON.stringify( s.allMoves() ) == '["L", "R", "M", "A"]' )

exports.ServerState = ServerState


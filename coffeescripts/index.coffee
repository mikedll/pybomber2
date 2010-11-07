

IMAGES =
  img1: null,
  frames1: 6,
  w1: 32,
  h1: 32

sprite =
  frame: 0

fps = 20
dt = 0.20
state = 0
ctx = null

canvasTag = (id, w, h) ->
  '<canvas id=\"' + id + '\" width=\"' + w + '\" height=\"' + h + '\"></canvas>'

imdLoad = () ->
  IMAGES['img1'] = new Image()
  IMAGES['img1'].src = "up_strip.bmp"

main = () ->
  if state == 0
    console.debug(" 0 state ")
    ctx.fillText(" Hello Mike. Wars your image?", 500, 10)
    state += 1

  else if state == 1
    console.debug(" 1 state ")
    imdLoad()
    state += 1

  else if state == 2
    console.debug( " 2 state " )
    if IMAGES['img1'].complete
      state += 1
  else if state == 3
    console.debug( " 3 state " )
    ctx.clearRect( 0, 0, IMAGES['w1'], IMAGES['h1'] )
    ctx.drawImage( IMAGES['img1'],
                   sprite.frame * IMAGES['w1'],
                   0,
                   IMAGES['w1'],
                   IMAGES['h1'],
                   0,
                   0,
                   IMAGES['w1'],
                   IMAGES['h1'] )
    sprite.frame += 1
    sprite.frame %= IMAGES['frames1']

  else
    console.debug( " Unexpected state " )

init = () ->
  w = 800
  h = 500
  $("body").append( canvasTag( "main", w, h ) )
  ctx = $('#main')[0].getContext('2d')
  setInterval( main, dt * 1000 );

$( init )



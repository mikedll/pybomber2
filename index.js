

var IMAGES = { 
    img1: null,
    frames1: 6,
    w1: 104,
    h1: 150
 };

var sprite = {
    frame: 0
};

var fps = 20;

var dt = 0.20; // seconds
var state = 0;
var ctx = null;

function canvasTag( id, w, h ) {
    var c = '<canvas id=\"' + id + '\" width=\"' + w + '\" height=\"' + h + '\"></canvas>';
    return c;
}

function imgLoad() {
    IMAGES['img1'] = new Image();
    IMAGES['img1'].src = "file:///Users/michaelrivera/work/pybomber2/gb_walk.png";
}

function main() {    
    if( state == 0 ) {
	console.debug(" 0 state ");

	ctx.fillText( "Hello Mike. Wher's your image?", 500, 10 );

	state += 1;
    }
    else if ( state == 1 ) {
	console.debug(" 1 state ");
	imgLoad();
	state += 1;
    }
    else if ( state == 2 ) {
	console.debug( " 2 state " );
	
	if( IMAGES['img1'].complete )
	    state += 1;
    }
    else if ( state == 3 ) {
	console.debug( " 3 state ");

	ctx.clearRect( 0, 0, IMAGES['w1'], IMAGES['h1'] );
	ctx.drawImage( IMAGES['img1'], 
		       sprite.frame * IMAGES['w1'],
		       0,
		       IMAGES['w1'],
		       IMAGES['h1'],
		       0,
		       0,
		       IMAGES['w1'],
		       IMAGES['h1'] );

	sprite.frame += 1;
	sprite.frame %= IMAGES['frames1'];
    }
    else {
	console.debug( "Unexpected state >= 4 ");
    }    
}

$(function () {
      var w = 800, h = 500;
      $("body").append( canvasTag( "main", w, h ) );

      ctx = $('#main')[0].getContext('2d');

      setInterval( main, dt * 1000 );
});


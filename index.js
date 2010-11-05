
function canvasTag( id, w, h ) {
    var c = '<canvas id=\"' + id + '\" width=\"' + w + '\" height=\"' + h + '\"></canvas>';
    return c;
}

function imgLoad() {
    var img = new Image();
    img.src = "gb_walk.png";
    return img;
}

$(function () {
      var w = 800, h = 500;
      $("body").append( canvasTag( "main", w, h ) );

      var ctx = $('#main')[0].getContext('2d');
      var img = imgLoad();

      ctx.fillText( "Hello Mike. Wher's your image?", w / 2, 0 );
      ctx.drawImage( img, 0, 0, 200, 200, 0, 0, 200, 200 );

});


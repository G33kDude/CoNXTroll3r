$(function() {
	$.get('/images/CR.png'); // load the error image into memory, to indicate error if the server goes down
});

$(document).keydown(function(e){
	console.log(e.which);
	switch(e.which) {
		case 37: W(); break; // left
		case 38: N(); break; // up
		case 39: E(); break; // right
		case 40: S(); break; // down
		default: return; // exit this handler for other keys
	}
	e.preventDefault();
});

function move(kind, direction, amount, speed)
{
	if (!speed) {speed=100;}
	$.ajax({
		'type': 'POST',
		'url': '/move',
		'data': {'kind':kind, 'direction':direction, 'amount':amount, 'speed':speed},
		'success': check,
		'error': error,
		'dataType': 'text'
	});
}

function check(data) {if (data) {error();} else {success();}}
function success(){$("#c").attr("src","/images/CG.png");}
function error(){$("#c").attr("src","/images/CR.png");}

function NW(){move('pivot', 'left', degrees, speed);}
function N (){move('move', 'forward', distance, speed);}
function NE(){move('pivot', 'right', degrees, speed);}

function W (){move('spin', 'left', degrees, speed);}
function C (){success();}
function E (){move('spin', 'right', degrees, speed);}

function SW(){move('pivot', 'left', -degrees, speed);}
function S (){move('move', 'backward', distance, speed);}
function SE(){move('pivot', 'right', -degrees, speed);}

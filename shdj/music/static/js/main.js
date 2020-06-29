$(document).ready( function(){

	$(document).scroll( function() {
		if ($(document).scrollTop() > 70) {
			$('#upperwhite').fadeIn(100);
		} 
		if ($(document).scrollTop() < 30) {
			$('#upperwhite').hide(100);
		}

	});
	$(window).resize(function() {
		if($(window).width()< 544){
			$('#centerlink').css('margin', '0 auto');
			$('#centertime').css('margin', '0 auto');
	}
	});
	$('#button').mousedown( function () {
		$('#button').css('background', '#fa1111');
	});
	$('#button').mouseup( function () {
		$('#button').css('background', '#fa2356');
	});
	$('#link').change( function() {
		if ($('#link').val().slice(0, 24) == 'https://www.youtube.com/' || $('#link').val().slice(0, 17) == 'https://youtu.be/' ||  $('#link').val().slice(0, 20) == 'https://vk.com/video' || $('#link').val().slice(0, 26) == 'https://www.instagram.com/'){
		} else{
			if ($('#link').val() !== ''){
				$('#table').fadeIn(100);
				setTimeout(function(){$('#table').hide(100);},10000);
			}
		}
	});
	$('.timeof').change( function() {
		if ($('.timeof').val().indexOf(':') >= 1 && $('.timeof').val().indexOf(':') < 3) {
			var tospl = $('.timeof').val().split(':')
			if (tospl.length != 2) {
				$('#table').fadeIn(100);
				setTimeout(function(){$('#table').hide(100);},10000);				
			}
			var typetime;
			if (tospl.length == 2) {
				for (var i = tospl.length - 1; i >= 0; i--) {
					typetime = parseInt(tospl[i], 10);
					console.log(typetime);
					if (isNaN(typetime)) {
						$('#table').fadeIn(100);
						setTimeout(function(){$('#table').hide(100);},10000);						
					}
				}
			}
		} else {
			if ($('.timeof').val() != '') {
				$('#table').fadeIn(100);
				setTimeout(function(){$('#table').hide(100);},10000);
			}
		}
	});
	$('.timeto').change( function() {
		if ($('.timeto').val().indexOf(':') >= 1 && $('.timeto').val().indexOf(':') < 3) {
			var tospl = $('.timeto').val().split(':')
			if (tospl.length != 2) {
				$('#table').fadeIn(100);
				setTimeout(function(){$('#table').hide(100);},10000);				
			}
			var typetime;
			if (tospl.length == 2) {
				for (var i = tospl.length - 1; i >= 0; i--) {
					typetime = parseInt(tospl[i], 10);
					console.log(typetime);
					if (isNaN(typetime)) {
						$('#table').fadeIn(100);
						setTimeout(function(){$('#table').hide(100);},10000);						
					}
				}
			}
		} else {
			if ($('.timeto').val() != '') {
				$('#table').fadeIn(100);
				setTimeout(function(){$('#table').hide(100);},10000);
			}
		}
	});

});

/*c4302b*/
/*console.log('a');*/
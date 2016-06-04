$(document).ready(function() {
	$('.image.header.item').popup();
	$('.ui.left.sidebar').sidebar('setting', 'transition', 'slide along');
	// $('#test').html($('.pusher').height());
	// $('.pushable').css('height', $('.pusher').height());
	$('.dropdown').dropdown({
		transition: 'drop'
	});
	
});


function toggleSidebar() {
	$('.ui.left.sidebar').sidebar('toggle');
	// $('#test').html($('.pusher').height());
}


window.onload = function() {
	twemoji.parse(document.body);
}
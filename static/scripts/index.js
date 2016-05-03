var last_timestamp = "";
var loading_messages=true;

// function notifyMe() {
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
    console.log("Desktop Notifications disabled")
  }
  else if (Notification.permission === "granted") {
    console.log("Desktop Notifications enabled")
  }
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
      if (permission === "granted") {
        console.log("Desktop Notifications active")
      }
    });
  }

// var notification = new Notification("Hi there!");

// Set the name of the hidden property and the change event for visibility
var hidden, visibilityChange; 
if (typeof document.hidden !== "undefined") { // Opera 12.10 and Firefox 18 and later support 
  hidden = "hidden";
  visibilityChange = "visibilitychange";
} else if (typeof document.mozHidden !== "undefined") {
  hidden = "mozHidden";
  visibilityChange = "mozvisibilitychange";
} else if (typeof document.msHidden !== "undefined") {
  hidden = "msHidden";
  visibilityChange = "msvisibilitychange";
} else if (typeof document.webkitHidden !== "undefined") {
  hidden = "webkitHidden";
  visibilityChange = "webkitvisibilitychange";
}

// If the page is hidden, pause the video;
// if the page is shown, play the video
// function handleVisibilityChange() {
//   if (document[hidden]) {
//     videoElement.pause();
//   } else {
//     videoElement.play();
//   }
// }

// document.addEventListener(visibilityChange, handleVisibilityChange, false);

function scrollArea() {
	$(".scroll.area").animate({
		scrollTop:$(".scroll.area").prop("scrollHeight")
	}, 300);
}

window.onload = function() {
	// $('.scroll.area').addClass('loading');
	$.get("/api/getlatestpost?timestamp="+encodeURIComponent(last_timestamp), function(data){$( "#message_feed" ).append( data );});
	while (loading_messages) {
		$.ajax({
		  url: "/api/getlatestpost?timestamp="+encodeURIComponent(last_timestamp),
		  dataType: 'html',
		  async: false,
		  error: function (msg) { console.log(msg); },
		  success: function(data) {
			if (data.length<10) {loading_messages = false};
			$( "#message_feed" ).append( data );
		  }
		});
	}

	scrollArea();

	setInterval(function()
		{
			if (last_timestamp!="") {
				$.get("/api/getlatestpost?timestamp="+encodeURIComponent(last_timestamp), function(data){
					$( "#message_feed" ).append( data );
					if (data.length>10) {
						if (document[hidden]) {
							new Notification(data);
						};
						scrollArea();
					};
				});

			}

			else {
				$.get("/api/getlatestpost", function(data){
					$( "#message_feed" ).append( data );
				});
			}
		},
		1000);
};

function sendChatMessage() {
	console.log($('#message_input')[0].value)
	$.get("/post?message_input="+encodeURIComponent($('#message_input')[0].value), function(data){});
	$('#message_input')[0].value=""
	return false
}

var address;
function sendRequest(stream_link) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_stream_url', true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({'stream_link': stream_link }));
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return;
        if (this.status == 200) {
            var response = JSON.parse(xhr.responseText).result;
            address = response;
            console.log(xhr.responseText)
        }
    }
}



window.addEventListener('load', function(){
    var stream_link = location.pathname;
    sendRequest(stream_link);

    var ws_uri = 'ws://' + location.hostname + ':8888/kurento';
    var ice_servers = undefined;
    var videoOutput = document.getElementById('videoOutput');
    var pipeline;
    var webRtcPeer;

    startButton = document.getElementById('start');
    startButton.addEventListener('click', start);

    stopButton = document.getElementById('stop');
    stopButton.addEventListener('click', stop);

    function start() {
        var options = {
        remoteVideo : videoOutput
      };
      webRtcPeer = kurentoUtils.WebRtcPeer.WebRtcPeerRecvonly(options,
        function(error){
          webRtcPeer.generateOffer(onOffer);
          webRtcPeer.peerConnection.addEventListener('iceconnectionstatechange', function(event){
            if(webRtcPeer && webRtcPeer.peerConnection){
              console.log("oniceconnectionstatechange -> " + webRtcPeer.peerConnection.iceConnectionState);
              console.log('icegatheringstate -> ' + webRtcPeer.peerConnection.iceGatheringState);
            }
          });
      });
    }

    function onOffer(error, sdpOffer){
      if(error) return onError(error);

    	kurentoClient(ws_uri, function(error, kurentoClient) {
    		if(error) return onError(error);

    		kurentoClient.create("MediaPipeline", function(error, p) {
    			if(error) return onError(error);
    			pipeline = p;
                pipeline.create("PlayerEndpoint", {networkCache: 0, uri: address.value}, function(error, player){
    			  if(error) return onError(error);

    			  pipeline.create("WebRtcEndpoint", function(error, webRtcEndpoint){
    				if(error) return onError(error);

            setIceCandidateCallbacks(webRtcEndpoint, webRtcPeer, onError);

    				webRtcEndpoint.processOffer(sdpOffer, function(error, sdpAnswer){
    					if(error) return onError(error);

              webRtcEndpoint.gatherCandidates(onError);

    					webRtcPeer.processAnswer(sdpAnswer);
    				});

    				player.connect(webRtcEndpoint, function(error){
    					if(error) return onError(error);

    					console.log("PlayerEndpoint-->WebRtcEndpoint connection established");

    					player.play(function(error){
    					  if(error) return onError(error);

    					  console.log("Player playing ...");
    					});
    				});
    			});
    			});
    		});
    	});
    }

    function stop() {
      address.disabled = false;
      if (webRtcPeer) {
        webRtcPeer.dispose();
        webRtcPeer = null;
      }
      if(pipeline){
        pipeline.release();
        pipeline = null;
      }
    }

  });

  function setIceCandidateCallbacks(webRtcEndpoint, webRtcPeer, onError){
    webRtcPeer.on('icecandidate', function(candidate){
      console.log("Local icecandidate " + JSON.stringify(candidate));

      candidate = kurentoClient.register.complexTypes.IceCandidate(candidate);

      webRtcEndpoint.addIceCandidate(candidate, onError);

    });
    webRtcEndpoint.on('OnIceCandidate', function(event){
      var candidate = event.candidate;

      console.log("Remote icecandidate " + JSON.stringify(candidate));

      webRtcPeer.addIceCandidate(candidate, onError);
    });
  }

  function onError(error) {
    if(error)
    {
      console.log(error);
      stop();
    }
  }

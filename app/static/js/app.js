"use strict";

const socket = io();
let connected = false;
let keystrokeId = 0;
const processingQueue = [];

function onSocketConnect() {
  connected = true;
  document.getElementById('status-connected').style.display = 'inline-block';
  document.getElementById('status-disconnected').style.display = 'none';
  document.getElementById('disconnect-reason').style.visibility = 'hidden';
}

function onSocketDisconnect(reason) {
  connected = false;
  document.getElementById('status-connected').style.display = 'none';
  document.getElementById('status-disconnected').style.display = 'inline-block';
  document.getElementById('disconnect-reason').style.visibility = 'visible';
  document.getElementById('disconnect-reason').innerText = 'Error: ' + reason;
}

function limitRecentKeys(limit) {
  const recentKeysDiv = document.getElementById('recent-keys');
  while (recentKeysDiv.childElementCount > limit) {
    recentKeysDiv.removeChild(recentKeysDiv.firstChild);
  }
}

function setFavourite(fav) {
  const card = document.createElement('div');
  card.classList.add('key-card');
  card.innerText = fav;  
  document.getElementById('recent-keys').appendChild(card);
  card.addEventListener("click", runFavourite);
}

function addFavourite(command) {
  const card = document.createElement('div');
  card.classList.add('key-card');
  card.innerText = command;  
  card.setAttribute('unsaved', 'true');
  document.getElementById('recent-keys').appendChild(card);
  const removalTimer = setTimeout(removeRecentFavourite.bind(null, card), 3000);
  card.addEventListener("click", keepRecentFavourite.bind(null, removalTimer, card));
}

function onDisplayHistoryChanged(evt) {
  if (evt.target.checked) {
    document.getElementById('recent-keys').style.visibility = 'visible';
  } else {
    document.getElementById('recent-keys').style.visibility = 'hidden';
    limitRecentKeys(0);
  }
}

function sendStringAsKeystrokes(stringKeys) {
	socket.emit('string', {string: stringKeys,});
}	

function sendFromInputBox(command) {
	let x = document.getElementById('domTextElement').value;
	console.log(x);	
	sendStringAsKeystrokes(x);
	addFavourite(x);
	document.getElementById('domTextElement').value = '';
}

function removeRecentFavourite(element) {
  element.remove();
}

function keepRecentFavourite(timer, element) {
  clearTimeout(timer);
  element.removeAttribute("unsaved");
  element.removeEventListener("click", keepRecentFavourite);
  element.addEventListener("click", runFavourite);
}

function runFavourite() {
	let x = this.innerText;
	console.log(x);	
	sendStringAsKeystrokes(x);
}

function onFavouritesLoad(message) {
	
}

document.getElementById('send-button').addEventListener("click", sendFromInputBox);
const collection = document.getElementsByClassName("FavCommand");
for (let i = 0; i < collection.length; i++) {
	collection[i].addEventListener("click", runFavourite);
}

//document.getElementById('display-history-checkbox').addEventListener("change", onDisplayHistoryChanged);
socket.on('connect', onSocketConnect);
socket.on('disconnect', onSocketDisconnect);
socket.emit('favourites_load');

socket.on('favourites_load', function(msg) {	
	//console.log('favourites_load', msg);
	var favArray = JSON.parse(msg);
	//console.log('favArray: ', favArray);
	for (let i in favArray) {
		//console.log('favourite: ', favArray[i]);
		setFavourite(favArray[i]);
	}
});
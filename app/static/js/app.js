"use strict";

const socket = io();
let connected = false;
let keystrokeId = 0;

$("#send-button").on("click", sendFromInputBox);
$("#domTextElement").on("keypress", function (e) {
  if (e.which == 13) {
    sendFromInputBox();
  }
});

socket.on('connect', onSocketConnect);
socket.on('disconnect', onSocketDisconnect);
socket.on('favourites_load', function (msg) {
  var favArray = JSON.parse(msg);
  for (let i in favArray) {
    setFavourite(favArray[i]);
  }
});

function onSocketConnect() {
  connected = true;
  $("#status").html("Connected");
}

function onSocketDisconnect(reason) {
  connected = false;
  $("#status").html('Error: ' + reason);
}

function setFavourite(command) {
  const card = $("<div class='key-card'>" + command + "</div>");
  $('#recent-keys').on("click", runFavourite);
  $('#recent-keys').append(card);  
}

function proposeFavourite(command) {
  const card = $("<div class='key-card' unsaved=true>" + command + "</div>");
  $('#recent-keys').append(card);
  const removalTimer = setTimeout(removeProposedFavourite.bind(null, card), 3000);
  card.on("click", function() {
    keepRecentFavourite(removalTimer, card);
  });
}

function sendStringAsKeystrokes(stringKeys) {
  socket.emit('string', { string: stringKeys, });
}

function sendFromInputBox() {
  let command = $("#domTextElement").val();
  sendStringAsKeystrokes(command);
  proposeFavourite(command);
  $("#domTextElement").val("");
}

function removeProposedFavourite(element) {
  element.remove();
}

function keepRecentFavourite(timer, element) {
  clearTimeout(timer);
  element.removeAttr("unsaved");
  element.on("click", runFavourite);
}

function runFavourite() {
  let x = this.innerText;
  sendStringAsKeystrokes(x);
}

socket.emit('favourites_load');
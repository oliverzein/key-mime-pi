"use strict";

const socket = io();
let connected = false;
let keystrokeId = 0;
let drake = null;

$("#send-button").on("click", sendFromInputBox);
$("#domTextElement").on("keypress", function (e) {
  if (e.which == 13) {
    sendFromInputBox();
  }
});

socket.on('connect', onSocketConnect);
socket.on('disconnect', onSocketDisconnect);

function onSocketConnect() {
  connected = true;
  $("#status").html("Connected");
}

function onSocketDisconnect(reason) {
  connected = false;
  $("#status").html('Error: ' + reason);
}

function toggleMoverActive() {
  socket.emit('mover', (state) => {
    //alert(state)
  });
}

function setFavourite(command) {
  const card = $("<div class='key-card'>" + command + "</div>");
  card.on("click", runFavourite);
  $('#recent-keys').append(card);
}

function proposeFavourite(command) {
  const card = $("<div class='key-card' unsaved=true>" + command + "</div>");
  $('#recent-keys').append(card);
  const removalTimer = setTimeout(removeProposedFavourite.bind(null, card), 3000);
  card.on("click", () => keepRecentFavourite(removalTimer, card));
}

function sendStringAsKeystrokes(stringKeys) {
  socket.emit('string', { string: stringKeys, });
  console.log(stringKeys)
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
  element.off().on("click", runFavourite);
  socket.emit('favourite_add', element.html());
}

function runFavourite() {
  sendStringAsKeystrokes($(this).html());
}

function displayFavs(favs) {
  var favArray = JSON.parse(favs);
  for (let i in favArray) {
    setFavourite(favArray[i]);
  }
  
  // setup drag & drop 
  drake = dragula([document.querySelector('#recent-keys'), document.querySelector('#remove')]);
  drake.on("drag", () => $("#remove").show());
  drake.on("dragend", () => $("#remove").hide());
  drake.on("drop", function(el, target) {
    if($(target).attr("id") === "remove") {
      drake.remove();
      socket.emit('favourite_remove', $(el).html());
    }
  });  
};

socket.emit('favourites_load', (response) => displayFavs(response));
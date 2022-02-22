function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function executefollow(profile_handle) {
  var follow_link, profile_link;
  follow_link = `${window.follow_link}`
  profile_link = `${window.profile_link}`
  fetch(follow_link, {
    method: "GET",
  }).then((_res) => {
    window.location.href = profile_link;
  });
}

function executeunfollow(profile_handle){
  var unfollow_link, profile_link;
  unfollow_link = `${window.unfollow_link}`
  profile_link = `${window.profile_link}`
  fetch(unfollow_link, {
    method: "GET",
  }).then((_res) => {
    window.location.href = profile_link;
  });
}

/*Taken from internet*/
function search_country() {
  var input, filter, a, i;
  input = document.getElementById("country_input");
  filter = input.value.toUpperCase();
  div = document.getElementById("country_dropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

// Code taken from https://stackoverflow.com/questions/1090948/change-url-parameters-and-specify-defaults-using-javascript
function toggle_sort(url, param) {
  var newAdditionalURL = "";
  var tempArray = url.split("?");
  var baseURL = tempArray[0];
  var additionalURL = tempArray[1];
  var temp = "";
  var done = 0;
  var new_add = "";
  if (additionalURL) {
    tempArray = additionalURL.split("&");
    for (var i = 0; i < tempArray.length; i++) {
      if (tempArray[i].split("=")[0] != param) {
        newAdditionalURL += temp + tempArray[i];
        temp = "&";
      } else {
        done = 1;
        if (tempArray[i].split("=")[1] == "ASC") {
          newAdditionalURL += temp + param + "=DESC";
          baseURL = "---";
        } else {
          newAdditionalURL += temp + param + "=ASC";
          baseURL = "---";
        }
      }
    }
  }

  console.log(url);
  console.log(done);

  if (done == 0) {
    newAdditionalURL += temp + param + "=ASC";
  }

  return baseURL + "?" + newAdditionalURL;
}

function toggle_sort_handle(url) {
  new_url = toggle_sort(url, "ratsort");

  window.location.href = new_url;
}

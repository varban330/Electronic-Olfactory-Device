function load_time(){
  // Get the snackbar DIV
  var x = document.getElementById("preloader");
  var y = document.getElementById('body')

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.style.display = "none"; y.style.display = "block" }, 1000);
}

document.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("mainbutton").click();
  }
});

function snackbarfunc(string) {
  // Get the snackbar DIV
  var x = document.getElementById("snackbar");
  x.innerHTML = string
  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function passwordcheck(){
  var password = document.getElementById("password").value;
  var repassword = document.getElementById("repassword").value;

  if(repassword != ""){
    if(password != repassword){
      document.getElementById("checker").innerHTML = "highlight_off";
      document.getElementById("checker").style.color = "red";
      return false;
    }
    else{
      document.getElementById("checker").innerHTML = "done_all";
      document.getElementById("checker").style.color = "green";
      return true;
    }
  }
  else{
    document.getElementById("checker").innerHTML = "autorenew";
    document.getElementById("checker").removeAttribute("style")
    return false
  }
}

function btnclick(){
    var url = "/reset-pwd-request/"
    var button = document.getElementById("mainbutton")
    olderhtml = button.innerHTML
    button.innerHTML = '<i class="fa fa-circle-o-notch fa-spin"></i>&nbsp;&nbsp;Wait'
    button.disabled = true
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }

    if(passwordcheck() == false){
      snackbarfunc("Passwords don't match");
      button.innerHTML = olderhtml
      button.disabled = false
      return
    }

    var myData = {
      password: document.getElementById('password').value,
      secret_key: document.getElementById('mainbutton').getAttribute("data-url"),
    }

    console.log("Mydata", myData)
    fetch(url, {
      method: "post",
      credentials: "same-origin",
      headers: {
          "Ocp-Apim-Subscription-Key": "94cea4adae3c452ebd3c2ff10dd54d7c",
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          "Content-Type": "application/json"
      },
      body: JSON.stringify(myData)
    }).then(function(response) {
      button.innerHTML = olderhtml
      button.disabled = false
      return response.json();
    }).then(function(data) {
      console.log("Data is ok", data);
      snackbarfunc(data["message"])
      if(data["message"] == "Password Reset Successful"){
        setTimeout(function(){window.location.href = "/thanks/";}, 2250);
      }
    }).catch(function(ex) {
      console.log("parsing failed", ex);
      console.log(url)
    });
}

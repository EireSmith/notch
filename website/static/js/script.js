
let clearAllBtn = document.querySelector(".footer clear");

//set end date after start date
document.getElementById("start").addEventListener("change", function() {
    var start = this.value;
    var end = document.getElementById('end');
    end.setAttribute("min", start)
});

//show notches
function showContracts() { document.getElementById("table").style="dispaly:block;"
  
};

//hide notches
function hideContracts() { document.getElementById("table").style="display:none;"
};

//delete contract
function deleteContract(contract_id) {
    fetch("/delete_notch", {method: "POST", body: JSON.stringify({ contract_id: contract_id})
}).then((_res)=> {window.location.href = "/"})
};

//update contract
function updateContract(contract_id) {
  var jobInput = document.getElementById('job').value;
  var startInput = document.getElementById('start').value;
  var endInput = document.getElementById('end').value;
  var payInput = document.getElementById('pay').value;
  fetch("/update_notch", {method: "POST", body: JSON.stringify({ contract_id: contract_id, job: jobInput, start: startInput,
    end: endInput, pay: payInput})
}).then((_res)=> {window.location.href = "/"})
};


function updateUser(user_id) {
  var firstName = document.getElementById('first_name').value;
  var familyName = document.getElementById('family_name').value;
  var password = document.getElementById('password').value;
  fetch("/update_user", {method: "POST", body: JSON.stringify({ user_id: user_id, first_name: firstName, family_name: familyName,
    password: password})
}).then((_res)=> {window.location.href = "/user-profile"})
};



function filesize(file){

  document.cookie = `filesize=${file.files[0].size}`;
}

//Change Login form to Sign up form
function changeDivContent(btn) {
  const divElement = document.getElementById("login-sign-up-form");
    divElement.innerHTML = `<div id="sign-up-form">
      <form action="signup" method = "POST">
          <h3 align="center">sign up</h3>
          <div class="inputField">
              <input style="font-size: 15px" name="first_name" id="first_name" type="text" placeholder="first name">
              <input style="font-size: 15px" name="family_name" id="family_name" type="text" placeholder="family name">
              <input style="font-size: 15px" name="email" id="email" type="email" placeholder="email">
              <input style="font-size: 15px" name="password" id="password" type="password" placeholder="password">
              <input style="font-size: 15px" name="password_confirm" id="password_confirm" type="password" placeholder="confirm password">       
          </div>
          <br />
          <button type="submit" class="submit">Sign up</button>  
      </form>
  </div>`;

}


//show buttons beneath each entry
function displayNotchViewButtons(int) {
  let doc = document.getElementsByClassName("notch_view_buttons")[int];

  if(doc.style.display === "none")
    {doc.style.display = "flex"}
  else 
    {doc.style.display = "none"}
};
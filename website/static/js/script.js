

let clearAllBtn = document.querySelector(".footer clear");

/*
function buttonActive(){ 
  let userEnteredJob= jobInput.value 
  let userEnteredStart= startInput.value
  let userEnteredPay = payInput.value
  
  if(userEnteredJob.trim() != 0  && userEnteredStart != 0 && userEnteredPay != 0){
    addBtn.classList.add("active"); 
    //updBtn.classList.add("active");

  } 
  else {
    addBtn.classList.remove("active"); 
    //updBtn.classList.remove("active");
  }
 };


jobInput.addEventListener("input", buttonActive)
startInput.addEventListener("input", buttonActive)
payInput.addEventListener("input", buttonActive)
*/


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


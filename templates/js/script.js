const jobInput = document.querySelector(".inputField input[class='job']");
const startInput = document.querySelector(".inputField input[class='start']");
const endInput = document.querySelector(".inputField input[class='end']");
const payInput = document.querySelector(".inputField input[class='pay']");
const addBtn = document.querySelector(".inputField button");
const clearAllBtn = document.querySelector(".footer clear");

baseURL = ' HEROKU '
;( function( window ) {

	'use strict';

	function extend( a, b ) {
		for( var key in b ) { 
			if( b.hasOwnProperty( key ) ) {
				a[key] = b[key];
			}
		}
		return a;
	}

	function DotNav( el, options ) {
		this.nav = el;
		this.options = extend( {}, this.options );
  		extend( this.options, options );
  		this._init();
	}

	DotNav.prototype.options = {};

	DotNav.prototype._init = function() {
		// special case "dotstyle-hop"
		var hop = this.nav.parentNode.className.indexOf( 'dotstyle-hop' ) !== -1;

		var dots = [].slice.call( this.nav.querySelectorAll( 'li' ) ), current = 0, self = this;

		dots.forEach( function( dot, idx ) {
			dot.addEventListener( 'click', function( ev ) {
				ev.preventDefault();
				if( idx !== current ) {
					dots[ current ].className = '';

					// special case
					if( hop && idx < current ) {
						dot.className += ' current-from-right';
					}

					setTimeout( function() {
						dot.className += ' current';
						current = idx;
						if( typeof self.options.callback === 'function' ) {
							self.options.callback( current );
						}
					}, 25 );						
				}
			} );
		} );
	}

	// add to global namespace
	window.DotNav = DotNav;

})( window );

let show = () => {
    fetch(baseURL).then(
        response => {
            response.json().then(
                data => {
                    console.log(data);
                    if(data.Results.length > 0){
                        var temp = "";
                        data.Results.forEach((x) => {
                            
                            temp += "<td>"+x.ID+"</td>";
                            temp += "<td>"+x.Job+"</td>";
                            temp += "<td>"+x.Start+"</td>";
                            temp += "<td>"+x.End+"</td>";
                            temp += "<td>"+x.Pay+"</td>";
                            temp += "<td>"+ "<button class='updBtn' onclick='updateContract("+x.ID+")'> <i class='fa fa-pencil-square-o'></button>" +
                            "</td>"
                            temp += "<td>"+ "<button class='delBtn' onclick='deleteContract("+x.ID+")'><i class='fa fa-ban'></i></button>" +
                            "</td></tr>"
                            
                        })
                    
                        document.getElementById("tab1").innerHTML = temp;
                    
                    }
                }  
            )
        }
    )
} 



let clearInput = ()=>{if(jobInput.value != 0 || startInput.value != 0 || endInput.value != 0 || payInput.value != 0) 
{jobInput.value = "" , startInput.value = "",  endInput.value = "" , payInput.value = ""}};

let removeTable =()=>{var rowCount = document.getElementById('tab1').rows.length; 
            while(--rowCount) document.getElementById('tab1').deleteRow(rowCount)}
    

function buttonActive(){ 
  let userEnteredJob= jobInput.value 
  let userEnteredStart= startInput.value
  let userEndteredPay = payInput.value
  
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



let addContract=()=>{
  let job=document.getElementById('job').value;
  let start=document.getElementById('start').value;
  let end=document.getElementById('end').value;
  let pay=document.getElementById('pay').value;
  let temp = "";
  fetch(baseURL+'add?job='+job+'&start='+start+'&end='+end+'&pay='+pay).then((resp)=>{console.log("Contract Added")});
  show();
  clearInput();
  


}


let deleteContract = (id) => { 
    fetch(baseURL+'delete?id='+id)
    .then((resp) => {
        
        console.log('Contract Deleted')
        show();
    })
};


let updateContract = (id) => {
    let updateJob = document.getElementById('job').value;
    let updateStart = document.getElementById('start').value;
    let updateEnd = document.getElementById('end').value;
    let updatePay = document.getElementById('pay').value;
     let text = "Are you sure?";
      if (confirm(text) == true) {
    fetch(baseURL+'update?id='+id+'&job='+updateJob+'&start='+updateStart+'&end='+updateEnd+'&pay='+updatePay)
    .then((resp) => {
        console.log('Contract Deleted')
        show();
    });
      } else {
          pass;
      }

}

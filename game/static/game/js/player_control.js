
const preloader = document.getElementById("preloader")

document.getElementById("new_level_btn").onclick = function(){

    preloader.hidden = false

}

document.getElementById("surprisebtn").onclick = function(){

    preloader.hidden = false

}

$("#invest_all").change(function() {

    if(this.checked) {

        document.getElementById("command_invest").value = document.getElementById('player_balance').value

    } else {

        document.getElementById("command_invest").value = ''

    }
});

document.getElementById('is_command').onchange = function(){
    
    if( document.getElementById('is_command').checked ) {

        document.getElementById('player_business_select').hidden = true
        document.getElementById('command_business_select').hidden = false

        document.getElementById('player_business_select').disabled = true
        document.getElementById('command_business_select').disabled = false

    } else {

        document.getElementById('player_business_select').hidden = false
        document.getElementById('command_business_select').hidden = true

        document.getElementById('player_business_select').disabled = false
        document.getElementById('command_business_select').disabled = true  

    }
}

const playerId = document.getElementById("player_id");
const playerBalance = document.getElementById("player_balance");
const investAllCheckbox = document.getElementById("invest_all");
const commandInvestInput = document.getElementById("command_invest");
const playerBusinessSelect = document.getElementById("player_business_select");
const commandBusinessSelect = document.getElementById("command_business_select");
const selector_business_category = document.getElementById("player_business_select_category");

investAllCheckbox.addEventListener("click", function() {
  commandInvestInput.value = playerBalance.getAttribute('value').replace(',','');
});

selector_business_category.addEventListener("change", function(){
  fetch('/get_player_control_business_data_'+ playerId.innerHTML+'_'+selector_business_category.value+'/')
      .then(response => response.json())
      .then(data => {

        const businessCards = data.businesses.map(business => {
          return `
            <div class="card mb-4">
              <div class="card-body p-4">
                <div class="card-title">
                  <div class="row">
                    <div class="col">
                      <h5 class="card-title mb-0">${business.fields.name}</h5>
                    </div>
                    <div class="col text-end">
                      <h5 class="card-text mb-0">${ business.fields.cost.toLocaleString('en-US', {useGrouping: true, grouping: [3], groupSeparator: ','}) }</h5>
                    </div>
                  </div>
                </div>
                <p class="card-text">Рентабельность: от ${business.fields.min_rent}% до ${business.fields.max_rent}%</p>
              </div>
              <div class="card-footer">
                <div class="row">
                  <div class="col-6 px-1">
                    ${
                      business.fields.cost <= data.player_balance
                        ? '<button class="btn btn-success w-100" onclick="buyPersonalBusiness( '+business.pk+' )">Личный бизнес</button>'
                        : '<button class="btn w-100 disabled">Нехватает средств</button>'
                    }
                  </div>
                  <div class="col-6 px-1">
                    ${
                      business.fields.cost <= data.command_bank && data.command_share > 0
                        ? '<button class="btn btn-danger w-100" onclick="buyCommandBusiness( '+business.pk+' )">Командный бизнес</button>'
                        : '<button class="btn w-100 disabled">Нехватает средств</button>'
                    }
                  </div>
                </div>
              </div>
            </div>`;
        }).join('');

        document.getElementById("business_cards").innerHTML = businessCards;
      });
});

// onclick="buyPersonalBusiness( '+business.pk+' )"

function updatePlayerControlData() {
  fetch('/get_player_control_data_'+ playerId.innerHTML+'/')
      .then(response => response.json())
      .then(data => {

          let formatted_balance = data.player_balance.toLocaleString('en-US', {useGrouping: true, grouping: [3], groupSeparator: ','});
          let command_count     = data.command_count.toLocaleString('en-US', {useGrouping: true, grouping: [3], groupSeparator: ','});

          if (data.player_balance < 0) {
            document.getElementById('player_balance').innerHTML = '<b class="text-danger">' + formatted_balance + '</b>';
          } else {
            document.getElementById('player_balance').innerHTML = '<b>' + formatted_balance + '</b>';
          }
          document.getElementById('player_level').innerHTML = '<b>Круг:</b> ' + data.player_level;
          document.getElementById('player_command_share').innerHTML = '<b>Доля КБ:</b> ' + command_count + ' - ' + data.command_share + '%';
      });
} 

function buyPersonalBusiness( business_id ) {
  fetch('/buy_personal_business_'+ playerId.innerHTML+'_'+business_id+'/')
      .then(response => response.json())
}

function buyCommandBusiness( business_id ) {
  fetch('/buy_command_business_'+ playerId.innerHTML+'_'+business_id+'/')
      .then(response => response.json())
}

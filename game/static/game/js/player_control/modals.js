const business_modal = document.getElementById("BusinessModal");

function showBusinessModal(category) {
  getPlayerBusinessData(category);

  var businessModalInstance = new bootstrap.Modal(business_modal);
  selector_business_category.value = category;
  selector_business_category.disabled = category !== "ALL";
  businessModalInstance.show();
}

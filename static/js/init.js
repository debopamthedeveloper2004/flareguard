(function($){
  $(function(){

    $('.sidenav').sidenav();

  }); // end of document ready
})(jQuery); // end of jQuery name space
document.addEventListener('DOMContentLoaded', function() {
  const btn = document.querySelector('.btn-large');
  
  btn.addEventListener('click', function(e) {
    // Add temporary click class
    this.classList.add('clicked');
    setTimeout(() => this.classList.remove('clicked'), 200);
    
    // Prediction result animation handler
    const result = document.getElementById('prediction-result');
    if(result) {
      result.classList.add('result-pulse');
      setTimeout(() => result.classList.remove('result-pulse'), 1000);
    }
  });
});
document.addEventListener('DOMContentLoaded', function() {
  // Auto-remove alerts after 5 seconds
  setTimeout(() => {
    const alerts = document.querySelectorAll('.danger-alert, .safe-alert');
    alerts.forEach(alert => alert.remove());
  }, 5000);
});
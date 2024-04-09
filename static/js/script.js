
var countDownDate = new Date("Apr 10, 2024 14:00:00").getTime();

var x = setInterval(function () {

  var now = new Date().getTime();

  var distance = countDownDate - now;

  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  document.getElementById("countdown").innerHTML = `<b>` + hours + `<span class="text-muted">h </span>`
    + minutes + `<span class="text-muted">m </span>` + seconds + `<span class="text-muted">s </span>` + `</b>`;

  if (distance < 0) {
    clearInterval(x);
    document.getElementById("countdown").innerHTML = "<b>Time Up!</b>";
  }
}, 1000);

new PerfectScrollbar(document.getElementById('comments'), {
  wheelPropagation: false
});

function submitGitHubLink(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Disable the submit button to avoid spam
  const submitButton = document.querySelector('button[type="submit"]');
  submitButton.disabled = true;

  // Change the button's text to indicate that the request is being processed
  submitButton.textContent = 'Processing...';

  // Get the form data
  const commitLink = document.getElementById('commitLink').value;

  // Send a POST request to the Flask backend
  fetch('/submitGitHubLink', {

    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ commitLink : commitLink }),
  })
    .then(response => {
      // Check the response status
      if (response.ok) {
        // Change the button's text to indicate success
        submitButton.classList.add('btn-success');
        submitButton.classList.remove('btn-primary');        
        submitButton.textContent = 'Submission Successful';

        // Enable the button after 2 seconds and reset the text
        setTimeout(() => {
          submitButton.textContent = 'Submit';
          submitButton.classList.add('btn-primary');
          submitButton.classList.remove('btn-success');          
          submitButton.disabled = false;
        }, 2000);
      } else {
        // Change the button's text to indicate failure
        submitButton.classList.add('btn-danger');
        submitButton.classList.remove('btn-primary');
        submitButton.textContent = 'Submission Failed';

        // Enable the button after 2 seconds and reset the text
        setTimeout(() => {
          submitButton.textContent = 'Submit';
          submitButton.classList.add('btn-primary');
          submitButton.classList.remove('btn-danger');
          submitButton.disabled = false;
        }, 2000);
      }
    })
    .catch(error => {
      // Handle any errors that occurred during the request
      console.error('Error:', error);

      // Change the button's text to indicate failure
      submitButton.textContent = 'Failure';

      // Enable the button after 2 seconds and reset the text
      setTimeout(() => {
        submitButton.textContent = 'Submit';
        submitButton.disabled = false;
      }, 2000);
    });
}


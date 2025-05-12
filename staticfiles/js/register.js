// Selecting DOM elements
const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");
const submitBtn = document.querySelector(".submit-btn");

// Function to toggle password visibility
const handleToggleInput = (e) => {
  // Toggle password visibility based on button text
  if (showPasswordToggle.textContent == "SHOW") {
    showPasswordToggle.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    showPasswordToggle.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
};

// Add event listener to toggle password visibility
showPasswordToggle.addEventListener("click", handleToggleInput);

// Event listener for email field keyup event
emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;
  // Display feedback indicating email validation check is in progress
  emailSuccessOutput.style.display = "block";
  emailSuccessOutput.textContent = `Checking ${emailVal}`;

  // Reset email field and feedback area styling
  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  // Perform email validation check when emailVal is not empty
  if (emailVal.length > 0) {
    console.log("emailVal", emailVal);
    fetch("/validate-email/", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        // Hide feedback after validation check is complete
        emailSuccessOutput.style.display = "none";
        // Handle error case
        if (data.email_error) {
          submitBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          // Enable submit button if no errors
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

// Event listener for username field keyup event
usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  // Display feedback indicating username validation check is in progress
  usernameSuccessOutput.style.display = "block";
  usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

  // Reset username field and feedback area styling
  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display = "none";

  // Perform username validation check when usernameVal is not empty
  if (usernameVal.length > 0) {
    console.log("usernameVal", usernameVal);
    fetch("/validate-username/", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        // Hide feedback after validation check is complete
        usernameSuccessOutput.style.display = "none";
        // Handle error case
        if (data.username_error) {
          submitBtn.disabled = true;
          usernameField.classList.add("is-invalid");
          feedBackArea.style.display = "block";
          feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
        } else {
          // Enable submit button if no errors
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

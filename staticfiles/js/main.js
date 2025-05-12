// Output a message to the console
console.log("Hello worldd");

// Retrieve DOM elements by their IDs
var answerLabel = document.getElementById("answerLabel");
var nextBtn = document.getElementById("next-btn");
var finishBtn = document.getElementById("finish-btn");
var showResultBtn = document.getElementById("show-result-btn");
var dummyBtn = document.getElementById("dummy");

// Conditional logic based on the presence of nextBtn
if (nextBtn) {
  // Check if nextBtn has elements
  if (nextBtn.length > 0) {
    // If nextBtn has elements, hide finishBtn and showResultBtn
    finishBtn.setAttribute("hidden", true);
    showResultBtn.setAttribute("hidden", true);
  } else {
    // If nextBtn has no elements, show finishBtn and showResultBtn
    finishBtn.setAttribute("hidden", false);
    showResultBtn.setAttribute("hidden", false);
  }
}

// Function to display the selected radio button value
function displayRadioValue() {
  // Output a message to the console
  console.log("sanity check");
  // Get all elements with name "option"
  var ele = document.getElementsByName("option");
  // Loop through each element
  for (i = 0; i < ele.length; i++) {
    // Check if the current element is checked
    if (ele[i].checked) {
      // Get the value of the checked element
      checked_val = ele[i].value;
      // Compare the checked value with the answer label value
      if (checked_val == answerLabel.value) {
        // Disable certain elements and display a message if the answer is correct
        document.getElementById("check").disabled = true;
        document.getElementById("option_one").disabled = true;
        document.getElementById("option_two").disabled = true;
        document.getElementById("option_three").disabled = true;
        document.getElementById("option_four").disabled = true;
        result_div.innerHTML = `
				<div class="h5 mb-3"><b>Correct</b></div>
				`;
      } else {
        // Disable certain elements and display a message if the answer is wrong
        document.getElementById("check").disabled = true;
        document.getElementById("option_one").disabled = true;
        document.getElementById("option_two").disabled = true;
        document.getElementById("option_three").disabled = true;
        document.getElementById("option_four").disabled = true;
        result_div.innerHTML = `
				<div class="h5 mb-3"><b>Wrong, Correct answer is ${answerLabel.value}</b></div>
				`;
      }
    }
  }
}

// Get the total score DOM element and initialize userScore variable
var totalScore = document.getElementById("totalScore"); //id of the total score text field
var userScore = 0;

// Add event listener to the check button
var checkBtn = document.getElementById("check"); //Id of the check button
if (checkBtn) {
  checkBtn.addEventListener("click", function () {
    // Get all elements with name "option"
    var ele = document.getElementsByName("option");
    // Loop through each element
    for (i = 0; i < ele.length; i++) {
      // Check if the current element is checked
      if (ele[i].checked) {
        // Get the value of the checked element
        checked_val = ele[i].value;
        // Compare the checked value with the answer label value
        if (checked_val == answerLabel.value) {
          // Increment userScore if the answer is correct and update sessionStorage
          userScore += 1;
          score = Number(totalScore.value) + userScore;
          sessionStorage.setItem("userScore", score);
          console.log(score);
        }
      }
    }
  });
}

// Add event listener to the dummy button
if (dummyBtn) {
  dummyBtn.addEventListener("click", function () {
    // Update totalScore value with the value stored in sessionStorage
    totalScore.value = sessionStorage.getItem("userScore");
  });
}

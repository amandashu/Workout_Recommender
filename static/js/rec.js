// function to show loading page
function findWorkouts() {
  let recommendations = document.getElementById("recommendations");
  recommendations.style.display = "none";

  let loading = document.getElementById("loading");
  loading.style.display = "block";
}

if (recEngine) {
  // keeps rec_engine to be selected aftering submitting
  document.getElementById('rec-engine').value = recEngine;
} else {
  // gives empty div a height when there rec_engine is not defined
  // so footer does not move up
  document.getElementById('recommendations').style.height = '70vh';
}

// disable find workouts button at first
let find_workouts = document.getElementById('find_workouts')
let hidden_selection = document.getElementById('hidden_selection')
if (hidden_selection.selected == true) {
  find_workouts.disabled = true;
}

// to enable submit button after selecting from rec engine
function enableSubmit() {
  if (hidden_selection.selected == false) {
    find_workouts.disabled = false;
  }
}

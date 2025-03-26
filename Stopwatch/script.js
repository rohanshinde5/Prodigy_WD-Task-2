let timer;
let startTime;
let elapsedTime = 0;
let running = false;

const display = document.querySelector(".display");
const startPauseBtn = document.getElementById("startPauseBtn");
const resetBtn = document.getElementById("resetBtn");
const lapBtn = document.getElementById("lapBtn");
const lapsContainer = document.querySelector(".laps");

function formatTime(ms) {
    let milliseconds = Math.floor(ms % 1000);
    let seconds = Math.floor((ms / 1000) % 60);
    let minutes = Math.floor((ms / (1000 * 60)) % 60);

    return (
        String(minutes).padStart(2, "0") + ":" +
        String(seconds).padStart(2, "0") + "." +
        String(milliseconds).padStart(3, "0")
    );
}

function updateDisplay() {
    const currentTime = Date.now();
    elapsedTime = currentTime - startTime;
    display.textContent = formatTime(elapsedTime);
}

function startPauseTimer() {
    if (!running) {
        startTime = Date.now() - elapsedTime;
        timer = setInterval(updateDisplay, 10);
        startPauseBtn.textContent = "Pause";
        startPauseBtn.style.background = "#e67e22";
        running = true;
    } else {
        clearInterval(timer);
        startPauseBtn.textContent = "Resume";
        startPauseBtn.style.background = "#27ae60";
        running = false;
    }
}

function resetTimer() {
    clearInterval(timer);
    elapsedTime = 0;
    running = false;
    display.textContent = "00:00.000";
    startPauseBtn.textContent = "Start";
    startPauseBtn.style.background = "#27ae60";
    lapsContainer.innerHTML = "";
}

function addLap() {
    if (!running) return;
    const lapTime = formatTime(elapsedTime);
    const lapItem = document.createElement("li");
    lapItem.textContent = lapTime;
    lapsContainer.appendChild(lapItem);
}

startPauseBtn.addEventListener("click", startPauseTimer);
resetBtn.addEventListener("click", resetTimer);
lapBtn.addEventListener("click", addLap);

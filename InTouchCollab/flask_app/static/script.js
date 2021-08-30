console.log('script loaded')
function showCreateGroup() {
    let x = document.getElementById("createGroup");
    if (x.style.display === "none") {
        x.style.display = "block";
        console.log('display block')
    } else {
        x.style.display = "none";
        console.log('display none')
    }
}

function hideCreateGroup() {
    document.getElementById('createGroup').style.display = "none";
}

async function getWeather() {
    let city = document.getElementById("city").innerHTML.toLowerCase();
    console.log(city);
    let state = document.getElementById("state").innerHTML.toLowerCase();
    console.log(state)

    let response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city},${state},us&appid=49a7ec53a7129684f487378a1416d407`);
    let coderData = await response.json();
    console.log(coderData.main.temp)

    kelv = coderData.main.temp;

    // temp in kelvin
    temp = Math.floor((kelv - 273.15) * 9/5 + 32);
    console.log('F', Math.floor(temp));
    document.getElementById("weather").innerText = `F ${temp}`;
    // K =(K − 273.15) × 9/5 + 32 = °F.
}
// console.log(getCoderData());
getWeather();
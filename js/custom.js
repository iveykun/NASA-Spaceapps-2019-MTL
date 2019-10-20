let focusElement = "", url = "";

function startGeneratingStarView() {
    const labelId = ["star-distance", "star-albedo", "star-luminosity", "star-radius", "star-temperature"];
    const labelName = ["Distance (Au)", "Bond Albedo (0-1)", "Luminosity (W)", "Radius of Star (m)", "Temperature of Star (K)"];
    const inputId = ["input-star-distance", "input-star-albedo", "input-star-luminosity", "input-star-radius", "input-star-temperature"];
    const inputStep = [1, 0.1, 1, 1, 0.01];
    const inputMax = [1, 0.1, 1, 1, 40000];
    let elementsLabels = [];
    $.each(labelName, function (key, value) {
        elementsLabels.push(
            {
                "label": {
                    "id": labelId[key],
                    "name": labelName[key]
                },
                "input": {
                    "id": inputId[key],
                    "min": 1,
                    "max": inputMax[key],
                    "step": inputStep[key]

                }
            }
        );
    });
    let documentRef = $("#starControlsDiv");
    $.each(elementsLabels, function (key, value) {
        let docs = createSliderElements(value);
        documentRef.append(docs);
    });
}

function startGeneratingPlanetView() {
    const labelId = ["planet-force", "planet-mass", "planet-surface-mass", "planet-radius", "planet-temperature"];
    const labelName = ["Gravity force (N)", "Mass of the planet (kg)", "Mass on planet surface (kg)", "Radius of Planet (m)", "Temperature of planet (K)"];
    const inputId = ["input-planet-force", "input-planet-mass", "input-planet-surfmass", "input-planet-radius", "input-planet-temperature"];
    const inputStep = [1, 0.1, 1, 1, 0.01];
    const inputMax = [1, 0.1, 1, 1, 40000];
    let elementsLabels = [];
    $.each(labelName, function (key, value) {
        elementsLabels.push(
            {
                "label": {
                    "id": labelId[key],
                    "name": labelName[key]
                },
                "input": {
                    "id": inputId[key],
                    "min": 1,
                    "max": inputMax[key],
                    "step": inputStep[key]

                }
            }
        );
    });
    let documentRef = $("#planetControlsDiv");
    $.each(elementsLabels, function (key, value) {
        let docs = createSliderElements(value);
        documentRef.append(docs);
    });
}

function createSliderElements(obj) {
    let planetOrStar = obj.label.id.split("-")[0] === "star" ? "star" : "planet";
    let dataValue = planetOrStar + "-" + obj.label.id.split("-")[1];
    let textRef = obj.label.id.toString().replace(planetOrStar, "text-" + planetOrStar);
    let eleRef = document.createElement("div");
    eleRef.className = "form-group";
    eleRef.innerHTML = "<label for='" + obj.label.id + "'>" + obj.label.name + "</label> &nbsp;" +
        "<label id='" + textRef + "'></label>";
    eleRef.innerHTML += '<input type="number" class="form-control custom-range" id="' + obj.input.id + '" ' +
        ' data-text="' + planetOrStar + '" step="0.01" data-value="' + dataValue + '"' +
        ' placeholder="' + dataValue + '" onfocus="setFocusElement(this);">';
    return eleRef;
}

function setFocusElement(ele) {
    focusElement = ele;
}

let starSketch = function (p) {
    console.log(p);
    let createStarEle = document.getElementById("createdStar");
    const width = createStarEle.clientWidth;
    const height = createStarEle.clientHeight;
    p.setup = function () {
        p.createCanvas(width, height, p.WEBGL);
    };

    p.draw = function () {
        // p.circle(width / 2, height / 2, 350);
        p.sphere(150);
    };
};

let planetSketch = function (p) {
    console.log(p);
    let createPlanetEle = document.getElementById("createdPlanet");
    const width = createPlanetEle.clientWidth;
    const height = createPlanetEle.clientHeight;
    p.setup = function () {
        p.createCanvas(width, height, p.WEBGL);
        p.text('Planet', width / 2, height / 2);
    };

    p.draw = function () {
        p.sphere(50);
    };
};

async function callTheApi() {
    const selectElement = focusElement.getAttribute("data-value");
    let response;
    switch (selectElement) {
        case "planet-temperature":
            let starDistance = $("#input-star-distance").val();
            let starAlbedo = $("#input-star-albedo").val();
            let starLumni = $("#input-star-luminosity").val();
            url = "http://10.202.62.183:8080/return_tempP/" + starDistance + "/" + starAlbedo + "/" + starLumni;
            response = await hitServer(url);
            p5PlanetSketch.fill(response.colorP);
            $("#input-planet-temperature").val(response.tempP);
            break;
        case "planet-force":
            let a = 60.00; // default mass of normal human
            let b = $("#input-planet-mass").val();
            let c = $("#input-planet-radius").val();
            url = "http://10.202.62.183:8080/return_gravity/60.00/" + b + "/" + c;
            response = await hitServer(url);
            $("#input-planet-force").val(response.forceGrav);
            break;
        case "star-distance":
            let tempP1 = $("#input-planet-temperature").val();
            let starLumn1 = $("#input-star-luminosity").val();
            let staAlbedo1 = $("#input-star-albedo").val();
            url = "http://10.202.62.183:8080/return_dist/" + tempP1 + "/" + starLumn1 + "/" + staAlbedo1;
            response = await hitServer(url);
            console.log(response);
            $("#input-star-distance").val(response.dist);
            break;
        case "star-albedo":
            let tempP = $("#input-planet-temperature").val();
            let starD = $("#input-star-distance").val();
            let starLumn = $("#input-star-luminosity").val();
            url = "http://10.202.62.183:8080/return_bAlb/" + tempP + "/" + starD + "/" + starLumn;
            response = await hitServer(url);
            break;
        case "star-temperature":
            let starsLumni = $("#input-star-luminosity").val();
            let starRadi = $("#input-star-radius").val();
            url = "http://10.202.62.183:8080/return_tempS/" + starsLumni + "/" + starRadi;
            response = await hitServer(url);
            p5StarSketch.fill(response.colorS);
            $("#input-star-temperature").val(response.tempS);
            break;
        case "star-luminosity":
            if ($("#input-star-luminosity").val() !== "") {
                let aa = $("#input-star-luminosity").val();
                url = "http://10.202.62.183:8080/habitable/" + aa;
                response = await hitServer(url);
                alert("The habitable zone ìs between " + response.innerHab + " meters and " + response.outerHab + " meters");
            } else {
                let planetTemp = $("#input-planet-temperature").val();
                let staAlbedo = $("#input-star-albedo").val();
                let starDistnce = $("#input-star-distance").val();
                url = "http://10.202.62.183:8080/return_lumi/" + planetTemp + "/" + starDistnce + "/" + staAlbedo;
                response = await hitServer(url);
            }
            break;
        case "star-radius":
            alert("working under development");
            break;
        case "planet-mass":
            alert("working under development");
            break;
        case "planet-surface":
            alert("working under development");
            break;
        case "planet-radius":
            alert("working under development");
            break;
    }
}

async function hitServer(url) {
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Accept": "*"
        }
    });
    return await response.json();
}

// globals
let majorActive = false;

let map = null;
// todo make sure this comment is needed
let markersLayer = null; // can be a L.LayerGroup or a markerClusterGroup

// "Use my current location" button
async function fillStateCityFromGeoLoc() {
    // Get lat and lon
    const coords = await new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject("Geolocation not supported.");
        }

        navigator.geolocation.getCurrentPosition(
            pos => resolve(pos.coords),
            err => reject(err)
        );
    });

    const { latitude, longitude } = coords;

    console.log(coords);

    console.log(latitude, longitude);

    // Reverse Geocode city and state
    const url =
    `https://nominatim.openstreetmap.org/reverse?` +
    `format=json&lat=${latitude}&lon=${longitude}`;

    let response;

    try {
        response = await fetch(url, {
            headers: { "User-Agent": "MajorHelp/2.0" }
        });
    
    } catch (err) {
        console.error("Network error:", err);
        alert("Unable to reach the location service. " +  
            "Please try again.");
        return;
    }

    if (!response.ok) {
        console.error("Location Service returned an error" + 
            response.status + "."
        );
    }

    const data = await response.json();

    console.log(data);

    const city = 
        data.address.city ||
        data.address.town ||
        data.address.village;

    const state = data.address.state;

    // Fill out the inputs
    const cityInput = document.getElementById("city-input")
        .value = city;
    
    const stateInput = document.getElementById("state-input")
        .value = state;
    
}

// "Do you have a Major in mind?" Checkbox
function toggleMajorInput(){
    if (document.getElementById("major-input-check").checked) {
        // checked, show input field
        document.getElementById("major-input-box")
            .style.display = "inline";
        majorActive = true;
    } else {
        // unchecked, hide.
        document.getElementById("major-input-box")
            .style.display = "none";

        // Remember to not submit anything
        // if the major field is hidden
        majorActive = false;
    }
}


async function displayOutput() {
    // fetch details from inputs and encode
    const budgetMax = encodeURIComponent(
        document.getElementById("budget-max").value);

    const budgetMin = encodeURIComponent(
        document.getElementById("budget-min").value);

    const city      = encodeURIComponent(
        document.getElementById("city-input").value);

    const state     = encodeURIComponent(
        document.getElementById("state-input").value);

    const outstate  = encodeURIComponent(
        document.getElementById("outstate-checkbox").checked);

    // Major is optional
    const major     = encodeURIComponent(
        majorActive ? document.getElementById("major-input").value 
                    : null);


    // Submit to backend
    let response;
    try {
        response = await fetch("/api/reverse_calculate/?" +
            `budget-max=${budgetMax}&budget-min=${budgetMin}` +
            `&city=${city}&state=${state}&outstate=${outstate}` +
            `&major=${major}`);
    } catch (err) {
        console.error("Network error:", err);
        alert("Unable to reach MajorHelp. Please try again.");
        return;
    }


    if (!response.ok) {
        console.error("MajorHelp returned an error" + 
            response.status + "."
        );
    }

    let data;
    try {
        data = await response.json()
    } catch(err) {
        console.error("Invalid JSON from server:", err);
        return;
    }

    showUniversitiesOnMap(data.unis);

}

// Helper: create or reset the map
function initMap(containerId = "results-map") {
    if (!map) {
        map = L.map(containerId, {
            // disable scroll wheel zoom until user interacts
            scrollWheelZoom: false
        });

        // Add OpenStreetMap tiles
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Use a plain layergroup by default
        markersLayer = L.layerGroup().addTo(map);
    } else {
        // clear existing markers
        markersLayer.clearLayers();
    }
}

// Add marker for a single university object and return marker
function addUniversityMarker(univ) {

    const marker = L.marker([univ.lat, univ.lon]);

    // A little bit overengineered but will handle partial tuition ranges by
    // only displaying one of the given halves (or N/a for none)
    const tuitionText = (univ.minTui || univ.maxTui)
        ? `${univ.minTui ? '$' + Number(univ.minTui).toLocaleString() : ''}` +
          `${(univ.minTui && univ.maxTui) ? ' - ' : ''}` +
          `${univ.maxTui ? '$' + Number(univ.maxTui).toLocaleString() : ''}`
        : 'N/A';

    // todo update
    const popupHtml = `
        <strong>${escapeHtml(univ.name)}</strong><br>
        ${escapeHtml(univ.city)}${univ.city && univ.state ? ', ' : ''}
        ${escapeHtml(univ.state)}<br>
        Tution: ${tuitionText}<br>
        <a href="${escapeAttr(univ.url)}" target="_blank" rel="noopener">
            View details
        </a>
    `;

    marker.bindPopup(popupHtml);
    marker.addTo(markersLayer);
    return marker;
}


// Main: show universities on the map. 
// `universities` is an array of objects with lat/lon
function showUniversitiesOnMap(universities) {
    initMap();

    const markersBounds = [];


    // Add university markers
    universities.forEach(univ => {
        if (typeof univ.lat !== "number" || 
            typeof univ.lon !== "number") return;

        addUniversityMarker(univ);
        markersBounds.push([univ.lat, univ.lon]);
    });

    if(markersBounds.length === 0) {
        // nothing to show - default to the USA
        map.setView([39.8283, -98.5795], 4);
    } else if (markersBounds.length === 1) {
        map.setView(markersBounds[0], 12);
    } else {
        map.fitBounds(markersBounds, { padding: [40, 40] });
    }

    // enable scroll zoom now that user has content visible
    map.scrollWheelZoom.enable();
}

// Minimal html-escaping helpers
function escapeHtml(s) {
    if (!s && s !== 0) return "";
    return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
function escapeAttr(s) {
    if (!s && s !== 0) return "";
    return String(s).replace(/"/g, "&quot;");
}

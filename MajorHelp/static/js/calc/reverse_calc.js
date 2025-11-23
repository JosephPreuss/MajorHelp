// globals
let map = null;
let markersLayer = null; 

let userLatitude;
let userLongitude;

let userCity;
let userState;

    initMap(); 
    map.setView([39.8283, -98.5795], 4);  // Show USA


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

    userLatitude  = coords.latitude;
    userLongitude = coords.longitude;

    // Reverse Geocode city and state
    const url =
    `https://nominatim.openstreetmap.org/reverse?` +
    `format=json&lat=${userLatitude}&lon=${userLongitude}`;

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

    //console.log(data);

    userCity = 
        data.address.city       ||
        data.address.town       ||
        data.address.village    ||
        data.address.hamlet;

    userState = data.address.state;

    // Fill out the inputs
    const cityInput = document.getElementById("city-input")
        .value = userCity;
    
    const stateInput = document.getElementById("state-input")
        .value = userState;
    
}


async function displayOutput() {
    // fetch details from inputs and encode
    const budgetMax = encodeURIComponent(
        document.getElementById("budget-max-raw").value);

    const budgetMin = encodeURIComponent(
        document.getElementById("budget-min-raw").value);

    // city and state will be encoded later
    const city      = 
        document.getElementById("city-input").value;

    const state     = 
        document.getElementById("state-input").value;

    const range     = encodeURIComponent(
        document.getElementById("range-input").value);

    const outstate  = encodeURIComponent(
        document.getElementById("outstate-checkbox").checked);


    // Determine lat and lon
    let lat;
    let lon;

    if (userLatitude && userLongitude && 
        userCity === city && userState === state
    ) {
        // Use previously saved geolocation coordinates
        lat = userLatitude;
        lon = userLongitude;
    } else if (state !== "No specific state") {
        // Convert city/state → lat/lon via Nominatim
        try {
            const coords = await geocodeCityState(city, state);
            userLatitude = coords.lat;
            userLongitude = coords.lon;
        } catch (err) {
            console.error(err);
            alert(err.message);
            return;
        }
    }


    // Submit to backend
    let response;
    try {
        response = await fetch("/api/reverse_calculate/?" +
            `budget-max=${budgetMax}&budget-min=${budgetMin}` +
            `&lat=${userLatitude}&lon=${userLongitude}` +
            `&range=${range}&outstate=${outstate}`);
    } catch (err) {
        console.error("Network error:", err);
        alert("Unable to reach MajorHelp. Please try again.");
        return;
    }


    if (!response.ok) {
        console.error("MajorHelp returned error " + 
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

// Convert user-typed city + state into latitude/longitude using Nominatim.
// Returns { lat, lon } or throws an error.
async function geocodeCityState(city, state) {
    const query = encodeURIComponent(`${city}, ${state}`);
    //console.log(query);
    const url = `https://nominatim.openstreetmap.org/search?` +
                `q=${query}&format=json&limit=1`;

    let response;
    try {
        response = await fetch(url, {
            headers: { "User-Agent": "MajorHelp/2.0" }
        });
    } catch (err) {
        throw new Error("Network error contacting geocoder");
    }

    if (!response.ok) {
        throw new Error(`Geocoder error: HTTP ${response.status}`);
    }

    const results = await response.json();

    if (!results || results.length === 0) {
        throw new Error("Could not find that location. Try another city/state.");
    }

    return {
        lat: Number(results[0].lat),
        lon: Number(results[0].lon)
    };
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

    const popupHtml = `
        <strong>${escapeHtml(univ.name)}</strong><br>
        ${escapeHtml(univ.city)}${univ.city && univ.state ? ', ' : ''}
        ${escapeHtml(univ.state)}<br>
        Tution: ${tuitionText}<br>
        ${univ.distance !== "N/a" ? `Distance: ${univ.distance} mi.<br>` : ''}, 
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


// To store the actual number without commas and periods,
// create a hidden input with the input name + "-raw"
function formatLocalizedNumber(input) {
    const locale = navigator.language || "en-US";

    // Save the caret position
    const selectionStart = input.selectionStart;

    // Remove all non-digits
    const digits = input.value.replace(/\D+/g, "");
    if (!digits) {
        input.value = "";
        return;
    }

    // Convert to number
    const number = parseInt(digits, 10);

    // Format with user's locale
    const formatted = new Intl.NumberFormat(locale).format(number);

    // Update field
    input.value = formatted;


    // Update raw container, if it exists
    let raw = document.getElementById(input.id + "-raw");

    if (raw)
        raw.value = number;


    // Restore caret position intelligently
    const newPos = Math.min(
        input.value.length, selectionStart + 
        (input.value.length - digits.length)
    );

    input.setSelectionRange(newPos, newPos);
}
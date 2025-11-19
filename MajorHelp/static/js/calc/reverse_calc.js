// Constants
const stateAcronyms = {
	"Alabama" : "AL",
	"Alaska" : "AK",
	"Arizona" : "AZ",
	"Arkansas" : "AR",
	"California" : "CA",
	"Colorado" : "CO",
	"Connecticut" : "CT",
	"Delaware" : "DE",
	"Florida" : "FL",
	"Georgia" : "GA",
	"Hawaii" : "HI",
	"Idaho" : "ID",
	"Illinois" : "IL",
	"Indiana" : "IN",
	"Iowa" : "IA",
	"Kansas" : "KS",
	"Kentucky" : "KY",
	"Louisiana" : "LA",
	"Maine" : "ME",
	"Maryland" : "MD",
	"Massachusetts" : "MA",
	"Michigan" : "MI",
	"Minnesota" : "MN",
	"Mississippi" : "MS",
	"Missouri" : "MO",
	"Montana" : "MT",
	"Nebraska" : "NE",
	"Nevada" : "NV",
	"New Hampshire" : "NH",
	"New Jersey" : "NJ",
	"New Mexico" : "NM",
	"New York" : "NY",
	"North Carolina" : "NC",
	"North Dakota" : "ND",
	"Ohio" : "OH",
	"Oklahoma" : "OK",
	"Oregon" : "OR",
	"Pennsylvania" : "PA",
	"Rhode Island" : "RI",
	"South Carolina" : "SC",
	"South Dakota" : "SD",
	"Tennessee" : "TN",
	"Texas" : "TX",
	"Utah" : "UT",
	"Vermont" : "VT",
	"Virginia" : "VA",
	"Washington" : "WA",
	"West Virginia" : "WV",
	"Wisconsin" : "WI",
	"Wyoming" : "WY",
	"District of Columbia" : "DC",
	"Guam" : "GU",
	"Marshall Islands" : "MH",
	"Northern Mariana Island" : "MP",
	"Puerto Rico" : "PR",
	"Virgin Islands" : "VI"
}

// globals
let majorActive = false;

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

    // Reverse Geocode city and state
    const url =
    `https://nominatim.openstreetmap.org/reverse?` +
    `format=json&lat=${latitude}&lon=${longitude}`;

    const response = await fetch(url, {
        headers: { "User-Agent": "MajorHelp/2.0" }
    });

    const data = await response.json();

    const city = 
        data.address.city ||
        data.address.town ||
        data.address.village;

    const state = data.address.state;

    // Fill out the inputs
    const cityInput = document.getElementById("city-input")
        .value = city;
    
    const stateInput = document.getElementById("state-input")
        .value = stateAcronyms[state];
    
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


function finalSubmit() {
    alert("Hello World!");
}
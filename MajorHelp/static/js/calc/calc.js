/*

Elements with unique ids that need to be appended to:
type    id              oninput / onchange function
------------------------------------------------------
div     calculator
div     input
input   uni-search          updateUniversityResults
div     uni-results
h3      uni-box
span    uni-name
input   outstate
select  dept-dropdown       updateMajorResults
div     major-results
h3      major-box
span    major-name
div     input-aid
div     aid-results
h3      aid-box

div     output
h3      summary
h1      total
span    uni-name-output
span    uni-tuition
span    uni-fees
span    major-name-output
span    major-tuition
span    major-fees
div     aid-output
span    aid-name-output
span    aid-amount
h2      total-bottom
h4      summary-bottom

*/

calcCount = 0;

const DEPARTMENT_CHOICES = [
    "Humanities and Social Sciences",
    "Natural Sciences and Mathematics",
    "Business and Economics",
    "Education",
    "Engineering and Technology",
    "Health Sciences",
    "Arts and Design",
    "Agriculture and Environmental Studies",
    "Communication and Media",
    "Law and Criminal Justice"
];

// Both for the calculator to handle two or more input fields at once and also
// to enable preset saving in the future.
const calcInput = [
/*     {
        'presetName'    :   "Preset 0",     // For later implimentation
        'uni'           :   "",
        'outstate'      :   false,
        'dept'          :   "",
        'major'         :   "",
        'aid'           :   "",
    },

    {
        'presetName'    :   "Preset 1",     // For later implimentation
        'uni'           :   "",
        'outstate'      :   false,
        'dept'          :   "",
        'major'         :   "",
        'aid'           :   "",
    }, */
]

function hidePanel() {
    document.getElementById("panel-open").style.display = "none";
    document.getElementById("panel-closed").style.display = "block";
}

function expandPanel() {
    document.getElementById("panel-closed").style.display = "none";
    document.getElementById("panel-open").style.display = "block";
}

function dismiss() {
    document.getElementById("calc-panel").style.display = "none";
}

function initializeCalculators() {
    const calculators = document.querySelectorAll("#calculators .calculator"); // Ingores master copy
    calculators.forEach((calc) => {
        const calcNum = parseInt(calc.id.split("-")[1]); // Extract number from id (e.g., "calculator-0" -> 0)
        const uniSearch = calc.querySelector(".uni-search");
        const deptDropdown = calc.querySelector(".dept-dropdown");

        // Attach event listeners
        uniSearch.addEventListener("input", () => updateUniversityResults(calcNum));
        deptDropdown.addEventListener("change", () => updateMajorResults(calcNum));

        // Add new entry to calcInput array
        calcInput.push({
            'presetName': `Preset ${calcCount}`,
            'uni': "",
            'outstate': false,
            'dept': "",
            'major': "",
            'aid': ""
        });

        calcCount++;
    });
}

function newCalc() {
    const masterCalc = document.getElementById("calculator-master-container").children[0];
    const clone = masterCalc.cloneNode(true);

    // While it might be tempting to just put in calcCount directly, that variable mutates.
    const calc = calcCount;//document.querySelectorAll("#calculators .calculator").length;

    clone.id = `calculator-${calcCount}`;

    // Update all IDs
    clone.querySelectorAll("[id]").forEach((el) => {
        el.id = el.id + calcCount; // Append calcCount to IDs
    });

    // Attach event listeners to the new calculator
    const uniSearch = clone.querySelector(".uni-search");
    const deptDropdown = clone.querySelector(".dept-dropdown");
    uniSearch.addEventListener("input", () => updateUniversityResults(calc));
    deptDropdown.addEventListener("change", () => updateMajorResults(calc));


    // Add new calculator to DOM
    document.getElementById("calculators").appendChild(clone);

    // Add new entry to calcInput array
    calcInput.push({
        'presetName': `Preset ${calcCount}`,
        'uni': "",
        'outstate': false,
        'dept': "",
        'major': "",
        'aid': ""
    });

    calcCount++;
  }


async function updateUniversityResults(calc) {
    console.log(calc);
    const query = document.getElementById(`uni-search-${calc}`).value.trim();
    if(!query) return;

    const data = await fetchUniversityData(query);
    if (data === null) return;
    const resultsContainer = document.getElementById(`uni-results-${calc}`);
    resultsContainer.innerHTML = "";

    if (data && data.universities.length > 0) {
        data.universities.forEach(uni => {
            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${uni.name}</strong> - ${uni.location}`;
            option.onclick = () => selectUniversity(calc, uni.name);
            resultsContainer.appendChild(option);
        });
    } else {
        resultsContainer.innerHTML = "<p>No universities found.</p>";
    }
}

async function fetchUniversityData(query) {
    try {
        const response = await fetch(`/api/university_search/?query=${query}`);
        if (!response.ok) throw new Error('University not found');
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

async function selectUniversity(calc, name) {

    // Update the input display
    document.getElementById(`uni-name-${calc}`).textContent = name;
    document.getElementById(`uni-box-${calc}`).style.visibility = "visible";
    document.getElementById(`uni-results-${calc}`).innerHTML = "";
    document.getElementById(`dept-dropdown-${calc}`).innerHTML =
        `<option value="" disabled selected>Select a Department</option>` +
        DEPARTMENT_CHOICES.map(dept => `<option value="${dept}">${dept}</option>`).join('');

    // Clear the major list if it is populated already
    document.getElementById(`major-results-${calc}`).replaceChildren();
    document.getElementById(`major-box-${calc}`).style.visibility = "hidden";

    // Clear the Financial Aid list if its populated already
    document.getElementById(`input-aid-${calc}`).style.display = "none";
    document.getElementById(`aid-results-${calc}`).replaceChildren();

    // Finally update the JSON
    calcInput[calc]['uni'] = name;
}

async function updateMajorResults(calc) {
    // Get data
    const university = document.getElementById(`uni-name-${calc}`).textContent;
    const department = document.getElementById(`dept-dropdown-${calc}`).value;
    if (!university || !department) return;

    const majorContainer = document.getElementById(`major-results-${calc}`);
    majorContainer.innerHTML = "";

    const data = await fetchMajors(university, department);
    if (data && data.majors.length > 0) {
        data.majors.forEach(major => {
            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${major.name}</strong>`;
            option.onclick = function() {
                selectMajor(calc, major.name);
            };
            majorContainer.appendChild(option);
        });
    } else {
        majorContainer.innerHTML = "<p>No majors found.</p>";
    }

    // Update dept in JSON
    calcInput[calc]['dept'] = department;
}

async function fetchMajors(university, department) {
    try {
        const response = await fetch(`/api/majors/?university=${encodeURIComponent(university)}&department=${encodeURIComponent(department)}`);
        if (!response.ok) throw new Error('Majors not found');
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

async function selectMajor(calc, major) {
    console.log("Major Clicked:", major);
    const university = document.getElementById(`uni-name-${calc}`).textContent;
    const outstate = document.getElementById(`outstate-${calc}`).checked;
    if (!university || !major) return;

    // Update input
    document.getElementById(`major-box-${calc}`).style.visibility = "visible";
    document.getElementById(`major-name-${calc}`).textContent = major;

    // Check if financial aid applies.
    aidData = await fetchFinancialAid(university);
    if (aidData === null) return;

    // Update the JSON
    calcInput[calc]['outstate'] = outstate;
    calcInput[calc]['major'] = major;
    
    if (aidData.aids.length > 0) {
        
        document.getElementById(`input-aid-${calc}`).style.display = "block";

        aidContainer = document.getElementById(`aid-results-${calc}`)

        aidContainer.replaceChildren();

        aidContainer.innerHTML = "<div class=\"result-item\" onclick=\"selectaid('None')\"><strong>None</strong></div>"

        aidData.aids.forEach(aid => {
            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${aid.name}</strong>`;
            option.onclick = function() {
                selectaid(calc, aid.name);
            };
            aidContainer.appendChild(option);
        });
    } else {
        // clear financial aid from the output if it was applied
        document.getElementById(`aid-output-${calc}`).style.display = "none";
        document.getElementById(`aid-name-${calc}`).innerText = "None";

        displayOutput(calc, university, outstate, major)
    }
}

async function fetchFinancialAid(query) {
    try {
        const response = await fetch(`/api/aid/?university=${encodeURIComponent(query)}`);
        if (!response.ok) {
            console.log(response.status + "\n" + response.statusText);
            throw new Error("Error Fetching Aid");
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}


function selectaid(calc, aid) {
    console.log("Aid Clicked:", aid)
    document.getElementById(`aid-name-${calc}`).innerText = aid;

    const university = document.getElementById(`uni-name-${calc}`).textContent;
    const outstate = document.getElementById(`outstate-${calc}`).checked;
    const major = document.getElementById(`major-name-${calc}`).textContent;

    calcInput[calc]['aid'] = aid;

    displayOutput(calc, university, outstate, major, aid);

}


async function displayOutput(calc, university, outstate, major, aid=null) {
    const data = await calculate(university, major, outstate, aid);
    if (!data) return;

    document.getElementById(`major-name-${calc}`).textContent = major;
    document.getElementById(`major-box-${calc}`).style.visibility = "visible";
    document.getElementById(`major-name-output-${calc}`).textContent = major;
    document.getElementById(`uni-name-output-${calc}`).textContent = university;
    document.getElementById(`uni-tuition-${calc}`).textContent = `$${data.uni.baseMinTui} - $${data.uni.baseMaxTui}`;
    document.getElementById(`uni-fees-${calc}`).textContent = `$${data.uni.fees}`;
    document.getElementById(`major-tuition-${calc}`).textContent = `$${data.major.baseMinTui} - $${data.major.baseMaxTui}`;
    document.getElementById(`major-fees-${calc}`).textContent = `$${data.major.fees}`;
    document.getElementById(`total-${calc}`).textContent = `$${data.minTui} - $${data.maxTui}`;
    document.getElementById(`total-bottom-${calc}`).textContent = `$${data.minTui} - $${data.maxTui}`;


    if(aid !== null && aid !== "None") {
        // Financial Aid was applied

        document.getElementById(`summary-${calc}`).textContent = `${data.uni.name} • ${data.major.name} • ${data.aid.name}`;
        document.getElementById(`summary-bottom-${calc}`).textContent = `${data.uni.name} • ${data.major.name} • ${data.aid.name}`;

        document.getElementById(`aid-output-${calc}`).style.display = "block";
        document.getElementById(`aid-name-output-${calc}`).innerText = data.aid.name;
        document.getElementById(`aid-amount-${calc}`).innerText = `- $${data.aid.amount}`
    } else { 

        // clear financial aid from the output if it was applied
        document.getElementById(`aid-output-${calc}`).style.display = "none";
        document.getElementById(`aid-name-${calc}`).innerText = "None";

        document.getElementById(`summary-${calc}`).textContent = `${data.uni.name} • ${data.major.name}`;
        document.getElementById(`summary-bottom-${calc}`).textContent = `${data.uni.name} • ${data.major.name}`;
    }

    document.getElementById(`output-${calc}`).style.display = 'block';
}

async function calculate(university, major, outstate, aid) {
    try {
        const response = await fetch(`/api/calculate/?university=${encodeURIComponent(university)}&major=${encodeURIComponent(major)}&outstate=${outstate}&aid=${aid}`);
        if (!response.ok) throw new Error('Calculation Failed.');
        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

// Run initialization after DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    initializeCalculators();
    // Attach click listener for "New Calculator"
    //document.querySelector(".fake-link[onclick='newCalc()']").addEventListener("click", newCalc);
});
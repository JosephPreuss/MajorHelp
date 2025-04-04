// Globals

loggedIn = false;
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
// to enable calc saving in the future.
const calcInput = [
/*  {
        'calcName'      :   "Calc 0",     // For later implimentation
        'uni'           :   "",
        'outstate'      :   false,
        'dept'          :   "",
        'major'         :   "",
        'aid'           :   "",
    },

    {
        'calcName'      :   "Calc 1",     // For later implimentation
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

    // Initialize pre-existing panels
    const panels = document.querySelectorAll("#calc-table .calc-entry"); // Ignores master
    panels.forEach((panel) => {

        // Extract number from id (e.g., "entry-0" -> 0)
        const panelNum = parseInt(panel.id.split("-")[1]);


        // Attach event listeners
        panel.querySelector(".save").addEventListener('click', () => saveCalc(panelNum));
        panel.querySelector(".clear").addEventListener('click', () => clearCalc(panelNum));
        panel.querySelector(".remove").addEventListener('click', () => removeCalc(panelNum));
    });

    // Initialize the calculators themselves
    const calculators = document.querySelectorAll("#calculators .calculator"); // Ingores master copy
    calculators.forEach((calc) => {

        // Extract number from id (e.g., "calculator-0" -> 0)
        const calcNum = parseInt(calc.id.split("-")[1]); 
        const uniSearch = calc.querySelector(".uni-search");
        const deptDropdown = calc.querySelector(".dept-dropdown");

        // Attach event listeners
        uniSearch.addEventListener("input", () => updateUniversityResults(calcNum));
        deptDropdown.addEventListener("change", () => updateMajorResults(calcNum));

        // Add new entry to calcInput array
        calcInput.push({
            'calcName': `Calculator ${calcCount}`,
            'uni': "",
            'outstate': false,
            'dept': "",
            'major': "",
            'aid': ""
        });

        calcCount++;
    });
}

function newCalc(values=null, load=false) {

    // While it might be tempting to just put in calcCount directly, that global mutates.
    const calc = calcCount;

    // check if calc isn't pointing to a previously created calculator
    if (calc < calcInput.length) {

        // simply reshow the calculator
        document.getElementById(`entry-${calc}`).style.display = "flex";
        document.getElementById(`calculator-${calc}`).style.display = "flex";
        const entryElem = document.getElementById(`entry-${calc}`);
        const calcElem = document.getElementById(`calculator-${calc}`);
        document.getElementById("calc-table").appendChild(entryElem);
        document.getElementById("calculators").appendChild(calcElem);

        // restore the json
        if (values) {
            calcInput[calc] = values;
        } else {
            calcInput[calc] = {
                'calcName': `Calculator ${calc}`,
                'uni': "",
                'outstate': false,
                'dept': "",
                'major': "",
                'aid': ""
            };
        }
        
/*         // point calcCount to the next availiable calculator
        for (var i = 0; i < calcInput.length; i++) {
            if (Object.keys(calcInput[i]).length === 0) {
                calcCount = i;
                return;
            }
        }
 */
        // There are no empty slots, point to the end of the list
        // calcCount = calcInput.length;
        
    } else {
        // calc is pointing to a new entry in calcInput.

        // Duplicate the calculator's panel
        const masterPanel = document.getElementById("calculator-master-panel-container").children[0];
        const panel = masterPanel.cloneNode(true);

        panel.id += calc;

        // Update the IDs
        panel.querySelectorAll("[id]").forEach((el) => {
            el.id = el.id + calc;
        });
        
        // Attach event listeners to the panel
        panel.querySelector(".save").addEventListener('click', () => saveCalc(calc));
        panel.querySelector(".clear").addEventListener('click', () => clearCalc(calc));
        panel.querySelector(".remove").addEventListener('click', () => removeCalc(calc));


        // Update contents of the panel
        if (values) {
            panel.querySelector(".calc-name").textContent = values.calcName;
        } else {
            panel.querySelector(".calc-name").textContent += calc;
        }

        // Add the panel to DOM
        document.getElementById("calc-table").appendChild(panel);

        // Duplicate the calculator itself
        const masterCalc = document.getElementById("calculator-master-container").children[0];
        const clone = masterCalc.cloneNode(true);

        clone.id = `calculator-${calcCount}`;

        // Update all IDs
        clone.querySelectorAll("[id]").forEach((el) => {
            el.id = el.id + calc; // Append calcCount to IDs
        });

        // Attach event listeners to the new calculator
        const uniSearch = clone.querySelector(".uni-search");
        const deptDropdown = clone.querySelector(".dept-dropdown");
        uniSearch.addEventListener("input", () => updateUniversityResults(calc));
        deptDropdown.addEventListener("change", () => updateMajorResults(calc));


        // Add new calculator to DOM
        document.getElementById("calculators").appendChild(clone);

        // Add new entry to calcInput array

        if (values) {
            calcInput.push(values);
        } else {
            calcInput.push({
                'calcName': `Calculator ${calcCount}`,
                'uni': "",
                'outstate': false,
                'dept': "",
                'major': "",
                'aid': ""
            });
        }


    }

    // Update calcCount
    let found = false;

    // point calcCount to the next availiable calculator
    for (var i = 0; !found && i < calcInput.length; i++) {
        // "if the index at i is an empty JSON object"
        if (Object.keys(calcInput[i]).length === 0) {
            calcCount = i;
            found = true;
        }
    }
    
    if (!found)
        calcCount = calcInput.length;

    // If the calculator isn't using default values, show them on the calculator's input fields
    if (values)
        updateCalc(calc);

    if (values && values.uni && values.major) {
        // Make sure to set the checkbox state BEFORE rendering output
        const outstateCheckbox = document.getElementById(`outstate-${calc}`);
        if (outstateCheckbox) {
            outstateCheckbox.checked = values.outstate === true;
        }
    
        displayOutput(calc, values.uni, values.outstate, values.major, values.aid || null);
    }
    

    // If the Calculator is one thats being loaded in, add the "Delete Save"
    // button to the panel.
    if (load) {
        const panel = document.getElementById(`entry-${calc}`);
        const deleteBtn = panel.querySelector(".delete-save");
        if (deleteBtn) {
            deleteBtn.style.display = "inline";
            deleteBtn.onclick = () => deleteSave(values.calcName.toLowerCase());
        }
    }
}

async function saveCalc(calc) {

    calcInput[calc].outstate = document.getElementById(`outstate-${calc}`).checked;
    // make the JSON of the calculator
    const json = calcInput[calc];
    const calcID = json['calcName'].toLowerCase();

    const data = {}

    data[calcID] = json;

    // post the data to the backend
    const response = await fetch(`/api/save_calc/`, {
        method: "POST",
        body: JSON.stringify(data),
        
        // Manual CSRF Token
        credentials: 'same-origin',
        headers: {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        }
    });

    // https://stackoverflow.com/questions/62416617/add-csrf-in-fetch-js-for-django

    if (!response.ok) {
        
        // Show error notification
        showNotification("Failed to save calculation. Please try again.", true);
        return;
    }

    // Show success notification
    showNotification("Calculation saved successfully!");

    // Automatically show the "Remove Save" button
    const panel = document.getElementById(`entry-${calc}`);
    const deleteBtn = panel.querySelector(".delete-save");
    if (deleteBtn) {
        deleteBtn.style.display = "inline";
    
        // Get the current calc name (key for saving)
        const calcKey = calcInput[calc].calcName.toLowerCase();
    
        // Re-bind the deleteSave functionality
        deleteBtn.onclick = () => deleteSave(calcKey);
    }
}

// https://docs.djangoproject.com/en/5.2/howto/csrf/#using-csrf
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showNotification(message, isError = false) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.className = "notification"; // Reset classes
    if (isError) {
        notification.classList.add("error");
    }
    notification.style.display = "block";

    // Auto-hide after 3 seconds
    setTimeout(() => {
        notification.style.display = "none";
    }, 3000);
}

// updateCalc takes an index in calcInput and updates its inputs to match the JSON
async function updateCalc(calc) {

    // Get the input values from the JSON
    const input = calcInput[calc];
    
    // Select the university
    await selectUniversity(calc, input.uni);

    // Select the department
    const deptDropdown = document.getElementById(`dept-dropdown-${calc}`);
    deptDropdown.value = input.dept;
    await updateMajorResults(calc);

    // Select the major
    await selectMajor(calc, input.major);

    console.log("None" ? "true" : "false");

    // If there is aid, select the aid
    if (input.aid) {
        await new Promise((r) => setTimeout(r, 100));
        selectaid(calc, input.aid);
    }
}

function clearCalc(calc) {

    // clear the frontend JSON
    calcInput[calc] =  {
        'calcName': `Calculator ${calc}`,
        'uni': "",
        'outstate': false,
        'dept': "",
        'major': "",
        'aid': ""
    };

    // Reset the HTML contents

    // reset the calculator's panel

    // Get the panel DOM
    const panel = document.getElementById(`entry-${calc}`);

    // Reset the name
    panel.querySelector(".calc-name").innerText = `Calculator ${calc}`;

    // Reset the summary

    // Get the container containing the summary
    const summary = panel.querySelector(".calc-details");

    Array.from(summary.children).forEach(child => {
        child.innerText = "None";
    });

    // Hide the aid span
    summary.querySelector(".aid").style.display = "none";
    

    // reset the calculator itself

    // get the calculator DOM
    const calculator = document.getElementById(`calculator-${calc}`);

    // Hide the output div
    calculator.querySelector(".output").style.display = "None";

    // clear the contents of the input div

    // University
    calculator.querySelector(".uni-search").value = "";

    calculator.querySelector(".uni-results").replaceChildren();

    calculator.querySelector(".uni-box").style.visibility = "hidden";
    calculator.querySelector(".uni-name").innerText = "Nothing";

    // outstate
    calculator.querySelector(".outstate").checked = false;

    // department
    calculator.querySelector(".dept-dropdown").replaceChildren();
    calculator.querySelector(".dept-dropdown").innerHTML = 
        "<option value=\"\" disabled selected>Select a Department</option>";

    // Major
    calculator.querySelector(".major-results").replaceChildren();

    calculator.querySelector(".major-box").style.visibility = "hidden";
    calculator.querySelector(".major-name").innerText = "Nothing";

    // Financial Aid
    calculator.querySelector(".input-aid").style.display = "None";

    calculator.querySelector(".aid-results").replaceChildren();

    calculator.querySelector(".aid-box").style.visibility = "hidden";
    calculator.querySelector(".aid-name").innerText = "Nothing";
}

function removeCalc(calc) {

    // Clear the calculator
    clearCalc(calc);

    // Mark the calc input as empty
    calcInput[calc] =  {};

    // Hide the panel
    document.getElementById(`entry-${calc}`).style.display = "None";
    
    // Hide the Calc
    document.getElementById(`calculator-${calc}`).style.display = "None";

    // point calcCount to the deleted calculator
    if (calc < calcCount)
        calcCount = calc;

    // Hide and unbind the Delete Save button
    const panel = document.getElementById(`entry-${calc}`);
    if (panel) {
        const deleteBtn = panel.querySelector(".delete-save");
        if (deleteBtn) {
            deleteBtn.style.display = "none";
            deleteBtn.onclick = null;
        }
    }
}

async function updateUniversityResults(calc) {
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
    const aidData = await fetchFinancialAid(university);
    if (aidData === null) return;

    // Update the JSON
    calcInput[calc]['outstate'] = outstate;
    calcInput[calc]['major'] = major;


    // Check if financial aid applies
    if (aidData.aids.length > 0) {

        // It does, so prompt the user
        
        document.getElementById(`input-aid-${calc}`).style.display = "block";

        aidContainer = document.getElementById(`aid-results-${calc}`)

        aidContainer.replaceChildren();

        aidContainer.innerHTML = `<div class=\"result-item\" onclick=\"selectaid(${calc}, \'None\')\"><strong>None</strong></div>`

        // Keep None option
        aidContainer.innerHTML = `<div class="result-item" onclick="selectaid(${calc}, 'None')"><strong>None</strong></div>`;

        // Add a custom aid input box
        const customAidContainer = document.createElement("div");
        customAidContainer.classList.add("result-item");
        customAidContainer.innerHTML = `
            <label for="custom-aid-${calc}"><strong>Enter custom aid amount ($):</strong></label><br>
            <input type="number" id="custom-aid-${calc}" min="0" style="margin-top: 5px; margin-bottom: 5px;" />
            <button type="button" onclick="applyCustomAid(${calc})">Apply</button>
        `;

        // Add any applicable aid
        aidData.aids.forEach(aid => {
            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${aid.name}</strong>`;
            option.onclick = function() {
                selectaid(calc, aid.name);
            };
            aidContainer.appendChild(option);
        });

        aidContainer.appendChild(customAidContainer);

    } else {
       // No predefined aid, but still show custom aid input and "None" option
        document.getElementById(`aid-output-${calc}`).style.display = "none";
        document.getElementById(`aid-name-${calc}`).innerText = "None";

        const aidContainer = document.getElementById(`aid-results-${calc}`);
        aidContainer.replaceChildren();

        // Always show the aid input section
        document.getElementById(`input-aid-${calc}`).style.display = "block";

        // Add "None" option
        const noneOption = document.createElement("div");
        noneOption.classList.add("result-item");
        noneOption.innerHTML = `<strong>None</strong>`;
        noneOption.onclick = () => selectaid(calc, "None");
        aidContainer.appendChild(noneOption);

        // Add a custom aid input box
        const customAidContainer = document.createElement("div");
        customAidContainer.classList.add("result-item");
        customAidContainer.innerHTML = `
            <label for="custom-aid-${calc}"><strong>Enter custom aid amount ($):</strong></label><br>
            <input type="number" id="custom-aid-${calc}" min="0" style="margin-top: 5px; margin-bottom: 5px;" />
            <button type="button" onclick="applyCustomAid(${calc})">Apply</button>
        `;
        aidContainer.appendChild(customAidContainer);

        // Proceed to display output
        displayOutput(calc, university, outstate, major);

    }
}

function applyCustomAid(calc) {
    const val = document.getElementById(`custom-aid-${calc}`).value;
    const amount = parseInt(val);
    if (isNaN(amount) || amount < 0) {
        showNotification("Please enter a valid custom aid amount.", true);
        return;
    }
    selectaid(calc, amount);  // use number instead of aid name
}


async function fetchFinancialAid(query) {
    try {
        const response = await fetch(`/api/aid/?university=${encodeURIComponent(query)}`);
        if (!response.ok) {
            console.log(response.status + "\n" + response.statusText);
            throw new Error("Error Fetching Aid");
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
    document.getElementById(`aid-box-${calc}`).style.visibility = "visible";

    const university = document.getElementById(`uni-name-${calc}`).textContent;
    const outstate = document.getElementById(`outstate-${calc}`).checked;
    const major = document.getElementById(`major-name-${calc}`).textContent;

    calcInput[calc]['aid'] = aid;

    displayOutput(calc, university, outstate, major, aid);

}


async function displayOutput(calc, university, outstate, major, aid=null) {
    const data = await calculate(university, major, outstate, aid);
    if (!data) return;

    // Update panel

    // Update the panel
    if (loggedIn) {

        // local variables
        const panel = document.getElementById(`entry-${calc}`);
        const calcName = panel.querySelector(".calc-name");


        // Update the calc name (if needed)

        // matches either the current selected university OR the default
        // "Calculator 1,2,3..." calc name
        const regex = "[C,c]alculator (\\d)+";

        if (calcName.textContent === calcInput[calc]['uni'] || 
            RegExp(regex).test(calcName.textContent))
        {

            // User has not redefined the default present name,
            // for readability, redefine the calc name to the 
            // University name.
            calcName.textContent = university;

            calcInput[calc]['calcName'] = university;
        }


        // Regardless of above, Update the summary in the panel
        panel.querySelector(".uni").textContent = university;
        panel.querySelector(".major").textContent = major;

        const aidBox = panel.querySelector(".aid");

        if (aid !== null && aid !== "None") {

            aidBox.style.display = "inline";
            aidBox.textContent = aid;
        } else {
            aidBox.style.display = "none";
        }

    }


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

async function loadSavedCalculators(savedCalculators) {
    const waitForElement = (id) => {
        return new Promise((resolve) => {
            const check = () => {
                const el = document.getElementById(id);
                if (el) return resolve(el);
                requestAnimationFrame(check);
            };
            check();
        });
    };

    let index = 0;
    for (const [key, data] of Object.entries(savedCalculators)) {
        if (index !== 0) newCalc();

        const panelId = `entry-${index}`;
        const calcId = `calculator-${index}`;

        await waitForElement(panelId);
        await waitForElement(calcId);

        const panel = document.getElementById(panelId);
        const calc = document.getElementById(calcId);

        calcInput[index] = {
            calcName: data.calcName || `Calculator ${index}`,
            uni: data.uni || "",
            outstate: data.outstate || false,
            dept: data.dept || "",
            major: data.major || "",
            aid: data.aid || ""
        };

        const deleteSaveBtn = panel.querySelector(".delete-save");
        if (deleteSaveBtn) {
            deleteSaveBtn.style.display = "inline";
            deleteSaveBtn.addEventListener('click', () => deleteSave(key)); // 👈 use key, not index
        }


        await selectUniversity(index, data.uni);

        const deptDropdown = document.getElementById(`dept-dropdown-${index}`);
        if (deptDropdown) {
            deptDropdown.value = data.dept;
            await updateMajorResults(index);
        }

        await selectMajor(index, data.major);

        if (data.aid && data.aid !== "None") {
            await new Promise((r) => setTimeout(r, 100));
            selectaid(index, data.aid);
        }

        document.getElementById(`uni-name-${index}`).textContent = data.uni;
        document.getElementById(`uni-box-${index}`).style.visibility = "visible";

        document.getElementById(`major-name-${index}`).textContent = data.major;
        document.getElementById(`major-box-${index}`).style.visibility = "visible";

        document.getElementById(`aid-name-${index}`).textContent = data.aid || "None";
        document.getElementById(`aid-box-${index}`).style.visibility = data.aid ? "visible" : "hidden";
        document.getElementById(`input-aid-${index}`).style.display = data.aid ? "block" : "none";

        panel.querySelector(".calc-name").textContent = data.calcName || `Calculator ${index}`;
        panel.querySelector(".uni").textContent = data.uni || "None";
        panel.querySelector(".major").textContent = data.major || "None";

        const aidElem = panel.querySelector(".aid");
        aidElem.textContent = data.aid || "None";
        aidElem.style.display = data.aid ? "inline" : "none";

        const outstateCheckbox = document.getElementById(`outstate-${index}`);
        if (outstateCheckbox) outstateCheckbox.checked = data.outstate === true;
        if (
            data.uni &&
            data.dept &&
            data.major &&
            typeof data.outstate !== 'undefined'
        ) {
            await displayOutput(index, data.uni, data.outstate, data.major, data.aid || null);
        }
        index++;
    }

    calcCount = index;
}

async function deleteSave(calcKey) {
    console.log(`Removing save for key: ${calcKey}`);

    const response = await fetch(`/api/save_calc/`, {
        method: "DELETE",
        body: JSON.stringify({ [calcKey]: true }),
        credentials: 'same-origin',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        }
    });

    if (!response.ok) {
        showNotification("Failed to delete saved calculation.", true);
        return;
    }

    showNotification("Saved calculation deleted.");

    // Hide delete Save button for all panels that match this key
    document.querySelectorAll(".calc-entry").forEach(panel => {
        const name = panel.querySelector(".calc-name").textContent.toLowerCase();
        if (name === calcKey.toLowerCase()) {
            const deleteBtn = panel.querySelector(".delete-save");
            if (deleteBtn) deleteBtn.style.display = "none";
        }
    });
}

async function updateCalcResults() {
    const query = document.getElementById("loadCalc").value.trim();
    if (!query) return;

    const data = await fetchSavedCalculators(query);
    if (!data === null) return;
    const resultsContainer = document.getElementById("loadResults");
    resultsContainer.innerHTML = "";

    console.log(data, data.calculators.length > 0);

    if (data && data.calculators.length > 0) {
        data.calculators.forEach(calc => {
            console.log(calc.calcName); 

            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${calc.calcName}</strong>`;
            option.onclick = () => loadSavedCalculator(calc);
            resultsContainer.appendChild(option);
        });
    } else {
        resultsContainer.innerHTML = "<p>No saved calculators found.</p>"; 
    }
}

async function fetchSavedCalculators(query) {
    try {
        const response = await fetch(`/api/calcs/?query=${query}`);
        if (!response.ok) throw new Error(`Could not find any saved Calculators with query ${query}.`);
        return await response.json();
    } catch(error) {
        console.error(error);
        return null;
    }
}

function loadSavedCalculator(calcJSON) {

    // clear the loaded results
    document.getElementById("loadResults").innerHTML = "";

    // clear the search bar
    document.getElementById("loadCalc").value = "";

    // call newCalc
    newCalc(calcJSON, true);

    // Send a notification to the user that the calculator has loaded successfully
    showNotification("Calculator loaded successfully!");
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("panel-open")) {
        loggedIn = true;
        
        // Set up load Calculator event listener
        document.getElementById("loadCalc").addEventListener("input", () => updateCalcResults());
    }
    console.log(loggedIn ? "User is logged in." : "User is anonymous.");

    const scriptTag = document.getElementById("saved-calcs-data");

    if (scriptTag) {
        let savedCalculators = {};
        try {
            savedCalculators = JSON.parse(scriptTag.textContent);
            console.log("Loaded saved data:", savedCalculators);
        } catch (e) {
            console.error("Failed to parse saved calculator data:", e);
        }
        
        // TODO, replace function call with a similar version that only gets the calculators from
        //       the previous session.

        //loadSavedCalculators(savedCalculators);
    }

    initializeCalculators(); 
});
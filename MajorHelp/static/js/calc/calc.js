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

aidData = null;

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

async function updateUniversityResults() {
    const query = document.getElementById("uni-search").value.trim();
    if (!query) return;
    
    const data = await fetchUniversityData(query);
    const resultsContainer = document.getElementById("university-results");
    resultsContainer.innerHTML = "";

    if (data && data.universities.length > 0) {
        data.universities.forEach(uni => {
            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${uni.name}</strong> - ${uni.location}`;
            option.onclick = () => selectUniversity(uni.name);
            resultsContainer.appendChild(option);
        });
    } else {
        resultsContainer.innerHTML = "<p>No universities found.</p>";
    }
}

async function selectUniversity(name) {
    // Check if any Financial Aid or misc applies
    aidData = await fetchFinancialAid(name);

    // ..and save the info for later.


    document.getElementById("uni-name").textContent = name;
    document.getElementById("uni-box").style.visibility = "visible";
    document.getElementById("university-results").innerHTML = "";
    document.getElementById("department-dropdown").innerHTML =
        `<option value="" disabled selected>Select a Department</option>` +
        DEPARTMENT_CHOICES.map(dept => `<option value="${dept}">${dept}</option>`).join('');

    // Clear the major list if it is populated already
    document.getElementById("major-results").replaceChildren();
    document.getElementById("major-box").style.visibility = "hidden";

    // Clear the Financial Aid list if its populated already
    document.getElementById("input-aid").style.display = "none";
    document.getElementById("aid-results").replaceChildren();
}

async function updateMajorResults() {
    const university = document.getElementById("uni-name").textContent;
    const department = document.getElementById("department-dropdown").value;
    if (!university || !department) return;

    const data = await fetchMajors(university, department);
    const majorContainer = document.getElementById("major-results");
    majorContainer.innerHTML = "";

    if (data && data.majors.length > 0) {
        data.majors.forEach(major => {
            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${major.name}</strong>`;
            option.onclick = function() {
                selectMajor(major.name);
            };
            majorContainer.appendChild(option);
        });
    } else {
        majorContainer.innerHTML = "<p>No majors found.</p>";
    }
}

async function selectMajor(major) {
    console.log("Major Clicked:", major);
    const university = document.getElementById("uni-name").textContent;
    const outstate = document.getElementById("outstate").checked;
    if (!university || !major) return;

    // Update input
    document.getElementById("major-box").style.visibility = "visible";
    document.getElementById("major-name").textContent = major;
    

    // Check if financial aid applies 
    if (aidData.aids.length > 0) {
        
        document.getElementById("input-aid").style.display = "block";

        aidContainer = document.getElementById("aid-results")

        aidContainer.replaceChildren();

        aidContainer.innerHTML = "<div class=\"result-item\" onclick=\"selectaid('None')\"><strong>None</strong></div>"

        aidData.aids.forEach(aid => {
            let option = document.createElement("div");
            option.classList.add("result-item");
            option.innerHTML = `<strong>${aid.name}</strong>`;
            option.onclick = function() {
                selectaid(aid.name);
            };
            aidContainer.appendChild(option);
        });
    } else {
        displayOutput(university, outstate, major)
    }
}

function selectaid(aid) {
    console.log("Aid Clicked:", aid)
    const university = document.getElementById("uni-name").textContent;
    const outstate = document.getElementById("outstate").checked;
    const major = document.getElementById("major-name").textContent;

    displayOutput(university, outstate, major, aid);

}

async function displayOutput(university, outstate, major, aid=null) {
    const data = await calculate(university, major, outstate, aid);
    if (!data) return;

    document.getElementById("major-name").textContent = major;
    document.getElementById("major-box").style.visibility = "visible";
    document.getElementById("major-name-output").textContent = major;
    document.getElementById("uni-name-output").textContent = university;
    document.getElementById("uni-tuition").textContent = `$${data.uni.baseMinTui} - $${data.uni.baseMaxTui}`;
    document.getElementById("uni-fees").textContent = `$${data.uni.fees}`;
    document.getElementById("major-tuition").textContent = `$${data.major.baseMinTui} - $${data.major.baseMaxTui}`;
    document.getElementById("major-fees").textContent = `$${data.major.fees}`;
    document.getElementById("total").textContent = `$${data.minTui} - $${data.maxTui}`;
    document.getElementById("total-bottom").textContent = `$${data.minTui} - $${data.maxTui}`;


    if(aid !== null && aid !== "None") {
        // Financial Aid was applied

        document.getElementById("summary").textContent = `${data.uni.name} • ${data.major.name} • ${data.aid.name}`;
        document.getElementById("summary-bottom").textContent = `${data.uni.name} • ${data.major.name} • ${data.aid.name}`;

        document.getElementById("aid-output").style.display = "block";
        document.getElementById("aid-name-output").innerText = data.aid.name;
        document.getElementById("aid-amount").innerText = `- $${data.aid.amount}`
    } else { 

        document.getElementById("summary").textContent = `${data.uni.name} • ${data.major.name}`;
        document.getElementById("summary-bottom").textContent = `${data.uni.name} • ${data.major.name}`;
    }

    document.getElementById("output").style.display = 'block';
}
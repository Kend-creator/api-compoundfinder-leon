const API_URL = "https://simply-cars-api-leon.vercel.app";


// GET ALL COMPOUNDS
async function loadCompounds() {
    try {
        const response = await fetch(`${API_URL}/compounds`);
        const data = await response.json();
        displayCompounds(data.compounds);
    }

    catch (error) {
        console.error(error);
        document.getElementById("compoundList").innerHTML = "Unable to connect to the API.";
    }
}


// DISPLAY COMPOUNDS
function displayCompounds(compounds) {
    const compoundList =
        document.getElementById("compoundList");

    compoundList.innerHTML = "";

    compounds.forEach(compound => {
        const card = document.createElement("div");
        card.className = "compound-card";
        card.innerHTML = `
            <div class="compound-formula">${compound.formula}</div>
            <h3>${compound.name}</h3>
            <p class="compound-category">${compound.category}</p>
            <p>${compound.elements.join(", ")}</p>
            <p>Molar mass: ${compound.molar_mass} g/mol</p>
            <button onclick="viewCompound(${compound.id})"> View Details</button>
        `;

        compoundList.appendChild(card);
    });

}

// GET ONE COMPOUND
async function viewCompound(id) {

    try {
        const response = await fetch(`${API_URL}/compounds/${id}`);
        const compound = await response.json();

        alert(`
            ${compound.name} (${compound.formula})
            Elements:
            ${compound.elements.join(", ")}

            State:
            ${compound.state}

            Molar Mass:
            ${compound.molar_mass} g/mol

            Description:
            ${compound.description}
        `);
    }
    catch (error) {
        console.error(error);
        alert("Unable to retrieve compound.");
    }

}

// SEARCH
async function searchCompounds() {

    const query = document.getElementById("searchInput").value;
    if (!query) {
        loadCompounds();
        return;
    }
    try {
        const response =
            await fetch(`${API_URL}/compounds/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        displayCompounds(data.results);
    }

    catch (error) {
        console.error(error);
        alert("Search failed.");
    }
}

loadCompounds();
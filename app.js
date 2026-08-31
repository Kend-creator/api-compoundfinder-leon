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
        const props = compound.physicalProperties;
        const elementSymbols = compound.composition
            .map(c => `${c.symbol}${c.atoms > 1 ? c.atoms : ""}`)
            .join("");

        const card = document.createElement("div");
        card.className = "compound-card";
        card.innerHTML = `
            <div class="compound-formula">${compound.formula}</div>
            <h3>${compound.name}</h3>
            <p class="compound-state">${props.state}</p>
            <p>${elementSymbols}</p>
            <p>Molar mass: ${props.molarMass} g/mol</p>
            ${compound.safetyData.isCorrosive ? `<span class="badge-danger">${compound.safetyData.signalWord}</span>` : ""}
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
        const props = compound.physicalProperties;
        const elements = compound.composition
            .map(c => `${c.element} (${c.symbol}): ${c.atoms}`)
            .join("\n            ");

        alert(`
            ${compound.name} (${compound.formula})
            SMILES: ${compound.smiles}

            Elements:
            ${elements}

            State: ${props.state}
            Molar Mass: ${props.molarMass} g/mol
            Density: ${props.densityGPerCm3} g/cm3
            Melting Point: ${props.meltingPointCelsius ?? "N/A"} C
            Boiling Point: ${props.boilingPointCelsius ?? "N/A"} C

            Safety: ${compound.safetyData.signalWord}${compound.safetyData.isCorrosive ? " (Corrosive)" : ""}

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
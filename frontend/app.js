const API_URL = "https://api-compoundfinder-leon.vercel.app";


// GET ALL COMPOUNDS
async function loadCompounds() {
    try {
        const response = await fetch(`${API_URL}/compounds`);
        const data = await response.json();
        displayCompounds(data.compounds);
    }

    catch (error) {
        console.error(error);
        document.getElementById("compoundList").innerHTML =
            '<p class="status-text">Unable to connect to the API.</p>';
    }
}


// DISPLAY COMPOUNDS
function displayCompounds(compounds) {
    const compoundList =
        document.getElementById("compoundList");

    compoundList.innerHTML = "";

    if (!compounds || compounds.length === 0) {
        compoundList.innerHTML = '<p class="status-text">No compounds found.</p>';
        return;
    }

    compounds.forEach((compound, index) => {
        const props = compound.physicalProperties;
        const state = (props.state || "").toLowerCase();

        const card = document.createElement("div");
        card.className = "compound-card";
        card.dataset.state = state;
        card.style.animationDelay = `${index * 40}ms`;
        card.innerHTML = `
            <div class="compound-formula">${compound.formula}</div>
            <h3>${compound.name}</h3>
            <div class="badge-row">
                <span class="state-badge" data-state="${state}">${props.state}</span>
                ${compound.safetyData.isCorrosive ? `<span class="badge-danger">${compound.safetyData.signalWord}</span>` : ""}
            </div>
            <p class="compound-description">${compound.description ?? ""}</p>
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
        const state = (props.state || "").toLowerCase();

        const elementsList = compound.composition
            .map(c => `<li>${c.element} (${c.symbol}): ${c.atoms}</li>`)
            .join("");

        const modalContent = document.getElementById("modalContent");
        modalContent.innerHTML = `
            <div class="modal-formula">${compound.formula}</div>
            <h3 id="modalTitle">${compound.name}</h3>
            <p class="modal-smiles">SMILES: ${compound.smiles}</p>

            <div class="badge-row">
                <span class="state-badge" data-state="${state}">${props.state}</span>
                ${compound.safetyData.isCorrosive ? `<span class="badge-danger">${compound.safetyData.signalWord} (Corrosive)</span>` : ""}
            </div>

            <p class="modal-section-title">Elements</p>
            <ul class="modal-elements">${elementsList}</ul>

            <p class="modal-section-title">Properties</p>
            <div class="modal-props">
                <div><span>Molar mass</span>${props.molarMass} g/mol</div>
                <div><span>Density</span>${props.densityGPerCm3} g/cm3</div>
                <div><span>Melting point</span>${props.meltingPointCelsius ?? "N/A"} &deg;C</div>
                <div><span>Boiling point</span>${props.boilingPointCelsius ?? "N/A"} &deg;C</div>
            </div>

            ${compound.uses && compound.uses.length ? `
            <p class="modal-section-title">Common Uses</p>
            <div class="modal-uses">
                ${compound.uses.map(u => `<span class="use-tag">${u}</span>`).join("")}
            </div>
            ` : ""}

            <p class="modal-section-title">Description</p>
            <p class="modal-description">${compound.description}</p>
        `;

        openModal();
    }
    catch (error) {
        console.error(error);
        alert("Unable to retrieve compound.");
    }

}

// MODAL CONTROLS
function openModal() {
    const overlay = document.getElementById("detailOverlay");
    overlay.hidden = false;
    requestAnimationFrame(() => overlay.classList.add("visible"));
}

function closeModal() {
    const overlay = document.getElementById("detailOverlay");
    overlay.classList.remove("visible");
    setTimeout(() => {
        overlay.hidden = true;
    }, 200);
}

document.getElementById("detailOverlay").addEventListener("click", (e) => {
    if (e.target.id === "detailOverlay") closeModal();
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
});

document.getElementById("searchInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") searchCompounds();
});

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
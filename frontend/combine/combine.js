const PROXY_URL = "/api/proxy";

// Shared navigation and theme controls
const menuButton = document.querySelector('.menu-button')
const navigation = document.querySelector('.main-nav')
const themeToggle = document.querySelector('.theme-toggle')

function updateThemeButton(theme) {
  const nextTheme = theme === 'dark' ? 'light' : 'dark'
  themeToggle.setAttribute('aria-label', `Switch to ${nextTheme} mode`)
  themeToggle.setAttribute('title', `Switch to ${nextTheme} mode`)
}

// Apply and persist the visitor's selected color theme
updateThemeButton(document.documentElement.dataset.theme || 'light')

themeToggle.addEventListener('click', () => {
  const currentTheme = document.documentElement.dataset.theme
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = nextTheme
  updateThemeButton(nextTheme)
  try {
    localStorage.setItem('compound-lab-theme', nextTheme)
  } catch {
    // The theme still changes when storage is unavailable.
  }
})

function closeMenu() {
  navigation.classList.remove('is-open')
  menuButton.setAttribute('aria-expanded', 'false')
}

// Mobile navigation behavior
menuButton.addEventListener('click', () => {
  const isOpen = navigation.classList.toggle('is-open')
  menuButton.setAttribute('aria-expanded', String(isOpen))
})

navigation.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', closeMenu)
})

// Known reaction outcomes indexed by alphabetized reactant keys
const reactions = {
  'HCl+NaOH': {
    type: 'NEUTRALIZATION',
    formula: 'NaCl + H₂O',
    name: 'Sodium chloride + Water',
    description:
      'An acid and a base neutralize one another, forming salt and water while releasing heat.',
  },
  'CH3COOH+NaHCO3': {
    type: 'ACID–CARBONATE',
    formula: 'CH₃COONa + CO₂ + H₂O',
    name: 'Sodium acetate + Carbon dioxide',
    description:
      'A lively acid–carbonate reaction creates sodium acetate, water, and bubbles of carbon dioxide.',
  },
  'CO2+H2O': {
    type: 'SYNTHESIS',
    formula: 'H₂CO₃',
    name: 'Carbonic acid',
    description: 'Dissolved carbon dioxide combines reversibly with water to produce a weak acid.',
  },
  'HCl+NaHCO3': {
    type: 'ACID–CARBONATE',
    formula: 'NaCl + CO₂ + H₂O',
    name: 'Sodium chloride + Carbon dioxide',
    description:
      'The bicarbonate reacts with acid, rapidly producing salt, water, and carbon dioxide gas.',
  },
  'H2O+NH3': {
    type: 'ACID–BASE EQUILIBRIUM',
    formula: 'NH₄⁺ + OH⁻',
    name: 'Ammonium + Hydroxide ions',
    description:
      'Ammonia accepts a proton from water, establishing an equilibrium of ammonium and hydroxide ions.',
  },
}

// Reaction workspace elements and in-memory session state
const slots = {
  a: document.querySelector('[data-slot="a"]'),
  b: document.querySelector('[data-slot="b"]'),
}
const mixButton = document.querySelector('.combine-button')
const mixButtonLabel = document.querySelector('.combine-button-label')
const resultPanel = document.querySelector('.result-panel')
const resultEmpty = document.querySelector('.result-empty')
const resultContent = document.querySelector('.result-content')
const discoveryList = document.querySelector('.discovery-list')
const discoveryCount = document.querySelector('.discovery-count')
const shelfHint = document.querySelector('.shelf-hint strong')
const selections = { a: null, b: null }
const discoveries = new Map()
let activeSlot = 'a'
let reactionTimer

// Highlight the vessel that will receive the next selected compound
function setActiveSlot(slotName) {
  activeSlot = slotName
  Object.entries(slots).forEach(([name, slot]) => {
    slot.classList.toggle('is-active', name === slotName)
  })
  shelfHint.textContent = slotName.toUpperCase()
}

// Return the result chamber to its initial waiting state
function resetResult() {
  clearTimeout(reactionTimer)
  resultPanel.classList.remove('is-reacting')
  resultEmpty.hidden = false
  resultContent.hidden = true
  resultEmpty.querySelector('strong').textContent = 'Awaiting reaction'
  resultEmpty.querySelector('p').textContent =
    'Your result will appear here after combining two compounds.'
}

// Enable mixing only when both vessels contain a compound
function updateMixState() {
  const ready = Boolean(selections.a && selections.b)
  mixButton.disabled = !ready
  mixButtonLabel.textContent = ready ? 'Combine compounds' : 'Select two compounds'

  document.querySelectorAll('.compound-option').forEach((option) => {
    option.classList.toggle(
      'is-used',
      option.dataset.key === selections.a?.key || option.dataset.key === selections.b?.key,
    )
  })
}

// Add a compound from the shelf to the selected vessel
function placeCompound(slotName, compound) {
  selections[slotName] = compound
  const slot = slots[slotName]
  slot.classList.add('has-compound')
  slot.style.setProperty('--liquid', compound.color)
  slot.querySelector('.slot-content strong').textContent = compound.formula
  slot.querySelector('.slot-content small').textContent = compound.name
  resetResult()
  updateMixState()
}

// Allow either vessel to be selected directly
Object.entries(slots).forEach(([name, slot]) => {
  slot.addEventListener('click', () => setActiveSlot(name))
})

// Convert shelf data attributes into a compound selection
document.querySelectorAll('.compound-option').forEach((option) => {
  option.addEventListener('click', () => {
    const compound = {
      key: option.dataset.key,
      formula: option.dataset.formula,
      name: option.dataset.name,
      color: getComputedStyle(option).getPropertyValue('--liquid').trim(),
    }
    placeCompound(activeSlot, compound)

    if (activeSlot === 'a' && !selections.b) {
      setActiveSlot('b')
    }
  })
})

// Add newly produced compounds to the session reaction log
function addDiscovery(result) {
  if (discoveries.has(result.formula)) return false
  discoveries.set(result.formula, result.name)
  discoveryCount.textContent = String(discoveries.size)
  discoveryList.querySelector('.empty-discoveries')?.remove()

  const chip = document.createElement('span')
  chip.className = 'discovery-chip'
  const formula = document.createElement('strong')
  formula.textContent = result.formula
  const name = document.createElement('span')
  name.textContent = result.name
  chip.append(formula, name)
  discoveryList.append(chip)
  return true
}

// Render the final reaction details and balanced display equation
function showReaction(result, isDiscovery) {
  resultPanel.classList.remove('is-reacting')
  resultEmpty.hidden = true
  resultContent.hidden = false
  resultContent.querySelector('.reaction-type').textContent = result.type
  resultContent.querySelector('.result-formula').textContent = result.formula
  resultContent.querySelector('.result-name').textContent = result.name
  resultContent.querySelector('.result-description').textContent = result.description
  resultContent.querySelector('.equation-inputs').textContent =
    `${selections.a.formula} + ${selections.b.formula}`
  resultContent.querySelector('.equation-output').textContent = result.formula
  resultContent.querySelector('.discovery-badge').hidden = !isDiscovery
}

// Run the reaction simulation and resolve known or stable mixtures
mixButton.addEventListener('click', () => {
  if (!selections.a || !selections.b) return

  const reactionKey = [selections.a.key, selections.b.key].sort().join('+')
  const knownReaction = reactions[reactionKey]
  const result = knownReaction || {
    type: 'NO REACTION OBSERVED',
    formula: 'No reaction',
    name: 'Stable mixture',
    description:
      'These compounds do not produce a clear reaction under standard virtual-lab conditions. Try another pairing.',
  }

  resultContent.hidden = true
  resultEmpty.hidden = false
  resultEmpty.querySelector('strong').textContent = 'Analyzing reaction…'
  resultEmpty.querySelector('p').textContent = 'Tracking molecular changes and energy transfer.'
  resultPanel.classList.add('is-reacting')
  mixButton.disabled = true
  mixButtonLabel.textContent = 'Reaction in progress…'

  reactionTimer = window.setTimeout(() => {
    const isDiscovery = knownReaction ? addDiscovery(result) : false
    showReaction(result, isDiscovery)
    updateMixState()
  }, 950)
})

// Clear both vessels without removing the session discovery history
document.querySelector('.reset-mix').addEventListener('click', () => {
  selections.a = null
  selections.b = null

  Object.values(slots).forEach((slot) => {
    slot.classList.remove('has-compound')
    slot.style.removeProperty('--liquid')
    slot.querySelector('.slot-content strong').textContent = 'Select compound'
    slot.querySelector('.slot-content small').textContent = 'Choose from the shelf below'
  })

  setActiveSlot('a')
  resetResult()
  updateMixState()
})

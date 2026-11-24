const PROXY_URL = "/api/proxy";

const MAX_GUESSES = 5
const MOLAR_MASS_CLOSE_THRESHOLD = 0.15

// Offline data keeps Guessr playable until the user's compound API is connected.
const SAMPLE_COMPOUNDS = [
  {
    id: 'water',
    name: 'Water',
    formula: 'H2O',
    compoundType: 'Molecular',
    composition: [{ symbol: 'H' }, { symbol: 'O' }],
    physicalProperties: { state: 'Liquid', molarMass: 18.02 },
    description: 'A bent polar molecule that is essential to life and an excellent solvent.',
  },
  {
    id: 'carbon-dioxide',
    name: 'Carbon dioxide',
    formula: 'CO2',
    compoundType: 'Molecular',
    composition: [{ symbol: 'C' }, { symbol: 'O' }],
    physicalProperties: { state: 'Gas', molarMass: 44.01 },
    description: 'A linear gas produced by respiration and used by plants during photosynthesis.',
  },
  {
    id: 'ammonia',
    name: 'Ammonia',
    formula: 'NH3',
    compoundType: 'Molecular',
    composition: [{ symbol: 'N' }, { symbol: 'H' }],
    physicalProperties: { state: 'Gas', molarMass: 17.03 },
    description: 'A pungent nitrogen compound widely used to manufacture fertilizers.',
  },
  {
    id: 'methane',
    name: 'Methane',
    formula: 'CH4',
    compoundType: 'Molecular',
    composition: [{ symbol: 'C' }, { symbol: 'H' }],
    physicalProperties: { state: 'Gas', molarMass: 16.04 },
    description: 'The simplest hydrocarbon, built around one tetrahedral carbon atom.',
  },
  {
    id: 'sodium-chloride',
    name: 'Sodium chloride',
    formula: 'NaCl',
    compoundType: 'Ionic',
    composition: [{ symbol: 'Na' }, { symbol: 'Cl' }],
    physicalProperties: { state: 'Solid', molarMass: 58.44 },
    description: 'A familiar crystalline ionic compound commonly known as table salt.',
  },
  {
    id: 'sodium-hydroxide',
    name: 'Sodium hydroxide',
    formula: 'NaOH',
    compoundType: 'Ionic',
    composition: [{ symbol: 'Na' }, { symbol: 'O' }, { symbol: 'H' }],
    physicalProperties: { state: 'Solid', molarMass: 40 },
    description: 'A strongly basic ionic compound used in manufacturing and laboratory work.',
  },
  {
    id: 'acetic-acid',
    name: 'Acetic acid',
    formula: 'CH3COOH',
    compoundType: 'Molecular',
    composition: [{ symbol: 'C' }, { symbol: 'H' }, { symbol: 'O' }],
    physicalProperties: { state: 'Liquid', molarMass: 60.05 },
    description: 'A weak organic acid responsible for the characteristic sharpness of vinegar.',
  },
  {
    id: 'calcium-carbonate',
    name: 'Calcium carbonate',
    formula: 'CaCO3',
    compoundType: 'Ionic',
    composition: [{ symbol: 'Ca' }, { symbol: 'C' }, { symbol: 'O' }],
    physicalProperties: { state: 'Solid', molarMass: 100.09 },
    description: 'A mineral compound found in limestone, chalk, shells, and pearls.',
  },
]

let allCompounds = []
let secretCompound = null
let guessesRemaining = MAX_GUESSES
let guessedNames = new Set()
let roundOver = false

// Shared navigation, theme persistence, and responsive menu behavior.
const themeToggle = document.querySelector('.theme-toggle')
const menuButton = document.querySelector('.menu-button')
const navigation = document.querySelector('.main-nav')

function updateThemeButton(theme) {
  const nextTheme = theme === 'dark' ? 'light' : 'dark'
  themeToggle.setAttribute('aria-label', `Switch to ${nextTheme} mode`)
  themeToggle.setAttribute('title', `Switch to ${nextTheme} mode`)
}

updateThemeButton(document.documentElement.dataset.theme || 'light')

themeToggle.addEventListener('click', () => {
  const currentTheme = document.documentElement.dataset.theme
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = nextTheme
  updateThemeButton(nextTheme)

  try {
    localStorage.setItem('compound-lab-theme', nextTheme)
  } catch {
    // Theme switching still works when storage is unavailable.
  }
})

function closeMenu() {
  navigation.classList.remove('is-open')
  menuButton.setAttribute('aria-expanded', 'false')
}

menuButton.addEventListener('click', () => {
  const isOpen = navigation.classList.toggle('is-open')
  menuButton.setAttribute('aria-expanded', String(isOpen))
})

navigation.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu))

/*
BACKEND INTEGRATION — intentionally disabled for this frontend-only delivery.

Replace SAMPLE_COMPOUNDS in init() with the server response when your proxy is ready:

  const PROXY_URL = '/api/proxy'
  const response = await fetch(`${PROXY_URL}?path=/compounds`)
  if (!response.ok) throw new Error('API request failed')
  const data = await response.json()
  allCompounds = data.compounds

Each compound should include:
  id, name, formula, description, compoundType,
  composition: [{ symbol }],
  physicalProperties: { state, molarMass }
*/

// Initialize the offline library and begin a new randomized round.
function init() {
  allCompounds = SAMPLE_COMPOUNDS
  populateNameList(allCompounds)
  startNewRound()
}

function populateNameList(compounds) {
  const datalist = document.querySelector('#compoundNames')
  datalist.replaceChildren()

  compounds.forEach((compound) => {
    const option = document.createElement('option')
    option.value = compound.name
    datalist.appendChild(option)
  })
}

// Reset every round-specific value while keeping the same local compound library.
function startNewRound() {
  secretCompound = allCompounds[Math.floor(Math.random() * allCompounds.length)]
  guessesRemaining = MAX_GUESSES
  guessedNames = new Set()
  roundOver = false

  document.querySelector('#guessHistory').innerHTML = `
    <div class="empty-history">
      <span>?</span>
      <p>Your comparison clues will appear here.</p>
    </div>
  `
  document.querySelector('#guessError').textContent = ''
  document.querySelector('#guessInput').value = ''
  document.querySelector('#guessInput').disabled = false
  document.querySelector('#submitGuessBtn').disabled = false
  document.querySelector('#roundEndPanel').hidden = true
  document.querySelector('#roundStatus').textContent = 'In progress'
  updateGuessesLeft()
  renderHint()
  document.querySelector('#guessInput').focus()
}

function updateGuessesLeft() {
  document.querySelector('#guessesLeft').textContent =
    `${guessesRemaining} guess${guessesRemaining === 1 ? '' : 'es'} left`
}

// Mask the answer's own name and formula if either appears in its description.
function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function maskAnswer(text, compound) {
  const blank = '█████'
  const nameRegex = new RegExp(escapeRegExp(compound.name), 'gi')
  const formulaRegex = new RegExp(
    `(?<![A-Za-z0-9])${escapeRegExp(compound.formula)}(?![A-Za-z0-9])`,
    'gi',
  )
  return text.replace(nameRegex, blank).replace(formulaRegex, blank)
}

function renderHint() {
  document.querySelector('#hintText').textContent = maskAnswer(
    secretCompound.description,
    secretCompound,
  )
}

// Validate the selected name, record the attempt, and end the round when appropriate.
function submitGuess() {
  if (roundOver) return

  const input = document.querySelector('#guessInput')
  const guessName = input.value.trim()
  const error = document.querySelector('#guessError')

  if (!guessName) {
    error.textContent = 'Enter a compound name before submitting.'
    return
  }

  const guessedCompound = allCompounds.find(
    (compound) => compound.name.toLowerCase() === guessName.toLowerCase(),
  )

  if (!guessedCompound) {
    error.textContent = 'Choose a recognized compound from the suggestion list.'
    return
  }

  if (guessedNames.has(guessedCompound.name)) {
    error.textContent = 'You already guessed that compound.'
    return
  }

  error.textContent = ''
  guessedNames.add(guessedCompound.name)
  guessesRemaining -= 1
  renderGuessRow(guessedCompound)
  input.value = ''

  if (guessedCompound.id === secretCompound.id) {
    endRound(true)
    return
  }

  updateGuessesLeft()
  if (guessesRemaining <= 0) endRound(false)
}

// Produce exact, close, or miss tiers for the four visible clue categories.
function buildClues(guess) {
  const stateMatch = guess.physicalProperties.state === secretCompound.physicalProperties.state
  const typeMatch = guess.compoundType === secretCompound.compoundType

  return [
    {
      label: 'State',
      value: guess.physicalProperties.state,
      tier: stateMatch ? 'hit' : 'miss',
    },
    {
      label: 'Type',
      value: guess.compoundType,
      tier: typeMatch ? 'hit' : 'miss',
    },
    buildMolarMassClue(
      guess.physicalProperties.molarMass,
      secretCompound.physicalProperties.molarMass,
    ),
    buildElementsClue(guess),
  ]
}

function buildMolarMassClue(guessMass, secretMass) {
  if (guessMass === secretMass) {
    return { label: 'Molar mass', value: `${guessMass} g/mol`, tier: 'hit' }
  }

  const percentDifference = Math.abs(guessMass - secretMass) / secretMass
  const arrow = guessMass < secretMass ? '↑' : '↓'
  const tier = percentDifference <= MOLAR_MASS_CLOSE_THRESHOLD ? 'close' : 'miss'
  return { label: 'Molar mass', value: `${guessMass} g/mol ${arrow}`, tier }
}

function buildElementsClue(guess) {
  const guessSymbols = [...new Set(guess.composition.map((element) => element.symbol))]
  const secretSymbols = [...new Set(secretCompound.composition.map((element) => element.symbol))]
  const shared = guessSymbols.filter((symbol) => secretSymbols.includes(symbol))
  const exactMatch =
    shared.length === guessSymbols.length && shared.length === secretSymbols.length

  if (exactMatch) return { label: 'Elements', value: shared.join(', '), tier: 'hit' }
  if (shared.length > 0) return { label: 'Elements', value: shared.join(', '), tier: 'close' }
  return { label: 'Elements', value: 'None', tier: 'miss' }
}

// Prepend each comparison so the latest attempt remains closest to the heading.
function renderGuessRow(guessedCompound) {
  const history = document.querySelector('#guessHistory')
  history.querySelector('.empty-history')?.remove()

  const row = document.createElement('article')
  row.className = 'guess-row'

  const name = document.createElement('div')
  name.className = 'guess-row-name'
  name.textContent = `${guessedCompound.name} (${guessedCompound.formula})`

  const tiles = document.createElement('div')
  tiles.className = 'clue-tiles'

  buildClues(guessedCompound).forEach((clue) => {
    const tile = document.createElement('div')
    tile.className = `clue-tile ${clue.tier}`

    const label = document.createElement('span')
    label.className = 'clue-label'
    label.textContent = clue.label

    const value = document.createElement('span')
    value.className = 'clue-value'
    value.textContent = clue.value

    tile.append(label, value)
    tiles.appendChild(tile)
  })

  row.append(name, tiles)
  history.prepend(row)
}

// Lock the controls and reveal the mystery compound after a win or final miss.
function endRound(won) {
  roundOver = true
  document.querySelector('#guessInput').disabled = true
  document.querySelector('#submitGuessBtn').disabled = true
  document.querySelector('#roundStatus').textContent = won ? 'Solved' : 'Round complete'

  const content = document.querySelector('#roundEndContent')
  content.innerHTML = `
    <h2 class="round-end-title ${won ? 'win' : 'lose'}" id="roundEndTitle">
      ${won ? 'Solved it.' : 'Out of guesses.'}
    </h2>
    <p class="round-end-formula">${secretCompound.name} · ${secretCompound.formula}</p>
    <p class="round-end-description">${secretCompound.description}</p>
  `

  document.querySelector('#roundEndPanel').hidden = false
  document.querySelector('#playAgainBtn').focus()
}

// Wire static controls after the document has loaded at the end of guessr.html.
document.querySelector('#submitGuessBtn').addEventListener('click', submitGuess)
document.querySelector('#guessInput').addEventListener('keydown', (event) => {
  if (event.key === 'Enter') submitGuess()
})
document.querySelector('#playAgainBtn').addEventListener('click', startNewRound)

init()

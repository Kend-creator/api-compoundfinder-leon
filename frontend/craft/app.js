const PROXY_URL = "/api/proxy";

const STORAGE_KEY = 'compound-craft-discovered'

const SAMPLE_COMPOUNDS = [
  {
    id: 'water',
    name: 'Water',
    formula: 'H₂O',
    composition: [
      { symbol: 'H', element: 'Hydrogen', atoms: 2 },
      { symbol: 'O', element: 'Oxygen', atoms: 1 },
    ],
    physicalProperties: {
      state: 'Liquid',
      molarMass: '18.02',
      meltingPointCelsius: 0,
      boilingPointCelsius: 100,
    },
    description:
      'A bent polar molecule and the familiar solvent that supports life on Earth.',
  },
  {
    id: 'carbon-dioxide',
    name: 'Carbon dioxide',
    formula: 'CO₂',
    composition: [
      { symbol: 'C', element: 'Carbon', atoms: 1 },
      { symbol: 'O', element: 'Oxygen', atoms: 2 },
    ],
    physicalProperties: {
      state: 'Gas',
      molarMass: '44.01',
      meltingPointCelsius: -56.6,
      boilingPointCelsius: -78.5,
    },
    description:
      'A linear gas used by plants during photosynthesis and produced by respiration.',
  },
  {
    id: 'ammonia',
    name: 'Ammonia',
    formula: 'NH₃',
    composition: [
      { symbol: 'N', element: 'Nitrogen', atoms: 1 },
      { symbol: 'H', element: 'Hydrogen', atoms: 3 },
    ],
    physicalProperties: {
      state: 'Gas',
      molarMass: '17.03',
      meltingPointCelsius: -77.7,
      boilingPointCelsius: -33.3,
    },
    description:
      'A pungent nitrogen compound widely used in fertilizers and chemical manufacturing.',
  },
  {
    id: 'methane',
    name: 'Methane',
    formula: 'CH₄',
    composition: [
      { symbol: 'C', element: 'Carbon', atoms: 1 },
      { symbol: 'H', element: 'Hydrogen', atoms: 4 },
    ],
    physicalProperties: {
      state: 'Gas',
      molarMass: '16.04',
      meltingPointCelsius: -182.5,
      boilingPointCelsius: -161.5,
    },
    description: 'The simplest hydrocarbon, built around a tetrahedral carbon atom.',
  },
  {
    id: 'sodium-chloride',
    name: 'Sodium chloride',
    formula: 'NaCl',
    composition: [
      { symbol: 'Na', element: 'Sodium', atoms: 1 },
      { symbol: 'Cl', element: 'Chlorine', atoms: 1 },
    ],
    physicalProperties: {
      state: 'Solid',
      molarMass: '58.44',
      meltingPointCelsius: 801,
      boilingPointCelsius: 1465,
    },
    description: 'An ionic compound better known as table salt.',
  },
  {
    id: 'hydrogen-chloride',
    name: 'Hydrogen chloride',
    formula: 'HCl',
    composition: [
      { symbol: 'H', element: 'Hydrogen', atoms: 1 },
      { symbol: 'Cl', element: 'Chlorine', atoms: 1 },
    ],
    physicalProperties: {
      state: 'Gas',
      molarMass: '36.46',
      meltingPointCelsius: -114.2,
      boilingPointCelsius: -85.1,
    },
    description: 'A polar diatomic molecule that forms hydrochloric acid when dissolved in water.',
  },
]

let allCompounds = []
let discoveredIds = new Set()
let bench = {}

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

function loadDiscoveredFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    discoveredIds = raw ? new Set(JSON.parse(raw)) : new Set()
  } catch {
    discoveredIds = new Set()
  }
}

function saveDiscoveredToStorage() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...discoveredIds]))
  } catch {
    // Discoveries remain available for the current page session.
  }
}

/*
BACKEND INTEGRATION — intentionally disabled for this frontend-only delivery.

Replace SAMPLE_COMPOUNDS in init() with the server response when your proxy is ready:

  const PROXY_URL = '/api/proxy'
  const response = await fetch(`${PROXY_URL}?path=/compounds`)
  if (!response.ok) throw new Error('API request failed')
  const data = await response.json()
  allCompounds = data.compounds

Each compound should include:
  id, name, formula, description,
  composition: [{ symbol, element, atoms }],
  physicalProperties: { state, molarMass, meltingPointCelsius, boilingPointCelsius }
*/

function init() {
  loadDiscoveredFromStorage()
  allCompounds = SAMPLE_COMPOUNDS
  buildPeriodicTable(allCompounds)
  renderDiscoveryLog()
  updateProgressTag()
  renderBench()
}

const PERIODIC_ROWS = [
  'H,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,He',
  'Li,Be,.,.,.,.,.,.,.,.,.,.,B,C,N,O,F,Ne',
  'Na,Mg,.,.,.,.,.,.,.,.,.,.,Al,Si,P,S,Cl,Ar',
  'K,Ca,Sc,Ti,V,Cr,Mn,Fe,Co,Ni,Cu,Zn,Ga,Ge,As,Se,Br,Kr',
  'Rb,Sr,Y,Zr,Nb,Mo,Tc,Ru,Rh,Pd,Ag,Cd,In,Sn,Sb,Te,I,Xe',
  'Cs,Ba,La,Hf,Ta,W,Re,Os,Ir,Pt,Au,Hg,Tl,Pb,Bi,Po,At,Rn',
  'Fr,Ra,Ac,Rf,Db,Sg,Bh,Hs,Mt,Ds,Rg,Cn,Nh,Fl,Mc,Lv,Ts,Og',
].map((row) => row.split(','))

const LANTHANIDES = 'La,Ce,Pr,Nd,Pm,Sm,Eu,Gd,Tb,Dy,Ho,Er,Tm,Yb,Lu'.split(',')
const ACTINIDES = 'Ac,Th,Pa,U,Np,Pu,Am,Cm,Bk,Cf,Es,Fm,Md,No,Lr'.split(',')

function buildPeriodicTable(compounds) {
  const container = document.querySelector('#periodicTable')
  const elementNames = new Map()

  compounds.forEach((compound) => {
    compound.composition.forEach((element) => {
      if (!elementNames.has(element.symbol)) {
        elementNames.set(element.symbol, element.element)
      }
    })
  })

  document.querySelector('#activeCount').textContent = String(elementNames.size)
  container.replaceChildren()

  PERIODIC_ROWS.forEach((row) => {
    row.forEach((symbol) => container.appendChild(buildCell(symbol, elementNames)))
  })

  const spacer = document.createElement('div')
  spacer.className = 'pt-spacer-row'
  container.appendChild(spacer)
  appendFBlockRow(container, LANTHANIDES, elementNames)
  appendFBlockRow(container, ACTINIDES, elementNames)
}

function appendFBlockRow(container, symbols, elementNames) {
  container.appendChild(buildCell('.', elementNames))
  container.appendChild(buildCell('.', elementNames))
  symbols.forEach((symbol) => container.appendChild(buildCell(symbol, elementNames)))
}

function buildCell(symbol, elementNames) {
  if (symbol === '.') return document.createElement('div')

  const isActive = elementNames.has(symbol)
  const tile = document.createElement('button')
  tile.type = 'button'
  tile.className = `element-tile${isActive ? '' : ' inactive'}`
  tile.disabled = !isActive
  tile.title = isActive ? elementNames.get(symbol) : `${symbol} is not in the sample library`
  tile.setAttribute(
    'aria-label',
    isActive ? `Add ${elementNames.get(symbol)} (${symbol})` : `${symbol} is unavailable`,
  )

  const symbolLabel = document.createElement('span')
  symbolLabel.className = 'symbol'
  symbolLabel.textContent = symbol
  tile.appendChild(symbolLabel)

  if (isActive) {
    const nameLabel = document.createElement('span')
    nameLabel.className = 'el-name'
    nameLabel.textContent = elementNames.get(symbol)
    tile.appendChild(nameLabel)
    tile.addEventListener('click', () => addToBench(symbol))
  }

  return tile
}

function addToBench(symbol) {
  bench[symbol] = (bench[symbol] || 0) + 1
  renderBench()
  checkForMatch()
}

function removeFromBench(symbol) {
  if (!bench[symbol]) return
  bench[symbol] -= 1
  if (bench[symbol] <= 0) delete bench[symbol]
  renderBench()
  checkForMatch()
}

function clearBench() {
  bench = {}
  renderBench()
  setStatus('', false)
}

function renderBench() {
  const slots = document.querySelector('#benchSlots')
  const symbols = Object.keys(bench).sort()
  document.querySelector('#formulaPreview').textContent = buildFormula(symbols)

  if (symbols.length === 0) {
    slots.innerHTML =
      '<p class="bench-placeholder">Select an active element from the shelf above</p>'
    return
  }

  slots.replaceChildren()
  symbols.forEach((symbol) => {
    const chip = document.createElement('div')
    chip.className = 'bench-chip'

    const label = document.createElement('span')
    label.textContent = `${symbol} × ${bench[symbol]}`

    const removeButton = document.createElement('button')
    removeButton.type = 'button'
    removeButton.textContent = '−'
    removeButton.setAttribute('aria-label', `Remove one ${symbol}`)
    removeButton.addEventListener('click', () => removeFromBench(symbol))

    chip.append(label, removeButton)
    slots.appendChild(chip)
  })
}

function buildFormula(symbols) {
  if (symbols.length === 0) return '—'
  return symbols.map((symbol) => `${symbol}${bench[symbol] > 1 ? bench[symbol] : ''}`).join('')
}

function compositionSignature(composition) {
  const map = {}
  composition.forEach((element) => {
    map[element.symbol] = element.atoms
  })
  return JSON.stringify(Object.keys(map).sort().map((key) => `${key}:${map[key]}`))
}

function benchSignature() {
  return JSON.stringify(Object.keys(bench).sort().map((key) => `${key}:${bench[key]}`))
}

function checkForMatch() {
  if (Object.keys(bench).length === 0) {
    setStatus('', false)
    return
  }

  const match = allCompounds.find(
    (compound) => compositionSignature(compound.composition) === benchSignature(),
  )

  if (match) {
    discover(match)
    return
  }

  setStatus('No exact match yet — keep experimenting.', false)
}

function discover(compound) {
  const isNew = !discoveredIds.has(compound.id)
  if (isNew) {
    discoveredIds.add(compound.id)
    saveDiscoveredToStorage()
    renderDiscoveryLog()
    updateProgressTag()
  }

  setStatus(`Match found — ${compound.name}.`, true)
  showReveal(compound, isNew)
  bench = {}
  renderBench()
}

function setStatus(message, success) {
  const status = document.querySelector('#benchStatus')
  status.textContent = message
  status.classList.toggle('success', success)
}

function renderDiscoveryLog() {
  const log = document.querySelector('#discoveryLog')
  log.replaceChildren()

  allCompounds.forEach((compound) => {
    const unlocked = discoveredIds.has(compound.id)
    const card = document.createElement(unlocked ? 'button' : 'div')
    card.className = `log-card ${unlocked ? 'unlocked' : 'locked'}`

    const formula = document.createElement('div')
    formula.className = 'log-formula'
    formula.textContent = unlocked ? compound.formula : '?????'

    const name = document.createElement('div')
    name.className = 'log-name'
    name.textContent = unlocked ? compound.name : 'Undiscovered'

    card.append(formula, name)
    if (unlocked) {
      card.type = 'button'
      card.setAttribute('aria-label', `View ${compound.name}`)
      card.addEventListener('click', () => showReveal(compound, false))
    }
    log.appendChild(card)
  })
}

function updateProgressTag() {
  document.querySelector('#progressTag').textContent =
    `${discoveredIds.size} / ${allCompounds.length} discovered`
}

function giveHint() {
  const undiscovered = allCompounds.filter((compound) => !discoveredIds.has(compound.id))
  if (undiscovered.length === 0) {
    setStatus('You have discovered every compound in the sample library.', true)
    return
  }

  const target = undiscovered[Math.floor(Math.random() * undiscovered.length)]
  const element = target.composition[Math.floor(Math.random() * target.composition.length)]
  setStatus(
    `Hint: one undiscovered compound contains ${element.element} (${element.symbol}).`,
    false,
  )
}

function showReveal(compound, isNewDiscovery) {
  const properties = compound.physicalProperties
  const content = document.querySelector('#revealContent')
  content.innerHTML = `
    <div class="reveal-card">
      ${isNewDiscovery ? '<p class="reveal-tag">New discovery</p>' : '<p class="reveal-tag">Compound archive</p>'}
      <div class="reveal-formula">${compound.formula}</div>
      <h3 id="revealTitle">${compound.name}</h3>
      <div class="reveal-props">
        <div><span>State</span>${properties.state}</div>
        <div><span>Molar mass</span>${properties.molarMass} g/mol</div>
        <div><span>Melting point</span>${properties.meltingPointCelsius ?? 'N/A'} °C</div>
        <div><span>Boiling point</span>${properties.boilingPointCelsius ?? 'N/A'} °C</div>
      </div>
      <p class="reveal-description">${compound.description}</p>
    </div>
  `

  const overlay = document.querySelector('#revealOverlay')
  overlay.hidden = false
  requestAnimationFrame(() => overlay.classList.add('visible'))
  document.querySelector('#modalCloseButton').focus()
}

function closeReveal() {
  const overlay = document.querySelector('#revealOverlay')
  overlay.classList.remove('visible')
  window.setTimeout(() => {
    overlay.hidden = true
  }, 180)
}

document.querySelector('#clearBtn').addEventListener('click', clearBench)
document.querySelector('#hintBtn').addEventListener('click', giveHint)
document.querySelector('#modalCloseButton').addEventListener('click', closeReveal)
document.querySelector('#revealOverlay').addEventListener('click', (event) => {
  if (event.target.id === 'revealOverlay') closeReveal()
})
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeReveal()
})

init()

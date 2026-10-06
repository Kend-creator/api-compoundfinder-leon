What exactly does the website gets from the API?
- The website only calls CompoundFinder calls the API repeatedly and uses all three public endpoints of the API
> GET /api/v1/compounds when the page loads, show all button is clicked, or searching with an empty search bar
> Get /api/v1/compounds/{id} when looking at the view details on a compound card
> GET /api/v1/compounds/search?q=... when the user searches a compound
- each request sends the api key header through the FETCH_OPTIONS
- API_URL is an empty string so the "fetch(/api/v1/compounds)" is a relative URL, meaning it calls whatever domain the page is hosted on. This is possible because both the API and the website are deployed together. 
- It uses all the fields that it gets from the compounds list

The Whole logic flow:
- Page Loads
- loadCompounds() fetches all the compounds
- displayCompounds() builds a card for each
- the user can either search (which is a new fetch, the cards are rebuilt from results) or clicks the view details of a compound card (fetch for one compound, filling and opening the modal).

Note for vercel.json
- This is a configuration file that makes the website and the API able deploy live together.
- Basically it tells vercel how to build the project and how to route each incoming request.

Routes and Endpoints to note:
> /health which is the health check endpoint
> /docs which is FastAPI's auto-generated Swagger docs page, for checking API functionality without needing to visit the website
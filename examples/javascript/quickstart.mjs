// Wasalt API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs

const HOST = 'wasalt-saudi-data.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Wasalt API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const cities = await get('/cities');
const riyadh = cities.find((c) => c.name === 'Riyadh');
console.log(`${riyadh.name}: ${riyadh.propertyCount} listings`);

// bedrooms is an exact set: '3,4' means 3 or 4 bedrooms.
const results = await get('/search-properties', {
  city_id: riyadh.id,
  property_for: 'sale',
  bedrooms: '3,4',
  rega_verified: 'true',
});
for (const row of results.listings) {
  console.log(`${String(row.price).padStart(10)} SAR  ${row.builtUpAreaSqm} m2  ${row.district}  ${row.id}`);
}

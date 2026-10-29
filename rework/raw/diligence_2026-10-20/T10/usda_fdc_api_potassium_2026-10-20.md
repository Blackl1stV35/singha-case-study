# USDA FoodData Central, potassium (nutrient 306): raw JSON rows for the five records used in T10

Tier P (United States Department of Agriculture, FoodData Central, the data owner's own site). Date read: 20 October 2026.

## How these rows were read
- Second read (this file's rows): the FoodData Central site's data endpoint `https://fdc.nal.usda.gov/portal-data/external/<fdcId>` returned the full JSON for each record (HTTP 200, saved to a scratch folder and parsed with Python). The potassium row (nutrient number 306, nutrient id 1092) and the `foodMeasures` (portion weights) are copied below exactly as the JSON gives them (JSON re-serialised, keys in the order returned). Nothing else is changed, except that for FDC 1105314 the nested `nutrientAnalysisDetails` list (six sub-sample analyses with store, date and lab method) is not repeated and its six amounts are listed in a line under the row.
- First read (earlier on 20 October 2026): the official API `https://api.nal.usda.gov/fdc/v1/food/<fdcId>?api_key=DEMO_KEY&nutrients=306`, read through the fetch tool; the values then recorded were 250.0 (170174), 1.00 (173206), 200.0 (169098), 358.0 (173944) and 326.0 (1105314) mg per 100 g. The second read gives the same five values. The API with the public DEMO_KEY returned HTTP 429 (rate limit 10 requests, Retry-After 13,044 seconds) when it was tried again, so the portal endpoint was used. No account was created and nothing was submitted.
- SR Legacy nutrient values are per 100 g of the edible food (USDA convention; the JSON of the portal endpoint carries the value without a unit basis line).
- The cup and fluid-ounce volumes behind the densities (236.588 mL and 29.5735 mL, US customary) are our assumption about USDA's unit; the nutrition-labelling cup of 240 mL would change a density by about 1.4 percent. For Sprite the record carries two portion weights that agree with each other as fluid ounces (30.8 g per fl oz and 369 g for 12 fl oz give 1.042 and 1.040 g/mL) and a third, "cup 12 fl oz 12 fl oz" 258 g, that does not fit them and is not used.

## Reading notes (ours)
- Coconut water (170174): the potassium value is a single data point (dataPoints 1), last updated 9/1/1984 in the nutrient row. Orange juice (169098): dataPoints 0 as returned (the JSON does not say how the value was obtained), nutrient row last updated 8/1/1982. Both are old values in the SR Legacy release of 2019. They are used as orders of magnitude for comparison, not as a measured survey.
- Sprite (173206): potassium 1 mg per 100 g from 4 data points (min 0, max 2), analytical. One product entry, not a survey of soft drinks.
- Banana (173944, SR Legacy): 358 mg per 100 g from 45 data points (min 308, max 426), analytical. Banana (1105314, Foundation): 326 mg per 100 g from 6 data points (min 300, max 355, median 326); the six sub-sample analyses are 307, 355, 340, 326, 325 and 300 mg.
- The earlier record cited the banana value 358 mg as "FDC 1105314 via Wikipedia". That ID is the Foundation entry and returns 326 mg per 100 g. The 358 mg value belongs to SR Legacy FDC 173944.
- The orange juice figure was earlier held as 496 mg per "250 mL". USDA's basis is 200 mg per 100 g, and 496 mg is per cup of 248 g.

## FDC 170174: Nuts, coconut water (liquid from coconuts)
foodType: SR Legacy; foodClass: FinalFood; ndbNumber: 12119; record lastUpdated: 4/1/2019.
Potassium row (JSON):
```json
{"type": "FoodNutrient", "nutrient": {"id": 1092, "number": "306", "name": "Potassium, K", "rank": 5700.0, "isNutrientLabel": false, "indentLevel": 1, "numberOfDecimals": 0, "shortestName": "Potassium, K", "nutrientUnit": {"name": "mg", "conversionToMicroGram": 1000, "aliases": []}}, "id": 1500673, "lastUpdated": "9/1/1984", "value": 250, "dataPoints": 1}
```
foodMeasures (JSON):
```json
[{"id": 86175, "gramWeight": 206.0, "rank": 3, "value": 1.0, "modifier": "coconut yields", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 86173, "gramWeight": 240.0, "rank": 1, "value": 1.0, "modifier": "cup", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 86174, "gramWeight": 15.0, "rank": 2, "value": 1.0, "modifier": "tbsp", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}]
```

## FDC 173206: Beverages, carbonated, SPRITE, lemon-lime, without caffeine
foodType: SR Legacy; foodClass: FinalFood; ndbNumber: 14145; record lastUpdated: 4/1/2019.
footnote: Includes retail and fast food, without ice products.
Potassium row (JSON):
```json
{"type": "FoodNutrient", "nutrient": {"id": 1092, "number": "306", "name": "Potassium, K", "rank": 5700.0, "isNutrientLabel": false, "indentLevel": 1, "numberOfDecimals": 0, "shortestName": "Potassium, K", "nutrientUnit": {"name": "mg", "conversionToMicroGram": 1000, "aliases": []}}, "foodNutrientDerivation": {"id": 1, "code": "A", "description": "Analytical", "foodNutrientSource": {"id": 1, "code": "1", "description": "Analytical or derived from analytical"}}, "id": 1758798, "lastUpdated": "4/1/2005", "value": 1, "dataPoints": 4, "max": 2, "min": 0}
```
foodMeasures (JSON):
```json
[{"id": 92105, "gramWeight": 258.0, "rank": 4, "value": 1.0, "modifier": "cup 12 fl oz 12 fl oz", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 92102, "gramWeight": 30.8, "rank": 1, "value": 1.0, "modifier": "fl oz", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 92104, "gramWeight": 492.0, "rank": 3, "value": 1.0, "modifier": "serving 16 fl oz", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 92103, "gramWeight": 369.0, "rank": 2, "value": 1.0, "modifier": "serving 12 fl oz", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}]
```

## FDC 169098: Orange juice, raw (Includes foods for USDA's Food Distribution Program)
foodType: SR Legacy; foodClass: FinalFood; ndbNumber: 9206; record lastUpdated: 4/1/2019.
Potassium row (JSON):
```json
{"type": "FoodNutrient", "nutrient": {"id": 1092, "number": "306", "name": "Potassium, K", "rank": 5700.0, "isNutrientLabel": false, "indentLevel": 1, "numberOfDecimals": 0, "shortestName": "Potassium, K", "nutrientUnit": {"name": "mg", "conversionToMicroGram": 1000, "aliases": []}}, "id": 1413134, "lastUpdated": "8/1/1982", "value": 200, "dataPoints": 0}
```
foodMeasures (JSON):
```json
[{"id": 84232, "gramWeight": 31.0, "rank": 2, "value": 1.0, "modifier": "fl oz", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 84233, "gramWeight": 86.0, "rank": 3, "value": 1.0, "modifier": "fruit yields", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 84231, "gramWeight": 248.0, "rank": 1, "value": 1.0, "modifier": "cup", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}]
```

## FDC 173944: Bananas, raw
foodType: SR Legacy; foodClass: FinalFood; ndbNumber: 9040; record lastUpdated: 4/1/2019.
Potassium row (JSON):
```json
{"type": "FoodNutrient", "nutrient": {"id": 1092, "number": "306", "name": "Potassium, K", "rank": 5700.0, "isNutrientLabel": false, "indentLevel": 1, "numberOfDecimals": 0, "shortestName": "Potassium, K", "nutrientUnit": {"name": "mg", "conversionToMicroGram": 1000, "aliases": []}}, "foodNutrientDerivation": {"id": 1, "code": "A", "description": "Analytical", "foodNutrientSource": {"id": 1, "code": "1", "description": "Analytical or derived from analytical"}}, "id": 1817950, "lastUpdated": "12/1/2002", "value": 358, "dataPoints": 45, "max": 426, "min": 308}
```
foodMeasures (JSON):
```json
[{"id": 93518, "gramWeight": 126.0, "rank": 8, "value": 1.0, "modifier": "NLEA serving", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 93517, "gramWeight": 152.0, "rank": 7, "value": 1.0, "modifier": "extra large (9\" or longer)", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 93516, "gramWeight": 136.0, "rank": 6, "value": 1.0, "modifier": "large (8\" to 8-7/8\" long)", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 93512, "gramWeight": 150.0, "rank": 2, "value": 1.0, "modifier": "cup, sliced", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 93514, "gramWeight": 101.0, "rank": 4, "value": 1.0, "modifier": "small (6\" to 6-7/8\" long)", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 93513, "gramWeight": 81.0, "rank": 3, "value": 1.0, "modifier": "extra small (less than 6\" long)", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 93515, "gramWeight": 118.0, "rank": 5, "value": 1.0, "modifier": "medium (7\" to 7-7/8\" long)", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}, {"id": 93511, "gramWeight": 225.0, "rank": 1, "value": 1.0, "modifier": "cup, mashed", "measureUnit": {"id": 9999, "name": "undetermined", "abbreviation": "undetermined"}}]
```

## FDC 1105314: Bananas, ripe and slightly ripe, raw
foodType: Foundation; foodClass: FinalFood; ndbNumber: 9040; record lastUpdated: 4/1/2020.
Potassium row (JSON):
```json
{"type": "FoodNutrient", "nutrient": {"id": 1092, "number": "306", "name": "Potassium, K", "rank": 5700.0, "isNutrientLabel": false, "indentLevel": 1, "numberOfDecimals": 0, "shortestName": "Potassium, K", "nutrientUnit": {"name": "mg", "conversionToMicroGram": 1000, "aliases": []}}, "foodNutrientDerivation": {"id": 1, "code": "A", "description": "Analytical", "foodNutrientSource": {"id": 1, "code": "1", "description": "Analytical or derived from analytical"}}, "id": 13337403, "lastUpdated": "3/27/2020", "value": 326, "dataPoints": 6, "max": 355, "min": 300, "median": 326, "minDateAcquired": "12/2/2019", "minYearAcquired": 2019}
```
Sub-sample amounts (mg per 100 g) from nutrientAnalysisDetails: [307, 355, 340, 326, 325, 300]; lab method as returned: AOAC 985.01 + 984.27.
foodMeasures (JSON):
```json
[{"id": 267795, "dataPoints": 102, "gramWeight": 115.0, "rank": 1, "value": 1.0, "modifier": "Peeled", "minDateAcquired": "12/2/2019", "measureUnit": {"id": 1119, "name": "Banana", "abbreviation": "Banana"}, "minYearAcquired": 2019}, {"id": 312674, "dataPoints": 0, "gramWeight": 140.0, "rank": 1, "value": 1.0, "measureUnit": {"id": 1121, "name": "RACC", "abbreviation": "RACC"}}]
```

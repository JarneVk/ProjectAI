# Labo-opdracht AI

## Stappenplan:

1. map inlezen
2. wagens verdelen over zones

## Input file:

csv bestand
| element | uitleg |
| ------- | ------ |
| reservatieID | unieke ID van reservatie |
| zoneID | ID van zone van reservatie |
| dag | index van dag van start reservatie |
| start tijd | minuten sinds middernacht | 
| duurtijd | totale duur [min] |
| mogelijke voertuig IDs | lijst met voertuigen feasable voor deze reservatie |
| penalty 1 | kost om reservatie niet toe te wijzen |
| penalty 2 | kost om reservatie in aanliggende zone toe te wijzen |


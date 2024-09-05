# life
Attempt to study interaction of various organisms based on data from the GLOBI dataset

We will use the data provided by Global Biotics Interactions (GLOBI).

The main data that we are interested in is the interactions data, which can be downloaded here:
https://www.globalbioticinteractions.org/data


Initially, I would like to focus on the iNaturalist data only.

>>>>

1) 

Specifically, in the file, interactions.csv, we only want those records where the sourceInstitutionCode = iNaturalist

There are currently just over 800K such interaction records in this dataset.

D select count(*) from interactions.csv where sourceInstitutionCode='iNaturalist';
100% ?████████████████████████████████████████████████████████████?
count_star() = 803983
D


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

2) 

Here are the different types of organism interactions that are included in this data set.


D select distinct(interactionTypeName) from interactions.csv where sourceInstitutionCode='iNaturalist';
100% ?████████████████████████████████████████████████████████████?
 74% ?████████████████████████████████████████████?               ? interactionTypeName = interactsWith

interactionTypeName = preysOn

interactionTypeName = kills

interactionTypeName = visitsFlowersOf

interactionTypeName = parasiteOf

interactionTypeName = pollinates

interactionTypeName = hasHost

interactionTypeName = hemiparasiteOf

interactionTypeName = visits

interactionTypeName = hasVector

interactionTypeName = eats

interactionTypeName = parasitoidOf

interactionTypeName = pathogenOf

interactionTypeName = laysEggsOn

interactionTypeName = symbiontOf

interactionTypeName = adjacentTo

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

3) The most relevant fields to query for now are:

interactionTypeName  E.g., hasHost
interactionTypeId E.g., http://purl.obolibrary.org/obo/RO_0002454
sourceTaxonName E.g., Rhopalomyia pomum
targetTaxonName E.g., Artemisia tridentata
sourceInstitutionCode = iNaturalist
sourceId -> This is the iNaturalist observation URL, e.g., https://www.inaturalist.org/observations/59157287

4)  Example.  Let's find out the different species of flowers that the Common Eastern Bumble Bee has visited:

Searching inaturalist.org for Common Eastern Bumble Bee leads us to the main taxon page:  https://www.inaturalist.org/taxa/118970-Bombus-impatiens
iNaturalist has about 184,000 thousand observations of the Common Eastern Bumble Bee (Bombus impatiens).

iNaturalist does not require the observers to enter any of the observation fields, such as the "Visits Flowers Of", so unfortunately, many of the
observations will not include this field.

GLOBI has about 19000 observations of interactions involving Bombus impatiens:

select count(*) from interactions.csv where sourceInstitutionCode='iNaturalist' and sourceTaxonName='Bombus impatiens';
100% ?████████████████████████████████████████████████████████████?
count_star() = 18903

Let's search for interactionTypeName="visitsFlowersOf".

D select sourceTaxonName, targetTaxonName, sourceId, interactionTypeId from interactions.csv where sourceInstitutionCode='iNaturalist' and sourceTaxonName='Bombus impatiens' and interactionTypeName='visitsFlowersOf' limit 10;
100% ?████████████████████████████████████████████████████████████?
┌──────────────────┬─────────────────────────┬───────────────────────────────────────────────────┬───────────────────────────────────────────┐
│ sourceTaxonName  │     targetTaxonName     │                     sourceId                      │             interactionTypeId             │
│     varchar      │         varchar         │                      varchar                      │                  varchar                  │
├──────────────────┼─────────────────────────┼───────────────────────────────────────────────────┼───────────────────────────────────────────┤
│ Bombus impatiens │ Gomphrena globosa       │ https://www.inaturalist.org/observations/59045989 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Pycnanthemum muticum    │ https://www.inaturalist.org/observations/59096035 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Pycnanthemum muticum    │ https://www.inaturalist.org/observations/59096035 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Hypochaeridinae         │ https://www.inaturalist.org/observations/59080912 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Hypochaeridinae         │ https://www.inaturalist.org/observations/59083320 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Agastache foeniculum    │ https://www.inaturalist.org/observations/59146423 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Conoclinium coelestinum │ https://www.inaturalist.org/observations/59146433 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Conoclinium coelestinum │ https://www.inaturalist.org/observations/59146428 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Agastache foeniculum    │ https://www.inaturalist.org/observations/59146452 │ http://purl.obolibrary.org/obo/RO_0002622 │
│ Bombus impatiens │ Helianthus              │ https://www.inaturalist.org/observations/59050864 │ http://purl.obolibrary.org/obo/RO_0002622 │
├──────────────────┴─────────────────────────┴───────────────────────────────────────────────────┴───────────────────────────────────────────┤
│ 10 rows                                                                                                                          4 columns │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D


5) Initially, I would like to construct weighted, directed graphs representing relationships, where the nodes would represent taxa and the edges would represent some sort of an interaction.
The "weight" of the edge could be the type of interaction, along with the recorded frequency of such interactions.  There could be multiple edges between two nodes, as there can be different types of interactions between two given taxons.

Once such graphs are constructed, it would be fun to find known multi-organism relationships.  For example, the fungus, Cerrena unicolor, has a very interesting relationship with two different types of wasps, as described here:
https://www.mushroomexpert.com/cerrena_unicolor.html

I am interested in studying such relationships.   



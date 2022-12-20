# Views

## Website Data

Dit is veruit de belangrijkste view. Aangezien de view snel beschikbaar moet zijn, houden we de berekende velden opgeslagen bij. Met behulp van een trigger, wat later in deze Markdown aan bod komt, updaten wij de velden.

```sql
CREATE UNIQUE INDEX idx_web_data
ON view_website_data 
using btree (naam) 

CREATE UNIQUE INDEX idx_web_data
ON view_website_data 
using btree (ondernemingsnummer) 
```

Om het type verstedelijking mee te geven, wordt er gewerkt met een extra functie.

```sql
CREATE OR REPLACE FUNCTION get_type_bebouwing(urban numeric)
RETURNS varchar(25) AS $$
BEGIN
  RETURN (
    SELECT CASE
      WHEN urban < 0.8 THEN 'Landelijk'
      WHEN urban < 1.3  THEN 'Randstedelijk'
      ELSE 'Stedelijk'
    END
  );
END;
$$ LANGUAGE plpgsql;
```

```sql
SELECT 
    k.ondernemingsnummer, k.naam, k.website,
    k.vennootschap, k.soortbusiness, s.sectornaam,
    ( SELECT sum(ts_stat.nentry) AS sum
           FROM ts_stat(format('select ts_document from "KMO" where ondernemingsnummer = %s'::text, k.ondernemingsnummer)) ts_stat(word, ndoc, nentry)) AS totaal_aantal_woorden_web,
    ( SELECT sum(ts_stat.nentry) AS sum
           FROM ts_stat(format('select ts_document from "Balans" where ondernemingsnummer = %s'::text, k.ondernemingsnummer)) ts_stat(word, ndoc, nentry)) AS totaal_aantal_woorden_pdf,
    ( SELECT array_agg(ARRAY[ts_stat.word::character varying(255), ts_stat.nentry::character varying(255)]) AS array_agg
           FROM ts_stat(format('select ts_document from "KMO" where ondernemingsnummer = %s'::text, k.ondernemingsnummer)) ts_stat(word, ndoc, nentry)
          WHERE (ts_stat.word IN ( SELECT z.zoekterm_description
                   FROM zoektermen z))) AS occ_web,
    ( SELECT array_agg(ARRAY[ts_stat.word::character varying(255), ts_stat.nentry::character varying(255)]) AS array_agg
           FROM ts_stat(format('select ts_document from "Balans" where ondernemingsnummer = %s'::text, k.ondernemingsnummer)) ts_stat(word, ndoc, nentry)
          WHERE (ts_stat.word IN ( SELECT z.zoekterm_description
                   FROM zoektermen z))) AS occ_pdf,
    (vpc.domein_environment + vpc.domein_social + vpc.domein_governance) / 3::double precision AS total_score,
    k.personeelsbestanden, k.beursgenoteerd, k.foundingdate,
    vpc.subdomeinen_environment, vpc.subdomeinen_social, vpc.subdomeinen_governance,
    vpc.domein_environment, vpc.domein_social, vpc.domein_governance,
    ssc.simple_env_scores, ssc.simple_soc_scores, ssc.simple_gov_scores,
    l.postcode, l.gemeente, l.adres,
    get_type_bebouwing(l.urban) AS get_type_bebouwing,
    l.hoofdzetel, ssc.distribution_environment, ssc.distribution_social, ssc.distribution_governance
FROM "KMO" k
     JOIN view_percentages vpc ON vpc.ondernemingsnummer = k.ondernemingsnummer
     JOIN view_simple_scores_companies ssc ON ssc.ondernemingsnummer = k.ondernemingsnummer
     JOIN "Balans" b ON b.ondernemingsnummer = k.ondernemingsnummer
     JOIN "Sector" s ON s.sectornummer = k.sectorid
     JOIN "Locatie" l ON l.ondernemingsnummer = k.ondernemingsnummer
ORDER BY ((vpc.domein_environment + vpc.domein_social + vpc.domein_governance) / 3::double precision) DESC;
```

## Percentages per KMO

Voor iedere KMO worden er zes kolommen bijgehouden. De eerste drie kolommen houden het percentage per subdomein bij. Dit percentage toont aan hoe goed een KMO scoort ten opzichte van andere bedrijven. De laatste drie kolommen zijn de totaalscore per domein.

```sql
SELECT k.ondernemingsnummer,
    ARRAY[
        percent_rank() OVER (ORDER BY (k.environment[0] + b.environment[0])), 
        percent_rank() OVER (ORDER BY (k.environment[1] + b.environment[1])), 
        percent_rank() OVER (ORDER BY (k.environment[2] + b.environment[2])), 
        percent_rank() OVER (ORDER BY (k.environment[3] + b.environment[3])), 
        percent_rank() OVER (ORDER BY (k.environment[4] + b.environment[4]))
        ] AS subdomeinen_environment,
    ARRAY[
        percent_rank() OVER (ORDER BY (k.social[0] + b.social[0])), 
        percent_rank() OVER (ORDER BY (k.social[1] + b.social[1])), 
        percent_rank() OVER (ORDER BY (k.social[2] + b.social[2])), 
        percent_rank() OVER (ORDER BY (k.social[3] + b.social[3]))
        ] AS subdomeinen_social,
    ARRAY[
        percent_rank() OVER (ORDER BY (k.governance[0] + b.governance[0])), 
        percent_rank() OVER (ORDER BY (k.governance[1] + b.governance[1]))
        ] AS subdomeinen_governance,
    percent_rank() OVER (ORDER BY ((
        ( SELECT sum(s.s) AS sum FROM unnest(b.environment) s(s))) + (( SELECT sum(s.s) AS sum FROM unnest(k.environment) s(s))
        ))) AS domein_environment,
    percent_rank() OVER (ORDER BY ((
        ( SELECT sum(s.s) AS sum FROM unnest(b.social) s(s))) + (( SELECT sum(s.s) AS sum FROM unnest(k.social) s(s))
        ))) AS domein_social,
    percent_rank() OVER (ORDER BY ((
        ( SELECT sum(s.s) AS sum FROM unnest(b.governance) s(s))) + (( SELECT sum(s.s) AS sum FROM unnest(k.governance) s(s))
        ))) AS domein_governance
FROM "KMO" k
JOIN "Balans" b ON k.ondernemingsnummer = b.ondernemingsnummer;
```

## Vereenvoudigde scores

Om de volgende view te verstaan, moet je de code achter de volgende twee functies. 

Met behulp van de functie ``transform_score_array`` geven we een nieuwe array mee. Als een percentage boven 20% is, dan houden we een één-score bij. In het geval het percentage kleiner is dan die *threshold*, dan wordt er een nulscore bijgehouden. 

```sql
DECLARE
    transformed_values integer[];
BEGIN
    SELECT ARRAY(
        SELECT CASE WHEN x >= 0.2 THEN 1 ELSE 0 END
        FROM unnest(input_array) as x
    ) INTO transformed_values;
    RETURN transformed_values;
END;
```

Met de ``count-scores`` functie tellen we het aantal percentages dat groter dan of gelijk is aan 20%.

```sql
BEGIN
  RETURN (SELECT COUNT(*) FROM unnest(arr) WHERE unnest >= 0.2);
END;
```

```sql
SELECT vpc.ondernemingsnummer,
    transform_score_array(vpc.subdomeinen_environment) AS distribution_environment,
    transform_score_array(vpc.subdomeinen_social) AS distribution_social,
    transform_score_array(vpc.subdomeinen_governance) AS distribution_governance,
    count_scores(vpc.subdomeinen_environment) AS simple_env_scores,
    count_scores(vpc.subdomeinen_social) AS simple_soc_scores,
    count_scores(vpc.subdomeinen_governance) AS simple_gov_scores
FROM view_percentages vpc;
```

## Sector Overview

De view houdt voornamelijk de sectorminima, -gemiddelden en -maxima bij. Dit is nodig als maatstaf bij de KMO-overzichtspagina's.

```sql
 SELECT s.sectornaam,
    ARRAY[min(b.balanstotaal), avg(b.balanstotaal), max(b.balanstotaal)] AS sector_balanstotaal,
    ARRAY[min(b.omzet), avg(b.omzet), max(b.omzet)] AS sector_omzet,
    ARRAY[min(k.personeelsbestanden)::numeric, avg(k.personeelsbestanden), max(k.personeelsbestanden)::numeric] AS sector_pb,
    ARRAY[( SELECT count(*) AS count
           FROM "KMO" k2
             JOIN "Locatie" l ON k2.ondernemingsnummer = l.ondernemingsnummer
          WHERE l.urban < 0.8
          GROUP BY k2.sectorid
         HAVING k2.sectorid = s.sectornummer), ( SELECT count(*) AS count
           FROM "KMO" k2
             JOIN "Locatie" l ON k2.ondernemingsnummer = l.ondernemingsnummer
          WHERE l.urban >= 0.8 AND l.urban <= 1.3
          GROUP BY k2.sectorid
         HAVING k2.sectorid = s.sectornummer), ( SELECT count(*) AS count
           FROM "KMO" k2
             JOIN "Locatie" l ON k2.ondernemingsnummer = l.ondernemingsnummer
          WHERE l.urban > 1.3
          GROUP BY k2.sectorid
         HAVING k2.sectorid = s.sectornummer)] AS sector_urban,
    ARRAY[min(pc.domein_environment), avg(pc.domein_environment), max(pc.domein_environment)] AS per_env,
    ARRAY[min(pc.domein_social), avg(pc.domein_social), max(pc.domein_social)] AS per_soc,
    ARRAY[min(pc.domein_governance), avg(pc.domein_governance), max(pc.domein_governance)] AS per_gov
   FROM view_percentages pc
     JOIN "KMO" k ON k.ondernemingsnummer = pc.ondernemingsnummer
     JOIN "Balans" b ON k.ondernemingsnummer = b.ondernemingsnummer
     JOIN "Sector" s ON k.sectorid = s.sectornummer
  GROUP BY s.sectornummer, s.sectornaam;
```


## Totale overview

Naast de statistieken per sector willen we ook de statistieken over de gehele dataset.

## Machine Learning Data

```sql
 SELECT 
    k.ondernemingsnummer,
    l.urban,
    b.balanstotaal,
    b.omzet,
    k.personeelsbestanden,
    k.foundingdate,
    v.domein_environment AS environment,
    v.domein_social AS social,
    v.domein_governance AS governance,
    (v.domein_environment + v.domein_social + v.domein_governance) / 3::double precision AS "general"
    FROM "KMO" k
    JOIN "Balans" b ON b.ondernemingsnummer = k.ondernemingsnummer
    JOIN "Locatie" l ON l.ondernemingsnummer = k.ondernemingsnummer
    JOIN view_percentages v ON k.ondernemingsnummer = v.ondernemingsnummer;
```

We hebben maximale waarden nodig voor het ANN-model. Om de maximale waarden op te halen, gebruiken we een tweede view. Aangezien de view niet snel zal veranderen, houden we hiervan een *materialized view* bij.

```sql
SELECT 
    max(view_machine_learning_data.urban) AS urb,
    max(view_machine_learning_data.balanstotaal) AS bt,
    max(view_machine_learning_data.omzet) AS omzet,
    max(view_machine_learning_data.personeelsbestanden) AS pb,
    EXTRACT(year FROM CURRENT_TIMESTAMP) - EXTRACT(year FROM min(view_machine_learning_data.foundingdate)) AS jaren
FROM view_machine_learning_data;
```

## Zoektermen toevoegen

Bij het toevoegen van een zoekterm moet de gebruiker meegeven in welke categorie. Hiervoor werken we met een keuzebalk waar de categorie wordt gekoppeld aan de juiste naam van een subdomein. Om al deze informatie mogelijk te maken, werken wij met een aparte *materialized view*. Dit omdat de klant nooit gespecifieerd heeft dat er subdomeinen bijkomen. Als dit wel het geval is, dan moet er een extra trigger bijkomen.

```sql
SELECT cz.domein,
    ( SELECT array_agg(cz2.categorie_naam) AS array_agg
           FROM categorie_zoektermen cz2
          WHERE cz2.domein::text = cz.domein::text) AS array_agg
   FROM categorie_zoektermen cz
  GROUP BY cz.domein;
```

Er wordt een overzicht getoond van alle zoektermen.

```sql
 SELECT
    cz.domein,
    zoektermen.categorie_id,
    zoektermen.categorie_naam,
    zoektermen.zoektermen
    FROM ( SELECT z2.categorie_id,
            cz_1.categorie_naam,
            ARRAY( SELECT z.zoekterm_description AS z
                   FROM zoektermen z
                  WHERE z.categorie_id = z2.categorie_id) AS zoektermen
        FROM zoektermen z2
        JOIN categorie_zoektermen cz_1 ON cz_1.categorie_id = z2.categorie_id
    GROUP BY z2.categorie_id, cz_1.categorie_naam
    ORDER BY z2.categorie_id) zoektermen
JOIN categorie_zoektermen cz ON cz.categorie_id = zoektermen.categorie_id;
```

# Triggers

We gebruiken triggers om vooral de *materialized views* te updaten.

Allereerst hebben we de scoreberekening. De scores worden opnieuw berekend wanneer de 

```sql
CREATE or REPLACE TRIGGER refresh_scores AFTER INSERT OR UPDATE OR DELETE OR TRUNCATE
	ON zoektermen
	FOR EACH STATEMENT
EXECUTE PROCEDURE recalculate_scores();

CREATE OR REPLACE FUNCTION recalculate_scores()
  RETURNS TRIGGER LANGUAGE plpgsql
  AS $$
  BEGIN
  	UPDATE "Balans" b SET 
		environment[0] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 1)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		environment[1] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 2)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		environment[2] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 3)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		environment[3] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 4)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		environment[4] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 5)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		social[0] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 6)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		social[1] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 7)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		social[2] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 8)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		social[3] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 9)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		governance[0] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 10)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer),
		governance[1] = (select ts_rank_cd(ts_document, query, 32) as rank from "Balans" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 11)) query where query @@ ts_document and b2.ondernemingsnummer = b.ondernemingsnummer);
	
	UPDATE "KMO" k SET 
		environment[0] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 1)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		environment[1] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 2)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		environment[2] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 3)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		environment[3] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 4)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		environment[4] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 5)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		social[0] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 6)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		social[1] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 7)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		social[2] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 8)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		social[3] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 9)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		governance[0] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 10)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0),
		governance[1] = coalesce((select ts_rank_cd(ts_document, query, 32) as rank from "KMO" b2, to_tsquery('dutch', (select string_agg(replace(zoekterm_description, ' ', ' <-> '), ' | ') from zoektermen where categorie_id = 11)) query where query @@ ts_document and b2.ondernemingsnummer = k.ondernemingsnummer),0);	
	
  RETURN NULL;
END $$;
```

De ``materialized view`` moet 'manueel' aangepast worden. Dit aan de hand van een *refresh materialized view* commando.
Enkel wanneer de volgende twee kolommen

```sql
CREATE TRIGGER refresh_post_update_kmo
  AFTER UPDATE OF environment, social, governance ON "KMO"
  FOR EACH STATEMENT
EXECUTE PROCEDURE refresh_views();

CREATE TRIGGER refresh_post_update_balans
  AFTER UPDATE OF environment, social, governance ON "KMO"
  ON "Balans"
  FOR EACH STATEMENT
EXECUTE PROCEDURE refresh_views();

CREATE OR REPLACE FUNCTION refresh_views()
  RETURNS TRIGGER LANGUAGE plpgsql
  AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY view_website_data;
  RETURN NULL;
END 
```
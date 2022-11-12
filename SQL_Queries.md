# 1. Ranking

```sql
select ts_rank(ts_document, query) as rank 
	from "KMO", to_tsquery('dutch','(klimaat | klimaatverandering | opwarming | scope1 | scope2 | scope3 | klimaatimpact | impact | co2 | broeikasgas | methaan | stikstof | klimaatbeleid | green | deal | klimaatactie )') query 
	where query @@ ts_document order by rank desc limit 100;

CREATE INDEX document_web_idx on "Balans" using gin(ts_document);

select naam from "KMO"
where ts_document @@ to_tsquery('dutch', 'shop') limit 5
```

# 2. Zoektermen (categorie)

```sql
insert into categorie_zoektermen (categorie_naam) values ('business conduct')

select * from categorie_zoektermen

update categorie_zoektermen
set domein = 'Governance'
where categorie_id >= 10

alter table categorie_zoektermen
alter column domein varchar(10)
```
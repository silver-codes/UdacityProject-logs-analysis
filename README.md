# NewsDB Reportýng Tool

_**NDBRT**_ ýs a reporting tool that prints out reports (in plain text) based on the data in the _**news**_ database. 
This reporting tool is a Python program using the psycopg2 module to connect to the database.

## Installation

make sure `psycopg2` is installed before runing the program
`$ pip3 install psycopg2`


## Usage

in order for this tool to run correctly, a few **views** must be cretaed in the database first.
use the following lines to setup these **views** after connecting to the database in **postgresql** 
`$psql`
`$\c news`
pathHits:

`create view pathHits as select path, count(*) as hits from log where status='200 OK' and path !='/' group by path order by hits desc;`
ArticleViews:
`create view ArticleViews as select a.title, p.hits from articles as a join pathHits as p on p.path like ('%' || a.slug);`
ArticleAuthor:
`create view ArticleAuthor as select a.title,u.name as Author from articles as a join authors as u on a.author=u.id;`
topAuthors:
`create view topAuthors as select author, sum(hits) as views from ArticleAuthorViews group by author order by views desc;`
requests:
`create view requests as select date_trunc('day', time)::timestamp::date date, count(*) as requests from log group by 1 order by 1;`
errors:
`create view errors as select date_trunc('day', time)::timestamp::date date, count(*) as errors from log where status like (4 || '%') group by 1 order by 1;`
errorPercentage:
`create view errorPercentage as select r.date, e.errors::decimal/r.requests::decimal*100 percentage from requests r join errors e on r.date=e.date;`

## License
MIT

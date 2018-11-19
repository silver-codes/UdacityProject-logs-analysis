#!/usr/bin/env python3
# 
# Udacity-FSND-ProjectI: building a reporting tool
# anlaysing the data from the news database
#created by: ahmed.e.haddad2.0@gmail.com


import psycopg2


print("Beginning of report: \n")
dbname="news"

###################The first problem: What are the most popular three articles of all time?
# based on site access data sorted in a descending list

def top3_articles():
	"""print out the top 3 visited articles in the news database."""
	db = psycopg2.connect(database=dbname) 
	c = db.cursor()
	"""get the top articles"""
	#c.execute(" create view pathHits as select path, count(*) as hits from log where status='200 OK' and path !='/' group by path order by hits desc;") #create pathHits VIEW
	#c.execute(" create view ArticleViews as select a.title, p.hits from articles as a join pathHits as p on p.path like ('%' || a.slug);") #create ArticleViews VIEW
	c.execute("select * from ArticleViews limit 3;")
	
	articles = c.fetchall()
	""" print the articles"""
	
	i = 0
	for article in articles:
		print(re.sub(+articles[i][0])+"..............    "+str(articles[i][1])+" hits")
		i += 1

	db.close()
	return
print("\nTop three visited articles are:\n")	
top3_articles() #calling the function

###################The Second problem: Who are the most popular article authors of all time? 
#

def top3_authors():
	'''print out the top 3 authors whom articles have grossed the most views in the news database.'''
	db = psycopg2.connect(database=dbname)
	c = db.cursor()
	'''query the top 3 authors'''
	#c.execute("create view ArticleAuthor as select a.title,u.name as Author from articles as a join authors as u on a.author=u.id;") #create ArticleAuthor VIEW
	#c.execute("create view topAuthors as select author, sum(hits) as views from ArticleAuthorViews group by author order by views desc;") #create topAuthors VIEW
	c.execute("select author, sum(hits) as TotalViews from (select aa.author, aa.title, av.hits from ArticleAuthor aa join ArticleViews av on aa.title=av.title) as maxes group by author order by TotalViews desc limit 3;") #sum articles hits 
	
	authors = c.fetchall()
	''' print top authors '''
	i = 0
	for author in authors:
		print(authors[i][0]+"     ...with...    "+str(authors[i][1])+" Total Views")
		i += 1
	
	db.close()
	return
print("\n\nThe top three authors are: \n")
top3_authors() #calling the function


###################The Third problem: On which days did more than 1% of requests lead to errors?
# calculate error status/total requests aggregated by date (4xx & 5xx codes)

def error_percentage():
	"""print out the days which had more than 1% error in requests."""
	
	db = psycopg2.connect(database=dbname) 
	c = db.cursor()
	"""get no of errory requests"""
	#c.execute("create view requests as select date_trunc('day', time)::timestamp::date date, count(*) as requests from log group by 1 order by 1;") #create requests VIEW
	#c.execute("create view errors as select date_trunc('day', time)::timestamp::date date, count(*) as errors from log where status like (4 || '%') group by 1 order by 1;") #create error VIEW 
	#c.execute("create view errorPercentage as select r.date, e.errors::decimal/r.requests::decimal*100 percentage from requests r join errors e on r.date=e.date;") #create errorPercentage VIEW
	
	c.execute("select * from errorPercentage where percentage>1;")
	
	days = c.fetchall()
	"""print the results"""
	i=0
	for dy in days:
		print(str(days[i][0])+", errors in requests:"+str(round(days[i][1]))+"%")
		i += 1
	#print(
	db.close()
	return
print("\n\nDays on which the requests had more 1% errors are :\n")	
error_percentage() #calling the function
 
#End
print("\n \n---End of Output---")
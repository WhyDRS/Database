# The WhyDRS Database

## A Public Database for Companies, Brokers, and Transfer Agents

Although information regarding the Direct Registration System and individual publicly traded stock is all available, it is scattered and can be hard to search.

This information has been gathered in one place to make it easy for any investor to get direct access to static information about their investments. [This Lemmy post](https://lemmy.whynotdrs.org/post/21495) goes into detail about the Database structure, goals, and development in addition to information on contributing.

You can view the raw data, volunteer missing information to be added to the database, or search for the entity you are interested in below. All data available is free for use and access.

[Click Here to Review the Database](https://whydrsdatabase.on.fleek.co/)

### Not your name, not your shares!

## How does the Database organized?

Initially, the Database operated by scraping all tickers from major exchanges like NYSE and NASDAQ. Soon after, the population method transitioned to using a key public resource at the SEC (perhaps insert link to CSV here) which includes company name, exchange, and crucially the CIK. A CIK is a unique numerical identifier which refers to one publicly trading stock, and is retired should that company stop trading.

Every 24 hours, this resource is polled and any newly appearing CIK are added as lines to the database. If companies leave public trading for some reason, they will remain on the database. 

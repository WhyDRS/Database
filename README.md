# The WhyDRS Database

### Not your name, not your shares!

## A Comprehensive Public Database for Companies, Brokers, and Transfer Agents

Managing and accessing information about the Direct Registration System and individual publicly traded stocks can be challenging due to scattered and unorganized data sources. This information has been gathered in one place to make it easy for any investor to get direct access to static information about their investments. [This Lemmy post](https://lemmy.whynotdrs.org/post/21495) goes into detail about the Database structure, goals, and development in addition to information on contributing.

You can:
- [View the raw data](https://database.whydrs.org/)
- Volunteer to add missing information
- Search for specific entities of interest

All data is freely available for use and access.

## How Is the Database Organized?

Initially, the database **used manually collected data** for all tickers from major exchanges like the NYSE and NASDAQ. We have since **automated this process**, utilizing the SEC's [**Company Tickers and Exchange Data**](https://www.sec.gov/files/company_tickers_exchange.json), which includes the ticker, company name, exchange, and, crucially, the **CIK**.

**CIK** stands for **Central Index Key** and is a unique number assigned to each publicly trading company. If a company stops trading, its CIK is retired.

Every 24 hours, this resource is **scraped automatically**, and new items are added to the database. If companies leave public trading for any reason, their information remains in the database to maintain historical records, ensuring that data remains accessible for analysis and reference.

## Features

- **Comprehensive Data:** Includes information on companies, brokers (pending), and transfer agents (pending).
- **Automated Updates:** Data is refreshed every 24 hours to ensure accuracy.
- **Free Access:** All data is freely available for use and access.
- **User Contributions:** Volunteers can add missing information to enhance the database.
- **Search Functionality:** Easily search for specific entities of interest.

## How to Use

- **View Raw Data:** Access the complete dataset [here](https://database.whydrs.org/).
- **Search for Entities:** Use the search functionality on the website to find specific companies, brokers (pending), or transfer agents (pending).
- **Contribute Data:** Volunteer to add or update information by submitting a pull request. You can also report a bug or request a feature in the [Issues tab](https://github.com/WhyDRS/Database/issues).

## Contributing

We welcome contributions from the community! If you have additional information or corrections, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear messages.
4. Submit a pull request detailing your changes.

## License

The source code is licensed under the [Affero General Public License (AGPL)](https://www.gnu.org/licenses/agpl-3.0.html) and the database is licensed under the [Open Database License ODbL](https://opendatacommons.org/licenses/odbl/1-0/).

## Contact

For questions, suggestions, or support, please contact us at [hi@whydrs.org](mailto:hi@whydrs.org).

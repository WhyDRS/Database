# WhyDRS Database Front-End Revamp

![WhyDRS Logo](assets/images/WhyDRS_Logo_transparent_background.png)

## 📋 Project Overview

Managing and accessing information about the Direct Registration System and individual publicly traded stocks can be challenging due to scattered and unorganized data sources. This information has been gathered in one place to make it easy for any investor to get direct access to static information about their investments. It is a volunteer asynchronous group effort in order to populate and maintain this database for the public good.

You can:
- [View through our custom UI](https://database.whydrs.org/)
- [View the raw data .json](https://github.com/WhyDRS/Database/blob/main/data/Issuers/Main_Database.json)
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

## 🛠️ Technologies Used

- HTML5
- CSS3 (with CSS Variables for theming)
- JavaScript (Vanilla)
- Responsive Design (Mobile-first approach)
- Vercel/Cloudflare (Development deployment platform)

## 🔍 Project Structure

- `/assets` - Images and other static assets
- `/css` - Styling files
- `/js` - JavaScript functionality
- `/data` - Database files (JSON)

## 🖥️ Local Development

To run this project locally:

1. Clone the repository
   ```
   git clone https://github.com/WhyDRS/Database.git
   ```

2. Checkout the main
   ```
   git checkout main
   ```

3a. Open the `index.html` file in your browser or use a local server

3b. Use the opensource webtool https://github.com/htmlpreview/htmlpreview.github.com to access the html. Access https://htmlpreview.github.io/ and paste the html to review in your browser.

## 🔮 Future Plans

- Enhanced data visualization components
- Additional broker guides
- Expanded search filters and sorting options

## 🤝 Contributing

Contributions to improve the WhyDRS front-end are welcome! Please feel free to submit a pull request or open an issue.

## 📄 License

This project is licensed under the [Affero General Public License (AGPL)](https://www.gnu.org/licenses/agpl-3.0.html) and the database is licensed under the [Open Database License ODbL](https://opendatacommons.org/licenses/odbl/1-0/).

## 📞 Contact

For questions, suggestions, or support, please contact us at hi@whydrs.org.

---

*Not your name, not your shares!*

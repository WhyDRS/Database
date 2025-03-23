Thank you for considering contributing to this project! Whether you're a developer, researcher, or just someone passionate about improving financial transparency, your contributions are welcome.


## Table of Contents
1. [Project Overview](#project-overview)
2. [Code of Conduct](#code-of-conduct)
3. [How to Contribute](#how-to-contribute)
4. [Getting Started with GitHub Desktop](#getting-started-with-github-desktop)
5. [Submitting Your Contributions](#submitting-your-contributions)
6. [License and Attribution](#license-and-attribution)


## Project Overview

This repository contains both the source code and a growing database of publicly traded companies. The database includes information on transfer agents, investor relations, company shares, and DRS (Direct Registration System) shares. DRS is the only way to register shares in your name and secure property rights over them.


## How to Contribute

You might contribute here by:
- Adding or updating information in the database (e.g., company details, transfer agent data, DRS information).
- Submitting enhancements, bug fixes, or new features for the source code.
- Improving documentation and guides.

## Contributing (For Beginners)

1. You will need to fork the repository by pressing the "Fork" button at the top, then "Create Fork". If you have trouble finding it, press CTRL+F on your keyboard and search "Fork". 

![Fork Button](assets/images/image.png)

![Create Fork](assets/images/image-2.png)

2. Sign into Github or make a new account to access your "fork", which gives you a personal copy of the database repository that you can edit.

![Link to Forked Repo](assets/images/image-3.png)

3. Open the `data/Issuers/Main-Database-CSV-Files` folder from your fork, select the letter you wish to contribute to, then press "." on your keyboard to enter VS Code for the Web.

![Data Folder](assets/images/image-4.png)

![Data Folder Letter A](assets/images/image-5.png)

![Github Dev Site](assets/images/image-6.png)

4. On the left-hand side, click the icon with four squares and search for "Excel Viewer" and Install the extension from MESCIUS. This will allow you to edit the CSV file as if you're working in a spreadsheet.

![Excel Viewer](assets/images/image-7.png)

5. Once the extension is installed, you can right-click on the tab of the previously opened CSV file and select "Reopen Editor With..." and press CSV Editor.

![Open With](assets/images/image-8.png)

![Open With CSV Editor](assets/images/image-9.png)

6. Make the changes to the CSV file that you'd like to submit, then once complete you should see a button on the left with a blue circle and a number inside it. Press that icon, write a message and press "Commit & Push" to save changes to your local fork.

![Edit Cell](assets/images/image-10.png)

![Commit & Push](assets/images/image-11.png)

7. Press the Top left menu then select "Go to Repository", press "Contribute" and then press "Open pull request". Make sure to select your branch and the base repository’s `main` branch.

![Back To Repository](assets/images/image-12.png)

![Open pull request](assets/images/image-13.png)

8. Press "Create pull request" and your submission will be reviewed. You may be asked to make some adjustments based on feedback.

![Create pull request](assets/images/image-14.png)

Once approved, your contribution will be merged into the project!

**Screenshots coming soon**. Also in the works: an easier way for contributors to enter their submissions.


## Getting Started with GitHub Desktop

For those new to contributing or unfamiliar with command-line tools, here’s how you can get started using [GitHub Desktop](https://desktop.github.com/).

1. **Fork the Repository:**
   - Go to the repository’s main page on GitHub and click the “Fork” button in the top right. This creates your own copy of the repository.

2. **Clone Your Fork Using GitHub Desktop:**
   - Open GitHub Desktop and click “File” > “Clone Repository.”
   - Select your fork from the list and choose a local folder to clone it to.

3. **Create a Branch:**
   - Before making changes, create a new branch for your work by selecting “Branch” > “New Branch.” Name your branch based on the feature or update you’re working on (e.g., `update-company-info`).

4. **Make Your Changes:**
   - For database updates: Add or edit the relevant files in the `data/` folder.
   - For source code: Make your changes in the `src/` folder.
   - Use any spreadsheet or code editors you’re comfortable with.

5. **Commit Your Changes:**
   - After making your changes, go to GitHub Desktop and you should see your updated files listed under “Changes.”
   - Write a clear and descriptive commit message, then click “Commit to [your branch name].”

6. **Push Your Branch:**
   - Once committed, push your branch to GitHub by clicking “Push origin” in GitHub Desktop.


## Submitting Your Contributions

1. **Open a Pull Request:**
   - On GitHub, go to your forked repository and click the “Pull Request” button. Select your branch and the base repository’s `main` branch.
   - Add a title and description explaining your changes.

2. **Review and Feedback:**
   - Your pull request will be reviewed. You may be asked to make some adjustments based on feedback.

3. **Merging:**
   - Once approved, your contribution will be merged into the project!


## License and Attribution

By contributing, you agree that your contributions will be licensed under the respective licenses for the source code and data:

- Source code contributions will be licensed under the AGPL.
- Data contributions will be licensed under the ODbL.

For more details, refer to the individual `LICENSE` files in the `src/` and `data/` directories.

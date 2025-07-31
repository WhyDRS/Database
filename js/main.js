// WhyDRS Landing Page JavaScript

// DOM Elements
const menuToggle = document.getElementById('menu-toggle');
const mainNav = document.querySelector('nav');
const currentYearElement = document.getElementById('current-year');
const searchForm = document.querySelector('#search-form');
const searchInput = document.querySelector('#search-input');
const heroSearchForm = document.querySelector('#hero-search-form');
const heroSearchInput = document.querySelector('#hero-search');
const resultsContainer = document.querySelector('#search-results');

// Autocomplete elements
let heroAutocompleteContainer = null;
let mainAutocompleteContainer = null;

// Database data
let databaseData = [];

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    const currentYear = new Date().getFullYear();
    currentYearElement.textContent = currentYear;

    // Mobile menu toggle
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            mainNav.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });
    }

    // Close menu when clicking a link (mobile)
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                menuToggle.classList.remove('active');
                mainNav.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
    });

    // Close menu when clicking outside nav
    document.addEventListener('click', function(event) {
        if (mainNav.classList.contains('active') && 
            !mainNav.contains(event.target) && 
            event.target !== menuToggle && 
            !menuToggle.contains(event.target)) {
            menuToggle.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
        
        // Close autocomplete dropdowns when clicking outside
        if (heroAutocompleteContainer && 
            !heroAutocompleteContainer.contains(event.target) && 
            event.target !== heroSearchInput) {
            heroAutocompleteContainer.style.display = 'none';
        }
        
        if (mainAutocompleteContainer && 
            !mainAutocompleteContainer.contains(event.target) && 
            event.target !== searchInput) {
            mainAutocompleteContainer.style.display = 'none';
        }
    });

    // Smooth scroll for all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            // Skip if it's just "#" (no specific target)
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Get header height to use as offset
                const headerHeight = document.querySelector('header').offsetHeight;
                // Add extra padding (20px) for visual comfort
                const scrollOffset = headerHeight + 20;
                
                // Calculate the element's position and apply offset
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - scrollOffset;
                
                // Scroll to the adjusted position
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // Load the database
    fetchDatabase();

    // Initialize autocomplete for hero search
    if (heroSearchInput) {
        initializeAutocomplete(heroSearchInput, 'hero');
    }
    
    // Initialize autocomplete for main search
    if (searchInput) {
        initializeAutocomplete(searchInput, 'main');
    }

    // Main search form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim().toUpperCase();
            if (query) {
                // Hide any open autocomplete
                if (mainAutocompleteContainer) {
                    mainAutocompleteContainer.style.display = 'none';
                }
                
                // Hide any backdrop elements
                const backdrops = document.querySelectorAll('.autocomplete-backdrop');
                backdrops.forEach(backdrop => {
                    backdrop.style.display = 'none';
                });
                
                searchDatabase(query);
                // Scroll to results
                resultsContainer.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Hero search form submission
    if (heroSearchForm) {
        heroSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = heroSearchInput.value.trim().toUpperCase();
            if (query) {
                // Hide any open autocomplete
                if (heroAutocompleteContainer) {
                    heroAutocompleteContainer.style.display = 'none';
                }
                
                // Hide any backdrop elements
                const backdrops = document.querySelectorAll('.autocomplete-backdrop');
                backdrops.forEach(backdrop => {
                    backdrop.style.display = 'none';
                });
                
                // Get the database section element
                const databaseSection = document.querySelector('#database');
                
                if (databaseSection) {
                    // Get header height to use as offset
                    const headerHeight = document.querySelector('header').offsetHeight;
                    // Add extra padding (20px) for visual comfort
                    const scrollOffset = headerHeight + 20;
                    
                    // Calculate the element's position and apply offset
                    const elementPosition = databaseSection.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - scrollOffset;
                    
                    // Scroll to the adjusted position
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: "smooth"
                    });
                    
                    // Set the main search input value
                    searchInput.value = query;
                    
                    // Wait for scroll to complete then search
                    setTimeout(() => {
                        searchDatabase(query);
                    }, 500);
                }
            }
        });
    }

    // Initialize scroll indicator functionality
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            const targetSection = document.querySelector('#how-it-works') || document.querySelector('#about');
            if (targetSection) {
                // Get header height to use as offset
                const headerHeight = document.querySelector('header').offsetHeight;
                // Add extra padding (20px) for visual comfort
                const scrollOffset = headerHeight + 20;
                
                // Calculate the element's position and apply offset
                const elementPosition = targetSection.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - scrollOffset;
                
                // Scroll to the adjusted position
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    }
});

// Initialize autocomplete functionality
function initializeAutocomplete(inputElement, type) {
    // Create backdrop element that covers the entire page
    const backdrop = document.createElement('div');
    backdrop.className = 'autocomplete-backdrop';
    document.body.appendChild(backdrop);
    
    // Create autocomplete container - append it to body instead of the form
    // This places it at the root level of the DOM, avoiding stacking context issues
    const autocompleteContainer = document.createElement('div');
    autocompleteContainer.className = 'autocomplete-container';
    document.body.appendChild(autocompleteContainer);
    
    // Store reference based on type
    if (type === 'hero') {
        heroAutocompleteContainer = autocompleteContainer;
    } else {
        mainAutocompleteContainer = autocompleteContainer;
    }
    
    // Hide by default
    autocompleteContainer.style.display = 'none';
    
    // Track current selected item
    let currentFocus = -1;
    
    // Input event listener to show suggestions
    inputElement.addEventListener('input', function() {
        const query = this.value.trim();
        
        // Clear previous results
        autocompleteContainer.innerHTML = '';
        
        // Hide if query is empty
        if (!query || !databaseData.length) {
            hideAutocomplete();
            return;
        }
        
        // Get suggestions
        const upperQuery = query.toUpperCase();
        const suggestions = databaseData.filter(item => 
            (item.Ticker && item.Ticker.toUpperCase().startsWith(upperQuery)) || 
            (item.Company_Name_Issuer && item.Company_Name_Issuer.toUpperCase().includes(upperQuery))
        ).slice(0, 10); // Limit to 10 results
        
        // If no suggestions, hide container
        if (suggestions.length === 0) {
            hideAutocomplete();
            return;
        }
        
        // Calculate position to place the dropdown below the input
        const inputRect = inputElement.getBoundingClientRect();
        autocompleteContainer.style.position = 'fixed';  // Use fixed positioning
        autocompleteContainer.style.width = `${inputRect.width}px`;
        autocompleteContainer.style.top = `${inputRect.bottom}px`;
        autocompleteContainer.style.left = `${inputRect.left}px`;
        
        // Show backdrop and container
        backdrop.style.display = 'block';
        autocompleteContainer.style.display = 'block';
        
        // Create suggestion items
        suggestions.forEach((company, index) => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'autocomplete-item';
            
            // Display ticker and company name
            const tickerDisplay = company.Ticker ? company.Ticker : '';
            const companyDisplay = company.Company_Name_Issuer ? company.Company_Name_Issuer : 'Unnamed Company';
            
            suggestionItem.innerHTML = `
                <strong>${tickerDisplay}</strong> ${tickerDisplay ? '- ' : ''}${companyDisplay}
            `.trim();
            
            // Add click event
            suggestionItem.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Store the selection value before hiding the dropdown
                const selectedValue = tickerDisplay || companyDisplay;
                
                // Immediately hide the dropdown before doing anything else
                hideAutocomplete();
                
                // Set the input value
                inputElement.value = selectedValue;
                
                // Set a flag to prevent the dropdown from reappearing due to focus events
                inputElement.setAttribute('data-just-selected', 'true');
                
                // Use setTimeout to allow the DOM to update before proceeding
                setTimeout(() => {
                    // If it's hero search, sync with main search
                    if (type === 'hero') {
                        const databaseSection = document.querySelector('#database');
                        
                        if (databaseSection) {
                            // Get header height to use as offset
                            const headerHeight = document.querySelector('header').offsetHeight;
                            // Add extra padding (20px) for visual comfort
                            const scrollOffset = headerHeight + 20;
                            
                            // Calculate the element's position and apply offset
                            const elementPosition = databaseSection.getBoundingClientRect().top;
                            const offsetPosition = elementPosition + window.pageYOffset - scrollOffset;
                            
                            // Scroll to the adjusted position
                            window.scrollTo({
                                top: offsetPosition,
                                behavior: "smooth"
                            });
                            
                            // Set the main search input value
                            searchInput.value = selectedValue;
                            
                            // Wait for scroll to complete then search
                            setTimeout(() => {
                                // Use exact match search when selecting from dropdown
                                searchDatabase(selectedValue, true);
                                
                                // Clear the flag after search is complete
                                inputElement.removeAttribute('data-just-selected');
                            }, 500);
                        }
                    } else {
                        // Main search - execute search directly with exact match
                        searchDatabase(selectedValue, true);
                        resultsContainer.scrollIntoView({ behavior: 'smooth' });
                        
                        // Clear the flag after search is complete
                        inputElement.removeAttribute('data-just-selected');
                    }
                }, 50); // Small delay to ensure DOM updates
            });
            
            autocompleteContainer.appendChild(suggestionItem);
        });
        
        // Reset current focus
        currentFocus = -1;
    });
    
    // Keyboard navigation
    inputElement.addEventListener('keydown', function(e) {
        const items = autocompleteContainer.querySelectorAll('.autocomplete-item');
        
        if (!items.length) return;
        
        // Down arrow key
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            currentFocus++;
            addActive(items, currentFocus);
        } 
        // Up arrow key
        else if (e.key === 'ArrowUp') {
            e.preventDefault();
            currentFocus--;
            addActive(items, currentFocus);
        } 
        // Enter key
        else if (e.key === 'Enter') {
            e.preventDefault();
            if (currentFocus > -1) {
                // Simulate click on active item
                if (items[currentFocus]) {
                    items[currentFocus].click();
                }
            } else {
                // Submit the form
                if (type === 'hero') {
                    heroSearchForm.dispatchEvent(new Event('submit'));
                } else {
                    searchForm.dispatchEvent(new Event('submit'));
                }
            }
        } 
        // Escape key
        else if (e.key === 'Escape') {
            hideAutocomplete();
        }
    });
    
    // Helper function to manage active items
    function addActive(items, index) {
        // Handle out of bounds
        if (index >= items.length) index = 0;
        if (index < 0) index = items.length - 1;
        
        // Remove active from all items
        Array.from(items).forEach(item => {
            item.classList.remove('autocomplete-active');
        });
        
        // Add active class to current focused item
        items[index].classList.add('autocomplete-active');
        currentFocus = index;
    }
    
    // Helper function to hide autocomplete
    function hideAutocomplete() {
        // Set display: none with !important to force hiding
        autocompleteContainer.style.cssText = 'display: none !important;';
        backdrop.style.cssText = 'display: none !important;';
        currentFocus = -1;
        
        // Hide all backdrops and autocomplete containers on the page for good measure
        document.querySelectorAll('.autocomplete-backdrop, .autocomplete-container').forEach(el => {
            el.style.cssText = 'display: none !important;';
        });
    }
    
    // Focus event to show suggestions if input has content
    inputElement.addEventListener('focus', function(e) {
        // Check if we just selected an item - if so, don't show dropdown again
        if (this.hasAttribute('data-just-selected')) {
            return;
        }
        
        const query = this.value.trim();
        if (query && databaseData.length) {
            // Trigger input event to show suggestions
            // Use a slight delay to prevent focus issues
            setTimeout(() => {
                this.dispatchEvent(new Event('input'));
            }, 10);
        }
    });
    
    // Click on backdrop should close the autocomplete
    backdrop.addEventListener('click', function() {
        hideAutocomplete();
    });
    
    // Handle window resize to reposition dropdown
    window.addEventListener('resize', function() {
        if (autocompleteContainer.style.display === 'block') {
            const inputRect = inputElement.getBoundingClientRect();
            autocompleteContainer.style.width = `${inputRect.width}px`;
            autocompleteContainer.style.top = `${inputRect.bottom}px`;
            autocompleteContainer.style.left = `${inputRect.left}px`;
        }
    });
    
    // Handle scroll to reposition dropdown
    window.addEventListener('scroll', function() {
        if (autocompleteContainer.style.display === 'block') {
            const inputRect = inputElement.getBoundingClientRect();
            autocompleteContainer.style.top = `${inputRect.bottom}px`;
            autocompleteContainer.style.left = `${inputRect.left}px`;
        }
    });
    
    // Global document click handler to close dropdown
    document.addEventListener('click', function(event) {
        // Don't do anything if clicking on the input or inside autocomplete
        if (event.target === inputElement || 
            autocompleteContainer.contains(event.target) || 
            event.target === backdrop) {
            return;
        }
        
        // Otherwise, hide the autocomplete
        hideAutocomplete();
    });
}

// Fetch the database
function fetchDatabase() {
    // Try multiple paths to find the database
    const paths = [
        'data/Issuers/Main_Database.json',
        './data/Issuers/Main_Database.json',
        '../data/Issuers/Main_Database.json',
        '/data/Issuers/Main_Database.json'
    ];
    
    // Try the first path
    tryFetchPath(paths, 0);
}

// Try fetching from a path, and if it fails, try the next one
function tryFetchPath(paths, index) {
    if (index >= paths.length) {
        console.error('Failed to load database from all paths');
        if (resultsContainer) {
            resultsContainer.innerHTML = '<div class="search-result"><h3>Failed to load database. Please try again later.</h3></div>';
        }
        return;
    }
    
    const path = paths[index];
    console.log(`Trying to load database from: ${path}`);
    
    fetch(path)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            databaseData = data;
            console.log(`Database loaded successfully from ${path}`);
        })
        .catch(error => {
            console.error(`Error loading database from ${path}:`, error);
            // Try the next path
            tryFetchPath(paths, index + 1);
        });
}

// Search the database
function searchDatabase(query, exactMatchOnly = false) {
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    if (!databaseData.length) {
        resultsContainer.innerHTML = '<div class="search-result"><h3>Database not loaded yet. Please try again.</h3></div>';
        return;
    }
    
    // Filter results
    const upperQuery = query.toUpperCase();
    let results;
    
    if (exactMatchOnly) {
        // Only match exact ticker
        results = databaseData.filter(item => 
            (item.Ticker && item.Ticker.toUpperCase() === upperQuery)
        );
        
        // If no results with exact ticker, try exact company name
        if (results.length === 0) {
            results = databaseData.filter(item => 
                (item.Company_Name_Issuer && item.Company_Name_Issuer.toUpperCase() === upperQuery)
            );
        }
    } else {
        // Regular search (partial matches)
        results = databaseData.filter(item => 
            (item.Ticker && item.Ticker.toUpperCase() === upperQuery) || 
            (item.Company_Name_Issuer && item.Company_Name_Issuer.toUpperCase().includes(upperQuery))
        );
    }
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="search-result"><h3>No results found</h3></div>';
        return;
    }
    
    // Display results
    results.forEach(company => {
        const resultHTML = `
            <div class="search-result">
                <h3>${company.Company_Name_Issuer || 'Unnamed Company'}</h3>
                
                <div class="result-section">
                    <h4>Company Information</h4>
                    <div class="result-details">
                        <div><strong>Ticker</strong> ${company.Ticker || 'N/A'}</div>
                        <div><strong>Exchange</strong> ${company.Exchange || 'N/A'}</div>
                        <div><strong>CUSIP</strong> ${company.CUSIP || 'N/A'}</div>
                        <div><strong>Shares Outstanding</strong> ${company.Shares_Outstanding || 'N/A'}</div>
                        <div><strong>CIK</strong> ${company.CIK || 'N/A'}</div>
                    </div>
                </div>
                
                <div class="result-section">
                    <h4>Direct Registration Information</h4>
                    <div class="result-details">
                        <div><strong>DRS Status</strong> ${company.DRS || 'Not Available'}</div>
                        <div><strong>Transfer Agent</strong> ${company.Transfer_Agent || 'N/A'}</div>
                        ${company.TA_URL ? `<div><strong>Transfer Agent Website</strong> <a href="${company.TA_URL}" target="_blank" rel="noopener noreferrer">Visit</a></div>` : '<div><strong>Transfer Agent Website</strong> N/A</div>'}
                        <div><strong>DTC Member Number</strong> ${company.DTC_Member_Number || 'N/A'}</div>
                        <div><strong>Percent Shares DRSd</strong> ${company.Percent_Shares_DRSd || 'N/A'}</div>
                    </div>
                </div>
                
                <div class="result-section">
                    <h4>Investor Relations</h4>
                    <div class="result-details">
                        <div><strong>IR Email</strong> ${company.IR_Emails || 'N/A'}</div>
                        <div><strong>IR Phone</strong> ${company.IR_Phone_Number || 'N/A'}</div>
                        ${company.IR_URL ? `<div><strong>IR Website</strong> <a href="${company.IR_URL}" target="_blank" rel="noopener noreferrer">Visit</a></div>` : '<div><strong>IR Website</strong> N/A</div>'}
                        <div><strong>Company Address</strong> ${company.IR_Company_Address || 'N/A'}</div>
                    </div>
                </div>
            </div>
        `;
        resultsContainer.innerHTML += resultHTML;
    });
}

// WhyDRS Database Table JavaScript

// DOM Elements
const tableBody = document.getElementById('table-body');
const tableSearch = document.getElementById('table-search');
const selectColumnsBtn = document.getElementById('select-columns');
const resetColumnsBtn = document.getElementById('reset-columns');
const prevPageBtn = document.getElementById('prev-page');
const nextPageBtn = document.getElementById('next-page');
const pageIndicator = document.getElementById('page-indicator');
const pageSizeSelect = document.getElementById('page-size');

// Table State
let tableData = [];
let filteredData = [];
let currentSort = {
    column: 'Ticker',
    direction: 'asc'
};
let pagination = {
    currentPage: 1,
    pageSize: 50,
    totalPages: 1
};
let visibleColumns = [
    'Ticker', 
    'Exchange', 
    'Company_Name_Issuer',
    'Transfer_Agent',
    'IR_Emails',
    'IR_Phone_Number'
];
let allColumns = [];

// Initialize the table
document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    const currentYear = new Date().getFullYear();
    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        currentYearElement.textContent = currentYear;
    }

    // Initialize page size from select
    pagination.pageSize = parseInt(pageSizeSelect.value);

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const mainNav = document.querySelector('nav');
    
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
        if (mainNav && mainNav.classList.contains('active') && 
            !mainNav.contains(event.target) && 
            event.target !== menuToggle && 
            !menuToggle.contains(event.target)) {
            menuToggle.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });

    // Load database data
    fetchDatabase();

    // Add event listeners for sorting
    const sortableHeaders = document.querySelectorAll('th.sortable');
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const column = this.getAttribute('data-column');
            sortTable(column);
        });
    });

    // Search functionality
    tableSearch.addEventListener('input', function() {
        filterTable(this.value.trim());
    });

    // Column selection
    selectColumnsBtn.addEventListener('click', showColumnSelector);
    resetColumnsBtn.addEventListener('click', resetColumns);

    // Pagination
    prevPageBtn.addEventListener('click', previousPage);
    nextPageBtn.addEventListener('click', nextPage);
    pageSizeSelect.addEventListener('change', function() {
        pagination.pageSize = parseInt(this.value);
        pagination.currentPage = 1;
        renderTable();
    });
});

// Fetch database data
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
        tableBody.innerHTML = '<tr><td colspan="6" class="loading-message">Failed to load database. Please try again later.</td></tr>';
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
            tableData = data;
            filteredData = [...tableData];
            
            // Extract all column names from the first item
            if (tableData.length > 0) {
                allColumns = Object.keys(tableData[0]);
            }
            
            console.log(`Database loaded successfully from ${path}`);
            sortTable(currentSort.column); // Initial sort
            updatePagination();
            renderTable();
        })
        .catch(error => {
            console.error(`Error loading database from ${path}:`, error);
            // Try the next path
            tryFetchPath(paths, index + 1);
        });
}

// Sort the table
function sortTable(column) {
    // Update sort direction
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'asc';
    }
    
    // Sort the filtered data
    filteredData.sort((a, b) => {
        const valueA = (a[column] || '').toString().toUpperCase();
        const valueB = (b[column] || '').toString().toUpperCase();
        
        if (valueA < valueB) {
            return currentSort.direction === 'asc' ? -1 : 1;
        }
        if (valueA > valueB) {
            return currentSort.direction === 'asc' ? 1 : -1;
        }
        return 0;
    });
    
    // Update sort icons
    const sortHeaders = document.querySelectorAll('th.sortable');
    sortHeaders.forEach(header => {
        const headerColumn = header.getAttribute('data-column');
        const sortIcon = header.querySelector('.sort-icon');
        
        if (headerColumn === currentSort.column) {
            sortIcon.textContent = currentSort.direction === 'asc' ? '▲' : '▼';
        } else {
            sortIcon.textContent = '';
        }
    });
    
    // Reset to first page
    pagination.currentPage = 1;
    renderTable();
}

// Filter the table based on search input
function filterTable(query) {
    if (!query) {
        filteredData = [...tableData];
    } else {
        const upperQuery = query.toUpperCase();
        filteredData = tableData.filter(item => {
            return visibleColumns.some(column => {
                const value = item[column];
                return value && value.toString().toUpperCase().includes(upperQuery);
            });
        });
    }
    
    updatePagination();
    renderTable();
}

// Update pagination state and controls
function updatePagination() {
    pagination.totalPages = Math.ceil(filteredData.length / pagination.pageSize);
    
    if (pagination.currentPage > pagination.totalPages) {
        pagination.currentPage = pagination.totalPages || 1;
    }
    
    pageIndicator.textContent = `Page ${pagination.currentPage} of ${pagination.totalPages}`;
    
    prevPageBtn.disabled = pagination.currentPage <= 1;
    nextPageBtn.disabled = pagination.currentPage >= pagination.totalPages;
}

// Navigate to previous page
function previousPage() {
    if (pagination.currentPage > 1) {
        pagination.currentPage--;
        updatePagination();
        renderTable();
        scrollToTableTop();
    }
}

// Navigate to next page
function nextPage() {
    if (pagination.currentPage < pagination.totalPages) {
        pagination.currentPage++;
        updatePagination();
        renderTable();
        scrollToTableTop();
    }
}

// Scroll to the top of the table
function scrollToTableTop() {
    const tableWrapper = document.querySelector('.table-wrapper');
    if (tableWrapper) {
        tableWrapper.scrollTop = 0;
        
        // Also scroll the window to keep the table in view
        const tablePosition = tableWrapper.getBoundingClientRect().top;
        if (tablePosition < 0) {
            window.scrollBy(0, tablePosition - 50); // 50px buffer
        }
    }
}

// Render the table with current data and pagination
function renderTable() {
    tableBody.innerHTML = '';
    
    if (filteredData.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="loading-message">No matching records found</td></tr>';
        return;
    }
    
    const start = (pagination.currentPage - 1) * pagination.pageSize;
    const end = Math.min(start + pagination.pageSize, filteredData.length);
    const pageData = filteredData.slice(start, end);
    
    pageData.forEach(item => {
        const row = document.createElement('tr');
        
        visibleColumns.forEach((column, index) => {
            const cell = document.createElement('td');
            cell.textContent = item[column] || '';
            
            // Make email and phone number cells copyable
            if (column === 'IR_Emails' || column === 'IR_Phone_Number') {
                if (item[column]) {
                    cell.classList.add('copyable-cell');
                    cell.setAttribute('data-copy', item[column]);
                    cell.addEventListener('click', handleCopyClick);
                }
            }
            
            row.appendChild(cell);
        });
        
        tableBody.appendChild(row);
    });
}

// Copy to clipboard functionality
function handleCopyClick(e) {
    const text = e.target.getAttribute('data-copy');
    const cell = e.target;
    
    // Use the modern Clipboard API with fallback to execCommand
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
            .then(() => {
                showCopySuccess(cell);
            })
            .catch(err => {
                console.error('Could not copy text: ', err);
                fallbackCopy(text, cell);
            });
    } else {
        fallbackCopy(text, cell);
    }
}

// Fallback copy method for older browsers
function fallbackCopy(text, cell) {
    // Create a temporary input element
    const tempInput = document.createElement('input');
    tempInput.value = text;
    tempInput.style.position = 'absolute';
    tempInput.style.left = '-9999px';
    document.body.appendChild(tempInput);
    tempInput.select();
    
    try {
        // Copy the text
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess(cell);
        } else {
            console.error('Fallback copy was unsuccessful');
        }
    } catch (err) {
        console.error('Fallback copy error: ', err);
    }
    
    // Remove the temporary element
    document.body.removeChild(tempInput);
}

// Show copy success visual feedback
function showCopySuccess(cell) {
    // Visual feedback
    cell.classList.add('copy-success');
    
    // Remove the success class after a delay
    setTimeout(() => {
        cell.classList.remove('copy-success');
    }, 1500);
}

// Show column selector modal
function showColumnSelector() {
    // Create modal if it doesn't exist
    let modal = document.querySelector('.column-selector-modal');
    
    if (!modal) {
        modal = document.createElement('div');
        modal.className = 'column-selector-modal';
        
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        
        // Header
        const modalHeader = document.createElement('div');
        modalHeader.className = 'modal-header';
        
        const modalTitle = document.createElement('h3');
        modalTitle.textContent = 'Select Columns';
        
        const closeButton = document.createElement('button');
        closeButton.className = 'close-modal';
        closeButton.textContent = '×';
        closeButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });
        
        modalHeader.appendChild(modalTitle);
        modalHeader.appendChild(closeButton);
        
        // Column options
        const columnOptions = document.createElement('div');
        columnOptions.className = 'column-options';
        
        allColumns.forEach(column => {
            const option = document.createElement('div');
            option.className = 'column-option';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `column-${column}`;
            checkbox.value = column;
            checkbox.checked = visibleColumns.includes(column);
            
            const label = document.createElement('label');
            label.htmlFor = `column-${column}`;
            label.textContent = formatColumnName(column);
            
            option.appendChild(checkbox);
            option.appendChild(label);
            columnOptions.appendChild(option);
        });
        
        // Footer
        const modalFooter = document.createElement('div');
        modalFooter.className = 'modal-footer';
        
        const cancelButton = document.createElement('button');
        cancelButton.className = 'button tertiary';
        cancelButton.textContent = 'Cancel';
        cancelButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });
        
        const applyButton = document.createElement('button');
        applyButton.className = 'button primary';
        applyButton.textContent = 'Apply';
        applyButton.addEventListener('click', () => {
            applyColumnSelection();
            modal.style.display = 'none';
        });
        
        modalFooter.appendChild(cancelButton);
        modalFooter.appendChild(applyButton);
        
        // Assemble modal
        modalContent.appendChild(modalHeader);
        modalContent.appendChild(columnOptions);
        modalContent.appendChild(modalFooter);
        modal.appendChild(modalContent);
        
        document.body.appendChild(modal);
        
        // Close when clicking outside the modal
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
    
    // Show the modal
    modal.style.display = 'flex';
}

// Apply column selection
function applyColumnSelection() {
    const checkboxes = document.querySelectorAll('.column-option input[type="checkbox"]');
    const newVisibleColumns = [];
    
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            newVisibleColumns.push(checkbox.value);
        }
    });
    
    // Ensure at least one column is visible
    if (newVisibleColumns.length === 0) {
        alert('Please select at least one column to display.');
        return;
    }
    
    visibleColumns = newVisibleColumns;
    updateTableHeaders();
    renderTable();
}

// Update table headers based on visible columns
function updateTableHeaders() {
    const headerRow = document.querySelector('.data-table thead tr');
    headerRow.innerHTML = '';
    
    visibleColumns.forEach(column => {
        const th = document.createElement('th');
        th.className = 'sortable';
        th.setAttribute('data-column', column);
        
        const sortIcon = document.createElement('span');
        sortIcon.className = 'sort-icon';
        if (column === currentSort.column) {
            sortIcon.textContent = currentSort.direction === 'asc' ? '▲' : '▼';
        }
        
        th.textContent = formatColumnName(column) + ' ';
        th.appendChild(sortIcon);
        
        th.addEventListener('click', function() {
            sortTable(column);
        });
        
        headerRow.appendChild(th);
    });
}

// Reset columns to default
function resetColumns() {
    visibleColumns = [
        'Ticker', 
        'Exchange', 
        'Company_Name_Issuer',
        'Transfer_Agent',
        'IR_Emails',
        'IR_Phone_Number'
    ];
    
    updateTableHeaders();
    renderTable();
}

// Format column name for display
function formatColumnName(column) {
    return column
        .replace(/_/g, ' ')
        .replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
} 
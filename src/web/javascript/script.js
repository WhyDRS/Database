/**
 * WhyDRS Database - Main JavaScript
 * Modern implementation with enhanced interactivity
 */

// Configuration object
const CONFIG = {
    // Data source URL
    dataUrl: 'src/web/data.json',
    
    // Default visible columns
    defaultVisibleColumns: [
        'Symbol', 
        'Name', 
        'Exchange', 
        'Transfer Agent',
        'Direct Registration',
        'Fee',
        'Website',
        'Phone'
    ],
    
    // DataTable settings
    pageLength: 10,
    lengthMenu: [5, 10, 25, 50, 100, -1],
    
    // Animation durations
    animationDuration: 300,
    counterDuration: 2000,
    
    // Chart colors
    chartColors: [
        '#2563eb', '#f59e0b', '#10b981', '#ef4444', 
        '#8b5cf6', '#ec4899', '#06b6d4', '#f97316'
    ]
};

// Application state
const APP = {
    dataTable: null,
    rawData: [],
    isInitialized: false,
    charts: {},
    isDarkMode: false,
    isMobileMenuOpen: false
};

/**
 * Document ready function
 */
$(document).ready(function() {
    console.log('WhyDRS Database initializing...');
    
    // Initialize UI components
    initUI();
    
    // Load data
    loadData();
    
    // Check for dark mode preference
    checkDarkModePreference();
    
    // Initialize particles for hero
    initParticles();
});

/**
 * Initialize UI components
 */
function initUI() {
    // Mobile menu toggle
    $('.menu-toggle').on('click', function() {
        toggleMobileMenu();
    });
    
    // Mobile menu links (close menu when clicked)
    $('.mobile-nav-link').on('click', function() {
        if (APP.isMobileMenuOpen) {
            toggleMobileMenu();
        }
    });
    
    // Dark mode toggle
    $('.theme-toggle').on('click', function() {
        toggleDarkMode();
    });
    
    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        if (this.hash !== '') {
            event.preventDefault();
            
            const hash = this.hash;
            const headerHeight = $('.header').outerHeight();
            
            $('html, body').animate({
                scrollTop: $(hash).offset().top - headerHeight
            }, 800, 'easeOutQuad');
            
            // Close mobile menu if open
            if (APP.isMobileMenuOpen) {
                toggleMobileMenu();
            }
            
            // Update active nav state
            $('.nav-link').removeClass('active');
            $(`.nav-link[href="${hash}"]`).addClass('active');
        }
    });
    
    // Back to top button
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 300) {
            $('#back-to-top').addClass('visible');
        } else {
            $('#back-to-top').removeClass('visible');
        }
        
        // Update active nav on scroll
        updateActiveNavOnScroll();
    });
    
    $('#back-to-top').on('click', function() {
        $('html, body').animate({ scrollTop: 0 }, 800, 'easeOutQuad');
        return false;
    });
    
    // Global search functionality
    $('#global-search').on('keyup', function() {
        if (APP.dataTable) {
            APP.dataTable.search($(this).val()).draw();
        }
    });
    
    // DataTable column controls
    $('#select-columns').on('click', function() {
        $('.dt-button.buttons-collection').click();
    });
    
    $('#reset-columns').on('click', function() {
        resetColumnsToDefault();
    });
}

/**
 * Initialize particles for hero section
 */
function initParticles() {
    const particles = document.querySelector('.hero-particles');
    if (!particles) return;
    
    // Create particles
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        // Random size
        const size = Math.random() * 5 + 1;
        
        // Random opacity
        const opacity = Math.random() * 0.5 + 0.1;
        
        // Random animation duration
        const duration = Math.random() * 20 + 10;
        
        // Apply styles
        particle.style.position = 'absolute';
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.opacity = opacity;
        particle.style.backgroundColor = 'white';
        particle.style.borderRadius = '50%';
        particle.style.animation = `float ${duration}s ease-in-out infinite`;
        
        // Add particle to container
        particles.appendChild(particle);
    }
}

/**
 * Update active navigation link based on scroll position
 */
function updateActiveNavOnScroll() {
    const scrollPosition = $(window).scrollTop() + 100;
    const headerHeight = $('.header').outerHeight();
    
    // Check each section
    $('section[id]').each(function() {
        const sectionTop = $(this).offset().top - headerHeight;
        const sectionBottom = sectionTop + $(this).outerHeight();
        const sectionId = $(this).attr('id');
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
            $('.nav-link').removeClass('active');
            $(`.nav-link[href="#${sectionId}"]`).addClass('active');
        }
    });
}

/**
 * Toggle mobile menu
 */
function toggleMobileMenu() {
    const mobileMenu = $('.mobile-menu');
    const menuToggle = $('.menu-toggle');
    
    if (APP.isMobileMenuOpen) {
        mobileMenu.removeClass('active');
        menuToggle.removeClass('active');
        $('body').removeClass('menu-open');
    } else {
        mobileMenu.addClass('active');
        menuToggle.addClass('active');
        $('body').addClass('menu-open');
    }
    
    APP.isMobileMenuOpen = !APP.isMobileMenuOpen;
}

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    const body = $('body');
    const icon = $('.theme-toggle i');
    
    if (body.hasClass('dark-mode')) {
        body.removeClass('dark-mode');
        icon.removeClass('fa-sun').addClass('fa-moon');
        APP.isDarkMode = false;
    } else {
        body.addClass('dark-mode');
        icon.removeClass('fa-moon').addClass('fa-sun');
        APP.isDarkMode = true;
    }
    
    // Save preference
    localStorage.setItem('dark-mode', APP.isDarkMode ? 'true' : 'false');
    
    // Update charts if they exist
    updateChartsTheme();
}

/**
 * Check for dark mode preference
 */
function checkDarkModePreference() {
    const savedPreference = localStorage.getItem('dark-mode');
    
    if (savedPreference === 'true') {
        $('body').addClass('dark-mode');
        $('.theme-toggle i').removeClass('fa-moon').addClass('fa-sun');
        APP.isDarkMode = true;
    } else if (savedPreference === null) {
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            $('body').addClass('dark-mode');
            $('.theme-toggle i').removeClass('fa-moon').addClass('fa-sun');
            APP.isDarkMode = true;
        }
    }
}

/**
 * Update charts theme based on dark mode
 */
function updateChartsTheme() {
    if (!APP.charts || Object.keys(APP.charts).length === 0) return;
    
    const textColor = APP.isDarkMode ? '#e5e7eb' : '#1f2937';
    const gridColor = APP.isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
    
    // Update each chart
    Object.values(APP.charts).forEach(chart => {
        if (!chart) return;
        
        // Update scales
        if (chart.options && chart.options.scales) {
            // For Chart.js v3+
            if (chart.options.scales.x) {
                chart.options.scales.x.ticks.color = textColor;
                chart.options.scales.x.grid.color = gridColor;
            }
            
            if (chart.options.scales.y) {
                chart.options.scales.y.ticks.color = textColor;
                chart.options.scales.y.grid.color = gridColor;
            }
        }
        
        // Update legend
        if (chart.options.plugins && chart.options.plugins.legend) {
            chart.options.plugins.legend.labels.color = textColor;
        }
        
        chart.update();
    });
}

/**
 * Load data from the API
 */
function loadData() {
    $('#loading-overlay').show();
    
    $.ajax({
        url: CONFIG.dataUrl,
        dataType: 'json',
        success: function(data) {
            console.log('Data loaded successfully');
            APP.rawData = data;
            
            // Initialize DataTable
            initDataTable(data);
            
            // Update statistics
            updateStatistics(data);
            
            // Initialize charts
            initCharts(data);
            
            // Hide loading overlay with slight delay for smoother transition
            setTimeout(() => {
                $('#loading-overlay').fadeOut(300);
                $('#data-table').removeClass('hidden').fadeIn(300);
            }, 500);
        },
        error: function(xhr, status, error) {
            console.error('Error loading data:', error);
            
            // Display error message
            $('#loading-overlay').html(`
                <div class="error-message">
                    <i class="fas fa-exclamation-circle"></i>
                    <h4>Error Loading Data</h4>
                    <p>${error || 'Could not load the database. Please try again later.'}</p>
                    <button class="btn btn-primary" onclick="location.reload()">Retry</button>
                </div>
            `);
        }
    });
}

/**
 * Initialize DataTable with the provided data
 */
function initDataTable(data) {
    if (!data || !data.length) return;
    
    // Extract column definitions from data
    const columns = Object.keys(data[0]).map(key => {
        return {
            title: key,
            data: key
        };
    });
    
    // Initialize DataTable
    APP.dataTable = $('#data-table').DataTable({
        data: data,
        columns: columns,
        pageLength: CONFIG.pageLength,
        lengthMenu: CONFIG.lengthMenu.map(n => [n, n === -1 ? 'All' : n]),
        dom: 'Blfrtip',
        buttons: [
            {
                extend: 'colvis',
                text: '<i class="fas fa-columns"></i> Columns',
                className: 'dt-button-primary'
            }
        ],
        responsive: true,
        language: {
            search: '',
            searchPlaceholder: 'Search in table...',
            lengthMenu: '_MENU_ rows per page',
            info: 'Showing _START_ to _END_ of _TOTAL_ entries',
            infoEmpty: 'No matching records found',
            infoFiltered: '(filtered from _MAX_ total entries)',
            paginate: {
                first: '<i class="fas fa-angle-double-left"></i>',
                previous: '<i class="fas fa-angle-left"></i>',
                next: '<i class="fas fa-angle-right"></i>',
                last: '<i class="fas fa-angle-double-right"></i>'
            }
        },
        order: [[1, 'asc']], // Sort by company name by default
        stateSave: true,
        columnDefs: [
            {
                // Format Website column
                targets: columns.findIndex(col => col.title === 'Website'),
                render: function(data, type, row) {
                    if (type === 'display' && data) {
                        // Ensure URL has protocol
                        let url = data;
                        if (!/^https?:\/\//i.test(url)) {
                            url = 'https://' + url;
                        }
                        
                        return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="table-link">
                                    <i class="fas fa-external-link-alt"></i> Visit
                                </a>`;
                    }
                    return data;
                }
            },
            {
                // Format Phone column
                targets: columns.findIndex(col => col.title === 'Phone'),
                render: function(data, type, row) {
                    if (type === 'display' && data) {
                        return `<a href="tel:${data.replace(/[^\d+]/g, '')}" class="table-link">
                                    <i class="fas fa-phone"></i> ${data}
                                </a>`;
                    }
                    return data;
                }
            },
            {
                // Format Direct Registration column
                targets: columns.findIndex(col => col.title === 'Direct Registration'),
                render: function(data, type, row) {
                    if (type === 'display') {
                        if (data === 'Yes') {
                            return `<span class="status-badge success">
                                        <i class="fas fa-check-circle"></i> Yes
                                    </span>`;
                        } else if (data === 'No') {
                            return `<span class="status-badge danger">
                                        <i class="fas fa-times-circle"></i> No
                                    </span>`;
                        } else {
                            return `<span class="status-badge neutral">
                                        <i class="fas fa-question-circle"></i> Unknown
                                    </span>`;
                        }
                    }
                    return data;
                }
            },
            {
                // Format Symbol column
                targets: columns.findIndex(col => col.title === 'Symbol'),
                render: function(data, type, row) {
                    if (type === 'display' && data) {
                        return `<span class="ticker-symbol">${data}</span>`;
                    }
                    return data;
                }
            }
        ],
        initComplete: function() {
            // Set default visible columns
            this.api().columns().every(function(index) {
                const columnTitle = $(this.header()).text();
                const visible = CONFIG.defaultVisibleColumns.includes(columnTitle);
                this.visible(visible);
            });
            
            // Apply custom styling to DataTables elements
            styleDataTable();
            
            APP.isInitialized = true;
            
            // Handle window resize for better mobile experience
            $(window).on('resize', function() {
                if (APP.dataTable) {
                    APP.dataTable.columns.adjust().responsive.recalc();
                }
            });
        }
    });
}

/**
 * Apply custom styling to DataTable elements
 */
function styleDataTable() {
    // Style search input
    $('.dataTables_filter input')
        .addClass('dt-search')
        .attr('placeholder', 'Search within table...');
    
    // Style length select
    $('.dataTables_length select').addClass('dt-select');
    
    // Add custom classes for better styling
    $('.dataTables_info').addClass('dt-info');
    $('.dataTables_paginate').addClass('dt-pagination');
    $('.paginate_button').addClass('dt-page-btn');
    $('.paginate_button.current').addClass('dt-page-btn-current');
}

/**
 * Reset columns to default visibility
 */
function resetColumnsToDefault() {
    if (!APP.dataTable) return;
    
    APP.dataTable.columns().every(function(index) {
        const columnTitle = $(this.header()).text();
        const visible = CONFIG.defaultVisibleColumns.includes(columnTitle);
        this.visible(visible);
    });
}

/**
 * Update statistics based on data
 */
function updateStatistics(data) {
    if (!data || !data.length) return;
    
    // Count unique companies
    const companyCount = data.length;
    
    // Count unique exchanges
    const exchanges = new Set();
    data.forEach(item => {
        if (item.Exchange) exchanges.add(item.Exchange);
    });
    const exchangeCount = exchanges.size;
    
    // Count unique transfer agents
    const transferAgents = new Set();
    data.forEach(item => {
        if (item['Transfer Agent']) transferAgents.add(item['Transfer Agent']);
    });
    const transferAgentCount = transferAgents.size;
    
    // Update hero stats
    $('#hero-company-count').text(companyCount);
    $('#hero-exchange-count').text(exchangeCount);
    $('#hero-agent-count').text(transferAgentCount);
    
    // Update database stats
    $('#company-count').text(companyCount);
    $('#exchange-count').text(exchangeCount);
    $('#transfer-agent-count').text(transferAgentCount);
    
    // Set last updated date to today's date
    const today = new Date();
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    $('#last-updated').text(today.toLocaleDateString('en-US', options));
    
    // Animate counters
    animateCounters();
}

/**
 * Animate counter elements
 */
function animateCounters() {
    $('.stat-value, .db-stat-value').each(function() {
        const $this = $(this);
        
        // Skip if it's a date value
        if ($this.hasClass('date')) return;
        
        const countTo = parseInt($this.text(), 10);
        
        if (isNaN(countTo)) return;
        
        $({ countNum: 0 }).animate({
            countNum: countTo
        }, {
            duration: CONFIG.counterDuration,
            easing: 'easeOutExpo',
            step: function() {
                $this.text(Math.floor(this.countNum));
            },
            complete: function() {
                $this.text(this.countNum);
            }
        });
    });
}

/**
 * Initialize charts
 */
function initCharts(data) {
    if (!data || !data.length || typeof Chart === 'undefined') return;
    
    // Initialize charts
    initExchangeChart(data);
    initTransferAgentChart(data);
    initGrowthChart(data);
}

/**
 * Initialize exchange distribution chart
 */
function initExchangeChart(data) {
    const ctx = document.getElementById('exchangeChart');
    if (!ctx) return;
    
    // Count companies by exchange
    const exchangeCounts = {};
    data.forEach(item => {
        if (item.Exchange) {
            exchangeCounts[item.Exchange] = (exchangeCounts[item.Exchange] || 0) + 1;
        }
    });
    
    // Sort exchanges by count (descending)
    const sortedExchanges = Object.entries(exchangeCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6); // Top 6 exchanges
    
    // Add "Other" category for remaining exchanges
    const topExchangesCount = sortedExchanges.reduce((sum, item) => sum + item[1], 0);
    const otherCount = data.filter(item => item.Exchange).length - topExchangesCount;
    
    if (otherCount > 0) {
        sortedExchanges.push(['Other', otherCount]);
    }
    
    // Prepare data for chart
    const labels = sortedExchanges.map(item => item[0]);
    const values = sortedExchanges.map(item => item[1]);
    
    // Create chart
    APP.charts.exchange = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: CONFIG.chartColors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: APP.isDarkMode ? '#1f2937' : '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            family: 'Inter, sans-serif',
                            size: 12
                        },
                        padding: 15,
                        color: APP.isDarkMode ? '#e5e7eb' : '#1f2937'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            const percentage = Math.round((value / data.length) * 100);
                            return `${value} companies (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize transfer agent chart
 */
function initTransferAgentChart(data) {
    const ctx = document.getElementById('transferAgentChart');
    if (!ctx) return;
    
    // Count companies by transfer agent
    const agentCounts = {};
    data.forEach(item => {
        if (item['Transfer Agent']) {
            agentCounts[item['Transfer Agent']] = (agentCounts[item['Transfer Agent']] || 0) + 1;
        }
    });
    
    // Sort transfer agents by count (descending)
    const sortedAgents = Object.entries(agentCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6); // Top 6 transfer agents
    
    // Add "Other" category for remaining transfer agents
    const topAgentsCount = sortedAgents.reduce((sum, item) => sum + item[1], 0);
    const otherCount = data.filter(item => item['Transfer Agent']).length - topAgentsCount;
    
    if (otherCount > 0) {
        sortedAgents.push(['Other', otherCount]);
    }
    
    // Prepare data for chart
    const labels = sortedAgents.map(item => item[0]);
    const values = sortedAgents.map(item => item[1]);
    
    // Create chart
    APP.charts.transferAgent = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: CONFIG.chartColors.slice(0, labels.length).reverse(),
                borderWidth: 2,
                borderColor: APP.isDarkMode ? '#1f2937' : '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            family: 'Inter, sans-serif',
                            size: 12
                        },
                        padding: 15,
                        color: APP.isDarkMode ? '#e5e7eb' : '#1f2937'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            const total = data.filter(item => item['Transfer Agent']).length;
                            const percentage = Math.round((value / total) * 100);
                            return `${value} companies (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize growth chart (with mock data)
 */
function initGrowthChart(data) {
    const ctx = document.getElementById('growthChart');
    if (!ctx) return;
    
    // Generate past 12 months labels
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const labels = [];
    const currentDate = new Date();
    
    for (let i = 11; i >= 0; i--) {
        const month = currentDate.getMonth() - i;
        const year = currentDate.getFullYear();
        const date = new Date(year, month, 1);
        const monthLabel = months[date.getMonth()];
        const yearLabel = date.getFullYear();
        labels.push(`${monthLabel} ${yearLabel}`);
    }
    
    // Generate mock growth data based on current total
    const totalCompanies = data.length;
    const growthData = [];
    let currentCount = Math.round(totalCompanies * 0.7); // Start at 70% of current count
    
    for (let i = 0; i < 11; i++) {
        growthData.push(currentCount);
        
        // Random growth each month
        const growth = Math.floor(Math.random() * 40) + 10;
        currentCount += growth;
    }
    
    // Set final month to the actual total
    growthData.push(totalCompanies);
    
    // Create gradient for background
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(37, 99, 235, 0.7)');
    gradient.addColorStop(1, 'rgba(37, 99, 235, 0)');
    
    // Create chart
    APP.charts.growth = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Companies',
                data: growthData,
                borderColor: CONFIG.chartColors[0],
                backgroundColor: gradient,
                borderWidth: 3,
                pointBackgroundColor: CONFIG.chartColors[0],
                pointRadius: 4,
                pointHoverRadius: 7,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        display: false,
                        color: APP.isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        color: APP.isDarkMode ? '#e5e7eb' : '#1f2937',
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        color: APP.isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
                        borderDash: [5, 5]
                    },
                    ticks: {
                        color: APP.isDarkMode ? '#e5e7eb' : '#1f2937'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `${context.raw} companies`;
                        }
                    }
                }
            }
        }
    });
}

// Add custom easing functions for animations
$.extend($.easing, {
    easeOutQuad: function(x, t, b, c, d) {
        return -c * (t /= d) * (t - 2) + b;
    },
    easeOutCubic: function(x, t, b, c, d) {
        return c * ((t = t / d - 1) * t * t + 1) + b;
    },
    easeOutExpo: function(x, t, b, c, d) {
        return (t === d) ? b + c : c * (-Math.pow(2, -10 * t / d) + 1) + b;
    }
});
  
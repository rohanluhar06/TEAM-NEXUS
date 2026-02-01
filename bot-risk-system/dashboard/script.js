/***********************
 * DOM Elements
 ***********************/
const analyzeBtn = document.getElementById('analyzeBtn');
const backBtn = document.getElementById('backBtn');
const usernameInput = document.getElementById('usernameInput');
const platformBtns = document.querySelectorAll('.platform-btn');
const tokenCountElement = document.getElementById('tokenCount');
const upgradeCta = document.getElementById('upgradeCta');
const dashboard = document.getElementById('dashboard');
const searchSection = document.querySelector('.search-section');

// Display elements
const displayUsername = document.getElementById('displayUsername');
const accountPlatform = document.getElementById('accountPlatform');
const riskScore = document.getElementById('riskScore');
const riskLabel = document.getElementById('riskLabel');
const riskExplanation = document.getElementById('riskExplanation');

/***********************
 * State
 ***********************/
let tokens = 3;
let selectedPlatform = 'instagram';

/***********************
 * Platform selection
 ***********************/
platformBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        platformBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedPlatform = btn.getAttribute('data-platform');
    });
});

/***********************
 * 🔥 INSTAGRAM BACKEND CALL
 ***********************/
async function analyzeInstagram(username) {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/analyze-instagram",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: username })
            }
        );

        const data = await response.json();

        if (data.error) {
            alert("Instagram fetch failed — account may be private.");
            return;
        }

        /* =========================
           REAL PROFILE STATS
        ========================== */

        document.getElementById("followersBox").textContent =
            data.profile.followers.toLocaleString();

        document.getElementById("followingBox").textContent =
            data.profile.following;

        document.getElementById("accountAgeBox").textContent =
            (data.profile.account_age_days / 365).toFixed(1) + " years";

        // simple demo engagement estimate
        const engagement =
            (data.profile.posts /
            Math.max(data.profile.followers, 1) * 100).toFixed(2);

        document.getElementById("engagementBox").textContent =
            engagement + "%";

        /* =========================
           MODEL OUTPUT
        ========================== */

        updateRiskGauge(data.analysis.bot_risk_score);

        riskExplanation.innerHTML =
            data.analysis.explanations.join("<br>");

        initializeActivityChart();

    } catch (err) {
        alert("Backend connection failed — check API server.");
        console.error(err);
    }
}

/***********************
 * Analyze account button
 ***********************/
analyzeBtn.addEventListener('click', () => {
    const username = usernameInput.value.trim();

    if (!username) {
        alert('Please enter a username.');
        return;
    }

    if (tokens <= 0) {
        alert('No tokens left.');
        return;
    }

    tokens--;
    tokenCountElement.textContent = tokens;

    if (tokens <= 0) {
        analyzeBtn.classList.add('disabled');
        upgradeCta.style.display = 'block';
    }

    // Display username
    const cleanUsername =
        username.startsWith('@') ? username : '@' + username;
    displayUsername.textContent = cleanUsername;

    // Platform display
    const platformNames = {
        instagram: 'Instagram',
        twitter: 'X (Twitter)',
        youtube: 'YouTube'
    };
    accountPlatform.textContent = platformNames[selectedPlatform];

    // Show dashboard
    searchSection.style.display = 'none';
    dashboard.style.display = 'block';

    // 🚀 LIVE CALL
    analyzeInstagram(username);

    dashboard.scrollIntoView({ behavior: 'smooth' });
});

/***********************
 * Back button
 ***********************/
backBtn.addEventListener('click', () => {
    dashboard.style.display = 'none';
    searchSection.style.display = 'block';
});

/***********************
 * Risk Gauge
 ***********************/
function updateRiskGauge(score) {
    const gaugeProgress = document.getElementById('gaugeProgress');
    const radius = 80;
    const circumference = 2 * Math.PI * radius;

    const offset = circumference - (score / 100) * circumference;
    gaugeProgress.style.strokeDashoffset = offset;

    const svg = gaugeProgress.closest('svg');
    let defs = svg.querySelector('defs');
    if (!defs) {
        defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        svg.insertBefore(defs, svg.firstChild);
    }

    if (score < 40) {
        gaugeProgress.style.stroke = '#4ade80';
        riskLabel.className = 'risk-label risk-low';
        riskLabel.textContent = 'LOW RISK';
    } else if (score < 80) {
        defs.innerHTML = `
            <linearGradient id="risk-gradient-medium">
                <stop offset="0%" style="stop-color:#4ade80"/>
                <stop offset="100%" style="stop-color:#f8961e"/>
            </linearGradient>`;
        gaugeProgress.style.stroke = 'url(#risk-gradient-medium)';
        riskLabel.className = 'risk-label risk-medium';
        riskLabel.textContent = 'MEDIUM RISK';
    } else {
        defs.innerHTML = `
            <linearGradient id="risk-gradient-high">
                <stop offset="0%" style="stop-color:#f8961e"/>
                <stop offset="100%" style="stop-color:#f72585"/>
            </linearGradient>`;
        gaugeProgress.style.stroke = 'url(#risk-gradient-high)';
        riskLabel.className = 'risk-label risk-high';
        riskLabel.textContent = 'HIGH RISK';
    }

    riskScore.textContent = score;
}

/***********************
 * Activity Chart (Demo)
 ***********************/
function initializeActivityChart() {
    const ctx = document.getElementById('activityChart').getContext('2d');

    if (window.activityChartInstance) {
        window.activityChartInstance.destroy();
    }

    window.activityChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug'],
            datasets: [
                { label: 'Posts', data: [12,19,8,15,22,18,25,30] },
                { label: 'Followers', data: [45,47,48,50,52,55,100,125] }
            ]
        },
        options: { responsive: true }
    });
}

/***********************
 * Enter key support
 ***********************/
usernameInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') analyzeBtn.click();
});

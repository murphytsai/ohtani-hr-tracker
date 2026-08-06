import json

def build_html():
    with open('ohtani_hrs_mlb.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)

    html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>大谷翔平歷年全壘打與被打投手統計 (Shohei Ohtani HR Tracker)</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans TC', 'Inter', sans-serif;
            background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #0b132b 100%);
            color: #f8fafc;
            min-height: 100vh;
        }
        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .glass-card-hover:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-2px);
            transition: all 0.2s ease-in-out;
        }
        .gold-gradient-text {
            background: linear-gradient(90deg, #fde047, #eab308, #ca8a04);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .dodger-blue-text {
            background: linear-gradient(90deg, #38bdf8, #0284c7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-8">
        
        <!-- Header -->
        <header class="glass-card rounded-2xl p-6 md:p-8 relative overflow-hidden">
            <div class="absolute -right-10 -bottom-10 opacity-10 pointer-events-none">
                <svg width="300" height="300" viewBox="0 0 24 24" fill="white"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            </div>
            <div class="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
                <div>
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-sm font-semibold mb-3">
                        <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
                        MLB Statcast 數據官方即時同步
                    </div>
                    <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight">
                        <span class="gold-gradient-text">大谷翔平</span> 歷年全壘打與被打投手統計
                    </h1>
                    <p class="text-slate-400 mt-2 text-sm md:text-base">
                        Shohei Ohtani Career Home Run Log & Pitcher Victimized Analysis
                    </p>
                </div>
                <div class="flex gap-4">
                    <div class="glass-card rounded-xl p-4 text-center min-w-[110px]">
                        <div class="text-xs text-slate-400 font-medium">生涯通算 HR</div>
                        <div id="stat-total-hrs" class="text-3xl font-black gold-gradient-text mt-1">--</div>
                    </div>
                    <div class="glass-card rounded-xl p-4 text-center min-w-[110px]">
                        <div class="text-xs text-slate-400 font-medium">被打投手總數</div>
                        <div id="stat-total-pitchers" class="text-3xl font-black dodger-blue-text mt-1">--</div>
                    </div>
                </div>
            </div>
        </header>

        <!-- Top Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="glass-card rounded-xl p-5 border-l-4 border-amber-400">
                <div class="text-slate-400 text-xs font-semibold uppercase tracking-wider">苦主榜首 (被轟最多)</div>
                <div id="stat-top-victim" class="text-lg font-bold text-white mt-1">--</div>
                <div id="stat-top-victim-count" class="text-xs text-amber-400 mt-0.5">-- 次</div>
            </div>
            <div class="glass-card rounded-xl p-5 border-l-4 border-sky-400">
                <div class="text-slate-400 text-xs font-semibold uppercase tracking-wider">最長飛行距離</div>
                <div id="stat-max-dist" class="text-lg font-bold text-white mt-1">--</div>
                <div id="stat-max-dist-detail" class="text-xs text-sky-400 mt-0.5">--</div>
            </div>
            <div class="glass-card rounded-xl p-5 border-l-4 border-emerald-400">
                <div class="text-slate-400 text-xs font-semibold uppercase tracking-wider">最大擊球初速</div>
                <div id="stat-max-ev" class="text-lg font-bold text-white mt-1">--</div>
                <div id="stat-max-ev-detail" class="text-xs text-emerald-400 mt-0.5">--</div>
            </div>
            <div class="glass-card rounded-xl p-5 border-l-4 border-purple-400">
                <div class="text-slate-400 text-xs font-semibold uppercase tracking-wider">最常受害球種</div>
                <div id="stat-top-pitch-type" class="text-lg font-bold text-white mt-1">--</div>
                <div id="stat-top-pitch-count" class="text-xs text-purple-400 mt-0.5">-- 次</div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Yearly HR Breakdown -->
            <div class="glass-card rounded-2xl p-6">
                <h3 class="text-base font-bold text-slate-200 mb-4 flex items-center gap-2">
                    <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                    歷年全壘打數量統計 (Yearly)
                </h3>
                <div class="h-60 relative">
                    <canvas id="yearlyChart"></canvas>
                </div>
            </div>

            <!-- Inning HR Breakdown -->
            <div class="glass-card rounded-2xl p-6 border-t-2 border-emerald-500/50">
                <h3 class="text-base font-bold text-slate-200 mb-4 flex items-center gap-2">
                    <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    各局全壘打分布統計 (Inning HRs)
                </h3>
                <div class="h-60 relative">
                    <canvas id="inningChart"></canvas>
                </div>
            </div>

            <!-- Top Pitchers Victimized -->
            <div class="glass-card rounded-2xl p-6">
                <h3 class="text-base font-bold text-slate-200 mb-4 flex items-center gap-2">
                    <svg class="w-5 h-5 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                    挨轟最多全壘打投手 Top 10
                </h3>
                <div class="h-60 relative">
                    <canvas id="pitcherChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Pitchers Leaderboard Summary Grid -->
        <div class="glass-card rounded-2xl p-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
                <div>
                    <h3 class="text-xl font-bold text-slate-100">受害投手全列表與被轟次數排行</h3>
                    <p class="text-xs text-slate-400 mt-1">點擊投手卡片可快速在下方表格中篩選該投手的被轟紀錄</p>
                </div>
                <div class="w-full md:w-64">
                    <input type="text" id="pitcher-search-input" placeholder="搜尋投手姓名..." 
                           class="w-full px-4 py-2 bg-slate-900/80 border border-slate-700 rounded-xl text-sm focus:outline-none focus:border-sky-500 text-slate-200">
                </div>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 max-h-60 overflow-y-auto pr-2" id="pitcher-grid">
                <!-- Dynamic Pitcher Cards -->
            </div>
        </div>

        <!-- Main Data Table Section -->
        <div class="glass-card rounded-2xl p-6">
            <!-- Filter Bar -->
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 pb-6 border-b border-slate-800">
                <div class="flex items-center gap-3">
                    <h3 class="text-xl font-bold text-slate-100">全壘打詳細日誌</h3>
                    <span id="showing-count-badge" class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/30">
                        共 -- 筆
                    </span>
                </div>

                <!-- Controls -->
                <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
                    <!-- Year Filter -->
                    <select id="year-filter" class="px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-sm focus:outline-none focus:border-sky-500 text-slate-200">
                        <option value="ALL">所有年份 (All Years)</option>
                    </select>

                    <!-- Pitcher Filter -->
                    <select id="pitcher-select-filter" class="px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-sm focus:outline-none focus:border-sky-500 text-slate-200 max-w-[200px]">
                        <option value="ALL">所有投手 (All Pitchers)</option>
                    </select>

                    <!-- Search Input -->
                    <input type="text" id="table-search" placeholder="搜尋隊伍 / 投手 / 球種..." 
                           class="px-4 py-2 bg-slate-900 border border-slate-700 rounded-xl text-sm focus:outline-none focus:border-sky-500 text-slate-200 flex-1 md:w-56">

                    <!-- Reset Button -->
                    <button id="reset-btn" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium rounded-xl transition">
                        重設篩選
                    </button>
                </div>
            </div>

            <!-- Table -->
            <div class="overflow-x-auto max-h-[600px] overflow-y-auto rounded-xl">
                <table class="w-full text-left text-sm text-slate-300 min-w-[900px]">
                    <thead class="bg-slate-900 text-xs font-semibold text-slate-400 uppercase tracking-wider sticky top-0 z-10 shadow">
                        <tr>
                            <th class="py-3.5 px-4 rounded-l-lg">生涯 #</th>
                            <th class="py-3.5 px-4">年度 #</th>
                            <th class="py-3.5 px-4">日期</th>
                            <th class="py-3.5 px-4">球隊</th>
                            <th class="py-3.5 px-4">對手</th>
                            <th class="py-3.5 px-4">局數</th>
                            <th class="py-3.5 px-4">被打投手</th>
                            <th class="py-3.5 px-4">投球手</th>
                            <th class="py-3.5 px-4">球種</th>
                            <th class="py-3.5 px-4">球速</th>
                            <th class="py-3.5 px-4">初速 (mph)</th>
                            <th class="py-3.5 px-4">距離 (ft)</th>
                            <th class="py-3.5 px-4">類型</th>
                            <th class="py-3.5 px-4 rounded-r-lg text-center">影片 HighLight</th>
                        </tr>
                    </thead>
                    <tbody id="hr-table-body" class="divide-y divide-slate-800/60">
                        <!-- Dynamic Rows -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Video Modal -->
        <div id="video-modal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
            <div class="glass-card rounded-2xl p-6 max-w-3xl w-full relative border border-slate-700 shadow-2xl">
                <button onclick="closeVideoModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white p-2 rounded-full bg-slate-800/80 transition">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
                <h3 id="modal-video-title" class="text-lg font-bold text-slate-100 mb-4 pr-10">--</h3>
                <div class="aspect-video bg-black rounded-xl overflow-hidden shadow-inner">
                    <video id="modal-video-player" controls autoplay class="w-full h-full object-contain"></video>
                </div>
            </div>
        </div>

        <!-- Data Sources Footer -->
        <footer class="glass-card rounded-2xl p-6 text-center text-xs text-slate-400 space-y-2 border border-slate-800">
            <div class="flex flex-wrap justify-center items-center gap-4 text-sm font-semibold text-slate-300">
                <span class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-sky-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z"/></svg>
                    資料來源 (Data Sources):
                </span>
                <a href="https://www.mlb.com/official-information" target="_blank" rel="noopener" class="text-sky-400 hover:text-sky-300 underline transition">MLB Official Stats API</a>
                <span class="text-slate-600">•</span>
                <a href="https://baseballsavant.mlb.com/statcast_search" target="_blank" rel="noopener" class="text-amber-400 hover:text-amber-300 underline transition">Baseball Savant (MLB Statcast)</a>
                <span class="text-slate-600">•</span>
                <a href="https://github.com/jldortiz/pybaseball" target="_blank" rel="noopener" class="text-emerald-400 hover:text-emerald-300 underline transition">Pybaseball Data Engine</a>
            </div>
            <p class="text-slate-500">
                本系統數據自動同步自 MLB 美國職棒大聯盟官方 Statcast 數據庫，包含比賽時間、投球手、球種、球速、擊球初速與飛行距離。
            </p>
        </footer>
    </div>

    <script>
        const rawData = """ + json_str + """;

        let currentData = [...rawData];

        // Init App
        document.addEventListener('DOMContentLoaded', () => {
            initSummaryStats(rawData);
            initYearlyChart(rawData);
            initInningChart(rawData);
            initPitcherChart(rawData);
            initPitcherGrid(rawData);
            populateFilters(rawData);
            renderTable(rawData);

            // Setup listeners
            document.getElementById('year-filter').addEventListener('change', filterData);
            document.getElementById('pitcher-select-filter').addEventListener('change', filterData);
            document.getElementById('table-search').addEventListener('input', filterData);
            document.getElementById('reset-btn').addEventListener('click', resetFilters);
            document.getElementById('pitcher-search-input').addEventListener('input', filterPitcherGrid);
        });

        function initSummaryStats(data) {
            document.getElementById('stat-total-hrs').textContent = data.length;

            const pitcherCounts = {};
            let maxDist = 0;
            let maxDistHR = null;
            let maxEV = 0;
            let maxEVHR = null;
            const pitchTypes = {};

            data.forEach(d => {
                // Pitcher count
                pitcherCounts[d.pitcher_name] = (pitcherCounts[d.pitcher_name] || 0) + 1;
                // Pitch type
                if(d.pitch_type && d.pitch_type !== 'N/A') {
                    pitchTypes[d.pitch_type] = (pitchTypes[d.pitch_type] || 0) + 1;
                }
                // Max distance
                if(d.distance && d.distance > maxDist) {
                    maxDist = d.distance;
                    maxDistHR = d;
                }
                // Max Exit Velo
                if(d.exit_velocity && d.exit_velocity > maxEV) {
                    maxEV = d.exit_velocity;
                    maxEVHR = d;
                }
            });

            const uniquePitchers = Object.keys(pitcherCounts).length;
            document.getElementById('stat-total-pitchers').textContent = uniquePitchers;

            // Top victim
            const sortedPitchers = Object.entries(pitcherCounts).sort((a,b) => b[1] - a[1]);
            if(sortedPitchers.length > 0) {
                document.getElementById('stat-top-victim').textContent = sortedPitchers[0][0];
                document.getElementById('stat-top-victim-count').textContent = `被轟 ${sortedPitchers[0][1]} 次`;
            }

            // Max dist
            if(maxDistHR) {
                document.getElementById('stat-max-dist').textContent = `${maxDistHR.distance} 英尺`;
                document.getElementById('stat-max-dist-detail').textContent = `${maxDistHR.date} vs ${maxDistHR.pitcher_name}`;
            }

            // Max EV
            if(maxEVHR) {
                document.getElementById('stat-max-ev').textContent = `${maxEVHR.exit_velocity} mph`;
                document.getElementById('stat-max-ev-detail').textContent = `${maxEVHR.date} vs ${maxEVHR.pitcher_name}`;
            }

            // Top pitch type
            const sortedPitches = Object.entries(pitchTypes).sort((a,b) => b[1] - a[1]);
            if(sortedPitches.length > 0) {
                document.getElementById('stat-top-pitch-type').textContent = sortedPitches[0][0];
                document.getElementById('stat-top-pitch-count').textContent = `共 ${sortedPitches[0][1]} 支`;
            }
        }

        function initYearlyChart(data) {
            const years = {};
            data.forEach(d => {
                years[d.year] = (years[d.year] || 0) + 1;
            });

            const ctx = document.getElementById('yearlyChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(years),
                    datasets: [{
                        label: '全壘打數 (HRs)',
                        data: Object.values(years),
                        backgroundColor: 'rgba(234, 179, 8, 0.75)',
                        borderColor: '#eab308',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.08)' },
                            ticks: { color: '#94a3b8' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#94a3b8' }
                        }
                    }
                }
            });
        }

        function initInningChart(data) {
            const innings = {};
            for(let i=1; i<=9; i++) {
                innings[`第 ${i} 局`] = 0;
            }
            innings['延長賽'] = 0;

            data.forEach(d => {
                const match = d.inning ? d.inning.match(/\d+/) : null;
                if(match) {
                    const num = parseInt(match[0]);
                    if(num <= 9) {
                        innings[`第 ${num} 局`] = (innings[`第 ${num} 局`] || 0) + 1;
                    } else {
                        innings['延長賽'] = (innings['延長賽'] || 0) + 1;
                    }
                }
            });

            const ctx = document.getElementById('inningChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(innings),
                    datasets: [{
                        label: '全壘打數 (HRs)',
                        data: Object.values(innings),
                        backgroundColor: [
                            'rgba(52, 211, 153, 0.85)',
                            'rgba(16, 185, 129, 0.65)',
                            'rgba(52, 211, 153, 0.85)',
                            'rgba(16, 185, 129, 0.65)',
                            'rgba(52, 211, 153, 0.75)',
                            'rgba(16, 185, 129, 0.65)',
                            'rgba(52, 211, 153, 0.65)',
                            'rgba(16, 185, 129, 0.65)',
                            'rgba(52, 211, 153, 0.75)',
                            'rgba(244, 63, 94, 0.75)'
                        ],
                        borderColor: '#10b981',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.08)' },
                            ticks: { color: '#94a3b8' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#94a3b8' }
                        }
                    }
                }
            });
        }

        function initPitcherChart(data) {
            const pitcherCounts = {};
            data.forEach(d => {
                pitcherCounts[d.pitcher_name] = (pitcherCounts[d.pitcher_name] || 0) + 1;
            });

            const top10 = Object.entries(pitcherCounts)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);

            const ctx = document.getElementById('pitcherChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: top10.map(item => item[0]),
                    datasets: [{
                        label: '被轟次數',
                        data: top10.map(item => item[1]),
                        backgroundColor: 'rgba(56, 189, 248, 0.75)',
                        borderColor: '#38bdf8',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.08)' },
                            ticks: { color: '#94a3b8', stepSize: 1 }
                        },
                        y: {
                            grid: { display: false },
                            ticks: { color: '#f8fafc', font: { size: 12, weight: 'bold' } }
                        }
                    }
                }
            });
        }

        function getPitcherHeadshotUrl(pitcherId) {
            if(!pitcherId) return 'https://midfield.mlbstatic.com/v1/people/generic/spots/120';
            return `https://midfield.mlbstatic.com/v1/people/${pitcherId}/spots/120`;
        }

        function initPitcherGrid(data) {
            const pitcherInfo = {};
            data.forEach(d => {
                if(!pitcherInfo[d.pitcher_name]) {
                    pitcherInfo[d.pitcher_name] = { count: 0, id: d.pitcher_id };
                }
                pitcherInfo[d.pitcher_name].count += 1;
            });

            const sorted = Object.entries(pitcherInfo).sort((a,b) => b[1].count - a[1].count || a[0].localeCompare(b[0]));
            const grid = document.getElementById('pitcher-grid');
            grid.innerHTML = '';

            sorted.forEach(([name, info]) => {
                const headshotUrl = getPitcherHeadshotUrl(info.id);
                const card = document.createElement('div');
                card.className = 'glass-card glass-card-hover rounded-xl p-2 flex justify-between items-center cursor-pointer text-xs transition border border-slate-800 gap-1.5';
                card.onclick = () => selectPitcher(name);
                card.setAttribute('data-name', name.toLowerCase());
                card.innerHTML = `
                    <div class="flex items-center gap-2 min-w-0">
                        <img src="${headshotUrl}" class="w-7 h-7 rounded-full object-cover border border-slate-700 bg-slate-900 flex-shrink-0" 
                             onerror="this.onerror=null; this.src='https://midfield.mlbstatic.com/v1/people/generic/spots/120';" alt="${name}">
                        <span class="font-medium text-slate-200 truncate">${name}</span>
                    </div>
                    <span class="px-2 py-0.5 rounded-full font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 flex-shrink-0">${info.count}</span>
                `;
                grid.appendChild(card);
            });
        }

        function filterPitcherGrid() {
            const term = document.getElementById('pitcher-search-input').value.toLowerCase();
            const cards = document.querySelectorAll('#pitcher-grid > div');
            cards.forEach(card => {
                const name = card.getAttribute('data-name');
                if(name.includes(term)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        function populateFilters(data) {
            const years = [...new Set(data.map(d => d.year))].sort((a,b) => b - a);
            const yearSelect = document.getElementById('year-filter');
            years.forEach(y => {
                const opt = document.createElement('option');
                opt.value = y;
                opt.textContent = `${y} 年 (${data.filter(d => d.year === y).length} 轟)`;
                yearSelect.appendChild(opt);
            });

            const pitchers = [...new Set(data.map(d => d.pitcher_name))].sort();
            const pitcherSelect = document.getElementById('pitcher-select-filter');
            pitchers.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p;
                opt.textContent = p;
                pitcherSelect.appendChild(opt);
            });
        }

        function selectPitcher(pitcherName) {
            document.getElementById('pitcher-select-filter').value = pitcherName;
            filterData();
            document.getElementById('hr-table-body').scrollIntoView({ behavior: 'smooth' });
        }

        function filterData() {
            const year = document.getElementById('year-filter').value;
            const pitcher = document.getElementById('pitcher-select-filter').value;
            const search = document.getElementById('table-search').value.toLowerCase();

            currentData = rawData.filter(d => {
                const matchYear = (year === 'ALL' || d.year.toString() === year);
                const matchPitcher = (pitcher === 'ALL' || d.pitcher_name === pitcher);
                const matchSearch = !search || 
                    d.pitcher_name.toLowerCase().includes(search) ||
                    d.opponent.toLowerCase().includes(search) ||
                    d.team.toLowerCase().includes(search) ||
                    d.pitch_type.toLowerCase().includes(search) ||
                    d.date.includes(search);

                return matchYear && matchPitcher && matchSearch;
            });

            renderTable(currentData);
        }

        function resetFilters() {
            document.getElementById('year-filter').value = 'ALL';
            document.getElementById('pitcher-select-filter').value = 'ALL';
            document.getElementById('table-search').value = '';
            filterData();
        }

        const TEAM_LOGOS = {
            'Los Angeles Angels': '108',
            'LAA': '108',
            'Los Angeles Dodgers': '119',
            'LAD': '119',
            'Oakland Athletics': '133',
            'Athletics': '133',
            'OAK': '133',
            'ATH': '133',
            'Seattle Mariners': '136',
            'SEA': '136',
            'Texas Rangers': '140',
            'TEX': '140',
            'Houston Astros': '117',
            'HOU': '117',
            'San Francisco Giants': '137',
            'SF': '137',
            'SFG': '137',
            'San Diego Padres': '135',
            'SD': '135',
            'SDP': '135',
            'Arizona Diamondbacks': '109',
            'ARI': '109',
            'AZ': '109',
            'Colorado Rockies': '115',
            'COL': '115',
            'New York Yankees': '147',
            'NYY': '147',
            'Boston Red Sox': '111',
            'BOS': '111',
            'Tampa Bay Rays': '139',
            'TB': '139',
            'TBR': '139',
            'Toronto Blue Jays': '141',
            'TOR': '141',
            'Baltimore Orioles': '110',
            'BAL': '110',
            'Chicago White Sox': '145',
            'CWS': '145',
            'CHW': '145',
            'Cleveland Guardians': '114',
            'Cleveland Indians': '114',
            'CLE': '114',
            'Detroit Tigers': '116',
            'DET': '116',
            'Kansas City Royals': '118',
            'KC': '118',
            'KCR': '118',
            'Minnesota Twins': '142',
            'MIN': '142',
            'Atlanta Braves': '144',
            'ATL': '144',
            'Miami Marlins': '146',
            'MIA': '146',
            'New York Mets': '121',
            'NYM': '121',
            'Philadelphia Phillies': '143',
            'PHI': '143',
            'Washington Nationals': '120',
            'WSH': '120',
            'WAS': '120',
            'Chicago Cubs': '112',
            'CHC': '112',
            'Cincinnati Reds': '113',
            'CIN': '113',
            'Milwaukee Brewers': '158',
            'MIL': '158',
            'Pittsburgh Pirates': '134',
            'PIT': '134',
            'St. Louis Cardinals': 'STL',
            'STL': '138'
        };

        const TEAM_ABBR = {
            'Los Angeles Angels': 'LAA',
            'LAA': 'LAA',
            'Los Angeles Dodgers': 'LAD',
            'LAD': 'LAD',
            'Oakland Athletics': 'ATH',
            'Athletics': 'ATH',
            'OAK': 'ATH',
            'ATH': 'ATH',
            'Seattle Mariners': 'SEA',
            'SEA': 'SEA',
            'Texas Rangers': 'TEX',
            'TEX': 'TEX',
            'Houston Astros': 'HOU',
            'HOU': 'HOU',
            'San Francisco Giants': 'SF',
            'SF': 'SF',
            'SFG': 'SF',
            'San Diego Padres': 'SD',
            'SD': 'SD',
            'SDP': 'SD',
            'Arizona Diamondbacks': 'ARI',
            'ARI': 'ARI',
            'AZ': 'ARI',
            'Colorado Rockies': 'COL',
            'COL': 'COL',
            'New York Yankees': 'NYY',
            'NYY': 'NYY',
            'Boston Red Sox': 'BOS',
            'BOS': 'BOS',
            'Tampa Bay Rays': 'TB',
            'TB': 'TB',
            'TBR': 'TB',
            'Toronto Blue Jays': 'TOR',
            'TOR': 'TOR',
            'Baltimore Orioles': 'BAL',
            'BAL': 'BAL',
            'Chicago White Sox': 'CWS',
            'CWS': 'CWS',
            'CHW': 'CWS',
            'Cleveland Guardians': 'CLE',
            'Cleveland Indians': 'CLE',
            'CLE': 'CLE',
            'Detroit Tigers': 'DET',
            'DET': 'DET',
            'Kansas City Royals': 'KC',
            'KC': 'KC',
            'KCR': 'KC',
            'Minnesota Twins': 'MIN',
            'MIN': 'MIN',
            'Atlanta Braves': 'ATL',
            'ATL': 'ATL',
            'Miami Marlins': 'MIA',
            'MIA': 'MIA',
            'New York Mets': 'NYM',
            'NYM': 'NYM',
            'Philadelphia Phillies': 'PHI',
            'PHI': 'PHI',
            'Washington Nationals': 'WSH',
            'WSH': 'WSH',
            'WAS': 'WSH',
            'Chicago Cubs': 'CHC',
            'CHC': 'CHC',
            'Cincinnati Reds': 'CIN',
            'CIN': 'CIN',
            'Milwaukee Brewers': 'MIL',
            'MIL': 'MIL',
            'Pittsburgh Pirates': 'PIT',
            'PIT': 'PIT',
            'St. Louis Cardinals': 'STL',
            'STL': 'STL'
        };

        function getTeamLogoUrl(teamName) {
            const id = TEAM_LOGOS[teamName];
            if(id) {
                return `https://www.mlbstatic.com/team-logos/team-cap-on-dark/${id}.svg`;
            }
            return null;
        }

        function getTeamAbbr(teamName) {
            return TEAM_ABBR[teamName] || teamName;
        }

        function renderTable(data) {
            const tbody = document.getElementById('hr-table-body');
            tbody.innerHTML = '';

            document.getElementById('showing-count-badge').textContent = `顯示 ${data.length} 筆`;

            if(data.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="13" class="text-center py-8 text-slate-500">
                            沒有符合條件的全壘打紀錄
                        </td>
                    </tr>
                `;
                return;
            }

            data.forEach(d => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/50 transition border-b border-slate-800/40';

                const rbiBadge = d.rbi === 4 ? 'bg-red-500/20 text-red-300 border-red-500/30' :
                                 d.rbi === 3 ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' :
                                 d.rbi === 2 ? 'bg-blue-500/20 text-blue-300 border-blue-500/30' : 'bg-slate-800 text-slate-400 border-slate-700';

                const teamLogo = getTeamLogoUrl(d.team);
                const oppLogo = getTeamLogoUrl(d.opponent);

                const teamAbbr = getTeamAbbr(d.team);
                const oppAbbr = getTeamAbbr(d.opponent);

                const teamImgTag = teamLogo ? `<img src="${teamLogo}" class="w-5 h-5 object-contain inline-block mr-1.5" alt="${teamAbbr}" title="${d.team}">` : '';
                const oppImgTag = oppLogo ? `<img src="${oppLogo}" class="w-5 h-5 object-contain inline-block mr-1.5" alt="${oppAbbr}" title="${d.opponent}">` : '';
                const pitcherHeadshot = getPitcherHeadshotUrl(d.pitcher_id);

                tr.innerHTML = `
                    <td class="py-3 px-4 font-bold text-amber-400">#${d.hr_num}</td>
                    <td class="py-3 px-4 text-slate-400">${d.season_hr_num}</td>
                    <td class="py-3 px-4 font-medium text-slate-200">${d.date}</td>
                    <td class="py-3 px-4 text-xs font-bold text-slate-200">
                        <div class="flex items-center gap-1" title="${d.team}">
                            ${teamImgTag} <span>${teamAbbr}</span>
                        </div>
                    </td>
                    <td class="py-3 px-4 text-xs font-semibold text-slate-300">
                        <div class="flex items-center gap-1" title="${d.opponent}">
                            ${oppImgTag} <span>${oppAbbr}</span>
                        </div>
                    </td>
                    <td class="py-3 px-4 text-xs text-slate-400">${d.inning}</td>
                    <td class="py-3 px-4 font-bold text-sky-300">
                        <div class="flex items-center gap-2 cursor-pointer hover:underline" onclick="selectPitcher('${d.pitcher_name}')">
                            <img src="${pitcherHeadshot}" class="w-6 h-6 rounded-full object-cover border border-slate-700 bg-slate-900 flex-shrink-0"
                                 onerror="this.onerror=null; this.src='https://midfield.mlbstatic.com/v1/people/generic/spots/120';" alt="${d.pitcher_name}">
                            <span>${d.pitcher_name}</span>
                        </div>
                    </td>
                    <td class="py-3 px-4 text-xs text-slate-400">${d.pitcher_hand || 'R'}</td>
                    <td class="py-3 px-4 text-xs text-slate-300">${d.pitch_type || '-'}</td>
                    <td class="py-3 px-4 text-xs text-slate-400">${d.pitch_speed ? d.pitch_speed + ' mph' : '-'}</td>
                    <td class="py-3 px-4 text-xs font-medium text-emerald-400">${d.exit_velocity ? d.exit_velocity + ' mph' : '-'}</td>
                    <td class="py-3 px-4 text-xs font-medium text-amber-300">${d.distance ? d.distance + ' ft' : '-'}</td>
                    <td class="py-3 px-4">
                        <span class="px-2 py-0.5 rounded-full text-xs font-semibold border ${rbiBadge}">${d.hr_type}</span>
                    </td>
                    <td class="py-3 px-4 text-center">
                        ${d.video_url ? `
                            <div onclick="openVideoModal('${d.video_url}', '#${d.hr_num} - ${d.date} vs ${d.pitcher_name} (${d.hr_type})')" 
                                 class="relative w-24 h-14 rounded-lg overflow-hidden border border-slate-700/80 bg-slate-900 group cursor-pointer shadow hover:border-red-500 hover:shadow-red-500/20 transition duration-300 mx-auto flex items-center justify-center">
                                ${d.video_thumbnail ? `
                                    <img src="${d.video_thumbnail}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300 opacity-90 group-hover:opacity-100" alt="Video Thumbnail"
                                         onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\'w-full h-full bg-slate-800/90 flex flex-col items-center justify-center text-red-400 text-xs font-semibold gap-1\'><svg class=\'w-4 h-4 text-red-500\' fill=\'currentColor\' viewBox=\'0 0 24 24\'><path d=\'M8 5v14l11-7z\'/></svg><span>播放 Highlights</span></div>';">
                                ` : `
                                    <div class="w-full h-full bg-gradient-to-br from-slate-800 to-slate-900 flex flex-col items-center justify-center text-red-400 text-xs font-semibold gap-1 border border-slate-700/50">
                                        <svg class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                                        <span>播放影片</span>
                                    </div>
                                `}
                                <!-- Subtle Hover Overlay -->
                                <div class="absolute inset-0 bg-black/0 group-hover:bg-black/40 flex items-center justify-center transition duration-300">
                                    <div class="w-8 h-8 rounded-full bg-red-600/90 text-white flex items-center justify-center shadow-lg opacity-0 group-hover:opacity-100 transform scale-75 group-hover:scale-100 transition duration-300">
                                        <svg class="w-4 h-4 translate-x-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                                    </div>
                                </div>
                            </div>
                        ` : `
                            <a href="${d.yt_url}" target="_blank" rel="noopener" 
                               class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 text-xs transition">
                                <svg class="w-3.5 h-3.5 text-red-500" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                                YouTube 搜尋
                            </a>
                        `}
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function openVideoModal(url, title) {
            const modal = document.getElementById('video-modal');
            const player = document.getElementById('modal-video-player');
            const titleEl = document.getElementById('modal-video-title');
            
            titleEl.textContent = title;
            player.src = url;
            modal.classList.remove('hidden');
            player.play();
        }

        function closeVideoModal() {
            const modal = document.getElementById('video-modal');
            const player = document.getElementById('modal-video-player');
            
            player.pause();
            player.src = '';
            modal.classList.add('hidden');
        }
    </script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("index.html generated successfully!")

if __name__ == '__main__':
    build_html()

document.addEventListener('DOMContentLoaded', function () {
    // 1. Skill Matrix Radar Chart
    const radarCanvas = document.getElementById('skillRadarChart');
    if (radarCanvas && typeof Chart !== 'undefined') {
        const labels = JSON.parse(radarCanvas.getAttribute('data-labels') || '[]');
        const userScores = JSON.parse(radarCanvas.getAttribute('data-user-scores') || '[]');
        const targetScores = JSON.parse(radarCanvas.getAttribute('data-target-scores') || '[]');

        new Chart(radarCanvas, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Your Proficiency',
                        data: userScores,
                        backgroundColor: 'rgba(79, 70, 229, 0.25)',
                        borderColor: '#4f46e5',
                        pointBackgroundColor: '#4f46e5',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: '#4f46e5',
                        borderWidth: 2
                    },
                    {
                        label: 'Target Requirement',
                        data: targetScores,
                        backgroundColor: 'rgba(6, 182, 212, 0.1)',
                        borderColor: '#06b6d4',
                        borderDash: [4, 4],
                        pointBackgroundColor: '#06b6d4',
                        pointBorderColor: '#fff',
                        borderWidth: 1.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: '#e2e8f0' },
                        grid: { color: '#e2e8f0' },
                        suggestedMin: 0,
                        suggestedMax: 3,
                        ticks: {
                            stepSize: 1,
                            callback: function(val) {
                                if (val === 1) return 'Beg';
                                if (val === 2) return 'Int';
                                if (val === 3) return 'Adv';
                                return '';
                            }
                        }
                    }
                },
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    // 2. Milestones Progress Bar Chart
    const milestoneCanvas = document.getElementById('milestoneProgressChart');
    if (milestoneCanvas && typeof Chart !== 'undefined') {
        const mLabels = JSON.parse(milestoneCanvas.getAttribute('data-labels') || '[]');
        const mPcts = JSON.parse(milestoneCanvas.getAttribute('data-pcts') || '[]');

        new Chart(milestoneCanvas, {
            type: 'bar',
            data: {
                labels: mLabels,
                datasets: [{
                    label: 'Milestone Progress %',
                    data: mPcts,
                    backgroundColor: mPcts.map(p => p === 100 ? '#10b981' : (p > 0 ? '#4f46e5' : '#cbd5e1')),
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { callback: v => v + '%' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
});

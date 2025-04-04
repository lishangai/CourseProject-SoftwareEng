// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 加载复习计划
    loadReviewSchedule();
    // 加载记忆强度分析
    loadMemoryStrengthChart();
    // 加载学习统计
    loadLearningStats();
});

// 加载复习计划
async function loadReviewSchedule() {
    try {
        const response = await fetch('/api/memory/review?user_id=1');
        if (!response.ok) {
            throw new Error('获取复习计划失败');
        }
        const schedule = await response.json();
        
        displayTodayReview(schedule);
        displayReviewHistory(schedule);
        
    } catch (error) {
        showAlert('加载复习计划失败: ' + error.message, 'danger');
    }
}

// 显示今日复习
function displayTodayReview(schedule) {
    const container = document.getElementById('today-review');
    const today = new Date().toISOString().split('T')[0];
    
    const todayReviews = schedule.filter(item => 
        item.next_review.startsWith(today)
    );
    
    if (todayReviews.length === 0) {
        container.innerHTML = '<p class="text-muted">今天没有需要复习的概念</p>';
        return;
    }
    
    container.innerHTML = todayReviews.map(item => `
        <div class="review-item card mb-3">
            <div class="card-body">
                <h6 class="card-title">${item.concept}</h6>
                <p class="card-text">
                    <small class="text-muted">记忆强度: ${Math.round(item.memory_strength * 100)}%</small>
                </p>
                <div class="btn-group">
                    <button class="btn btn-sm btn-primary" onclick="startReview('${item.concept}')">
                        开始复习
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="skipReview('${item.concept}')">
                        跳过
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// 显示复习历史
function displayReviewHistory(schedule) {
    const container = document.getElementById('review-history');
    const today = new Date().toISOString().split('T')[0];
    
    const history = schedule.filter(item => 
        item.next_review < today
    ).sort((a, b) => new Date(b.next_review) - new Date(a.next_review));
    
    if (history.length === 0) {
        container.innerHTML = '<p class="text-muted">暂无复习历史</p>';
        return;
    }
    
    container.innerHTML = history.map(item => `
        <div class="review-item card mb-3">
            <div class="card-body">
                <h6 class="card-title">${item.concept}</h6>
                <p class="card-text">
                    <small class="text-muted">
                        上次复习: ${new Date(item.next_review).toLocaleDateString()}<br>
                        复习次数: ${item.review_count}
                    </small>
                </p>
                <div class="progress">
                    <div class="progress-bar" role="progressbar" 
                         style="width: ${item.memory_strength * 100}%">
                        ${Math.round(item.memory_strength * 100)}%
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// 加载记忆强度分析
async function loadMemoryStrengthChart() {
    try {
        const response = await fetch('/api/memory/strength?user_id=1');
        if (!response.ok) {
            throw new Error('获取记忆强度数据失败');
        }
        const data = await response.json();
        
        const chartData = [
            {
                x: data.concepts,
                y: data.strengths,
                type: 'bar',
                marker: {
                    color: 'rgb(13, 110, 253)'
                }
            }
        ];
        
        const layout = {
            title: '概念记忆强度分布',
            yaxis: {
                title: '记忆强度',
                range: [0, 1]
            },
            margin: {
                l: 50,
                r: 50,
                t: 50,
                b: 50
            }
        };
        
        Plotly.newPlot('memory-strength-chart', chartData, layout);
    } catch (error) {
        showAlert('加载记忆强度分析失败: ' + error.message, 'danger');
        // 使用模拟数据作为备用
        useMockMemoryStrengthData();
    }
}

// 使用模拟数据作为备用
function useMockMemoryStrengthData() {
    const data = [
        {
            x: ['概念1', '概念2', '概念3', '概念4', '概念5'],
            y: [0.8, 0.6, 0.9, 0.4, 0.7],
            type: 'bar',
            marker: {
                color: 'rgb(13, 110, 253)'
            }
        }
    ];
    
    const layout = {
        title: '概念记忆强度分布',
        yaxis: {
            title: '记忆强度',
            range: [0, 1]
        },
        margin: {
            l: 50,
            r: 50,
            t: 50,
            b: 50
        }
    };
    
    Plotly.newPlot('memory-strength-chart', data, layout);
}

// 加载学习统计
async function loadLearningStats() {
    try {
        const response = await fetch('/api/memory/stats?user_id=1');
        if (!response.ok) {
            throw new Error('获取学习统计数据失败');
        }
        const stats = await response.json();
        
        displayLearningStats(stats);
    } catch (error) {
        showAlert('加载学习统计失败: ' + error.message, 'danger');
        // 使用模拟数据作为备用
        useMockLearningStats();
    }
}

// 显示学习统计
function displayLearningStats(stats) {
    const container = document.getElementById('learning-stats');
    
    container.innerHTML = `
        <div class="list-group">
            <div class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>已学习概念</span>
                    <span class="badge bg-primary rounded-pill">${stats.total_concepts}</span>
                </div>
            </div>
            <div class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>已掌握概念</span>
                    <span class="badge bg-success rounded-pill">${stats.mastered_concepts}</span>
                </div>
            </div>
            <div class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>总复习次数</span>
                    <span class="badge bg-info rounded-pill">${stats.review_count}</span>
                </div>
            </div>
            <div class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>平均记忆强度</span>
                    <span class="badge bg-warning rounded-pill">${Math.round(stats.average_strength * 100)}%</span>
                </div>
            </div>
        </div>
    `;
}

// 使用模拟数据作为备用
function useMockLearningStats() {
    const stats = {
        total_concepts: 25,
        mastered_concepts: 15,
        review_count: 120,
        average_strength: 0.75
    };
    
    displayLearningStats(stats);
}

// 开始复习
async function startReview(concept) {
    try {
        const response = await fetch('/api/memory/review/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ concept })
        });
        
        if (!response.ok) {
            throw new Error('开始复习失败');
        }
        
        const result = await response.json();
        showAlert(result.message, 'info');
        
        // 重新加载复习计划
        loadReviewSchedule();
        
    } catch (error) {
        showAlert('开始复习失败: ' + error.message, 'danger');
    }
}

// 跳过复习
async function skipReview(concept) {
    try {
        const response = await fetch('/api/memory/review/skip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ concept })
        });
        
        if (!response.ok) {
            throw new Error('跳过复习失败');
        }
        
        const result = await response.json();
        showAlert(result.message, 'info');
        
        // 重新加载复习计划
        loadReviewSchedule();
        
    } catch (error) {
        showAlert('操作失败: ' + error.message, 'danger');
    }
}

// 显示提示信息
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.row'));
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
} 
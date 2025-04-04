// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化事件监听
    initializeEventListeners();
});

// 初始化事件监听
function initializeEventListeners() {
    // 生成按钮点击事件
    document.getElementById('generate-btn').addEventListener('click', handleGenerate);
    
    // 输入框回车事件
    document.getElementById('concept-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleGenerate();
        }
    });
}

// 处理生成学习路径
async function handleGenerate() {
    const conceptInput = document.getElementById('concept-input');
    const levelSelect = document.getElementById('level-select');
    const concept = conceptInput.value.trim();
    const level = levelSelect.value;
    
    if (!concept) {
        showAlert('请输入要学习的概念', 'warning');
        return;
    }
    
    showLoading(true);
    
    try {
        // 获取学习路径
        const path = await fetchLearningPath(concept, level);
        displayLearningPath(path);
        
        // 更新学习资源
        updateResources(path);
        
        // 更新学习建议
        updateLearningTips(level);
        
    } catch (error) {
        showAlert('生成学习路径失败: ' + error.message, 'danger');
    } finally {
        showLoading(false);
    }
}

// 获取学习路径
async function fetchLearningPath(concept, level) {
    const response = await fetch('/api/learning/path', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ concept, user_level: level })
    });
    
    if (!response.ok) {
        throw new Error('获取学习路径失败');
    }
    
    return await response.json();
}

// 显示学习路径
function displayLearningPath(path) {
    const container = document.querySelector('.timeline');
    container.innerHTML = '';
    
    // 显示每天的学习计划
    for (const [day, plan] of Object.entries(path)) {
        const dayCard = document.createElement('div');
        dayCard.className = 'card mb-3';
        dayCard.innerHTML = `
            <div class="card-body">
                <h6 class="card-title">${day}</h6>
                <p class="card-text"><strong>学习目标：</strong>${plan.goal}</p>
                <div class="activities">
                    <strong>学习活动：</strong>
                    <ul class="list-unstyled">
                        ${plan.activities.map(activity => `<li>• ${activity}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
        container.appendChild(dayCard);
    }
    
    document.getElementById('learning-path').style.display = 'block';
}

// 更新学习资源
function updateResources(path) {
    const container = document.getElementById('resources-list');
    const resources = new Set();
    
    // 收集所有资源
    Object.values(path).forEach(plan => {
        plan.resources.forEach(resource => resources.add(resource));
    });
    
    // 显示资源列表
    container.innerHTML = `
        <ul class="list-group">
            ${Array.from(resources).map(resource => `
                <li class="list-group-item">
                    <i class="bi bi-link-45deg"></i>
                    ${resource}
                </li>
            `).join('')}
        </ul>
    `;
}

// 更新学习建议
function updateLearningTips(level) {
    const container = document.getElementById('learning-tips');
    const tips = {
        beginner: [
            '从基础概念开始，打好基础',
            '多做练习，巩固理解',
            '遇到不懂的地方及时提问'
        ],
        intermediate: [
            '深入理解核心原理',
            '尝试实际应用场景',
            '与其他概念建立联系'
        ],
        advanced: [
            '探索前沿发展',
            '尝试创新应用',
            '参与相关讨论'
        ]
    };
    
    container.innerHTML = `
        <ul class="list-group">
            ${tips[level].map(tip => `
                <li class="list-group-item">
                    <i class="bi bi-lightbulb"></i>
                    ${tip}
                </li>
            `).join('')}
        </ul>
    `;
}

// 显示加载状态
function showLoading(show) {
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = show;
    generateBtn.innerHTML = show ? '生成中...' : '生成路径';
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
// 格式化日期
export function formatDate(dateString) {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}

// 格式化文件大小
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 格式化任务类型
export function formatTaskType(type) {
  const map = {
    'detection': '目标检测',
    'classification': '图像分类',
    'segmentation': '语义分割',
    'pose': '姿态估计'
  };
  return map[type] || type;
}

// 格式化影像类型
export function formatImageType(type) {
  const map = {
    'xray': 'X光片',
    'ct': 'CT扫描',
    'pathology': '病理切片',
    'ultrasound': '超声图像'
  };
  return map[type] || type;
}

import axios from '@/utils/axios';

/**
 * 获取数据集列表
 * @returns {Promise<Array>} 包含数据集列表的Promise
 */
export function getDatasets() {
  // 修正：直接返回axios请求的Promise，响应拦截器会自动处理数据提取
  return axios.get('/api/datasets');
}

/**
 * 创建新数据集(空文件夹)
 * @param {Object} dataset - 数据集基本信息
 * @returns {Promise<Object>} 包含新创建数据集的Promise
 */
export function createDataset(dataset) {
  // 修正：直接返回Promise
  return axios.post('/api/datasets', {
    name: dataset.name,
    taskType: dataset.taskType,
    imageType: dataset.imageType,
    description: dataset.description
  });
}

/**
 * 批量导入图片到数据集
 * @param {string} datasetId - 数据集ID
 * @param {FormData} formData - 包含图片文件的FormData
 * @returns {Promise<Object>} 包含导入结果的Promise
 */
export function batchImportImages(datasetId, formData) {
  // 修正：直接返回Promise
  return axios.post(`/api/datasets/${datasetId}/images/batch`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

/**
 * 复制数据集中的图片
 * @param {string} datasetId - 源数据集ID
 * @param {string} targetDatasetId - 目标数据集ID
 * @param {Array<string>} imageIds - 要复制的图片ID数组
 * @returns {Promise<Object>} 包含复制结果的Promise
 */
export function copyImages(datasetId, targetDatasetId, imageIds) {
  // 修正：直接返回Promise
  return axios.post(`/api/datasets/${datasetId}/images/copy`, {
    targetDatasetId,
    imageIds
  });
}
/**
 * 更新数据集信息
 * @param {string} datasetId - 数据集ID
 * @param {Object} dataset - 要更新的数据集信息
 * @returns {Promise<Object>} 包含更新后数据集的Promise
 */
export function updateDataset(datasetId, dataset) {
  // 修正：直接返回Promise
  return axios.put(`/api/datasets/${datasetId}`, dataset);
}

/**
 * 获取数据集详情
 * @param {string} datasetId - 数据集ID
 * @returns {Promise<Object>} 包含数据集详情的Promise
 */
export function getDatasetDetails(datasetId) {
  // 修正：直接返回Promise
  return axios.get(`/api/datasets/${datasetId}`);
}

/**
 * 删除数据集
 * @param {string} datasetId - 数据集ID
 * @returns {Promise<Object>} 包含删除结果的Promise
 */
export function deleteDataset(datasetId) {
  // 修正：直接返回Promise
  return axios.delete(`/api/datasets/${datasetId}`);
}

/**
 * 复制数据集
 * @param {string} datasetId - 数据集ID
 * @returns {Promise<Object>} 包含复制后新数据集的Promise
 */
export function copyDataset(datasetId) {
  // Post请求的第二个参数是body，这里没有body，所以传null
  // 修正：直接返回Promise
  return axios.post(`/api/datasets/${datasetId}/copy`, null);
}

/**
 * 迁移数据集（改变任务类型）
 * @param {string} datasetId - 数据集ID
 * @param {Object} params - 迁移参数，包含新任务类型和新名称
 * @returns {Promise<Object>} 包含迁移后新数据集的Promise
 */
export function moveDataset(datasetId, params) {
  // 修正：直接返回Promise
  return axios.post(`/api/datasets/${datasetId}/move`, params);
}

/**
 * 分享数据集
 * @param {string} datasetId - 数据集ID
 * @param {Object} params - 分享参数，包含目标用户ID和权限
 * @returns {Promise<Object>} 包含分享结果的Promise
 */
export function shareDataset(datasetId, params) {
  // 修正：直接返回Promise
  return axios.post(`/api/datasets/${datasetId}/share`, params);
}

/**
 * 删除数据集中的图片
 * @param {string} datasetId - 数据集ID
 * @param {string} imageId - 图片ID
 * @returns {Promise<Object>} 包含删除结果的Promise
 */
export function deleteImage(datasetId, imageId) {
  // 修正：直接返回Promise
  return axios.delete(`/api/datasets/${datasetId}/images/${imageId}`);
}

/**
 * 搜索用户（用于分享功能）
 * @param {string} query - 搜索关键词
 * @returns {Promise<Array>} 包含搜索结果的Promise
 */
export function searchUsers(query) {
  // 修正：直接返回Promise
  return axios.get(`/api/users?search=${encodeURIComponent(query)}`);
}